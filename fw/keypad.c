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

#include <avr/io.h>

#include "keypad.h"

// Connections to the 164 shift register:
// r164_data_pin  = 3 = PORTD, bit 3
// r164_clock_pin = 2 = PORTD, bit 2

#define R164_DATA_PORT (PORTD)
#define r164_data_pin 3
#define r164_data_mask_high (1 << r164_data_pin)
#define r164_data_mask_low (~r164_data_mask_high)

#define R164_CLOCK_PORT (PORTD)
#define r164_clock_pin 2
#define r164_clock_mask_high (1 << r164_clock_pin)
#define r164_clock_mask_low (~r164_clock_mask_high)

// Connections to the 165 shift register:
// r165_load_pin  = arduino digital pin 8 = PORTB, bit 0
// r165_data_pin  = arduino digital pin 9 = PORTB, bit 1
// r165_clock_pin = arduino digital pin 7 = PORTD, bit 7

#define R165_LOAD_PORT (PORTB)
#define r165_load_pin 0
#define r165_load_mask_high (1 << r165_load_pin)
#define r165_load_mask_low (~r165_load_mask_high)

#define R165_DATA_PORT (PINB)
#define r165_data_pin 1
#define r165_data_mask (1 << r165_data_pin)

#define R165_CLOCK_PORT (PORTD)
#define r165_clock_pin 7
#define r165_clock_mask_high (1 << r165_clock_pin)
#define r165_clock_mask_low (~r165_clock_mask_high)

#define kButtonUpDefaultDebounceCount 12 // Default debouce count

uint8_t button_current[8];				// current physical state
uint8_t button_last[8];					// previous physical state
uint8_t button_state[8];				// debounced state
uint8_t button_event[8];				// final state changed
uint8_t button_debounce_count[8][8];	// debouncer

// -----------------------------------------------------------------------
void buttonCheck(uint8_t row, uint8_t index)
{
	// if the current physical button state is different from the
	// last physical button state AND the current debounced state
	if (((button_current[row] ^ button_last[row]) & (1 << index))
	&& ((button_current[row] ^ button_state[row]) & (1 << index))) {
		// if the current physical button state is depressed
		if (button_current[row] & (1 << index)) {
			// queue up a new button event immediately
			button_event[row] = 1 << index;
			// and set the debounced state to down.
			button_state[row] |= (1 << index);
		// otherwise the button was previously depressed and now
		// has been released so we set our debounce counter.
		} else {
			button_debounce_count[row][index] = kButtonUpDefaultDebounceCount;
		}

	// if the current physical button state is the same as
	// the last physical button state but the current physical
	// button state is different from the current debounce state...
	} else if (((button_current[row] ^ button_last[row]) & (1 << index)) == 0
	&& (button_current[row] ^ button_state[row]) & (1 << index)) {
		// if the the debounce counter has
		// been decremented to 0 (meaning thebutton has been up for
		// kButtonUpDefaultDebounceCount iterations
		if ((button_debounce_count[row][index] > 0) && (--button_debounce_count[row][index] == 0)) {

			// queue up a button state change event
			button_event[row] = 1 << index;

			// and toggle the buttons debounce state.
			if (button_current[row] & (1 << index)) {
				button_state[row] |= (1 << index);
			} else {
				button_state[row] &= ~(1 << index);
			}
		}
	}
}

// -----------------------------------------------------------------------
void keypad_scan(button_event_f event_fun)
{
	R164_DATA_PORT &= r164_data_mask_low;

	// 164 register
	for (uint8_t i=0 ; i<8 ; i++) {
		R164_CLOCK_PORT |= r164_clock_mask_high;
		R164_CLOCK_PORT &= r164_clock_mask_low;
		R164_DATA_PORT |= r164_data_mask_high;

		// SlowDown is put in here to waste a little time while we wait for the state of the output
		// pins to settle. Without this time wasting loop, a single button press would show up as
		// two presses (the button and its neighbour)
		volatile int SlowDown = 0;
		while (SlowDown < 15) {
			SlowDown++;
		}

		button_last[i] = button_current[i];

		// 165 register
		R165_LOAD_PORT &= r165_load_mask_low;
		R165_LOAD_PORT |= r165_load_mask_high;

		for (uint8_t id=0 ; id<8 ; id++) {

			if ((R165_DATA_PORT & r165_data_mask) >> 1 == 0) {
				button_current[i] |= (1 << id);
			} else {
				button_current[i] &= ~(1 << id);
			}

			R165_CLOCK_PORT |= r165_clock_mask_high;
			R165_CLOCK_PORT &= r165_clock_mask_low;

			buttonCheck(i, id);

			if (button_event[i] & (1 << id)) {
				button_event[i] &= ~(1 << id);
				uint8_t state = button_state[i] & (1 << id);
				event_fun(id, i, state);
			}
		}
	}
}

// vim: tabstop=4 shiftwidth=4 autoindent
