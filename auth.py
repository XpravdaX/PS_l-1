import json
import os

class AuthManager:
    """Класс для управления аутентификацией пользователей"""
    
    def __init__(self, users_file="users.json"):
        self.users_file = users_file
        self.users = self.load_users()
    
    def load_users(self):
        """Загрузка пользователей из файла"""
        if os.path.exists(self.users_file):
            try:
                with open(self.users_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return self.get_default_users()
        else:
            return self.get_default_users()
    
    def get_default_users(self):
        """Возвращает список пользователей по умолчанию"""
        users = {
            "admin": "admin123",
            "user": "user123",
            "Валентина": "33333"
        }
        self.save_users(users)
        return users
    
    def save_users(self, users=None):
        """Сохранение пользователей в файл"""
        if users is None:
            users = self.users
        with open(self.users_file, 'w', encoding='utf-8') as f:
            json.dump(users, f, ensure_ascii=False, indent=2)
    
    def check_credentials(self, username, password):
        """Проверка учетных данных"""
        username = username.strip()
        return username in self.users and self.users[username] == password
    
    def add_user(self, username, password):
        """Добавление нового пользователя"""
        if username in self.users:
            return False, "Пользователь уже существует"
        
        self.users[username] = password
        self.save_users()
        return True, "Пользователь успешно добавлен"
    
    def change_password(self, username, old_password, new_password):
        """Изменение пароля пользователя"""
        if username not in self.users:
            return False, "Пользователь не найден"
        
        if self.users[username] != old_password:
            return False, "Неверный старый пароль"
        
        self.users[username] = new_password
        self.save_users()
        return True, "Пароль успешно изменен"
    
    def get_all_users(self):
        """Получение списка всех пользователей"""
        return list(self.users.keys())
    
    def get_users_info(self):
        """Получение информации о пользователях для отображения"""
        return "Тестовые пользователи:\n" + "\n".join([f"{user} / {pwd}" for user, pwd in self.users.items()])