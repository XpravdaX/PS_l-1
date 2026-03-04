import customtkinter as ctk
from tkinter import messagebox
from config import FontConfig, SizeConfig, ColorConfig, center_window
from auth import AuthManager
from phonebook import ContactManager, PhoneBookUI


class LoginWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Инициализация менеджеров
        self.auth_manager = AuthManager()

        # Настройки окна
        self.title("Авторизация - Телефонная книга")
        self.geometry(SizeConfig.LOGIN_WINDOW)
        self.resizable(False, False)

        # Центрирование окна
        center_window(self)

        # Создание интерфейса
        self.create_widgets()

        # Привязка клавиши Enter к функции входа
        self.bind('<Return>', lambda event: self.check_login())

        # Фокус на поле ввода имени
        self.username_entry.focus()

    def create_widgets(self):
        """Создание элементов интерфейса"""

        # Заголовок
        self.title_label = ctk.CTkLabel(
            self,
            text="Добро пожаловать!",
            font=FontConfig.TITLE
        )
        self.title_label.pack(pady=SizeConfig.PAD_XLARGE)

        # Фрейм для формы входа
        self.login_frame = ctk.CTkFrame(self)
        self.login_frame.pack(pady=SizeConfig.PAD_LARGE, padx=SizeConfig.PAD_XLARGE,
                              fill="both", expand=True)

        # Поле для имени пользователя
        self.username_label = ctk.CTkLabel(
            self.login_frame,
            text="Имя пользователя:",
            font=FontConfig.SUBHEADER
        )
        self.username_label.pack(pady=(SizeConfig.PAD_LARGE, SizeConfig.PAD_SMALL))

        self.username_entry = ctk.CTkEntry(
            self.login_frame,
            placeholder_text="Введите имя",
            width=SizeConfig.ENTRY_WIDTH,
            height=SizeConfig.ENTRY_HEIGHT,
            font=FontConfig.ENTRY_NORMAL
        )
        self.username_entry.pack(pady=SizeConfig.PAD_SMALL)

        # Поле для пароля
        self.password_label = ctk.CTkLabel(
            self.login_frame,
            text="Пароль:",
            font=FontConfig.SUBHEADER
        )
        self.password_label.pack(pady=(SizeConfig.PAD_MEDIUM, SizeConfig.PAD_SMALL))

        self.password_entry = ctk.CTkEntry(
            self.login_frame,
            placeholder_text="Введите пароль",
            show="•",
            width=SizeConfig.ENTRY_WIDTH,
            height=SizeConfig.ENTRY_HEIGHT,
            font=FontConfig.ENTRY_NORMAL
        )
        self.password_entry.pack(pady=SizeConfig.PAD_SMALL)

        # Кнопка входа
        self.login_button = ctk.CTkButton(
            self.login_frame,
            text="Войти",
            command=self.check_login,
            width=SizeConfig.BUTTON_WIDTH_LARGE,
            height=SizeConfig.BUTTON_HEIGHT_LARGE,
            font=FontConfig.BUTTON_LARGE
        )
        self.login_button.pack(pady=SizeConfig.PAD_LARGE)

        # Информация о тестовых пользователях
        self.info_label = ctk.CTkLabel(
            self.login_frame,
            text=self.auth_manager.get_users_info(),
            font=FontConfig.SMALL,
            text_color=ColorConfig.INFO_TEXT
        )
        self.info_label.pack(pady=SizeConfig.PAD_MEDIUM)

    def check_login(self):
        """Проверка логина и пароля"""
        username = self.username_entry.get()
        password = self.password_entry.get()

        if self.auth_manager.check_credentials(username, password):
            messagebox.showinfo("Успех", f"Добро пожаловать, {username}!")
            self.open_phonebook(username)
        else:
            messagebox.showerror("Ошибка", "Неверное имя пользователя или пароль!")
            self.password_entry.delete(0, 'end')
            self.password_entry.focus()

    def open_phonebook(self, username):
        """Открытие главного окна телефонной книги"""
        self.withdraw()  # Скрываем окно авторизации
        phonebook = PhoneBookApp(self, username)
        phonebook.protocol("WM_DELETE_WINDOW", lambda: self.on_closing(phonebook))

    def on_closing(self, phonebook):
        """Обработка закрытия приложения"""
        phonebook.destroy()
        self.destroy()


