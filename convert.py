import uuid
from telethon import TelegramClient
from telethon.sessions import StringSession
from session_converter import SessionManager
import asyncio
import os
from pyrogram import Client

API_ID = 20512430
API_HASH = '80a65f8a496198608d8e68d837c4f798'


class SessionConverter:

    @staticmethod
    async def convert_to_pyrogram(session_file_path: str, save_path: str = "."):
        try:
            # Создаем директорию, если она не существует
            os.makedirs(save_path, exist_ok=True)
            
            session = SessionManager.from_telethon_file(session_file_path)

            session.pyrogram_file(
                f"{save_path}/{str(uuid.uuid4())[:8]}_pyrogram.session",
                api_id=API_ID,
            )
        except Exception as e:
            raise e

    @staticmethod
    async def convert_to_telethon(session_file_path: str, save_path: str = "."):

        try:
            session = SessionManager.from_pyrogram_session_file(session_file_path)

            session.telethon_file(
                f"{save_path}/{str(uuid.uuid4())[:8]}_telethon.session"
            )

        except Exception as e:
            raise e



async def check_telethon_connection(session_file_path: str):

    client = TelegramClient(session_file_path, API_ID, API_HASH)
    await client.start()

    print(await client.get_me())

    await client.disconnect()


async def check_pyrogram_connection(session_file_path: str, workdir: str):
    client = Client(
        session_file_path.strip(".session"), API_ID, API_HASH, workdir=workdir
    )
    await client.start()

    print(await client.get_me())

    await client.stop()


async def main():
    session_file = "./my.session"
    
    # Проверяем существование файла сессии
    if not os.path.exists(session_file):
        print(f"Ошибка: Файл {session_file} не найден!")
        return
    
    await SessionConverter.convert_to_pyrogram(
        session_file, "./pyrogram_sessions"
    )
    print("Successfully converted from TELETHON to PYROGRAM")


if __name__ == "__main__":
    asyncio.run(main())