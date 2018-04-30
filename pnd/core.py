# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 21:05:51 2018

@author: silas
"""
import os
import appdirs
import random
import json

# Init appdirs
_dirs = appdirs.AppDirs('pnd', 'sbischoff-ai')
if not os.path.exists(_dirs.user_data_dir):
    os.makedirs(_dirs.user_data_dir)
if not os.path.exists(_dirs.user_config_dir):
    os.makedirs(_dirs.user_config_dir)

# Init ruleset
classes = {}
ruleset = {}
def _init_ruleset():
    global ruleset, classes
    storepath = os.path.join(os.path.dirname(__file__), 'resources', 'init_store', 'lotfp')
    with open(os.path.join(storepath, 'ruleset.json')) as file:
        ruleset = json.load(file)
    for class_to_load in os.listdir(os.path.join(storepath, 'classes')):
        with open(os.path.join(storepath, 'classes', class_to_load)) as file:
            classes[class_to_load.rstrip('.json')] = json.load(file)
_init_ruleset()

def save_ruleset(name:str, save_classes:bool = True):
    '''Stores the ruleset in file, load with *load_ruleset(name)*.'''
    global ruleset, classes
    ruleset['Name'] = name
    if not os.path.exists(os.path.join(_dirs.user_data_dir, name)):
        os.makedirs(os.path.join(_dirs.user_data_dir, name, 'classes'))
    with open(os.path.join(_dirs.user_data_dir, name, 'ruleset.json'), mode = 'w') as file:
        json.dump(ruleset, file, indent = 4)
    if save_classes:
        for class_to_save in classes:
            save_class(class_to_save, target_ruleset = name)

def load_ruleset(name:str):
    '''Loads a stored ruleset with the given *name*.'''
    global ruleset, classes
    storepath = os.path.join(_dirs.user_data_dir, name)
    with open(os.path.join(storepath, 'ruleset.json')) as file:
        ruleset = json.load(file)
    classes.clear()
    classes_to_load = os.listdir(os.path.join(storepath, 'classes'))
    for class_to_load in classes_to_load:
        with open(os.path.join(storepath, 'classes', class_to_load)) as file:
            classes[class_to_load.rstrip('.json')] = json.load(file)

def save_class(class_name:str, target_ruleset:str = ruleset['Name']):
    '''Stores the class *class_name* on disk, load with 
    *load_ruleset(name)*.'''
    with open(os.path.join(_dirs.user_data_dir, target_ruleset, 'classes', class_name + '.json'), mode = 'w') as file:
        json.dump(classes[class_name], file, indent = 4)

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
    def d(n): return random.randint(1,n)
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
                for _ in range(int(pool[1])): rolls.append(d(n))
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
                for _ in range(int(term[0])): result += d(n)
        first = False
    if result > _max:
        result = _max
    elif result < _min:
        result = _min
    return result