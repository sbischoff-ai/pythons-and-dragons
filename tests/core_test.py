# -*- coding: utf-8 -*-
'''
For unit testing, install pytest package and run "pytest" in
the project folder.
'''

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(\
                os.path.dirname(__file__), '..')))
import pytest
from pnd import core

class mock_AppDirs:
    def __init__(self, tempdir):
        self.user_data_dir = tempdir.mkdir('user_data')
        self.user_config_dir = tempdir.mkdir('user_config')

def test_appdata(tmpdir):
    core._dirs = mock_AppDirs(tmpdir)
    core.save_ruleset('ruleset1', save_classes = False)
    assert core.ruleset['Name'] == 'ruleset1'
    assert os.path.exists(tmpdir.join('user_data', 'ruleset1', 'classes'))
    assert len(os.listdir(tmpdir.join('user_data', 'ruleset1', 'classes'))) == 0
    assert 'ruleset.json' in os.listdir(tmpdir.join('user_data', 'ruleset1'))
    core.save_ruleset('ruleset2')
    assert core.ruleset['Name'] == 'ruleset2'
    assert 'Fighter.json' in os.listdir(tmpdir.join('user_data', 'ruleset2', 'classes'))
    core.save_class('Fighter', target_ruleset = 'ruleset1')
    assert 'Fighter.json' in os.listdir(tmpdir.join('user_data', 'ruleset1', 'classes'))

def test_roll():
    for _ in range(20):
        assert core.roll('1d6') in range(1,7)
        assert core.roll() in range(1,21)
        assert core.roll('1D8MIN 3') in range(3,9)
        assert core.roll('-4 d2 +12max 6') in range(4,7)
        assert core.roll('5ma X  3') == 3
        assert core.roll('d4') in range(1,5)
        assert core.roll('worst 2 of6    D3-2 mIN2') in range(2,5)
        assert core.roll('2d6+2d2-4d4+12') in range(0,29)
    with pytest.raises(ValueError): core.roll('min2')
    with pytest.raises(ValueError): core.roll('2W8')
    with pytest.raises(ValueError): core.roll('best 4 of 3d4')