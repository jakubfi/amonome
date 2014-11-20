// amonome firmware is a heavily refactorized, modularized,
// cleaned up, optimized, freed from arduino framework
// and ported to C99 version of arduinome firmware.
// Also, there are some minor changes:
//
//  * 115200 bps serial communication
//  * no ADC support
//  * changed startup animation
//  * software reboot to bootloader
//  * build ready for two 8x8 boards working as one 8x16
//
// "ArduinomeFirmware" - Arduino Based Monome Clone by Owen Vallis & Jordan Hochenbaum 06/16/2008
//
//  * Revised 06/26/2008
//  * Revised 07/20/2008 by Ben Southall
//  * Revised 03/21/2009 Ben Southall
//  * Revised 01/21/2012 Jordan Hochenbaum v3.3 rev.a
//
//  This program is free software; you can redistribute it and/or modify
//  it under the terms of the GNU General Public License as published by
//  the Free Software Foundation; either version 2 of the License, or
//  (at your option) any later version.
//
//  This program is distributed in the hope that it will be useful,
//  but WITHOUT ANY WARRANTY; without even the implied warranty of
//  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
//  GNU General Public License for more details.
//
//  You should have received a copy of the GNU General Public License
//  along with this program; if not, write to the Free Software
//  Foundation, Inc.,
//  51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA

#include <inttypes.h>
#include <avr/io.h>
#include <avr/wdt.h>
#include <avr/interrupt.h>
#include <util/delay.h>

#include "serial.h"
#include "display.h"
#include "keypad.h"
#include "softboot.h"

#define PORTD_Data_Direction 0xFE
#define PORTB_Data_Direction 0xFD

int8_t IntensityChange;
int8_t DisplayTestChange;
int8_t ShutdownModeChange;
int8_t WaitingForAddress;

// -----------------------------------------------------------------------
void on_button_event(uint8_t x, uint8_t y, uint8_t state)
{
	serial_write((0 << 4) | (state ? 1 : 0));
	serial_write((x << 4) | y);
}

// -----------------------------------------------------------------------
inline static void process_command(uint8_t byte0, uint8_t byte1)
{
	uint8_t x, y, state;
	uint8_t command = byte0 >> 4;

	switch (command) {
		// command: led
		case 2:
			state = byte0 & 0x0f;
			x = byte1 >> 4;
			y = byte1 & 0x0f;
			display_pixel(x, y, state);
			break;

		// command: led_row
		case 7:
			y = byte0 & 0x07;
			display_row(y, byte1);
			break;

		// command: led_col
		case 8:
			x = byte0 & 0x07;
			display_col(x, byte1);
			break;

		// command: led_intensity
		case 3:
			IntensityChange = byte1 & 0x0f;
			break;

		// command: led_test
		case 4:
			DisplayTestChange = byte1 & 0x0f;
			break;

		// command: shutdown
		case 6:
			ShutdownModeChange = byte1 & 0x0f;
			break;

		// software reset to bootloader
		case 15:
			if ((byte0 == 0xfa) && (byte1 == 0xaf)) {
				softboot_do();
			}
			break;

		// command: adc_enable (ignored)
		case 5:
		default:
			break;
	}
}

// -----------------------------------------------------------------------
ISR(TIMER2_OVF_vect)
{
	static uint8_t byte0;
	uint8_t byte1;

	// first up: enable interrupts to keep the serial class responsive
	sei();

	if (serial_available() <= 0) return;

	do {
		if (WaitingForAddress) {
			byte0 = serial_read();
			WaitingForAddress = 0;
		}

		if (serial_available()) {
			byte1 = serial_read();
			WaitingForAddress = 1;
			process_command(byte0, byte1);
		}
	} while (serial_available() > 16);
}

// -----------------------------------------------------------------------
void comm_init()
{
	// Set up 8-bit counter 2, output compare switched off,
	// normal waveform generation (whatever that might mean)
	TCCR2A = 0;
	// set counter to be clocked at 16Mhz/8 = 2Mhz
	TCCR2B = 1 << CS21;

	// set the interrupt mask so that we get an interrupt
	// on timer 2 overflow, i.e. after 256 clock cycles.
	// The timer 2 interrupt routine will execute every
	// 128 uS.
	TIMSK2 = 1 << TOIE2;

	IntensityChange = -1;
	DisplayTestChange = -1;
	ShutdownModeChange = -1;

	WaitingForAddress = 1;
	serial_begin(115200, SERIAL_8N1);
}

// -----------------------------------------------------------------------
void hw_init()
{
	DDRD = PORTD_Data_Direction;
	DDRB = PORTB_Data_Direction;
}

void startup_anim();

// -----------------------------------------------------------------------
// ---- MAIN -------------------------------------------------------------
// -----------------------------------------------------------------------
int main(void)
{
	hw_init();
	display_init();
	keypad_init();
	softboot_check();
	comm_init();
	startup_anim();
	sei();

	while (1) {
		keypad_scan(on_button_event);
		display_update();

		if (IntensityChange >= 0) {
			display_intensity(IntensityChange);
			IntensityChange = -1;
		}

		if (DisplayTestChange >= 0) {
			display_test(DisplayTestChange);
			DisplayTestChange = -1;
		}

		if (ShutdownModeChange >= 0) {
			display_active(ShutdownModeChange);
			ShutdownModeChange = -1;
		}
	}

	return 0;
}

// vim: tabstop=4 shiftwidth=4 autoindent
