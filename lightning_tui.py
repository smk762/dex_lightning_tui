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
author = '{:^100}'.format('AtomicDEX Lightning TUI v0.1 by Dragonhound')


def main():
    tui = LightningTUI()
    status = tui.get_status()

    while True:
        try:
            os.system('clear')
            print(colorize(header, 'lightgreen'))
            print(colorize(author, 'cyan'))
            print("")
            if status['lightning_status'] == "Initialized":
                line1 = f"[{status['lightning_name']} | {status['lightning_status']} | Port {status['lightning_port']} | Color #{status['lightning_color']}]"
                line2 = f"[{status['platform_coin']} | {status['coin_address']} | {status['coin_balance']}]"
                line3 = f"[{status['coin']} | {status['lightning_address']} | {status['lightning_balance']}]"
                print(colorize('{:^100}'.format(line1), 'orange'))
                print(colorize('{:^100}'.format(line2), 'orange'))
                print(colorize('{:^100}'.format(line3), 'orange'))

            else: print(colorize('{:^100}'.format("Lightning not initialized. Please initialize lightning first."), "red"))
            print("")

            try:
                for item in tui.menu_items:
                    i = tui.menu_items.index(item)
                    option = list(item.keys())[0]
                    print(colorize(f"{' '*6}[{i}] {option}", 'blue'))
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
        status = tui.get_status()
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