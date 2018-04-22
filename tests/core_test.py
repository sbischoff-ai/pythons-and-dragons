# -*- coding: utf-8 -*-
'''
For unit testing, install pytest package and run "pytest" in
the project folder.
'''

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(\
                os.path.dirname(__file__), '..')))

from pnd import core

def test_roll():
    for i in range(20):
        assert core.roll('1d6') in range(1,7)
        assert core.roll() in range(1,21)
        assert core.roll('1D8MIN 3') in range(3,9)
        assert core.roll('-4 d2 +12max 6') in range(4,7)