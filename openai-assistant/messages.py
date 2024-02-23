''' messages.py - OpenAI Thread Messages '''


from pathlib import Path
from openai import OpenAI
import configparser
import os


class Message:
    def __init__(self):
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.parent_dir = os.path.dirname(self.current_dir)
        self.config = configparser.ConfigParser()
        self.config_file = Path(f'{self.parent_dir}/config.ini')
        self.config.read(self.config_file)
        self.API_KEY = self.config.get('settings', 'API_KEY')
        self.client = OpenAI(api_key=self.API_KEY)

    def create_message(self, tid, msg, role='user'):
        m = self.client.beta.threads.messages.create(
            tid,
            role=role,
            content=msg
        )
        return m

    def get_messages_from_thread(self, tid: str, limit: int, order: str, after: str = None, before: str = None):
        m = self.client.beta.threads.messages.list(
            tid,
            limit=limit,
            order=order,
            after=after,
            before=before
        )
        return m

    def get_message(self, tid: str, mid: str):
        m = self.client.beta.threads.messages.retrieve(
            message_id=mid,
            thread_id=tid
        )
        return m
