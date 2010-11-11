#!/usr/bin/env python
# -*- coding: utf-8 -*-

# CoffeTime.py: 당신이 농땡이 칠 때에도 바쁜 사람처럼 보이게 만드는 프로그램.
#             Ideas and grm files come from Cappucino(GTK) by
#             Enrico Zini & Cosimo Vagarini.
# Copyright (c) 2008 Homin Lee (Suapapa) <ff4500@gmail.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys

while(True):
    try:
        ret = os.system("polygen -X 1 %s" % "compileline.grm")
        if (ret != 0): sys.exit(0)
        sys.stdout.flush()
    except KeyboardInterrupt:
        sys.exit(0)

