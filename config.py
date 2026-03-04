import customtkinter as ctk

# Настройка внешнего вида
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")


# Настройки шрифтов
class FontConfig:
    TITLE = ("Arial", 24, "bold")
    HEADER = ("Arial", 16, "bold")
    SUBHEADER = ("Arial", 14)
    NORMAL = ("Arial", 12)
    NORMAL_BOLD = ("Arial", 12, "bold")
    SMALL = ("Arial", 11)
    SMALL_ITALIC = ("Arial", 10, "italic")
    MONOSPACE = ("Courier", 12)

    BUTTON_LARGE = ("Arial", 14, "bold")
    BUTTON_NORMAL = ("Arial", 12)
    BUTTON_SMALL = ("Arial", 11)

    ENTRY_NORMAL = ("Arial", 12)


# Настройки размеров
class SizeConfig:
    LOGIN_WINDOW = "400x500"
    PHONEBOOK_WINDOW = "900x650"

    # Кнопки
    BUTTON_WIDTH_LARGE = 250
    BUTTON_WIDTH_MEDIUM = 110
    BUTTON_WIDTH_SMALL = 80
    BUTTON_HEIGHT_LARGE = 40
    BUTTON_HEIGHT_NORMAL = 35
    BUTTON_HEIGHT_SMALL = 30

    ENTRY_WIDTH = 250
    ENTRY_HEIGHT = 35

    PAD_SMALL = 5
    PAD_MEDIUM = 10
    PAD_LARGE = 20
    PAD_XLARGE = 40


# Настройки цветов
class ColorConfig:
    PRIMARY = "green"
    DANGER = "#c42e2e"
    DANGER_HOVER = "#a52626"
    INFO_TEXT = "gray"

    BUTTON_DELETE = "#c42e2e"
    BUTTON_DELETE_HOVER = "#a52626"

    CONTACT_CARD = ("gray85", "gray25")
    CONTACT_CARD_HOVER = ("gray80", "gray30")
    CONTACT_CARD_SELECTED = ("gray75", "gray35")


# Настройки файлов
class FileConfig:
    CONTACTS_FILE = "contacts.json"

# Функция для центрирования окон
def center_window(window):
    """Центрирование окна на экране"""
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')