class PhoneBookApp(ctk.CTkToplevel):
    def __init__(self, parent, username):
        super().__init__(parent)

        self.username = username
        self.contact_manager = ContactManager()

        # Настройки окна
        self.title(f"Телефонная книга - Пользователь: {username}")
        self.geometry(SizeConfig.PHONEBOOK_WINDOW)
        self.resizable(False, False)

        center_window(self)

        # Создание интерфейса
        self.ui = PhoneBookUI(self, username, self.contact_manager)
        self.setup_ui_handlers()

        # Загрузка контактов в список
        self.refresh_contacts_list()
        self.bind_shortcuts()

        # Обработка закрытия окна
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setup_ui_handlers(self):
        """Настройка обработчиков событий для UI"""
        ui = self.ui

        ui.add_button.configure(command=self.add_contact)
        ui.update_button.configure(command=self.update_contact)
        ui.delete_button.configure(command=self.delete_contact)
        ui.find_button.configure(command=self.find_contact)
        ui.clear_button.configure(command=self.clear_fields)
        ui.search_button.configure(command=self.search_contacts)

        self.logout_button = ctk.CTkButton(
            ui.top_frame,
            text="Выйти",
            command=self.logout,
            width=SizeConfig.BUTTON_WIDTH_SMALL,
            height=SizeConfig.BUTTON_HEIGHT_SMALL,
            font=FontConfig.BUTTON_SMALL
        )
        self.logout_button.pack(side="right", padx=SizeConfig.PAD_MEDIUM)

    def bind_shortcuts(self):
        """Привязка горячих клавиш"""
        self.bind('<Control-d>', lambda e: self.delete_contact())
        self.bind('<Control-f>', lambda e: self.find_contact())
        self.bind('<Control-n>', lambda e: self.clear_fields())
        self.bind('<Escape>', lambda e: self.on_closing())

    def refresh_contacts_list(self):
        """Обновление списка контактов"""
        self.ui.refresh_contacts_list()

    def add_contact(self):
        """Добавление нового контакта"""
        name = self.ui.name_entry.get()
        phone = self.ui.phone_entry.get()

        success, message = self.contact_manager.add_contact(name, phone)

        if success:
            self.refresh_contacts_list()
            self.ui.clear_fields()
            messagebox.showinfo("Успех", message)
        else:
            messagebox.showwarning("Предупреждение", message)

    def update_contact(self):
        """Обновление существующего контакта"""
        name = self.ui.name_entry.get()
        phone = self.ui.phone_entry.get()

        success, message = self.contact_manager.update_contact(name, phone)

        if success:
            self.refresh_contacts_list()
            self.ui.clear_fields()
            messagebox.showinfo("Успех", message)
        else:
            # Если контакт не найден, предлагаем добавить
            result = messagebox.askyesno("Контакт не найден",
                                         "Контакт с таким именем не найден. Добавить новый?")
            if result:
                self.add_contact()

    def delete_contact(self):
        """Удаление контакта"""
        name = self.ui.name_entry.get()

        if not name:
            messagebox.showwarning("Предупреждение", "Введите имя контакта для удаления!")
            return

        result = messagebox.askyesno("Подтверждение",
                                     f"Вы уверены, что хотите удалить контакт '{name}'?")

        if result:
            success, message = self.contact_manager.delete_contact(name)

            if success:
                self.refresh_contacts_list()
                self.ui.clear_fields()
                messagebox.showinfo("Успех", message)
            else:
                messagebox.showwarning("Предупреждение", message)

    def find_contact(self):
        """Поиск контакта"""
        name = self.ui.name_entry.get()

        if not name:
            messagebox.showwarning("Предупреждение", "Введите имя для поиска!")
            return

        found_contacts = self.contact_manager.find_by_name(name)

        if found_contacts:
            result_text = "Найденные контакты:\n\n"
            for contact in found_contacts:
                result_text += f"{contact['name']}: {contact['phone']}\n"

            self.ui.refresh_contacts_list(found_contacts)
            messagebox.showinfo("Результаты поиска", result_text)
        else:
            messagebox.showinfo("Поиск", "Контакты не найдены")

    def search_contacts(self):
        """Поиск контактов по введенному тексту"""
        search_text = self.ui.search_entry.get()
        filtered_contacts = self.contact_manager.find_contacts(search_text)

        self.ui.refresh_contacts_list(filtered_contacts)

        total = len(self.contact_manager.contacts)
        found = len(filtered_contacts)
        self.ui.stats_label.configure(text=f"Найдено: {found} из {total}")

    def clear_fields(self):
        """Очистка полей ввода"""
        self.ui.clear_fields()

    def logout(self):
        """Выход из аккаунта"""
        result = messagebox.askyesno("Подтверждение", "Вы уверены, что хотите выйти?")
        if result:
            self.on_closing()

    def on_closing(self):
        """Обработка закрытия окна"""
        self.master.deiconify()
        self.destroy()


if __name__ == "__main__":
    app = LoginWindow()
    app.mainloop()