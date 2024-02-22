''' chad.py - the main program of chad '''
from __future__ import annotations

import sys
import shutil
import os
import configparser
from pathlib import Path
from utils.sendMessage import send_text
from utils.openai import (
    spicy_gpt,
    funny_gpt,
    mario_gpt,
    chad_gpt
)
from utils.query import (
    find_guid_by_display_name,
    pull_latest_text_message,
    wal_checkpoint
)
import logging
import json
import time


current_dir = os.path.dirname(os.path.abspath(__file__))
# chat_room = 'Pasteurized EGG'

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


def main():
    validate_python()
    validate_dbfile()
    wal_checkpoint(chat_db)
    last_msg = None
    while True:
        guid = find_guid_by_display_name(chat_db, chat_room)
        msg = pull_latest_text_message(chat_db, guid)
        if debug_mode:
            logger.info(f'GUID: {guid}')
        if msg == last_msg:
            if debug_mode:
                logger.info('No new messages. Refreshing...')
                logger.info('Sleep for 5s..')
            copy_db()
            wal_checkpoint(chat_db)
            time.sleep(5)
        else:
            if debug_mode:
                logger.info('New Messages found!')
                logger.info(guid)
                logger.info(msg)
            last_msg = msg
            text = msg['text']

            if msg['sender'] == '+13212761077':
                # Marcella
                response = funny_gpt(text, API_KEY)

            elif msg['sender'] == '+14075294686':
                # Edd
                response = spicy_gpt(text, API_KEY)

            elif msg['sender'] == '+19416269361':
                # Mario
                response = mario_gpt(text, API_KEY)

            else:
                response = chad_gpt(text, API_KEY)

            logger.info(response)
            send_text(response, chat_room)


if __name__ == "__main__":
    main()
