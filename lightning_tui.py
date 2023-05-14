#!/usr/bin/env python3
import os
import time
from lib_tui import LightningTUI, colorize, color_input

header = '''
            _                  _      _____  ________   __  
       /\  | |                (_)    |  __ \|  ____\ \ / /  
      /  \ | |_ ___  _ __ ___  _  ___| |  | | |__   \ V /   
     / /\ \| __/ _ \| '_ ` _ \| |/ __| |  | |  __|   > <    
    / ____ \ || (_) | | | | | | | (__| |__| | |____ / . \   
   /_/    \_\__\___/|_| |_| |_|_|\___|_____/|______/_/ \_\  
     _       _         _      _           _                 
    | |     (_)       | |    | |         (_)                
    | |      _   __ _ | |__  | |_  _ __   _  _ __    __ _   
    | |     | | / _` || '_ \ | __|| '_ \ | || '_ \  / _` |  
    | |____ | || (_| || | | || |_ | | | || || | | || (_| |  
    |______||_| \__, ||_| |_| \__||_| |_||_||_| |_| \__, |  
                 __/ |                               __/ |  
                |___/                               |___/   
'''
author = '{:^60}'.format('AtomicDEX Lightning TUI v0.1 by Dragonhound')


def main():
    tui = LightningTUI()

    while True:
        try:
            os.system('clear')
            print(colorize(header, 'lightgreen'))
            print(colorize(author, 'cyan'))
            print("")

            try:
                for item in tui.menu_items:
                    i = tui.menu_items.index(item)
                    option = list(item.keys())[0]
                    print(colorize(f"[{i}] {option}", 'blue'))
                choice = color_input("\n Select menu option: ")
                if int(choice) < 0:
                    raise ValueError
                print("")
                if int(choice) == 0:
                    node = list(tui.menu_items[int(choice)].values())[0]()
                else:
                    list(tui.menu_items[int(choice)].values())[0]()
                print("")
            except (ValueError, IndexError):
                print(colorize("Invalid menu option!", 'error'))
                pass
            except Exception as e:
                print(colorize(f"Error: {e}", 'error'))
                pass
        except KeyboardInterrupt:
            tui.exit_tui()
        input(colorize("Press Enter to continue...", 'orange'))

def show_logo(logofile="logo.txt"):
    os.system('clear')
    print("\n")
    with (open(logofile, "r")) as logo:
        for line in logo:
            parts = line.split(' ')
            row = ''
            for part in parts:
                if part.find('~') == -1:
                    row += colorize(part, 'blue')
                else:
                    row += colorize(part, 'black')
            print(row, end='')
            time.sleep(0.04)
        time.sleep(0.4)
    print("\n")

if __name__ == "__main__":

    show_logo()
    main()
    print("Done, Exiting...")