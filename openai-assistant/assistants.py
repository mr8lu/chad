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

    def list_assistants(self):
        ''' List available assistants
        {
        "object": "list",
        "data": [
            {
            "id": "asst_abc123",
            "object": "assistant",
            "created_at": 1698982736,
            "name": "Coding Tutor",
            "description": null,
            "model": "gpt-4",
            "instructions": "You are a helpful assistant designed to make me better at coding!",
            "tools": [],
            "file_ids": [],
            "metadata": {}
            },
            {
            "id": "asst_abc456",
            "object": "assistant",
            "created_at": 1698982718,
            "name": "My Assistant",
            "description": null,
            "model": "gpt-4",
            "instructions": "You are a helpful assistant designed to make me better at coding!",
            "tools": [],
            "file_ids": [],
            "metadata": {}
            },
            {
            "id": "asst_abc789",
            "object": "assistant",
            "created_at": 1698982643,
            "name": null,
            "description": null,
            "model": "gpt-4",
            "instructions": null,
            "tools": [],
            "file_ids": [],
            "metadata": {}
            }
        ],
        "first_id": "asst_abc123",
        "last_id": "asst_abc789",
        "has_more": false
        }
        '''
        assistants = self.client.beta.assistants.list(
            order="desc",
            limit="10",
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
            instruction=common_const(),
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
