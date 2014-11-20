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

#ifndef DISPLAY_H
#define DISPLAY_H

void display_init();

void display_clear();
void display_pixel(uint8_t x, uint8_t y, uint8_t state);
void display_row(uint8_t row, uint8_t value);
void display_col(uint8_t col, uint8_t value);
void display_update();

void display_intensity(uint8_t intensity);
void display_test(uint8_t state);
void display_active(uint8_t state);

#endif

// vim: tabstop=4 shiftwidth=4 autoindent
