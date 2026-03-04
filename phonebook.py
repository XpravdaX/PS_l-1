import json
import os
import customtkinter as ctk
from config import FontConfig, SizeConfig, ColorConfig, FileConfig, center_window


class ContactManager:
    """Класс для управления контактами"""

    def __init__(self, contacts_file=FileConfig.CONTACTS_FILE):
        self.contacts_file = contacts_file
        self.contacts = self.load_contacts()

    def load_contacts(self):
        """Загрузка контактов из файла"""
        if os.path.exists(self.contacts_file):
            try:
                with open(self.contacts_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return self.get_default_contacts()
        else:
            return self.get_default_contacts()

    def get_default_contacts(self):
        """Возвращает список контактов по умолчанию"""
        return [
            {"name": "Ирина", "phone": "555-55-55"},
            {"name": "Максим", "phone": "111-11-11"}
        ]

    def save_contacts(self):
        """Сохранение контактов в файл"""
        with open(self.contacts_file, 'w', encoding='utf-8') as f:
            json.dump(self.contacts, f, ensure_ascii=False, indent=2)

    def get_all_contacts(self):
        """Получение всех контактов"""
        return sorted(self.contacts, key=lambda x: x['name'].lower())

    def add_contact(self, name, phone):
        """Добавление нового контакта"""
        name = name.strip()
        phone = phone.strip()

        if not name or not phone:
            return False, "Заполните все поля!"

        # Проверка на существующий контакт
        for contact in self.contacts:
            if contact['name'].lower() == name.lower():
                return False, "Контакт с таким именем уже существует!"

        self.contacts.append({"name": name, "phone": phone})
        self.save_contacts()
        return True, "Контакт успешно добавлен!"

    def update_contact(self, name, new_phone):
        """Обновление существующего контакта"""
        name = name.strip()
        new_phone = new_phone.strip()

        if not name or not new_phone:
            return False, "Заполните все поля!"

        for contact in self.contacts:
            if contact['name'].lower() == name.lower():
                contact['phone'] = new_phone
                self.save_contacts()
                return True, "Контакт успешно обновлен!"

        return False, "Контакт не найден"

    def delete_contact(self, name):
        """Удаление контакта"""
        name = name.strip()

        for i, contact in enumerate(self.contacts):
            if contact['name'].lower() == name.lower():
                del self.contacts[i]
                self.save_contacts()
                return True, "Контакт успешно удален!"

        return False, "Контакт не найден"

    def find_contacts(self, search_term):
        """Поиск контактов по имени или телефону"""
        search_term = search_term.strip().lower()

        if not search_term:
            return self.get_all_contacts()

        return [
            contact for contact in self.contacts
            if search_term in contact['name'].lower() or search_term in contact['phone'].lower()
        ]

    def find_by_name(self, name):
        """Поиск контакта по имени (частичное совпадение)"""
        name = name.strip().lower()

        return [
            contact for contact in self.contacts
            if name in contact['name'].lower()
        ]


class ContactCard(ctk.CTkFrame):
    """Виджет для отображения одного контакта"""

    def __init__(self, parent, contact, on_click_callback, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.contact = contact
        self.on_click_callback = on_click_callback

        self.configure(
            fg_color=("gray85", "gray25"),
            corner_radius=8,
            height=50
        )

        self.bind("<Button-1>", self.on_click)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

        self.create_content()

    def create_content(self):
        """Создание содержимого карточки"""
        # Имя контакта
        self.name_label = ctk.CTkLabel(
            self,
            text=self.contact['name'],
            font=FontConfig.NORMAL_BOLD,
            anchor="w"
        )
        self.name_label.pack(side="left", padx=15, pady=10, fill="both", expand=True)
        self.name_label.bind("<Button-1>", self.on_click)

        self.phone_label = ctk.CTkLabel(
            self,
            text=self.contact['phone'],
            font=FontConfig.NORMAL,
            anchor="e"
        )
        self.phone_label.pack(side="right", padx=15, pady=10)
        self.phone_label.bind("<Button-1>", self.on_click)

    def on_click(self, event):
        """Обработка клика по карточке"""
        self.configure(fg_color=("gray75", "gray35"))
        self.after(100, lambda: self.configure(fg_color=("gray85", "gray25")))

        # Вызов callback с данными контакта
        if self.on_click_callback:
            self.on_click_callback(self.contact)

    def on_enter(self, event):
        """Подсветка при наведении"""
        self.configure(fg_color=("gray80", "gray30"))

    def on_leave(self, event):
        """Снятие подсветки"""
        self.configure(fg_color=("gray85", "gray25"))


class PhoneBookUI:
    """Класс для создания интерфейса телефонной книги"""

    def __init__(self, parent, username, contact_manager):
        self.parent = parent
        self.username = username
        self.contact_manager = contact_manager
        self.contact_cards = []  # Список для хранения виджетов контактов
        self.create_widgets()

    def create_widgets(self):
        """Создание элементов интерфейса"""

        # Верхняя панель с информацией о пользователе
        self.top_frame = ctk.CTkFrame(self.parent)
        self.top_frame.pack(fill="x", padx=SizeConfig.PAD_MEDIUM, pady=SizeConfig.PAD_MEDIUM)

        self.user_label = ctk.CTkLabel(
            self.top_frame,
            text=f"Вы вошли как: {self.username}",
            font=FontConfig.SMALL_ITALIC
        )
        self.user_label.pack(side="left", padx=SizeConfig.PAD_MEDIUM)

        self.main_frame = ctk.CTkFrame(self.parent)
        self.main_frame.pack(pady=SizeConfig.PAD_MEDIUM, padx=SizeConfig.PAD_MEDIUM,
                             fill="both", expand=True)

        # Левая панель - редактирование контакта
        self.create_edit_panel()

        # Правая панель - список контактов
        self.create_list_panel()

    def create_edit_panel(self):
        """Создание панели редактирования"""
        self.edit_frame = ctk.CTkFrame(self.main_frame, width=300)
        self.edit_frame.pack(side="left", padx=SizeConfig.PAD_MEDIUM,
                             pady=SizeConfig.PAD_MEDIUM, fill="y")
        self.edit_frame.pack_propagate(False)  # Запрещаем изменение размера

        # Заголовок панели редактирования
        self.edit_label = ctk.CTkLabel(
            self.edit_frame,
            text="Редактирование контакта",
            font=FontConfig.HEADER
        )
        self.edit_label.pack(pady=SizeConfig.PAD_MEDIUM)

        # Поле для имени
        self.name_label = ctk.CTkLabel(
            self.edit_frame,
            text="Имя:",
            font=FontConfig.NORMAL
        )
        self.name_label.pack(pady=(SizeConfig.PAD_MEDIUM, 0))

        self.name_entry = ctk.CTkEntry(
            self.edit_frame,
            placeholder_text="Введите имя",
            width=SizeConfig.ENTRY_WIDTH,
            height=SizeConfig.ENTRY_HEIGHT,
            font=FontConfig.ENTRY_NORMAL
        )
        self.name_entry.pack(pady=SizeConfig.PAD_SMALL)

        # Поле для телефона
        self.phone_label = ctk.CTkLabel(
            self.edit_frame,
            text="Телефон:",
            font=FontConfig.NORMAL
        )
        self.phone_label.pack(pady=(SizeConfig.PAD_MEDIUM, 0))

        self.phone_entry = ctk.CTkEntry(
            self.edit_frame,
            placeholder_text="Введите телефон",
            width=SizeConfig.ENTRY_WIDTH,
            height=SizeConfig.ENTRY_HEIGHT,
            font=FontConfig.ENTRY_NORMAL
        )
        self.phone_entry.pack(pady=SizeConfig.PAD_SMALL)

        # Кнопки
        self.create_buttons()

    def create_buttons(self):
        """Создание кнопок управления"""
        self.button_frame = ctk.CTkFrame(self.edit_frame, fg_color="transparent")
        self.button_frame.pack(pady=SizeConfig.PAD_LARGE)

        # Первый ряд кнопок
        self.button_row1 = ctk.CTkFrame(self.button_frame, fg_color="transparent")
        self.button_row1.pack(pady=SizeConfig.PAD_SMALL)

        self.add_button = ctk.CTkButton(
            self.button_row1,
            text="Добавить",
            width=SizeConfig.BUTTON_WIDTH_MEDIUM,
            height=SizeConfig.BUTTON_HEIGHT_NORMAL,
            font=FontConfig.BUTTON_NORMAL
        )
        self.add_button.pack(side="left", padx=SizeConfig.PAD_SMALL)

        self.update_button = ctk.CTkButton(
            self.button_row1,
            text="Коррекция",
            width=SizeConfig.BUTTON_WIDTH_MEDIUM,
            height=SizeConfig.BUTTON_HEIGHT_NORMAL,
            font=FontConfig.BUTTON_NORMAL
        )
        self.update_button.pack(side="left", padx=SizeConfig.PAD_SMALL)

        # Второй ряд кнопок
        self.button_row2 = ctk.CTkFrame(self.button_frame, fg_color="transparent")
        self.button_row2.pack(pady=SizeConfig.PAD_SMALL)

        self.delete_button = ctk.CTkButton(
            self.button_row2,
            text="Удалить",
            width=SizeConfig.BUTTON_WIDTH_MEDIUM,
            height=SizeConfig.BUTTON_HEIGHT_NORMAL,
            font=FontConfig.BUTTON_NORMAL,
            fg_color=ColorConfig.BUTTON_DELETE,
            hover_color=ColorConfig.BUTTON_DELETE_HOVER
        )
        self.delete_button.pack(side="left", padx=SizeConfig.PAD_SMALL)

        self.find_button = ctk.CTkButton(
            self.button_row2,
            text="Найти",
            width=SizeConfig.BUTTON_WIDTH_MEDIUM,
            height=SizeConfig.BUTTON_HEIGHT_NORMAL,
            font=FontConfig.BUTTON_NORMAL
        )
        self.find_button.pack(side="left", padx=SizeConfig.PAD_SMALL)

        # Кнопка очистки
        self.clear_button = ctk.CTkButton(
            self.edit_frame,
            text="Очистить поля",
            width=SizeConfig.ENTRY_WIDTH,
            height=SizeConfig.BUTTON_HEIGHT_NORMAL,
            font=FontConfig.BUTTON_NORMAL
        )
        self.clear_button.pack(pady=SizeConfig.PAD_MEDIUM)

    def create_list_panel(self):
        """Создание панели списка контактов"""
        self.list_frame = ctk.CTkFrame(self.main_frame)
        self.list_frame.pack(side="right", padx=SizeConfig.PAD_MEDIUM,
                             pady=SizeConfig.PAD_MEDIUM, fill="both", expand=True)

        # Заголовок списка
        self.list_label = ctk.CTkLabel(
            self.list_frame,
            text="Список контактов",
            font=FontConfig.HEADER
        )
        self.list_label.pack(pady=SizeConfig.PAD_MEDIUM)

        # Поле поиска
        self.create_search_bar()

        # Контейнер для карточек контактов с прокруткой
        self.contacts_container = ctk.CTkScrollableFrame(
            self.list_frame,
            label_text="",
            corner_radius=8
        )
        self.contacts_container.pack(pady=SizeConfig.PAD_MEDIUM, padx=SizeConfig.PAD_MEDIUM,
                                     fill="both", expand=True)

        # Статистика
        self.stats_label = ctk.CTkLabel(
            self.list_frame,
            text="Всего контактов: 0",
            font=FontConfig.SMALL_ITALIC
        )
        self.stats_label.pack(pady=SizeConfig.PAD_SMALL)

    def create_search_bar(self):
        """Создание панели поиска"""
        self.search_frame = ctk.CTkFrame(self.list_frame, fg_color="transparent")
        self.search_frame.pack(pady=SizeConfig.PAD_SMALL, padx=SizeConfig.PAD_MEDIUM, fill="x")

        self.search_entry = ctk.CTkEntry(
            self.search_frame,
            placeholder_text="Поиск по имени или телефону...",
            height=SizeConfig.ENTRY_HEIGHT,
            font=FontConfig.ENTRY_NORMAL
        )
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0, SizeConfig.PAD_SMALL))

        self.search_button = ctk.CTkButton(
            self.search_frame,
            text="🔍",
            width=40,
            height=SizeConfig.BUTTON_HEIGHT_NORMAL,
            font=FontConfig.BUTTON_NORMAL
        )
        self.search_button.pack(side="right")

    def on_contact_click(self, contact):
        """Обработка клика по контакту"""
        # Заполняем поля данными выбранного контакта
        self.name_entry.delete(0, "end")
        self.name_entry.insert(0, contact['name'])
        self.phone_entry.delete(0, "end")
        self.phone_entry.insert(0, contact['phone'])

    def refresh_contacts_list(self, contacts=None):
        """Обновление списка контактов"""
        # Очищаем контейнер
        for widget in self.contacts_container.winfo_children():
            widget.destroy()

        self.contact_cards.clear()

        if contacts is None:
            contacts = self.contact_manager.get_all_contacts()

        # Создаем карточки для каждого контакта
        for contact in contacts:
            card = ContactCard(
                self.contacts_container,
                contact,
                self.on_contact_click,
                fg_color=("gray85", "gray25")
            )
            card.pack(fill="x", padx=5, pady=2)
            self.contact_cards.append(card)

        # Обновление статистики
        self.stats_label.configure(text=f"Всего контактов: {len(self.contact_manager.contacts)}")

    def clear_fields(self):
        """Очистка полей ввода"""
        self.name_entry.delete(0, "end")
        self.phone_entry.delete(0, "end")
        self.search_entry.delete(0, "end")
        self.refresh_contacts_list()
        self.name_entry.focus()