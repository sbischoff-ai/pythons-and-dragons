# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 21:05:51 2018

@author: silas
"""

import numpy.random as rd

def roll(dice = '1d20'):
    '''Returns the result of a die roll specified in *dice*.
    
    Parameters
    __________
    dice: string
        Specifies the die roll. It has to consist of terms
        of the form *'mdn'*, *'dn'* or *'m'* connected by 
        *'+'* or *'-'*, where *m* and *n* are integer numbers.
        Defaul is *'1d20'*.
    
    Returns
    _______
    int
        Sum of the terms specified in *dice*, where *dn*
        is a random integer from [1,n].'''
    result = 0
    dice = str(dice).lower().replace(' ', '').replace('-', '+-')\
                    .lstrip('+').split('+')
    for term in dice:
        term = term.split('d')
        if len(term) == 1:
            result += int(term[0])
        elif len(term) == 2:
            if term[0] == '':
                factor = 1
            elif term[0] == '-':
                factor = -1
            else:
                factor = int(term[0])
            result += factor*rd.randint(1,int(term[1])+1)
    return result