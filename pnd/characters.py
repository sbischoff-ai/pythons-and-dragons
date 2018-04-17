# -*- coding: utf-8 -*-
"""
Created on Sun Apr 15 17:25:03 2018

@author: silas
"""

import core

class PlayerCharacter:
    '''Docstring is TODO'''
    def __init__(self, name:str, char_class:str = 'Fighter'):
        self.Name = name
        self.Abilities = dict([[ability, core.roll('3d6')]\
                               for ability in core.ruleset['Abilities']])
        self.Class = char_class
        self.Level = 1
        hit_dice = core.classes[self.Class]['Level'][1]['Hit_Dice']
        hit_dice += self.get_bonus('CON', roll = True)
        hit_dice += 'min' + str(core.classes[self.Class]['Min_HP'])
        self.Max_HP = core.roll(hit_dice)
        self.HP = self.Max_HP
        self.To_Hit = core.classes[self.Class]['Level'][1]['To_Hit']
        self.Experience = 0
        
    def level_up(self):
        #if self.Experience <
        self.Level += 1
        hit_dice = core.classes[self.Class]['Level'][self.Level]['Hit_Dice']
        hit_dice += self.get_bonus('CON', roll = True)
        bonus_hp = core.roll(hit_dice)
        self.Max_HP += bonus_hp
        self.HP += bonus_hp
        self.To_Hit += core.classes[self.Class]['Level'][self.Level]['To_Hit']
        
    def get_bonus(self, ability:str, roll:bool = False):
        bonus = core._get_bonus(self.Abilities[ability])
        if roll: return ('+'+str(bonus)).replace('+-','-')
        return bonus
    
class CharGenerator:
    def __init__(self):
        pass