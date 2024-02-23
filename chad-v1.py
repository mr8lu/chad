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
from OpenAIAssistant.runs import Run
from OpenAIAssistant.threads import Thread
from OpenAIAssistant.messages import Message
from OpenAIAssistant.assistants import Assistant
from OpenAIAssistant.constraint import (
    spicy_latina,
    dad_joke,
    palestine,
    ofd_persona
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
        self.room_name = 'Pasteurized EGG'
        # Call each method to get user data
        self.users = [self.edd(), self.marcella(), self.mario(), self.ofd()]
        self.numbers = []
        self.instructions = {}

        for n in self.users:
            number = n['number']
            self.numbers.append(number)
            self.instructions[number] = n['instruction']

    def edd(self):
        # Assuming spicy_latina is defined elsewhere or is a literal string
        data = {'name': 'Edd Siu', 'number': '+14075294686', 'instruction': spicy_latina()}
        return data

    def marcella(self):
        # Assuming dad_joke is defined elsewhere or is a literal string
        data = {'name': 'Marcella Grillo', 'number': '+13212761077', 'instruction': dad_joke()}
        return data

    def mario(self):
        # Assuming mario is defined elsewhere or is a literal string
        data = {'name': 'Mario Massad', 'number': '+19416269361', 'instruction': palestine()}
        return data

    def ofd(self):
        # Assuming ofd is defined elsewhere or is a literal string
        data = {'name': 'OFD', 'number': '+14042101792', 'instruction': ofd_persona()}
        return data


def validate_python():
    return sys.version_info >= (3, 10)


def copy_db():
    original_chat_db = Path('~/Library/Messages/chat.db').expanduser()
    wal = Path(f'{original_chat_db}-wal')
    wal_prod = Path(f'{chat_db}-wal')
    shm = Path(f'{original_chat_db}-shm')
    shm_prod = Path(f'{chat_db}-shm')
    logger.debug(f'Copying {original_chat_db} to {chat_db}...')
    logger.debug(f'Copying {wal} to {wal_prod}...')
    logger.debug(f'Copying {shm} to {shm_prod}...')
    shutil.copyfile(wal, wal_prod)
    shutil.copyfile(original_chat_db, chat_db)
    shutil.copyfile(shm, shm_prod)


def validate_dbfile():
    if not os.path.exists(chat_db):
        copy_db()
    return True


def read_last_message():
    lm = Path(f'{current_dir}/.cache')
    try:
        with open(lm, "r") as file:
            data = json.load(file)
            return data["last_msg"]
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def write_last_message(msg):
    lm = Path(f'{current_dir}/.cache')
    with open(lm, "w") as file:
        json.dump(msg, file)


class Bot:
    def __init__(self, name, chat_room):
        # check if Bot/Assistant exists
        logger.debug(f'Initialize ChatBot: Check if assistant {name} exist for {chat_room}', extra={'class': 'Bot'})
        exists, self.aid = self.check_assistant_exist(name)
        a = Assistant()
        if not exists:
            assistant = a.create_default_assistant()
        else:
            assistant = a.get_assistant(self.aid)
        egg = PasteurizedEgg()
        self.room_name = egg.room_name
        self.users = egg.users
        self.numbers = egg.numbers
        self.user_instructions = egg.instructions
        if chat_room == self.room_name:
            '''
            thread_dict example: {'+13213211234': 'thread_id'}
            '''
            self.thread_dict = self.create_threads(self.aid, self.users)
            logger.debug(self.thread_dict)

    def read_responses(self, messages):
        response = ''
        for msg in messages.data:
            if msg.role == 'assistant':
                content = msg.content
                for m in content:
                    response += m.text.value + ' '
        return response

    def check_assistant_exist(self, name):
        logger.debug('Check assistants...', extra={'class': 'Bot', 'function': 'check_assistant_exist'})
        A = Assistant()
        try:
            assistants = A.list_assistants(order='desc', limit=10)
            logger.debug(assistants)
        except TypeError as e:
            logger.error(e)
        if assistants.data:
            for assistant in assistants.data:
                assistant_name = assistant.name
                aid = assistant.id
                logger.info('Listing assistants...', extra={'class': 'Bot', 'function': 'check_assistant_exist'})
                if assistant_name == name:
                    return True, aid
        else:
            logger.warning(f'Assistant {name} does not exist, creating...', extra={'class': 'Bot', 'function': 'check_assistant_exist'})
            return False, None

    def add_thread(self, sender, msg, aid):
        '''
        '''
        R = Run()
        logger.debug(f'Creating thread for {sender}')
        thread_metadata = {'number': sender}
        run = R.create_thread_and_run(aid, msg, t_metadata=thread_metadata)
        tid = run['thread_id']
        logger.debug('OpenAI Run', extra={'value': run})
        self.thread_dict[sender] = tid
        return run, tid

    def create_threads(self, aid, users):
        '''return
        {'+13210004444': 'thread_id'}
        '''
        logger.debug('Initialize threads for users..')
        tids = {}
        T = Thread()
        for user in users:
            number = user['number']
            tid = T.create_thread(metadata=user)
            tids[number] = tid
        logger.debug('Users', extra={'value': users})
        logger.debug('Thread IDs', extra={'value': tid})
        return tids


def main():
    if validate_python():
        logger.debug('Python3 >= 3.10', extra={'function': 'main'})
    if validate_dbfile():
        logger.debug('Python Version is good.', extra={'function': 'main'})
    query.wal_checkpoint(chat_db)
    logger.info('Chat.db checkpointing...')
    # last_msg = read_last_message()
    last_msg = {}
    chad = Bot('ChadGPT', chat_room)
    while True:
        guid = query.find_guid_by_display_name(chat_db, chat_room)
        msg = query.pull_latest_text_message(chat_db, guid)
        logger.debug(msg)
        logger.debug(last_msg)

        logger.debug(chad)
        M = Message()
        R = Run()
        if msg == last_msg:
            logger.info('======== No new messages found ======')
            time.sleep(5)
            copy_db()
            query.wal_checkpoint(chat_db)
        else:
            logger.info('======== Submitting new messages ======')
            last_msg = msg
            text = msg['text']
            sender = msg['sender']

            if sender in chad.numbers:
                tid = chad.thread_dict[sender].id
                message = M.create_message(tid, text)
                prompt = chad.user_instructions[sender]
                run = R.create_run(tid, chad.aid, instructions=prompt)
            else:
                run, tid = chad.add_thread(sender, text, chad.aid)
                message = M.get_messages_from_thread(tid)

            logger.debug('DEBUG:  RUN and RUN ID')
            logger.debug(run)
            run_id = run.id
            finish, run = R.get_run(tid, run_id)
            if finish:
                logger.debug('OpenAI Run has finished!', extra={'usage': run.usage})
                response_data = M.get_messages_from_thread(tid, after=message.id, limit='20', order='desc')
                response = chad.read_responses(response_data)
                logger.debug(response)
                # send_text(response, chat_room)
                logger.info('======== SENT ======')
            else:
                logger.debug('OpenAI Run has failed!')


if __name__ == "__main__":
    main()
