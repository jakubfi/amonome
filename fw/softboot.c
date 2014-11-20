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

#include <avr/wdt.h>
#include <avr/io.h>
#include <avr/interrupt.h>
#include <util/delay.h>

#include "serial.h"
#include "keypad.h"
#include "display.h"

// -----------------------------------------------------------------------
static void softboot_anim()
{
	display_clear();
	for (uint8_t i=0 ; i<2 ; i++) {
		display_row(3, 0b00011000);
		display_row(4, 0b00011000);
		display_update();
		_delay_ms(50);
		display_row(3, 0);
		display_row(4, 0);
		display_update();
		_delay_ms(50);
	}
}

// -----------------------------------------------------------------------
void softboot_do()
{
	serial_end();
	cli();
	softboot_anim();

	GPIOR0 = 0xaa;
	((void*(*)(void))0x3e00)();
}

// -----------------------------------------------------------------------
void softboot_button_event(uint8_t x, uint8_t y, uint8_t state)
{
	if (state) {
		if ((x == 0) && (y == 7)) {
			softboot_do();
		}
	}
}

// -----------------------------------------------------------------------
void softboot_check()
{
	for (uint8_t i=0 ; i<50 ; i++) {
		keypad_scan(softboot_button_event);
	}
}

// vim: tabstop=4 shiftwidth=4 autoindent
