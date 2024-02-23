''' chad.py - the main program of chad '''
from __future__ import annotations

import sys
import shutil
import os
import configparser
from pathlib import Path
from utils.sendMessage import send_text
from utils import query
import logging
import json
import time


current_dir = os.path.dirname(os.path.abspath(__file__))

config = configparser.ConfigParser()
config.read('config.ini')
chat_room = config.get('settings', 'chat_room')
debug_mode = config.getboolean('settings', 'debug_mode')
log_file = config.get('settings', 'log_file')
chat_db = config.get('settings', 'chat_db')
chat_db = Path(f'{current_dir}/{chat_db}').expanduser()
API_KEY = config.get('settings', 'API_KEY')


class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_message = {
            "level": record.levelname,
            "name": record.name,
            "msg": record.getMessage(),
            "time": self.formatTime(record, self.datefmt),
        }

        # Include any additional fields
        if hasattr(record, 'extra_field'):
            log_message['extra_field'] = record.extra_field

        return json.dumps(log_message)


if debug_mode:
    # Configure Logger
    logger = logging.getLogger('debug_logger')
    logger.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)

    console_handler.setFormatter(JsonFormatter())
    file_handler.setFormatter(JsonFormatter())

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)


class PasteurizedEgg:
    def edd(self):
        data = {'name': 'Edd Siu',
                'number': '+14075294686'}
        return data

    def marcella(self):
        data = {'name': 'Marcella Grillo',
                'number': '+13212761077'}
        return data

    def mario(self):
        data = {'name': 'Mario Massad',
                'number': '+19416269361'}
        return data

    def ofd(self):
        data = {'name': 'OFD',
                'number': ['+14042101792', 'self']}
        return data


def validate_python():
    return sys.version_info >= (3, 10)


def copy_db():
    original_chat_db = Path('~/Library/Messages/chat.db').expanduser()
    wal = Path(f'{original_chat_db}-wal')
    wal_prod = Path(f'{chat_db}-wal')
    shm = Path(f'{original_chat_db}-shm')
    shm_prod = Path(f'{chat_db}-shm')
    if debug_mode:
        logger.info(f'Copying {original_chat_db} to {chat_db}...')
        logger.info(f'Copying {wal} to {wal_prod}...')
        logger.info(f'Copying {shm} to {shm_prod}...')
    shutil.copyfile(wal, wal_prod)
    shutil.copyfile(original_chat_db, chat_db)
    shutil.copyfile(shm, shm_prod)


def validate_dbfile():
    if not os.path.exists(chat_db):
        copy_db()


def last_message():
    data = {}
    lm = Path(f'{current_dir}/.cache')
    if not os.path.exists(lm):
        with open(lm, 'w') as f:
            f.write(json.dumps(data))
    else:
        with open(lm, 'r') as f:
            data = f.read()
    data = json.loads(data)
    return data


class Bot:
    def __init__(self, name):
        from openai.assistants import Assistant
        # check if Bot/Assistant exists
        exists, aid = self.check_assistant_exist(name)
        if not exists:
            # create assistant if needed
            self.assistant = Assistant.create_default_assistant()
        else:
            self.assistant = Assistant.get_assistant(aid)

    def check_assistant_exist(self, name):
        assistants = self.a.list_assistants()
        assistants = assistants['data']
        a_list = []
        for assistant in assistants:
            name = assistant['name']
            aid = assistant['id']
            item = {name: aid}
            a_list.append(item)
        for key, value in a_list:
            if key == name:
                return True, value
        return False


def main():
    validate_python()
    validate_dbfile()
    query.wal_checkpoint(chat_db)
    # need to replace this with a file
    last_msg = None
    while True:
        guid = find_guid
        chad = Bot('ChadGPT')


if __name__ == "__main__":
    main()
