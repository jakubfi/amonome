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

#include <util/delay.h>

#include "display.h"

// -----------------------------------------------------------------------
void startup_anim()
{
	uint8_t v = 0b00001111;

	for (int8_t i=7 ; i>=0 ; i--) {
		display_col(0, (v<<i) & 0xf0);
		display_update();
		_delay_ms(40);
	}
}

// vim: tabstop=4 shiftwidth=4 autoindent
