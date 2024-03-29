''' assistant.py - Utilize OpenAI Assistant API '''
from pathlib import Path
from openai import OpenAI
from .constraint import common_const
import configparser
import os


class Assistant:
    def __init__(self):
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.parent_dir = os.path.dirname(self.current_dir)
        self.config = configparser.ConfigParser()
        self.config_file = Path(f'{self.parent_dir}/config.ini')
        self.config.read(self.config_file)
        self.API_KEY = self.config.get('settings', 'API_KEY')
        self.client = OpenAI(api_key=self.API_KEY)
        self.MODEL = "gpt-4-turbo-preview"

    def list_assistants(self, limit: int, order: str, after: str = None, before: str = None):
        assistants = self.client.beta.assistants.list(
            order=order,
            limit=limit,
            after=after,
            before=before,
        )
        return assistants

    def create_default_assistant(self):
        '''
        This is create the default assistant Chad using GPT4-Turbo model
        {
            "id": "asst_abc123",
            "object": "assistant",
            "created_at": 1698984975,
            "name": "Math Tutor",
            "description": null,
            "model": "gpt-4",
            "instructions": "You are a personal math tutor. When asked a question, write and run Python code to answer the question.",
            "tools": [
                {
                "type": "code_interpreter"
                }
            ],
            "file_ids": [],
            "metadata": {}
        }
        '''
        assistant = self.client.beta.assistants.create(
            name="ChadGPT",
            instructions=common_const(),
            tools=[],
            model=self.MODEL
        )
        return assistant

    def get_assistant(self, assistant_id):
        ''' get assistant '''
        assistant = self.client.beta.assistants.retrieve(assistant_id)
        return assistant

    def modify_assistant(self, assistant):
        ''' modify assistant '''
        updated_assistant = self.client.beta.assistants.update(
            assistant['id'],
            instructions=assistant['instructions'],
            name=assistant['name'],
            tools=assistant['tools'],
            model=assistant['model'],
            file_ids=assistant['file_ids'],
            metadata=assistant['metadata']
        )
        return updated_assistant

    def delete_assistant(self, a_id):
        response = self.client.beta.assistants.delete(a_id)
        return response
