''' chad.py - the main program of chad '''
from __future__ import annotations

import sys
import os
import json
import time
import shutil
import configparser
from pathlib import Path
from utils import query
from utils.sendMessage import send_text
from utils.logging_config import configure_logging
from openai.runs import Run
from openai.threads import Thread
from openai.messages import Message
from openai.assistants import Assistant
from openai.constraint import (
    spicy_latina,
    dad_joke,
    mario,
    ofd
)


current_dir = os.path.dirname(os.path.abspath(__file__))
config = configparser.ConfigParser()
config.read('config.ini')
chat_room = config.get('settings', 'chat_room')
chat_db = config.get('settings', 'chat_db')
chat_db = Path(f'{current_dir}/{chat_db}').expanduser()
API_KEY = config.get('settings', 'API_KEY')
debug_mode = config.getboolean('settings', 'debug_mode')
log_file = config.get('settings', 'log_file')
logger = configure_logging(debug_mode, log_file)


class PasteurizedEgg:
    def __init__(self):
        room_name = 'Pasteurized EGG'
        users = [self.edd,
                 self.marcella,
                 self.mario,
                 self.ofd]
        numbers = []
        instructions = {}
        for n in users:
            number = n['number']
            numbers.append(number)
            instructions[number] = n['instruction']
        return room_name, users, numbers, instructions

    def edd(self):
        data = {'name': 'Edd Siu',
                'number': '+14075294686',
                'instruction': spicy_latina}
        return data

    def marcella(self):
        data = {'name': 'Marcella Grillo',
                'number': '+13212761077',
                'instruction': dad_joke}
        return data

    def mario(self):
        data = {'name': 'Mario Massad',
                'number': '+19416269361',
                'instruction': mario}
        return data

    def ofd(self):
        data = {'name': 'OFD',
                'number': '+14042101792',
                'instruction': ofd}
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
        logger.info('Copying chat.db')
    else:
        logger.info('chat.db found!')
    return True


def read_last_message():
    logger.info('Check if cache exist')
    data = {}
    lm = Path(f'{current_dir}/.cache')
    if not os.path.exists(lm):
        logger.debug('cache not exist, create cache', extra={'function': 'read_last_message'})
        with open(lm, 'w') as f:
            f.write(json.dumps(data))
    else:
        logger.debug('cache exist', extra={'function': 'read_last_message'})
        with open(lm, 'r') as f:
            data = f.read()
    data = json.loads(data)
    logger.debug(data)
    return data


def write_last_message(msg):
    lm = Path(f'{current_dir}/.cache')
    data = json.dumps(msg)
    with open(lm, 'w') as f:
        f.write(data)
    logger.info('Write latest message to cache')
    return True, data


class Bot:
    def __init__(self, name, chat_room):
        # check if Bot/Assistant exists
        logger.info(f'Check if assistant {name} exist for {chat_room}', extra={'class': 'Bot'})
        exists, aid = self.check_assistant_exist(name)
        if not exists:
            self.assistant = Assistant.create_default_assistant()
        else:
            self.assistant = Assistant.get_assistant(aid)
        self.room_name, self.users, self.numbers, self.user_instructions = PasteurizedEgg()
        if chat_room == self.room_name:
            '''
            thread_dict example: {'+13213211234': 'thread_id'}
            '''
            self.thread_dict = self.create_threads(aid, self.users)
        logger.info('Loading contacts', extra={'class': 'Bot'})
        return aid

    def read_responses(self, messages):
        response = ''
        for msg in messages['data']:
            if msg['role'] == 'assistant':
                content = msg['content']
                for m in content:
                    response += m['text']['value'] + ' '
        return response

    def check_assistant_exist(self, name):
        logger.info('Listing assistants...', extra={'class': 'Bot', 'function': 'check_assistant_exist'})
        assistants = self.a.list_assistants()
        assistants = assistants['data']
        for assistant in assistants:
            assistant_name = assistant['name']
            aid = assistant['id']
            if assistant_name == name:
                logger.info('Listing assistants...', extra={'class': 'Bot', 'function': 'check_assistant_exist'})
                return True, aid
                logger.info(f'Assistant {name} does not exist, creating...', extra={'class': 'Bot', 'function': 'check_assistant_exist'})
        return False, None

    def add_thread(self, sender, msg, aid):
        '''
        '''
        logger.info(f'Creating thread for {sender}')
        thread_metadata = {'number': sender}
        run = Run.create_thread_and_run(aid, msg, t_metadata=thread_metadata)
        tid = run['thread_id']
        logger.debug('OpenAI Run', extra={'value': run})
        self.thread_dict[sender] = tid
        return run, tid

    def create_threads(self, aid, users):
        '''return
        {'+13210004444': 'thread_id'}
        '''
        logger.info('Initialize threads for users..')
        tids = {}
        for user in users:
            number = user['number']
            tid = Thread.create_thread(metadata=user)
            tids[number] = tid
        logger.debug('Users', extra={'value': users})
        logger.debug('Thread IDs', extra={'value': tid})
        return tids


def main():
    if validate_python():
        logger.info('Python3 >= 3.10', extra={'function': 'main'})
    if validate_dbfile():
        logger.info('Python Version is good.', extra={'function': 'main'})
    query.wal_checkpoint(chat_db)
    logger.info('Chat.db checkpointing...')
    # need to replace this with a file
    last_msg = read_last_message()
    while True:
        guid = query.find_guid_by_display_name(chat_db, chat_room)
        msg = query.pull_latest_text_message(chat_db, guid)
        chad = Bot('ChadGPT', chat_room)
        if msg == last_msg:
            time.sleep(5)
            copy_db()
            query.wal_checkpoint(chat_db)
        else:
            write_last_message(msg)
            text = msg['text']
            sender = msg['sender']

        if sender in chad.numbers:
            tid = chad.thread_dict[sender]
            message = Message.create_message(tid, text)
            prompt = chad.user_instructions[sender]
            run = Run.create_run(tid, chad, instructions=prompt)
        else:
            run, tid = chad.add_thread(sender, text, chad)
            message = Message.get_messages_from_thread(tid)

        run_id = run['id']
        finish, run = Run.get_run(tid, run_id)
        if finish:
            logger.debug('OpenAI Run has finished!', extra={'usage': run['usage']})
            response_data = Message.get_messages_from_thread(tid, after=message['id'])
            response = chad.read_responses(response_data)
            logger.info(response)
            # send_text(response, chat_room)
        else:
            logger.debug('OpenAI Run has failed!')


if __name__ == "__main__":
    main()
