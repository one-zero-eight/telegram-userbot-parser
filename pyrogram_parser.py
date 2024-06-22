from pyrogram import Client, filters
import json
from pydantic import BaseModel
from datetime import datetime

# File for saving data
filename = "parser.json"
# specify the name of the session file for userbot
app = Client("my_account")


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


def saveJson(message):
    """Saves the message to a JSON file"""
    message_save = StructureMessage.model_validate_json(message)

    # Opening a file and writing data
    with open(filename, "r+", encoding="utf-8") as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            data = []
        data.append(message_save.serializableDict())
        file.seek(0)
        json.dump(data, file, ensure_ascii=False, indent=4)


# Handler for new messages in the specified chats
@app.on_message(
    filters.chat(["@sportinIU", "@opportunitiesforyou", "@test_kanal_capstone"])
)
async def new_message_handler(client, message):
    """Processes new messages and saves them if there is a text or signature"""
    if message.text or message.caption:
        message = str(message)
        saveJson(message)


if __name__ == "__main__":
    app.run()
