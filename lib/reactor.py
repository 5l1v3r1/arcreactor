#!/usr/bin/env python
#
# part of ArcReactor application
#
# this module includes some of the 
# core functionality ArcReactor uses
# throughout the application. handles
# things like logging, message output,
# syslog events, interacting with config
# files and some preliminary database
# interaction.
#

import logging
import socket
import time
import os, sys
import ConfigParser
import signal

# define all our needed paths
PATH_HOME = '/opt/arcreactor'
PATH_LOGS = '/opt/arcreactor/var/logs'
PATH_DATA = '/opt/arcreactor/data'
PATH_CONF = '/opt/arcreactor/conf'
PATH_MODS = '/opt/arcreactor/lib'
PATH_HIST = '/opt/arcreactor/.console_history'

# define our config parser
config = ConfigParser.ConfigParser()


ascii = '''


  ______                       _______                                   __                         
 /      \                     /       \                                 /  |                        
/$$$$$$  |  ______    _______ $$$$$$$  |  ______    ______    _______  _$$ |_     ______    ______  
$$ |__$$ | /      \  /       |$$ |__$$ | /      \  /      \  /       |/ $$   |   /      \  /      \ 
$$    $$ |/$$$$$$  |/$$$$$$$/ $$    $$< /$$$$$$  | $$$$$$  |/$$$$$$$/ $$$$$$/   /$$$$$$  |/$$$$$$  |
$$$$$$$$ |$$ |  $$/ $$ |      $$$$$$$  |$$    $$ | /    $$ |$$ |        $$ | __ $$ |  $$ |$$ |  $$/ 
$$ |  $$ |$$ |      $$ \_____ $$ |  $$ |$$$$$$$$/ /$$$$$$$ |$$ \_____   $$ |/  |$$ \__$$ |$$ |      
$$ |  $$ |$$ |      $$       |$$ |  $$ |$$       |$$    $$ |$$       |  $$  $$/ $$    $$/ $$ |      
$$/   $$/ $$/        $$$$$$$/ $$/   $$/  $$$$$$$/  $$$$$$$/  $$$$$$$/    $$$$/   $$$$$$/  $$/       
                                                                                                    
                                    ArcReactor [version 1.0]
                                        ohdae [ams] - 2012
                                https://github.com/ohdae/arcreactor

'''   

def start_logger():
    # setup our logger
    # TODO: add log rotation function
    debug_log = PATH_LOGS+'/reactor.log'
    if os.path.exists(debug_log):
        # remove this print. debug msg.
        print('[*] logs will be appened to %s' % debug_log)
        logging.basicConfig(filename=debug_log, filemode='a',
                        format='%(asctime)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S', level=logging.DEBUG)
        return True
    else:
        status('error', 'arcreactor', 'log file does not exist.')
        return False

def signal_handler(signal, frame):
    status('info', 'arcreactor', 'Ctrl+C signal caught. shutting down ArcReactor')

def load_keywords(file_path):
    # basic function for loading all keyword based config files
    file_data = []
    if os.path.exists(file_path) is False:
        status('error', 'arcreactor', 'unable to load %s' % file_path)
        return False
    status('info', 'arcreactor', 'loading contents of %s' % file_path)
    f = open(file_path, 'rb')
    for line in f.readlines():
        # skip any commented lines
        if line.startswith('#'): continue
        # skip any empty lines
        text = line.strip('\n')
        if len(text) == 0: continue
        file_data.append(text)
    f.close()
    return file_data

def load_config(file_path):
    opts = {}
    # make sure the config file exists
    if not os.path.exists(file_path):
        return False
    # utilize the ConfigParser module for easier parsing
    config.read(file_path)
    opts['siem_host'] = config.get('syslog', 'host')
    opts['siem_port'] = config.getint('syslog', 'port')
    opts['siem_name'] = config.get('syslog', 'name')
    opts['siem_max'] = config.get('syslog', 'max')
    return opts 

def load_sources(file_path):
    # basic function for loading all www source config files
    file_data = []
    if os.path.exists(file_path) is False:
        status('error', 'arcreactor', 'unable to load %s' % file_path)
        return False
    status('info', 'arcreactor', 'loading contents of %s' % file_path)
    f = open(file_path, 'rb')
    for line in f.readlines():
        # skip all commented lines
        if line.startswith('#'): continue
        # skip all empty lines
        text = line.strip('\n')
        if len(text) == 0: continue
        if text.startswith('http'):
            file_data.append(text)
    f.close()
    return file_data

def status(level, module, message):
    msg = '%s - %s' % (module, message)
    if level == 'error':
        print('[!] %s' % msg)
        logging.error(msg)
    else:
        print('[~] %s' % msg)
        logging.info(msg)

def send_syslog(message):
    # create socket for sending syslog events
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 'notice' is the default event. 3 + 5 * 8
    # change this is need be
    data = '<%d>%s' % (29, message)
    sock.sendto(data, (opts['siem_host'], int(opts['siem_port'])))
    sock.close()

def test_syslog():
    try:
        send_syslog('DEBUG MESSAGE')
        return True
    except:
        return False






