# Chad

A GPT-4 chatbot for iMessage.

## Description

Chad is designed to provide a ChatGPT-like experience within iMessage, integrating the OpenAI Assistance API to maintain individual threads for each contact. One of the main challenges encountered during development was interfacing directly with iMessage, which this project seeks to simplify for users.

## Features

- **OpenAI GPT-4 Integration**: Leverages the latest OpenAI models for responsive and intelligent conversations.
- **Individual Threads**: Maintains separate conversation threads for each contact.
- **Debug Mode**: For developers, a debug mode is included to troubleshoot and enhance the chatbot's integration.
- **Customizable Settings**: Through `config.ini`, users can customize their experience, including enabling a welcome message for new chats.

## Prerequisites

Before you install Chad, ensure you have the following:

- Python version `3.10` or higher.
- OpenAI library version `1.12.0` or higher.

## Installation

1. **Install Python Dependencies**:

   Ensure you have Python 3.10 or higher installed. Then, install the required Python libraries using pip:

   ```bash
   pip install openai>=1.12.0
	```   

2. Replace `[Your iMessage Chat Name]` and `[Your-API-Key-here]` with your actual iMessage chat name and OpenAI API key, respectively.


## Usage

Once installed and configured, run Chad using the following command:
```shell
python3 chad.py
```
For additional usage options and advanced configurations, refer to the config.ini settings section.

## License
License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
