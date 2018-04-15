# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 21:05:51 2018

@author: silas
"""

import random as _rd
import json as _json

_rd.seed()

ruleset = dict(bonus_table    = [[ 3, -3],
                                 [ 5, -2],
                                 [ 8, -1],
                                 [12,  0],
                                 [15, +1],
                                 [17, +2],
                                 [18, +3]],
                abilities     = ['STR', 'DEX', 'CON',
                                  'INT', 'WIS', 'CHA'],
                saving_throws = ['Paralyze','Poison', 'Breath',
                                 'Device', 'Magic'])

def save_ruleset(name:str):
    '''Stores the ruleset so it can be loaded with 
    *load_ruleset(name)* later.'''
    with open('.\\store\\rulesets\\' + name + '.json', mode = 'w') as file:
        _json.dump(ruleset, file, indent = 2)
    return None

def load_ruleset(name:str):
    '''Loads a stored ruleset with the given *name*.'''
    global ruleset
    with open('.\\store\\rulesets\\' + name + '.json') as file:
        ruleset = _json.load(file)
    return None

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
        the number of dice.
    
    Returns
    _______
    int
        Sum of the terms specified in *dice*, where *dn*
        is a uniformly distributed random integer from [1,n].'''
    result = 0
    def d(n): return _rd.randint(1,n)
    dice = str(dice).lower().replace(' ', '').replace('-', '+-')\
                    .lstrip('+').split('+')
    for term in dice:
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
    return result

def get_bonus(ability:int) -> int:
    '''Returns the ability bonus for an ability score within
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
    for bonus in ruleset['bonus_table']:
        if ability <= bonus[0]: return bonus[1]
    return ruleset['bonus_table'][-1][1]

