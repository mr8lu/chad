''' runs.py - OpenAI Assistant Runs '''


from pathlib import Path
from openai import OpenAI
import configparser
import os


class Run:
    def __init__(self):
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.parent_dir = os.path.dirname(self.current_dir)
        self.config = configparser.ConfigParser()
        self.config_file = Path(f'{self.parent_dir}/config.ini')
        self.config.read(self.config_file)
        self.API_KEY = self.config.get('settings', 'API_KEY')
        self.client = OpenAI(api_key=self.API_KEY)

    def create_run(self, tid, aid, model: str = None, instructions: str = None, additional_instructions: str = None, tools=None, metadata={}):
        run = self.client.beta.threads.runs.create(
            thread_id=tid,
            assistant_id=aid,
            model=model,
            instructions=instructions,
            additional_instructions=additional_instructions,
            tools=tools,
            metadata=metadata
        )
        return run

    def create_thread_and_run(self, aid, role, msg, t_metadata={}, model: str = None, instructions: str = None, tools=None, metadata={}):
        run = self.client.beta.threads.create_and_run(
            assistant_id=aid,
            thread={
                "messages": [
                    {
                        "role": role,
                        "content": msg,
                        "metadata": t_metadata
                    }
                ]
            },
            metadata=metadata
        )
        return run

    def list_runs(self, tid: str, limit: int, order: str, after: str, before: str):
        if order not in ['asc', 'desc']:
            raise ValueError("Order must be 'asc' or 'desc'")
        runs = self.client.beta.threads.runs.list(
            tid,
            limit=limit,
            order=order
        )
        return runs

    def get_run(self, tid, rid):
        run = self.client.beta.threads.runs.retrieve(
            thread_id=tid,
            run_id=rid
        )
        return run

    '''
    I think this is still in beta and the document isn't clear to me.
    ======= Skip for now =========
    def send_tool_output_to_run(self, tid, rid, output):
        run = self.client.beta.threads.runs.submit_tool_outputs(
            thread_id=tid,
            run_id=rid,
            tool_output=output
        )
    '''
