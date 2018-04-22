# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 21:05:51 2018

@author: silas
"""
import os as _os
import random as _rd
import json as _json

_rd.seed()

ruleset = dict( Name           = 'lotfp',
                Bonus_Table    = [[ 3, -3],
                                  [ 5, -2],
                                  [ 8, -1],
                                  [12,  0],
                                  [15, +1],
                                  [17, +2],
                                  [18, +3]],
                Abilities     = ['STR', 'DEX', 'CON',
                                 'INT', 'WIS', 'CHA'],
                Saving_Throws = ['Paralyze','Poison', 'Breath',
                                 'Device', 'Magic'])

classes = dict(
    Fighter = {'Min_HP' : 8,
               'Level'  : {
               1: {'Experience'   : 0,
                   'Saving_Throws': {'Paralyze': 14,
                                     'Poison'  : 12,
                                     'Breath'  : 15,
                                     'Device'  : 13,
                                     'Magic'   : 16},
                   'Hit_Dice'     : '+1d8',
                   'Spells'       : None,
                   'To_Hit'       : +1},
                                     
               2: {'Experience'   : 2000,
                   'Saving_Throws': {'Paralyze': 14,
                                     'Poison'  : 12,
                                     'Breath'  : 15,
                                     'Device'  : 13,
                                     'Magic'   : 16},
                   'Hit_Dice'     : '+1d8',
                   'Spells'       : None,
                   'To_Hit'       : +1},
                                     
               3: {'Experience'   : 4000,
                   'Saving_Throws': {'Paralyze': 14,
                                     'Poison'  : 12,
                                     'Breath'  : 15,
                                     'Device'  : 13,
                                     'Magic'   : 16},
                   'Hit_Dice'     : '+1d8',
                   'Spells'       : None,
                   'To_Hit'       : +1}
                          }
              })

def save_ruleset(name:str, save_classes:bool = True):
    '''Stores the ruleset in file, load with *load_ruleset(name)*.'''
    global ruleset, classes
    ruleset['Name'] = name
    if name not in _os.listdir('.\\store'):
        _os.mkdir('.\\store\\' + name)
        _os.mkdir('.\\store\\' + name + '\\classes')
    with open('.\\store\\' + name + '\\ruleset.json', mode = 'w') as file:
        _json.dump(ruleset, file)
    if save_classes:
        for class_to_save in classes:
            save_class(class_to_save)

def load_ruleset(name:str):
    '''Loads a stored ruleset with the given *name*.'''
    global ruleset, classes
    with open('.\\store\\' + name + '\\ruleset.json') as file:
        ruleset = _json.load(file)
    classes.clear()
    classes_to_load = _os.listdir('.\\store\\' + name + '\\classes')
    for class_to_load in classes_to_load:
        with open('.\\store\\' + name + \
                  '\\classes\\' + class_to_load) as file:
            classes[class_to_load.rstrip('.json')] = _json.load(file)

def save_class(class_name:str, target_ruleset:str = ruleset['Name']):
    '''Stores the class *class_name* on disk, load with 
    *load_ruleset(name)*.'''
    with open('.\\store\\' + target_ruleset + '\\classes\\' \
              + class_name + '.json', mode = 'w') as file:
        _json.dump(classes[class_name], file)

def roll(dice:str = '1d20') -> int:
    '''Returns the result of a die roll specified in *dice*.
    
    Parameters
    __________
    dice: string, default: '1d20'
        Specifies the die roll. It has to consist of terms
        of the form *'mdn'*, *'dn'* or *'m'* connected by 
        *'+'* or *'-'*, where *m* and *n* are integer numbers.
        One may also put *'best n of'* or *'worst n of'*
        before a dice term, where *n* has to be smaller than
        the number of dice. You can add *'min n'* to the end,
        where n is the enforced minimum result. The same is
        possible with *'max'* or both at the same time (in
        arbitrary order).
    
    Returns
    _______
    int
        Sum of the terms specified in *dice*, where *dn*
        is a uniformly distributed random integer from [1,n].'''
    result = 0
    def d(n): return _rd.randint(1,n)
    dice = str(dice).lower().replace(' ', '').replace('-', '+-')\
                    .lstrip('+').split('+')
    _min = float('-inf')
    _max = float('inf')
    first = True
    for term in reversed(dice):
        if first and term.__contains__('m'):
            minmax = term.split('m')
            term = minmax[0]
            if minmax[1].lstrip('in').isnumeric():
                _min = int(minmax[1].lstrip('in'))
            else:
                _max = int(minmax[1].lstrip('ax'))
            if len(minmax) == 3:
                if _min > float('-inf'):
                    _max = int(minmax[2].lstrip('ax'))
                else:
                    _min = int(minmax[2].lstrip('in'))
        term = term.split('d')
        if len(term) == 1:
            result += int(term[0])
        elif len(term) == 2:
            n = int(term[1])
            if term[0] == '':
                result += d(n)
            elif term[0] == '-':
                result -= d(n)
            elif term[0].__contains__('of'):
                pool = term[0].split('of')
                rolls = []
                for i in range(int(pool[1])): rolls.append(d(n))
                sgn = -1 if pool[0].startswith('-') else 1
                pool[0] = pool[0].lstrip('-')
                if pool[0].startswith('best'):
                    rolls.sort(reverse = True)
                    pool[0] = int(pool[0].lstrip('best'))
                elif pool[0].startswith('worst'):
                    rolls.sort()
                    pool[0] = int(pool[0].lstrip('worst'))
                if pool[0] > int(pool[1]): raise ValueError('Count your dice!')
                result += sgn*sum(rolls[:pool[0]])
            else:
                for i in range(int(term[0])): result += d(n)
        first = False
    if result > _max:
        result = _max
    elif result < _min:
        result = _min
    return result 

def _get_bonus(ability:int) -> int:
    '''Returns the ability bonus for an ability score according to
    the current ruleset.
    
    Parameters
    __________
    ability: int
        The ability score for which to return the bonus.
    
    Returns
    _______
    int
        The ability bonus according to the *bonus_table*
        of the current ruleset.
    '''
    for bonus in ruleset['Bonus_Table']:
        if ability <= bonus[0]: return bonus[1]
    return ruleset['Bonus_Table'][-1][1]

