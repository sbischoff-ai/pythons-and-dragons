# -*- coding: utf-8 -*-
"""
Created on Sun Apr 15 17:25:03 2018

@author: silas
"""

import pnd.core as core

class _Character:
    '''Is abstract base class for PlayerCharacters and NonPlayerCharacters'''
    
    def __init__(self, name:str):
        self.Name = name
        self.Max_HP = 4
        self.HP = 4
        self.Abilities = dict([[ability, 10] for ability in core.ruleset['Abilities']])
        self.Saving_Throws = dict([[save, 16] for save in core.ruleset['Saving_Throws']])
        self.To_Hit = 0
    
    def ability_bonus(self, ability:str, roll:bool = False):
        '''Returns the ability bonus for an ability score according to
        the current ruleset.
    
        Parameters
        __________
        ability: str
            The ability for which to return the bonus as a string such as *'STR'* or *'DEX'*.
        
        roll: bool, default = False
            Whether or not the result should be a string compatible with the *roll()* function from the core module.
    
        Returns
        _______
        int
            The ability bonus according to the *bonus_table*
            of the current ruleset.
        
        if roll == True: str
            The ability bonus as a string of the form *'+2'* or *'-1'*, compatible with *pnd.core.roll()*.
        '''
        result = core.ruleset['Bonus_Table'][-1][1]
        for bonus in core.ruleset['Bonus_Table']:
            if self.Abilities[ability] <= bonus[0]: result = bonus[1]
        if roll: return ('+'+str(result)).replace('+-','-')
        return result
        

class PlayerCharacter(_Character):
    '''Docstring is TODO'''
    
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
        self.Experience = 0
        self.Level = 1
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