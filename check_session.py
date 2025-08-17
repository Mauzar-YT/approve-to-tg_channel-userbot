import asyncio
import os
from pyrogram import Client

class SessionChecker:
    def __init__(self):
        self.api_id = None
        self.api_hash = None
        self.session_name = None
        
    async def get_credentials(self):
        """Получение учетных данных от пользователя"""
        print("=== Проверка сессии Pyrogram ===")
        
        # Проверяем наличие config.py
        if os.path.exists('config.py'):
            try:
                from config import API_ID, API_HASH
                self.api_id = API_ID
                self.api_hash = API_HASH
                print(f"✓ Найдены учетные данные в config.py")
            except ImportError:
                print("⚠ config.py найден, но не содержит API_ID и API_HASH")
        
        # Запрашиваем данные, если их нет
        if not self.api_id:
            self.api_id = input("Введите API_ID: ").strip()
        if not self.api_hash:
            self.api_hash = input("Введите API_HASH: ").strip()
            
        self.session_name = input("Введите название сессии Pyrogram (без расширения): ").strip()
        
    async def check_session(self):
        """Проверка существующей сессии Pyrogram"""
        print(f"\n🔍 Проверяем сессию {self.session_name}...")
        
        try:
            # Создаем клиент Pyrogram
            client = Client(name=self.session_name, api_id=int(self.api_id), api_hash=self.api_hash, system_version="4.17.30-vxCUSTOM")
            
            # Запускаем клиент
            await client.start()
            
            # Получаем информацию о пользователе
            me = await client.get_me()
            
            print("✅ Сессия авторизована!")
            print(f"👤 Имя: {me.first_name}")
            print(f"📝 Фамилия: {me.last_name or 'Не указана'}")
            print(f"🔗 Username: @{me.username or 'Не указан'}")
            print(f"🆔 ID: {me.id}")
            
            await client.stop()
            return True
                
        except Exception as e:
            error_msg = str(e)
            if "msg_id is too high" in error_msg or "time has to be synchronized" in error_msg:
                print("⚠️ Проблема с синхронизацией времени. Попробуйте:")
                print("   1. Синхронизировать время на компьютере")
                print("   2. Перезапустить скрипт")
                print("   3. Подождать несколько минут и попробовать снова")
            elif "session" in error_msg.lower() and "not found" in error_msg.lower():
                print("❌ Файл сессии не найден. Проверьте название сессии.")
            else:
                print(f"❌ Ошибка при проверке сессии: {e}")
            return False

async def main():
    checker = SessionChecker()
    
    # Получаем учетные данные
    await checker.get_credentials()
    
    # Проверяем сессию
    await checker.check_session()

if __name__ == "__main__":
    asyncio.run(main())
