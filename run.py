#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, signal, time, threading
from functions import *
from ConfigParser import SafeConfigParser

try:
  import requests
except ImportError:
  print 'python-requests is not installed, please check the docs!'
  print 'https://github.com/p0nt/pontstrader'
  sys.exit()

try:
  import redis
except ImportError:
  print 'redis is not installed, please check the docs!'
  print 'https://github.com/p0nt/pontstrader'
  sys.exit()

try:
  from colorama import Fore, Back, Style, init
except ImportError:
  print 'python-colorama is not installed, please check the docs!'
  print 'https://github.com/p0nt/pontstrader'
  sys.exit()

def sigint_handler(signum, frame):
  print 'Stop pressing CTRL+C!'

signal.signal(signal.SIGINT, sigint_handler)

menu_actions  = {}  

# Main menu
def main_menu():
    os.system('clear')
    white((25 * '-'))
    green('  P O N T S T R A D E R  ')
    white((25 * '-'))
    yellow('1. Buy')
    yellow('2. Sell')
    yellow('3. Buy and Sell')
    yellow('4. Balances')
    yellow('5. Orderbook')
    yellow('6. Watch coin')
    yellow('7. Withdraw')
    yellow('8. Deposit')
    yellow('9. Arbitrage')
    yellow('10. Trailing Stop Loss (24/7)')
    yellow('11. Take Profit (24/7)')
    yellow('12. Stop Loss + Take Profit (24/7)')
    yellow('13. Trailing + Take Profit (24/7)')
    red("\n0. Quit")
    choice = raw_input(Fore.WHITE+" >>  ")
    exec_menu(choice)

    return

# Execute menu
def exec_menu(choice):
    os.system('clear')
    ch = choice.lower()
    if ch == '':
        menu_actions['main_menu']()
    else:
        try:
            menu_actions[ch]()
        except KeyError:
            print "Invalid selection, please try again.\n"
            menu_actions['main_menu']()
    return

# Read config
def read_config():
  try:
    configfile = (os.path.dirname(os.path.realpath(__file__))) + '/config.ini'
    parser = SafeConfigParser()
    parser.read(configfile)
    bittrex_key = str(parser.get('bittrex', 'key'))
    bittrex_secret = str(parser.get('bittrex', 'secret'))
    subscription_key = str(parser.get('subscription', 'key'))
    pushover_user = str(parser.get('pushover', 'user'))
    pushover_app = str(parser.get('pushover', 'app'))
    pushbullet_token = str(parser.get('pushbullet', 'token'))
    return bittrex_key, bittrex_secret, subscription_key, pushover_user, pushover_app, pushbullet_token
  except:
    print 'Unable to parse config.ini, make sure to read the manual first...exiting!'
    sys.exit()

# Buy
def menu_buy():
  buy(bittrex_key, bittrex_secret, subscription_key)
  menu_actions['main_menu']()
  return

# Sell
def menu_sell():
  sell(bittrex_key, bittrex_secret, subscription_key)
  menu_actions['main_menu']()
  return

# Buy and Sell
def menu_buysell():
  buysell(bittrex_key, bittrex_secret, subscription_key)
  menu_actions['main_menu']()
  return

# Balances
def menu_balances():
  balances(bittrex_key, bittrex_secret, subscription_key)
  menu_actions['main_menu']()
  return

# Orderbook
def menu_orderbook():
  orderbook(bittrex_key, bittrex_secret, subscription_key)
  menu_actions['main_menu']()
  return

# Watch
def menu_watch():
  watch(bittrex_key, bittrex_secret, subscription_key)
  menu_actions['main_menu']()
  return

# Withdraw
def menu_withdraw():
  withdraw(bittrex_key, bittrex_secret)
  menu_actions['main_menu']()
  return

# Deposit
def menu_deposit():
  deposit(bittrex_key, bittrex_secret)
  menu_actions['main_menu']()
  return

# Arbitrage
def menu_arbitrage():
  arbitrage(subscription_key)
  menu_actions['main_menu']()
  return

# Trailing
def menu_tsl():
  trailing(bittrex_key, bittrex_secret, pushover_user, pushover_app, pushbullet_token, subscription_key)
  menu_actions['main_menu']()
  return

# Take Profit
def menu_tp():
  takeprofit(bittrex_key, bittrex_secret, pushover_user, pushover_app, pushbullet_token, subscription_key)
  menu_actions['main_menu']()
  return

# Stop Loss Take Profit
def menu_sltp():
  stoplosstakeprofit(bittrex_key, bittrex_secret, pushover_user, pushover_app, pushbullet_token, subscription_key)
  menu_actions['main_menu']()
  return

# Trailing Take Profit
def menu_ttp():
  trailingtakeprofit(bittrex_key, bittrex_secret, pushover_user, pushover_app, pushbullet_token, subscription_key)
  menu_actions['main_menu']()
  return

# Back to main menu
def back():
    menu_actions['main_menu']()

# Exit program
def exit():
  count = threading.activeCount()
  if count > 1:
    threads = threading.enumerate()
    thread_counter = 0
    for t in threading.enumerate():
      if 'arbitrage' in t.name:
        pass
      elif 'Main' in t.name:
        pass
      else:
        thread_counter += 1
    if thread_counter > 0:
      yellow('WARNING: There are currently {0} active trade(s), are you sure you want to exit?'.format(thread_counter))
      green('1. yes')
      red('2. no')
      try:
        yes_no = raw_input(Fore.WHITE+'Enter your choice [1-2] : ')
        yes_no = int(yes_no)
      except:
        white('Invalid number... going back to Main Menu')
        menu_actions['main_menu']()
      if yes_no == 1:
        white('Exiting...')
        sys.exit()
      elif yes_no == 2:
        white('Ok... going back to Main Menu')
        menu_actions['main_menu']()
      else:
        white('Invalid number... going back to Main Menu')
        menu_actions['main_menu']()
    else:
      white('Exiting...')
      sys.exit()
  else:
    white('Exiting...')
    sys.exit()

# Menu definition
menu_actions = {
    'main_menu': main_menu,
    '1': menu_buy,
    '2': menu_sell,
    '3': menu_buysell,
    '4': menu_balances,
    '5': menu_orderbook,
    '6': menu_watch,
    '7': menu_withdraw,
    '8': menu_deposit,
    '9': menu_arbitrage,
    '10': menu_tsl,
    '11': menu_tp,
    '12': menu_sltp,
    '13': menu_ttp,
    '0': exit,
}

# Main Program
if __name__ == "__main__":
    readconfig = read_config()
    bittrex_key = str(readconfig[0])
    bittrex_secret = str(readconfig[1])
    subscription_key = str(readconfig[2])
    pushover_user = str(readconfig[3])
    pushover_app = str(readconfig[4])
    pushbullet_token = str(readconfig[5])
    main_menu()
