/*
	HardwareSerial.cpp - Hardware serial library for Wiring
	Copyright (c) 2006 Nicholas Zambetti.	All right reserved.

	Modified and minimalized for amonome to work outside Arduino framework

	This library is free software; you can redistribute it and/or
	modify it under the terms of the GNU Lesser General Public
	License as published by the Free Software Foundation; either
	version 2.1 of the License, or (at your option) any later version.

	This library is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	See the GNU
	Lesser General Public License for more details.

	You should have received a copy of the GNU Lesser General Public
	License along with this library; if not, write to the Free Software
	Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA	02110-1301	USA
	
	Modified 23 November 2006 by David A. Mellis
	Modified 28 September 2010 by Mark Sproul
	Modified 14 August 2012 by Alarus
*/

#include <inttypes.h>
#include <stdbool.h>
#include <avr/interrupt.h>

#include "serial.h"

#define cbi(sfr, bit) (_SFR_BYTE(sfr) &= ~_BV(bit))
#define sbi(sfr, bit) (_SFR_BYTE(sfr) |= _BV(bit))

// Define constants and variables for buffering incoming serial data.	We're
// using a ring buffer (I think), in which head is the index of the location
// to which to write the next incoming character and tail is the index of the
// location from which to read.
#define SERIAL_BUFFER_SIZE 64

struct ring_buffer {
	char buffer[SERIAL_BUFFER_SIZE];
	volatile uint8_t head;
	volatile uint8_t tail;
};

bool transmitting;
struct ring_buffer rx_buffer;
struct ring_buffer tx_buffer;

// -----------------------------------------------------------------------
inline static void store_char(char c, struct ring_buffer *buffer)
{
	uint8_t i = (buffer->head + 1) % SERIAL_BUFFER_SIZE;

	// if we should be storing the received character into the location
	// just before the tail (meaning that the head would advance to the
	// current location of the tail), we're about to overflow the buffer
	// and so we don't write the character or advance the head.
	if (i != buffer->tail) {
		buffer->buffer[buffer->head] = c;
		buffer->head = i;
	}
}

// -----------------------------------------------------------------------
ISR(USART_RX_vect)
{
	if (bit_is_clear(UCSR0A, UPE0)) {
		store_char(UDR0, &rx_buffer);
	}
}

// -----------------------------------------------------------------------
ISR(USART_UDRE_vect)
{
	if (tx_buffer.head == tx_buffer.tail) {
		// Buffer empty, so disable interrupts
		cbi(UCSR0B, UDRIE0);
	} else {
		// There is more data in the output buffer. Send the next byte
		char c = tx_buffer.buffer[tx_buffer.tail];
		tx_buffer.tail = (tx_buffer.tail + 1) % SERIAL_BUFFER_SIZE;
		UDR0 = c;
	}
}

// -----------------------------------------------------------------------
void serial_begin(unsigned long baud, uint8_t config)
{
	uint16_t baud_setting;
	bool use_u2x = true;

	transmitting = false;
	rx_buffer.head = rx_buffer.tail = 0;
	tx_buffer.head = tx_buffer.tail = 0;

#if F_CPU == 16000000UL
	// hardcoded exception for compatibility with the bootloader shipped
	// with the Duemilanove and previous boards and the firmware on the 8U2
	// on the Uno and Mega 2560.
	if (baud == 57600) {
		use_u2x = false;
	}
#endif

try_again:
	
	if (use_u2x) {
		UCSR0A = 1 << U2X0;
		baud_setting = (F_CPU / 4 / baud - 1) / 2;
	} else {
		UCSR0A = 0;
		baud_setting = (F_CPU / 8 / baud - 1) / 2;
	}
	
	if ((baud_setting > 4095) && use_u2x) {
		use_u2x = false;
		goto try_again;
	}

	// assign the baud_setting, a.k.a. ubbr (USART Baud Rate Register)
	UBRR0H = baud_setting >> 8;
	UBRR0L = baud_setting;

	//set the data bits, parity, and stop bits
	UCSR0C = config;
	
	sbi(UCSR0B, RXEN0);
	sbi(UCSR0B, TXEN0);
	sbi(UCSR0B, RXCIE0);
	cbi(UCSR0B, UDRIE0);
}

// -----------------------------------------------------------------------
void serial_end(void)
{
	// wait for transmission of outgoing data
	while (tx_buffer.head != tx_buffer.tail);

	cbi(UCSR0B, RXEN0);
	cbi(UCSR0B, TXEN0);
	cbi(UCSR0B, RXCIE0);	
	cbi(UCSR0B, UDRIE0);
	
	// clear any received data
	rx_buffer.head = rx_buffer.tail;
}

// -----------------------------------------------------------------------
int serial_available(void)
{
	return (int)(SERIAL_BUFFER_SIZE + rx_buffer.head - rx_buffer.tail) % SERIAL_BUFFER_SIZE;
}

// -----------------------------------------------------------------------
int serial_peek(void)
{
	if (rx_buffer.head == rx_buffer.tail) {
		return -1;
	} else {
		return rx_buffer.buffer[rx_buffer.tail];
	}
}

// -----------------------------------------------------------------------
int serial_read(void)
{
	// if the head isn't ahead of the tail, we don't have any characters
	if (rx_buffer.head == rx_buffer.tail) {
		return -1;
	} else {
		char c = rx_buffer.buffer[rx_buffer.tail];
		rx_buffer.tail = (unsigned int)(rx_buffer.tail + 1) % SERIAL_BUFFER_SIZE;
		return c;
	}
}

// -----------------------------------------------------------------------
void serial_flush()
{
	// UDR is kept full while the buffer is not empty, so TXC triggers when EMPTY && SENT
	while (transmitting && ! (UCSR0A & _BV(TXC0)));
	transmitting = false;
}

// -----------------------------------------------------------------------
size_t serial_write(char c)
{
	uint8_t i = (tx_buffer.head + 1) % SERIAL_BUFFER_SIZE;
	
	// If the output buffer is full, there's nothing for it other than to 
	// wait for the interrupt handler to empty it a bit
	// ???: return 0 here instead?
	while (i == tx_buffer.tail);
	
	tx_buffer.buffer[tx_buffer.head] = c;
	tx_buffer.head = i;
	
	sbi(UCSR0B, UDRIE0);
	// clear the TXC bit -- "can be cleared by writing a one to its bit location"
	transmitting = true;
	sbi(UCSR0A, TXC0);
	
	return 1;
}

// vim: tabstop=4 shiftwidth=4 autoindent
