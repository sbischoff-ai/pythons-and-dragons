# -*- coding: utf-8 -*-

import cmd, pnd.core

class PnD(cmd.Cmd):
    intro = '''

        ______      _   _                           ______                                 
        | ___ \    | | | |                     ___  |  _  \                                
        | |_/ /   _| |_| |__   ___  _ __  ___ ( _ ) | | | |_ __ __ _  __ _  ___  _ __  ___ 
        |  __/ | | | __| '_ \ / _ \| '_ \/ __|/ _ \/\ | | | '__/ _` |/ _` |/ _ \| '_ \/ __|
        | |  | |_| | |_| | | | (_) | | | \__ \ (_>  < |/ /| | | (_| | (_| | (_) | | | \__ \\
        \_|   \__, |\__|_| |_|\___/|_| |_|___/\___/\/___/ |_|  \__,_|\__, |\___/|_| |_|___/
               __/ |                                                  __/ |                
              |___/                                                  |___/                 
        
        '''
    
    prompt = 'PnD: '

    def do_exit(self, arg):
        print('Thank you for using PnD.')
        return True
    
    def do_roll(self, arg):
        try:
            result = pnd.core.roll(arg)
            print(str(result))
        except ValueError as error:
            print(error)

PnD().cmdloop()