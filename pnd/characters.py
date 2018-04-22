# -*- coding: utf-8 -*-
"""
Created on Sun Apr 15 17:25:03 2018

@author: silas
"""

import core

class _Character:
    '''Is abstract base class for PlayerCharacters and NonPlayerCharacters'''

    Max_HP = 4
    HP = 4
    Abilities = None
    Saving_Throws = None
    To_Hit = 0
    
    def __init__(self, name:str):
        self.Name = name
        self.Abilities = dict([[ability, 10] \
                               for ability in core.ruleset['Abilities']])
        self.Saving_Throws = dict([[save, 16] \
                                   for save in core.ruleset['Saving_Throws']])
    
    def ability_bonus(self, ability:str, roll:bool = False):
        '''Returns the ability bonus for *ability* according to the current
        ruleset.'''
        bonus = core._get_bonus(self.Abilities[ability])
        if roll: return ('+'+str(bonus)).replace('+-','-')
        return bonus
        

class PlayerCharacter(_Character):
    '''Docstring is TODO'''
    
    Class = None
    Level = 1
    Experience = 0
    Next_Level = 0
    
    def __init__(self, name:str, char_class:str = 'Fighter'):
        _Character.__init__(self, name)
        self.Abilities = dict([[ability, core.roll('3d6')]\
                               for ability in core.ruleset['Abilities']])
        self.Class = char_class
        self.Saving_Throws = core.classes[self.Class]['Level']\
                                         [1]['Saving_Throws']
        hit_dice = core.classes[self.Class]['Level'][1]['Hit_Dice']
        hit_dice += self.ability_bonus('CON', roll = True)
        hit_dice += 'min' + str(core.classes[self.Class]['Min_HP'])
        self.Max_HP = core.roll(hit_dice)
        self.HP = self.Max_HP
        self.To_Hit = core.classes[self.Class]['Level'][1]['To_Hit']
        self.Next_Level = core.classes[self.Class]['Level']\
                                      [2]['Experience']
        
    def level_up(self):
        assert self.Experience >= self.Next_Level
        self.Level += 1
        self.Saving_Throws = core.classes[self.Class]['Level']\
                                         [self.Level]['Saving_Throws']
        hit_dice = core.classes[self.Class]['Level'][self.Level]['Hit_Dice']
        hit_dice += self.ability_bonus('CON', roll = True)
        bonus_hp = core.roll(hit_dice)
        self.Max_HP += bonus_hp
        self.HP += bonus_hp
        self.To_Hit += core.classes[self.Class]['Level']\
                                   [self.Level]['To_Hit']
        try:
            self.Next_Level = core.classes[self.Class]['Level']\
                                          [self.Level+1]['Experience']
        except KeyError:
            self.Next_Level = float('inf')
    
class CharGenerator:
    def __init__(self):
        pass