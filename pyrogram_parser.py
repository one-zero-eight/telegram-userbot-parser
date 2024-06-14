from pyrogram import Client, filters
import json


filename='parser.json'
app = Client("my_account")

def save_json(message):
    message_save = {
        "_": "Message",
        "id": message.id,
        "sender_chat": {
            "_": "Chat",
            "id": message.sender_chat.id,
            "type": str(message.chat.type), 
            "title": message.sender_chat.title,
            "username": message.sender_chat.username,
        },
        "date": message.date.isoformat(),
        "chat": {
            "_": "Chat",
            "id": message.chat.id,
            "type": str(message.chat.type),
            "title": message.chat.title,
            "username": message.chat.username
        },
        "text": message.caption if message.caption else message.text
    }
    with open(filename, 'r+', encoding='utf-8') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                 data =[]
            data.append(message_save)
            file.seek(0)
            json.dump(data, file, ensure_ascii=False, indent=4)

@app.on_message(filters.chat(["@sportinIU", "@opportunitiesforyou", "@test_kanal_capstone"]))
async def new_message_handler(client, message):
    save_json(message)
    print(message)


app.run()