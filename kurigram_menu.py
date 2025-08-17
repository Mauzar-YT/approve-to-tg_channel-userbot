import asyncio
import os
from pyrogram import Client
from pyrogram.errors import FloodWait, SessionPasswordNeeded, PhoneCodeInvalid
import time

class KurigramMenu:
    def __init__(self):
        self.api_id = None
        self.api_hash = None
        self.session_name = None
        self.client = None
        
    async def get_credentials(self):
        """Получение учетных данных от пользователя"""
        print("=== Kurigram Menu ===")
        
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
        
    def show_menu(self):
        """Показать главное меню"""
        print("\n" + "="*50)
        print("🎯 KURIGRAM MENU")
        print("="*50)
        print("1. 🔍 Проверить сессию")
        print("2. 📊 Получить статистику аккаунта")
        print("3. 👥 Получить список диалогов")
        print("4. 📱 Получить информацию о чате")
        print("5. 🔄 Создать новую сессию")
        print("6. 🗑️ Удалить сессию")
        print("7. 📋 Список доступных сессий")
        print("8. ✅ Одобрить все запросы на вступление")
        print("9. 🔄 Одобрить запросы по одному")
        print("0. ❌ Выход")
        print("="*50)
        
    async def check_session(self):
        """Проверка существующей сессии Pyrogram"""
        print(f"\n🔍 Проверяем сессию {self.session_name}...")
        
        try:
            # Создаем клиент Pyrogram
            self.client = Client(
                name=self.session_name, 
                api_id=int(self.api_id), 
                api_hash=self.api_hash, 
                system_version="4.17.30-vxCUSTOM"
            )
            
            # Запускаем клиент
            await self.client.start()
            
            # Получаем информацию о пользователе
            me = await self.client.get_me()
            
            print("✅ Сессия авторизована!")
            print(f"👤 Имя: {me.first_name}")
            print(f"📝 Фамилия: {me.last_name or 'Не указана'}")
            print(f"🔗 Username: @{me.username or 'Не указан'}")
            print(f"🆔 ID: {me.id}")
            print(f"📱 Телефон: {me.phone_number or 'Не указан'}")
            print(f"✅ Подтвержден: {'Да' if me.is_verified else 'Нет'}")
            print(f"🤖 Бот: {'Да' if me.is_bot else 'Нет'}")
            
            await self.client.stop()
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
            
    async def get_account_stats(self):
        """Получить статистику аккаунта"""
        print(f"\n📊 Получаем статистику аккаунта...")
        
        try:
            self.client = Client(
                name=self.session_name, 
                api_id=int(self.api_id), 
                api_hash=self.api_hash, 
                system_version="4.17.30-vxCUSTOM"
            )
            
            await self.client.start()
            
            # Получаем информацию о пользователе
            me = await self.client.get_me()
            
            # Получаем диалоги
            dialogs = []
            async for dialog in self.client.get_dialogs():
                dialogs.append(dialog)
                
            print("✅ Статистика аккаунта:")
            print(f"👤 Пользователь: {me.first_name} {me.last_name or ''}")
            print(f"🆔 ID: {me.id}")
            print(f"📱 Телефон: {me.phone_number or 'Не указан'}")
            print(f"💬 Количество диалогов: {len(dialogs)}")
            
            # Подсчитываем типы чатов
            users = sum(1 for d in dialogs if d.chat.type.value == "private")
            groups = sum(1 for d in dialogs if d.chat.type.value == "group")
            channels = sum(1 for d in dialogs if d.chat.type.value == "channel")
            
            print(f"👥 Чаты с пользователями: {users}")
            print(f"👥 Группы: {groups}")
            print(f"📢 Каналы: {channels}")
            
            await self.client.stop()
            return True
            
        except Exception as e:
            print(f"❌ Ошибка при получении статистики: {e}")
            return False
            
    async def get_dialogs_list(self):
        """Получить список диалогов"""
        print(f"\n👥 Получаем список диалогов...")
        
        try:
            self.client = Client(
                name=self.session_name, 
                api_id=int(self.api_id), 
                api_hash=self.api_hash, 
                system_version="4.17.30-vxCUSTOM"
            )
            
            await self.client.start()
            
            print("📋 Список диалогов:")
            print("-" * 60)
            
            count = 0
            async for dialog in self.client.get_dialogs():
                count += 1
                chat = dialog.chat
                chat_type = chat.type.value
                
                if chat_type == "private":
                    name = f"{chat.first_name} {chat.last_name or ''}".strip()
                    username = f"@{chat.username}" if chat.username else "Нет username"
                    print(f"{count:2d}. 👤 {name} ({username}) - ID: {chat.id}")
                elif chat_type == "group":
                    print(f"{count:2d}. 👥 {chat.title} - ID: {chat.id}")
                elif chat_type == "channel":
                    print(f"{count:2d}. 📢 {chat.title} - ID: {chat.id}")
                elif chat_type == "bot":
                    print(f"{count:2d}. 🤖 {chat.first_name} - ID: {chat.id}")
                    
                if count >= 50:  # Ограничиваем вывод
                    print("... (показаны первые 50 диалогов)")
                    break
                    
            await self.client.stop()
            return True
            
        except Exception as e:
            print(f"❌ Ошибка при получении списка диалогов: {e}")
            return False
            
    async def get_chat_info(self):
        """Получить информацию о конкретном чате"""
        chat_id = input("\nВведите ID чата или username (например: 123456789 или @username): ").strip()
        
        if not chat_id:
            print("❌ ID чата не указан")
            return False
            
        print(f"\n📱 Получаем информацию о чате {chat_id}...")
        
        try:
            self.client = Client(
                name=self.session_name, 
                api_id=int(self.api_id), 
                api_hash=self.api_hash, 
                system_version="4.17.30-vxCUSTOM"
            )
            
            await self.client.start()
            
            # Пытаемся получить чат
            try:
                chat = await self.client.get_chat(chat_id)
            except:
                print("❌ Чат не найден или у вас нет доступа")
                await self.client.stop()
                return False
                
            print("✅ Информация о чате:")
            print(f"🆔 ID: {chat.id}")
            print(f"📝 Тип: {chat.type.value}")
            
            if chat.type.value == "private":
                print(f"👤 Имя: {chat.first_name}")
                print(f"📝 Фамилия: {chat.last_name or 'Не указана'}")
                print(f"🔗 Username: @{chat.username or 'Не указан'}")
                print(f"📱 Телефон: {chat.phone_number or 'Не указан'}")
                print(f"✅ Подтвержден: {'Да' if chat.is_verified else 'Нет'}")
                print(f"🤖 Бот: {'Да' if chat.is_bot else 'Нет'}")
            elif chat.type.value in ["group", "supergroup"]:
                print(f"👥 Название: {chat.title}")
                print(f"📝 Описание: {chat.description or 'Не указано'}")
                print(f"🔗 Username: @{chat.username or 'Не указан'}")
                print(f"👥 Участников: {chat.members_count or 'Неизвестно'}")
            elif chat.type.value == "channel":
                print(f"📢 Название: {chat.title}")
                print(f"📝 Описание: {chat.description or 'Не указано'}")
                print(f"🔗 Username: @{chat.username or 'Не указан'}")
                print(f"👥 Подписчиков: {chat.members_count or 'Неизвестно'}")
                
            await self.client.stop()
            return True
            
        except Exception as e:
            print(f"❌ Ошибка при получении информации о чате: {e}")
            return False
            
    async def create_new_session(self):
        """Создать новую сессию"""
        print("\n🔄 Создание новой сессии...")
        
        phone = input("Введите номер телефона (с кодом страны, например: +79001234567): ").strip()
        
        if not phone:
            print("❌ Номер телефона не указан")
            return False
            
        session_name = input("Введите название для новой сессии: ").strip()
        
        if not session_name:
            print("❌ Название сессии не указано")
            return False
            
        try:
            # Создаем новый клиент
            client = Client(
                name=session_name,
                api_id=int(self.api_id),
                api_hash=self.api_hash,
                system_version="4.17.30-vxCUSTOM"
            )
            
            print("📱 Отправляем код подтверждения...")
            await client.connect()
            
            # Отправляем код
            sent_code = await client.send_code(phone)
            
            # Запрашиваем код от пользователя
            code = input("Введите код подтверждения из Telegram: ").strip()
            
            try:
                # Пытаемся войти с кодом
                await client.sign_in(phone, sent_code.phone_code_hash, code)
                print("✅ Сессия успешно создана!")
                return True
                
            except SessionPasswordNeeded:
                # Если включена двухфакторная аутентификация
                password = input("Введите пароль двухфакторной аутентификации: ").strip()
                await client.check_password(password)
                print("✅ Сессия успешно создана!")
                return True
                
            except PhoneCodeInvalid:
                print("❌ Неверный код подтверждения")
                return False
                
        except Exception as e:
            print(f"❌ Ошибка при создании сессии: {e}")
            return False
        finally:
            try:
                await client.disconnect()
            except:
                pass
                
    def delete_session(self):
        """Удалить сессию"""
        session_name = input("\nВведите название сессии для удаления: ").strip()
        
        if not session_name:
            print("❌ Название сессии не указано")
            return False
            
        session_file = f"{session_name}.session"
        
        if os.path.exists(session_file):
            try:
                os.remove(session_file)
                print(f"✅ Сессия {session_name} успешно удалена")
                return True
            except Exception as e:
                print(f"❌ Ошибка при удалении сессии: {e}")
                return False
        else:
            print(f"❌ Файл сессии {session_name} не найден")
            return False
            
    def list_sessions(self):
        """Показать список доступных сессий"""
        print("\n📋 Доступные сессии:")
        print("-" * 40)
        
        sessions_found = False
        for file in os.listdir("."):
            if file.endswith(".session"):
                sessions_found = True
                session_name = file.replace(".session", "")
                file_size = os.path.getsize(file)
                print(f"📁 {session_name} ({file_size} байт)")
                
        if not sessions_found:
            print("❌ Сессии не найдены")
            
        return sessions_found

    async def approve_all_join_requests(self):
        """Одобрить все запросы на вступление в канал"""
        print(f"\n✅ Одобрение всех запросов на вступление...")
        
        try:
            # Запрашиваем ID канала у пользователя
            channel_id = input("Введите ID канала или username (например: -1001234567890 или @username): ").strip()
            if not channel_id:
                print("❌ ID канала не указан")
                return False
            
            # Создаем клиент
            self.client = Client(
                name=self.session_name, 
                api_id=int(self.api_id), 
                api_hash=self.api_hash, 
                system_version="4.17.30-vxCUSTOM"
            )
            
            await self.client.start()
            
            # Проверяем права администратора
            try:
                chat_member = await self.client.get_chat_member(channel_id, "me")
                if chat_member.status.value not in ["creator", "administrator"]:
                    print("❌ У вас нет прав администратора в этом канале")
                    await self.client.stop()
                    return False
            except Exception as e:
                print(f"❌ Ошибка при проверке прав: {e}")
                await self.client.stop()
                return False
            
            # Получаем количество запросов на вступление
            try:
                join_requests = []
                async for request in self.client.get_chat_join_requests(channel_id):
                    join_requests.append(request)
                
                request_count = len(join_requests)
                
                if request_count == 0:
                    print("✅ Запросов на вступление нет")
                    await self.client.stop()
                    return True
                    
                print(f"📋 Найдено {request_count} запросов на вступление")
                
                # Показываем информацию о запросах
                print("\n📝 Список запросов:")
                print("-" * 50)
                for i, request in enumerate(join_requests[:10], 1):  # Показываем первые 10
                    # В Pyrogram объект ChatJoiner имеет атрибут user, а не from_user
                    user = request.user
                    name = f"{user.first_name} {user.last_name or ''}".strip()
                    username = f"@{user.username}" if user.username else "Нет username"
                    print(f"{i:2d}. 👤 {name} ({username}) - ID: {user.id}")
                
                if request_count > 10:
                    print(f"... и еще {request_count - 10} запросов")
                
                # Запрашиваем подтверждение
                confirm = input(f"\nОдобрить все {request_count} запросов? (y/N): ").strip().lower()
                if confirm not in ['y', 'yes', 'да', 'д']:
                    print("❌ Операция отменена")
                    await self.client.stop()
                    return False
                
                # Одобряем все запросы
                print("🔄 Одобряем запросы...")
                result = await self.client.approve_all_chat_join_requests(channel_id)
                
                if result:
                    print(f"✅ Успешно одобрено {request_count} запросов на вступление!")
                else:
                    print("❌ Ошибка при одобрении запросов")
                
                await self.client.stop()
                return result
                
            except Exception as e:
                error_msg = str(e)
                if "CHAT_ADMIN_REQUIRED" in error_msg:
                    print("❌ Требуются права администратора для управления запросами на вступление")
                elif "CHAT_WRITE_FORBIDDEN" in error_msg:
                    print("❌ Нет прав на запись в чат")
                elif "CHAT_NOT_FOUND" in error_msg:
                    print("❌ Канал не найден")
                else:
                    print(f"❌ Ошибка при получении запросов на вступление: {e}")
                
                await self.client.stop()
                return False
                
        except Exception as e:
            print(f"❌ Ошибка при одобрении запросов: {e}")
            return False

    async def approve_join_requests_one_by_one(self):
        """Одобрить запросы на вступление по одному"""
        print(f"\n🔄 Одобрение запросов на вступление по одному...")
        
        try:
            # Запрашиваем ID канала у пользователя
            channel_id = input("Введите ID канала или username (например: -1001234567890 или @username): ").strip()
            if not channel_id:
                print("❌ ID канала не указан")
                return False
            
            # Создаем клиент
            self.client = Client(
                name=self.session_name, 
                api_id=int(self.api_id), 
                api_hash=self.api_hash, 
                system_version="4.17.30-vxCUSTOM"
            )
            
            await self.client.start()
            
            # Проверяем права администратора
            try:
                chat_member = await self.client.get_chat_member(channel_id, "me")
                if chat_member.status.value not in ["creator", "administrator"]:
                    print("❌ У вас нет прав администратора в этом канале")
                    await self.client.stop()
                    return False
            except Exception as e:
                print(f"❌ Ошибка при проверке прав: {e}")
                await self.client.stop()
                return False
            
            # Получаем запросы на вступление
            try:
                join_requests = []
                async for request in self.client.get_chat_join_requests(channel_id):
                    join_requests.append(request)
                
                request_count = len(join_requests)
                
                if request_count == 0:
                    print("✅ Запросов на вступление нет")
                    await self.client.stop()
                    return True
                    
                print(f"📋 Найдено {request_count} запросов на вступление")
                
                # Показываем информацию о запросах
                print("\n📝 Список запросов:")
                print("-" * 50)
                for i, request in enumerate(join_requests, 1):
                    user = request.user
                    name = f"{user.first_name} {user.last_name or ''}".strip()
                    username = f"@{user.username}" if user.username else "Нет username"
                    print(f"{i:2d}. 👤 {name} ({username}) - ID: {user.id}")
                
                # Запрашиваем подтверждение
                confirm = input(f"\nОдобрить все {request_count} запросов по одному? (y/N): ").strip().lower()
                if confirm not in ['y', 'yes', 'да', 'д']:
                    print("❌ Операция отменена")
                    await self.client.stop()
                    return False
                
                # Одобряем запросы по одному
                print("🔄 Начинаем одобрение запросов по одному...")
                approved_count = 0
                failed_count = 0
                
                for i, request in enumerate(join_requests, 1):
                    user = request.user
                    name = f"{user.first_name} {user.last_name or ''}".strip()
                    username = f"@{user.username}" if user.username else "Нет username"
                    
                    try:
                        # Используем метод approve_chat_join_request для каждого пользователя
                        result = await self.client.approve_chat_join_request(channel_id, user.id)
                        
                        if result:
                            print(f"✅ {i:2d}/{request_count} Одобрен: {name} ({username}) - ID: {user.id}")
                            approved_count += 1
                        else:
                            print(f"❌ {i:2d}/{request_count} Ошибка: {name} ({username}) - ID: {user.id}")
                            failed_count += 1
                            
                    except Exception as e:
                        print(f"❌ {i:2d}/{request_count} Ошибка при одобрении {name} ({username}): {e}")
                        failed_count += 1
                    
                    # Небольшая задержка между запросами
                    await asyncio.sleep(1)
                
                # Итоговая статистика
                print(f"\n📊 Итоги:")
                print(f"✅ Успешно одобрено: {approved_count}")
                print(f"❌ Ошибок: {failed_count}")
                print(f"📋 Всего запросов: {request_count}")
                
                await self.client.stop()
                return True
                
            except Exception as e:
                error_msg = str(e)
                if "CHAT_ADMIN_REQUIRED" in error_msg:
                    print("❌ Требуются права администратора для управления запросами на вступление")
                elif "CHAT_WRITE_FORBIDDEN" in error_msg:
                    print("❌ Нет прав на запись в чат")
                elif "CHAT_NOT_FOUND" in error_msg:
                    print("❌ Канал не найден")
                else:
                    print(f"❌ Ошибка при получении запросов на вступление: {e}")
                
                await self.client.stop()
                return False
                
        except Exception as e:
            print(f"❌ Ошибка при одобрении запросов: {e}")
            return False

async def main():
    menu = KurigramMenu()
    
    # Получаем учетные данные
    await menu.get_credentials()
    
    while True:
        menu.show_menu()
        
        try:
            choice = input("\nВыберите действие (0-9): ").strip()
            
            if choice == "0":
                print("👋 До свидания!")
                break
            elif choice == "1":
                await menu.check_session()
            elif choice == "2":
                await menu.get_account_stats()
            elif choice == "3":
                await menu.get_dialogs_list()
            elif choice == "4":
                await menu.get_chat_info()
            elif choice == "5":
                await menu.create_new_session()
            elif choice == "6":
                menu.delete_session()
            elif choice == "7":
                menu.list_sessions()
            elif choice == "8":
                await menu.approve_all_join_requests()
            elif choice == "9":
                await menu.approve_join_requests_one_by_one()
            else:
                print("❌ Неверный выбор. Попробуйте снова.")
                
        except KeyboardInterrupt:
            print("\n👋 До свидания!")
            break
        except Exception as e:
            print(f"❌ Произошла ошибка: {e}")
            
        input("\nНажмите Enter для продолжения...")

if __name__ == "__main__":
    asyncio.run(main()) 