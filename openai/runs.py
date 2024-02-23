''' thread.py - OpenAI Assistant Thread '''


from pathlib import Path
from openai import OpenAI
import configparser
import os


class Thread:
    def __init__(self):
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.parent_dir = os.path.dirname(self.current_dir)
        self.config = configparser.ConfigParser()
        self.config_file = Path(f'{self.parent_dir}/config.ini')
        self.config.read(self.config_file)
        self.API_KEY = self.config.get('settings', 'API_KEY')
        self.client = OpenAI(api_key=self.API_KEY)

    def create_thread(self):
        empty_thread = self.client.beta.threads.create()
        return empty_thread

    def get_thread(self, tid: str):
        thread = self.client.beta.threads.retrieve(tid)
        return thread

    def update_thread(self, tid: str, metadata):
        thread = self.client.beta.threads.update(
            tid,
            metadata=metadata
        )
        return thread

    def delete_thread(self, tid: str):
        r = self.client.beta.threads.delete(tid)
        return r
