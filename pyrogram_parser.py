from pyrogram import Client, filters
import json
from pydantic import BaseModel
from datetime import datetime
import httpx
import os
import asyncio

# File for saving data
filename = "parser.json"
# specify the name of the session file for userbot
app = Client("my_account")
# The url of the server
url = "http://127.0.0.1:5000/api/messages"


class Chat(BaseModel):
    id: int
    type: str
    title: str
    username: str


class StructureMessage(BaseModel):
    id: int
    sender_chat: Chat
    date: datetime
    chat: Chat
    text: str = None
    caption: str = None

    def serializableDict(self):
        """Converts an object into a dictionary with date conversion to an ISO format string"""
        new_dict = self.dict()
        new_dict["date"] = new_dict["date"].isoformat()
        return new_dict


async def saveJson(message_save):
    """Saves the message to a JSON file"""
    async with asyncio.Lock():
        if not os.path.exists(filename):
            with open(filename, "w", encoding="utf-8") as file:
                file.write("[]")
        # Opening a file and writing data
        with open(filename, "r+", encoding="utf-8") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = []
            data.append(message_save.serializableDict())
            file.seek(0)
            json.dump(data, file, ensure_ascii=False, indent=4)


async def resend_all_message():
    """Resending messages to the server"""
    async with asyncio.Lock():
        if not os.path.exists(filename):
            return
        with open(filename, "r+", encoding="utf-8") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = []
            if not data:
                return
            async with httpx.AsyncClient() as client:
                for history_message in data:
                    response = await client.post(url, json=history_message)
                    print(
                        f"Status code: {response.status_code}, message id: {history_message['id']}"
                    )
                    if response.status_code != 200:
                        return
            file.seek(0)
            json.dump([], file, ensure_ascii=False, indent=4)
            file.truncate()


async def send_to_server(message_save):
    """Send message to the server"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=message_save.serializableDict())
            print(f"Status code: {response.status_code}, message id: {message_save.id}")
            if response.status_code == 200:
                await resend_all_message()
            else:
                await saveJson(message_save)
        except httpx.RequestError:
            await saveJson(message_save)


# Handler for new messages in the specified chats
@app.on_message(
    filters.chat(["@sportinIU", "@opportunitiesforyou", "@test_kanal_capstone"])
)
async def new_message_handler(client, message):
    """Processes new messages and saves them if there is a text or signature"""
    if message.text or message.caption:
        message = str(message)
        message_save = StructureMessage.model_validate_json(message)
        await send_to_server(message_save)
        # saveJson(message)


if __name__ == "__main__":
    app.run()
