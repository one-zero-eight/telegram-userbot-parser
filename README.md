# Telegram Message Parser Bot

## Overview
This Python script uses a Pyrogram to analyze messages from Telegram channels and send them to a Fast API or another server. If a failure occurs during message delivery (status code is not 200), it saves the message in a JSON file and tries again after successful delivery of a new received message from the telegram channel.

## Installation
### Requirements
- Python 3.12
- Poetry

### Installation Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/one-zero-eight/telegram-userbot-parser.git
   cd telegram-userbot-parser
2. Install dependencies using Poetry:
    ```terminal
    poetry install --with code-style
3. Getting the API for the user bot:
    - go to the website https://core.telegram.org/api/obtaining_api_id and use the account to get the API. Be sure to write down the api_id and api_hash that you will receive on the site.
    - Create a Python file and use this code to get your session file to use user bot. write down your data in api_id and api_hash. Run this file and go through all the necessary steps. You can read more here https://docs.pyrogram.org/intro/quickstart
        ```python
            import asyncio
            from pyrogram import Client

            api_id = 12345
            api_hash = "0123456789abcdef0123456789abcdef"


            async def main():
                async with Client("my_account", api_id, api_hash) as app:
                    await app.send_message("me", "Greetings from **Pyrogram**!")


            asyncio.run(main())

4. Using the example .env.example, fill it in with your data. In the "url", specify the address of your server. In "PROGRAM_SESSION_STRING" - specify the name of your session file for program

5. Run the file pyrogram_parser.py
    ```python
    python pyrogram_parser.py

### Futures
 - Parses messages from specified Telegram channels.
 - Sends parsed data to a server via HTTP POST requests.
 - Retries sending messages stored in a JSON file upon server error.

### Technologies Used
 - Python 3.12
 - Pyrogram
 - FastAPI
 - httpx
 - dotenv
 - Docker, Docker Compose

### License
This project is licensed under the MIT License - see the LICENSE file for details.
