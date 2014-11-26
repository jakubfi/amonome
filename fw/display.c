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

#include "display.h"

// max7219 registers
#define max7219_reg_noop        0x00
#define max7219_reg_digit0      0x01
#define max7219_reg_digit1      0x02
#define max7219_reg_digit2      0x03
#define max7219_reg_digit3      0x04
#define max7219_reg_digit4      0x05
#define max7219_reg_digit5      0x06
#define max7219_reg_digit6      0x07
#define max7219_reg_digit7      0x08
#define max7219_reg_decodeMode  0x09
#define max7219_reg_intensity   0x0a
#define max7219_reg_scanLimit   0x0b
#define max7219_reg_shutdown    0x0c
#define max7219_reg_displayTest 0x0f

// Connections to the Max7219 (LEDs driver)
// max_data_pin  = arduino pin 4 = PORTD, bit 4
// max_clock_pin = arduino pin 6 = PORTD, bit 6
// max_load_pin  = arduino pin 5 = PORTD bit 5
#define MAX_DATA_PORT (PORTD)
#define max_data_pin 4
#define max_data_mask_high (1 << max_data_pin)
#define max_data_mask_low (~max_data_mask_high)

#define MAX_CLOCK_PORT (PORTD)
#define max_clock_pin 6
#define max_clock_mask_high (1 << max_clock_pin)
#define max_clock_mask_low (~max_clock_mask_high)

#define MAX_LOAD_PORT (PORTD)
#define max_load_pin 5
#define max_load_mask_high (1 << max_load_pin)
#define max_load_mask_low (~max_load_mask_high)

// indexed by row number
uint8_t ledmem[8];

// -----------------------------------------------------------------------
// max_send - helper function that sends a single byte of data to the MAX chip
static void max_send(uint8_t data)
{
	for (uint8_t i=8 ; i>0 ; i--) {
		uint8_t mask = 1 << (i-1); // get bitmask

		// check and send value of this bit
		if (data & mask) {
			MAX_DATA_PORT |= max_data_mask_high;
		} else {
			MAX_DATA_PORT &= max_data_mask_low;
		}

		// Pulse the MAX clock
		MAX_CLOCK_PORT &= max_clock_mask_low;  // "tick" prepeare for bit input
		MAX_CLOCK_PORT |= max_clock_mask_high; // "tock" input bit
	}
}

// -----------------------------------------------------------------------
// max_cmd is the "easy" function to use for a single max7219
// dig is the row call, and seg is the column call
// dig and seg refer to pin names from tech doc
static inline void max_cmd(uint8_t dig, uint8_t seg)
{
	MAX_LOAD_PORT &= max_load_mask_low;

	max_send(dig); // specify register
	max_send(seg); // ((data & 0x01) * 256) + data >> 1); // put data

	MAX_LOAD_PORT |= max_load_mask_high;
}

// -----------------------------------------------------------------------
void display_init()
{
	display_test(0);
	max_cmd(max7219_reg_scanLimit, 7);
	display_intensity(15);
	display_update();
	display_active(1);
}

// -----------------------------------------------------------------------
void display_update()
{
	for (uint8_t y=0 ; y<8 ; y++) {
		max_cmd(y+1, ledmem[y]);
	}
}

// -----------------------------------------------------------------------
void display_clear()
{
	for (uint8_t y=0 ; y<8 ; y++) {
		display_row(y, 0);
	}
}

// -----------------------------------------------------------------------
void display_pixel(uint8_t x, uint8_t y, uint8_t state)
{
	if (state == 0) {
		ledmem[y] &= ~(1 << x);
	} else {
		ledmem[y] |= (1 << x);
	}
}

// -----------------------------------------------------------------------
void display_row(uint8_t y, uint8_t value)
{
	ledmem[y] = value;
}

// -----------------------------------------------------------------------
void display_col(uint8_t x, uint8_t value)
{
	for (uint8_t y=0 ; y<8 ; y++) {
		display_pixel(x, y, value & 1);
		value >>= 1;
	}
}

// -----------------------------------------------------------------------
void display_intensity(uint8_t intensity)
{
	max_cmd(max7219_reg_intensity, intensity);
}

// -----------------------------------------------------------------------
void display_test(uint8_t state)
{
	max_cmd(max7219_reg_displayTest, state);
}

// -----------------------------------------------------------------------
void display_active(uint8_t state)
{
	max_cmd(max7219_reg_shutdown, state);
}

// vim: tabstop=4 shiftwidth=4 autoindent
