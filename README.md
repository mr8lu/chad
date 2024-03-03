# Chad
A GPT-4 chatbot for iMessage.

## Description
Provide ChatGPT-like experience within iMessage. 
By implementing the OpenAI Assistance API integration with iMessage the 
objective is provide each contact their own threads with OpenAI Assistance API.

Some of the challenges I faced while developing this is in fact the interaction 
with iMessage. 


## Installation
Python: `>=3.10`

OpenAI: `>=1.12.0`


## Usage

Create `config.ini`:
```ini
[settings]
debug_mode = True
log_file = chad.log
chat_db = chat.db
chat_room = [Your iMessage Chat Name]
quiet_mode = True
welcome_mode = False
welcome_message = 

API_KEY = [Your-API-Key-here]
```
