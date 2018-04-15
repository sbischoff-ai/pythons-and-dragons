# -*- coding: utf-8 -*-
"""
Created on Sun Apr 15 17:25:03 2018

@author: silas
"""

from core import roll as _roll, ruleset as _ruleset

class PlayerCharacter:
    '''Docstring is TODO'''
    def __init__(self, name:str):
        self.name = name
        self.abilities = dict([[ability, _roll('3d6')]\
                               for ability in _ruleset['abilities']])
        self.hp = 6
        self.level = 1

class CharGenerator:
    def __init__(self):
        pass