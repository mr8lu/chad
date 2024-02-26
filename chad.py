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
    welcome_msg,
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
welcome_message = config.get('settings', 'welcome_message')
welcome_mode = config.get('settings', 'welcome_mode')
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
        data = {'name': 'OFD', 'number': 'self', 'instruction': ofd_persona()}
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
        self.aid = ''
        exists = self.check_assistant_exist(name)
        print(self.aid)
        a = Assistant()
        if not exists:
            self.assistant = a.create_default_assistant()
            time.sleep(15)
        else:
            self.assistant = a.get_assistant(self.aid)
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
        else:
            self.thread_dict = {}
        logger.debug(self.thread_dict)

    def read_responses(self, messages):
        logger.debug('==== read response ====')
        logger.debug(messages)
        for msg in messages.data:
            if msg.role == 'assistant':
                response = msg.content[0]
                logger.debug(response.text)
        return response.text

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
                    self.aid = aid
                    return True
        else:
            logger.warning(f'Assistant {name} does not exist, creating...', extra={'class': 'Bot', 'function': 'check_assistant_exist'})
            return False

    def add_thread(self, sender, msg, aid):
        '''
        '''
        R = Run()
        logger.debug(f'Creating thread for {sender}')
        thread_metadata = {'number': sender}
        run = R.create_thread_and_run(aid, msg, t_metadata=thread_metadata)
        tid = run.id
        logger.debug('OpenAI Run', extra={'value': run})
        self.thread_dict[sender] = tid
        logger.debug(f'add_thread function is good! Thread ID: {tid}')
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
    last_msg = None
    init_msg = 0
    chad = Bot('ChadGPT', chat_room)
    M = Message()
    R = Run()
    while True:
        guid = query.find_guid_by_display_name(chat_db, chat_room)
        msg = query.pull_latest_text_message(chat_db, guid)
        logger.debug('======= New Loop ==========')
        logger.info(msg)
        logger.info(init_msg)

        if msg == last_msg and init_msg != 0:
            time.sleep(5)
            copy_db()
            query.wal_checkpoint(chat_db)
            logger.info('======== No new messages found ======')
        else:
            if last_msg == None and init_msg == 0:
                logger.info('======== Welcome messages ======')
                text = welcome_msg(welcome_message)
                sender = 'general'
                if welcome_mode == True:
                    wrun, tid = chad.add_thread(sender, text, chad.aid)
                    response = R.get_run_messages(wrun)
                    send_text(response, chat_room)
                    logger.info('======== SENT Welcome messages ======')
                init_msg += 1

            else:
                logger.info('======== Submitting new messages ======')
                text = msg['text']
                sender = msg['sender']
                last_msg = msg

                if sender in chad.numbers:
                    tid = chad.thread_dict[sender].id
                    m = M.create_message(tid, text)
                    logger.debug('======= MESSAGE: =========')
                    logger.debug(m)
                    instruction = chad.assistant.instructions
                    logger.debug('======= Instruction: =========')
                    prompt = instruction + chad.user_instructions[sender]
                    logger.debug(prompt)
                    run = R.create_run(tid, chad.aid, instructions=prompt)
                else:
                    run, tid = chad.add_thread(sender, text, chad.aid)

                logger.debug('======= Create Run ======')
                logger.debug(run)
                response = R.get_run_messages(run)
                logger.debug('======= Received Response ======')
                logger.debug(response)
                send_text(response, chat_room)
                logger.info('======== SENT ======')


if __name__ == "__main__":
    main()
