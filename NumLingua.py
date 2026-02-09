import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import json
from typing import Dict, List, Optional
from enum import Enum


# ============ ЯДРО КОНВЕРТЕРА (остаётся тем же) ============

class NumberConverter:
    """Базовый класс для конвертации чисел"""
    
    def __init__(self):
        self.ones: Dict[int, str] = {}
        self.teens: Dict[int, str] = {}
        self.tens: Dict[int, str] = {}
        self.hundreds: Dict[int, str] = {}
        self.thousands: List[str] = []
        self.zero = "ноль"
        self.negative = "минус"
        
    def convert(self, num: int) -> str:
        """Основной метод конвертации"""
        if num == 0:
            return self.zero
            
        if num < 0:
            return f"{self.negative} {self.convert(-num)}"
            
        result = []
        
        # Обработка тысяч
        if num >= 1000:
            thousands_part = num // 1000
            if thousands_part > 0:
                if thousands_part == 1:
                    result.append("одна тысяча")
                elif thousands_part == 2:
                    result.append("две тысячи")
                elif 3 <= thousands_part <= 4:
                    result.append(self._convert_hundreds(thousands_part) + " тысячи")
                elif 5 <= thousands_part <= 20:
                    result.append(self._convert_hundreds(thousands_part) + " тысяч")
                else:
                    last_digit = thousands_part % 10
                    if last_digit == 1:
                        result.append(self._convert_hundreds(thousands_part) + " тысяча")
                    elif 2 <= last_digit <= 4:
                        result.append(self._convert_hundreds(thousands_part) + " тысячи")
                    else:
                        result.append(self._convert_hundreds(thousands_part) + " тысяч")
                num %= 1000
        
        # Обработка сотен, десятков и единиц
        if num > 0:
            result.append(self._convert_hundreds(num))
            
        return " ".join(result)
    
    def _convert_hundreds(self, num: int) -> str:
        """Конвертирует числа 1-999"""
        result = []
        
        # Сотни
        hundreds = (num // 100) * 100
        if hundreds in self.hundreds:
            result.append(self.hundreds[hundreds])
        
        # Десятки и единицы
        tens_ones = num % 100
        if tens_ones:
            if tens_ones < 20:
                if tens_ones < 10:
                    result.append(self.ones[tens_ones])
                else:
                    result.append(self.teens[tens_ones])
            else:
                tens = (tens_ones // 10) * 10
                ones = tens_ones % 10
                result.append(self.tens[tens])
                if ones:
                    result.append(self.ones[ones])
        
        return " ".join(result)


class RussianConverter(NumberConverter):
    """Конвертер для русского языка"""
    
    def __init__(self):
        super().__init__()
        
        self.ones = {
            0: '', 1: 'один', 2: 'два', 3: 'три', 4: 'четыре',
            5: 'пять', 6: 'шесть', 7: 'семь', 8: 'восемь', 9: 'девять'
        }
        
        self.teens = {
            10: 'десять', 11: 'одиннадцать', 12: 'двенадцать',
            13: 'тринадцать', 14: 'четырнадцать', 15: 'пятнадцать',
            16: 'шестнадцать', 17: 'семнадцать', 18: 'восемнадцать',
            19: 'девятнадцать'
        }
        
        self.tens = {
            20: 'двадцать', 30: 'тридцать', 40: 'сорок',
            50: 'пятьдесят', 60: 'шестьдесят', 70: 'семьдесят',
            80: 'восемьдесят', 90: 'девяносто'
        }
        
        self.hundreds = {
            100: 'сто', 200: 'двести', 300: 'триста',
            400: 'четыреста', 500: 'пятьсот', 600: 'шестьсот',
            700: 'семьсот', 800: 'восемьсот', 900: 'девятьсот'
        }
        
        self.zero = "ноль"
        self.negative = "минус"


class EnglishConverter(NumberConverter):
    """Конвертер для английского языка"""
    
    def __init__(self):
        super().__init__()
        
        self.ones = {
            0: '', 1: 'one', 2: 'two', 3: 'three', 4: 'four',
            5: 'five', 6: 'six', 7: 'seven', 8: 'eight', 9: 'nine'
        }
        
        self.teens = {
            10: 'ten', 11: 'eleven', 12: 'twelve',
            13: 'thirteen', 14: 'fourteen', 15: 'fifteen',
            16: 'sixteen', 17: 'seventeen', 18: 'eighteen',
            19: 'nineteen'
        }
        
        self.tens = {
            20: 'twenty', 30: 'thirty', 40: 'forty',
            50: 'fifty', 60: 'sixty', 70: 'seventy',
            80: 'eighty', 90: 'ninety'
        }
        
        self.hundreds = {
            100: 'one hundred', 200: 'two hundred', 300: 'three hundred',
            400: 'four hundred', 500: 'five hundred', 600: 'six hundred',
            700: 'seven hundred', 800: 'eight hundred', 900: 'nine hundred'
        }
        
        self.thousands = ["thousand", "million", "billion"]
        self.zero = "zero"
        self.negative = "minus"
    
    def convert(self, num: int) -> str:
        """Английский вариант с поддержкой миллионов"""
        if num == 0:
            return self.zero
            
        if num < 0:
            return f"{self.negative} {self.convert(-num)}"
            
        # Обработка больших чисел
        if num >= 1000000:
            millions = num // 1000000
            remainder = num % 1000000
            
            result = []
            if millions == 1:
                result.append("one million")
            else:
                result.append(self._convert_english_part(millions) + " million")
                
            if remainder > 0:
                if remainder < 100:
                    result.append("and")
                result.append(self._convert_english_part(remainder))
                
            return " ".join(result)
        
        return self._convert_english_part(num)
    
    def _convert_english_part(self, num: int) -> str:
        """Конвертирует числа 1-999999"""
        if num == 0:
            return ""
            
        if num < 1000:
            return super()._convert_hundreds(num)
        
        # Тысячи
        thousands = num // 1000
        remainder = num % 1000
        
        result = []
        if thousands == 1:
            result.append("one thousand")
        else:
            result.append(self._convert_english_part(thousands) + " thousand")
        
        if remainder > 0:
            if remainder < 100:
                result.append("and")
            result.append(self._convert_english_part(remainder))
        
        return " ".join(result)


class EsperantoConverter:
    """Конвертер для языка эсперанто"""
    
    def __init__(self):
        self.unuoj = ['', 'unu', 'du', 'tri', 'kvar', 'kvin', 'ses', 'sep', 'ok', 'naŭ']
        self.dekoj = ['', 'dek', 'dudek', 'tridek', 'kvardek', 'kvindek', 
                     'sesdek', 'sepdek', 'okdek', 'naŭdek']
        self.centoj = ['', 'cent', 'ducent', 'tricent', 'kvarcent', 'kvincent',
                      'sescent', 'sepcent', 'okcent', 'naŭcent']
        self.mil = ['', 'mil']
        self.nul = "nul"
        self.negativa = "negativa"
    
    def convert(self, num: int) -> str:
        if num == 0:
            return self.nul
            
        if num < 0:
            return f"{self.negativa} {self.convert(-num)}"
            
        result = []
        
        # Тысячи
        if num >= 1000:
            miloj = num // 1000
            if miloj == 1:
                result.append("mil")
            else:
                result.append(self._convert_part(miloj) + " mil")
            num %= 1000
        
        if num > 0:
            result.append(self._convert_part(num))
        
        return ' '.join(result)
    
    def _convert_part(self, num: int) -> str:
        result = []
        
        cent = num // 100
        if cent > 0:
            result.append(self.centoj[cent])
        
        dek = (num % 100) // 10
        if dek > 0:
            result.append(self.dekoj[dek])
        
        unu = num % 10
        if unu > 0:
            result.append(self.unuoj[unu])
        
        return ' '.join(result)


class LatinConverter:
    """Конвертер для латыни"""
    
    def __init__(self):
        self.modern = {
            0: 'nulla', 1: 'unus', 2: 'duo', 3: 'tres', 4: 'quattuor',
            5: 'quinque', 6: 'sex', 7: 'septem', 8: 'octo', 9: 'novem',
            10: 'decem', 11: 'undecim', 12: 'duodecim', 13: 'tredecim',
            14: 'quattuordecim', 15: 'quindecim', 16: 'sedecim',
            17: 'septendecim', 18: 'duodeviginti', 19: 'undeviginti',
            20: 'viginti', 30: 'triginta', 40: 'quadraginta',
            50: 'quinquaginta', 60: 'sexaginta', 70: 'septuaginta',
            80: 'octoginta', 90: 'nonaginta', 100: 'centum',
            200: 'ducenti', 300: 'trecenti', 400: 'quadringenti',
            500: 'quingenti', 600: 'sescenti', 700: 'septingenti',
            800: 'octingenti', 900: 'nongenti', 1000: 'mille'
        }
    
    def convert(self, num: int, style: str = 'modern') -> str:
        if style == 'roman':
            return self.to_roman(num)
        
        if num in self.modern:
            return self.modern[num]
        
        if num < 100:
            tens = (num // 10) * 10
            ones = num % 10
            if ones == 0:
                return self.modern[tens]
            return f"{self.modern[tens]} {self.modern[ones].lower()}"
        
        return f"{num} (не реализовано для латыни)"
    
    def to_roman(self, num: int) -> str:
        if not 1 <= num <= 3999:
            return "Только числа 1-3999 для римских цифр"
        
        val = [
            1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1
        ]
        syms = [
            "M", "CM", "D", "CD", "C", "XC", "L", "XL", 
            "X", "IX", "V", "IV", "I"
        ]
        
        roman = ""
        i = 0
        while num > 0:
            for _ in range(num // val[i]):
                roman += syms[i]
                num -= val[i]
            i += 1
        return roman


class NumberTranslator:
    """Основной класс для работы с конвертерами"""
    
    def __init__(self):
        self.converters = {
            'ru': RussianConverter(),
            'en': EnglishConverter(),
            'eo': EsperantoConverter(),
            'la': LatinConverter()
        }
        
        self.language_names = {
            'ru': 'Русский',
            'en': 'English',
            'eo': 'Esperanto',
            'la': 'Latin'
        }
        
        self.language_emojis = {
            'ru': '🇷🇺',
            'en': '🇺🇸', 
            'eo': '🟢',
            'la': '🏛️'
        }
    
    def translate(self, number: int, language: str = 'ru', 
                  style: str = 'modern') -> str:
        if language not in self.converters:
            available = ', '.join(self.converters.keys())
            return f"Язык '{language}' не поддерживается. Доступны: {available}"
        
        try:
            converter = self.converters[language]
            
            if language == 'la':
                return converter.convert(number, style)
            else:
                return converter.convert(number)
                
        except ValueError as e:
            return f"Ошибка: {str(e)}"
        except Exception as e:
            return f"Неожиданная ошибка: {str(e)}"


# ============ ГРАФИЧЕСКИЙ ИНТЕРФЕЙС ============

class LanguageButton(QPushButton):
    """Кнопка выбора языка"""
    
    def __init__(self, lang_code: str, name: str, emoji: str):
        super().__init__()
        self.lang_code = lang_code
        self.name = name
        self.emoji = emoji
        
        self.setCheckable(True)
        self.setFixedSize(150, 80)
        
        self.update_style(False)
        
        # Создаем макет для кнопки
        layout = QVBoxLayout()
        
        # Эмодзи
        emoji_label = QLabel(emoji)
        emoji_label.setAlignment(Qt.AlignCenter)
        emoji_label.setStyleSheet("font-size: 24px;")
        
        # Название языка
        name_label = QLabel(name)
        name_label.setAlignment(Qt.AlignCenter)
        name_label.setStyleSheet("font-weight: bold; font-size: 12px;")
        
        layout.addWidget(emoji_label)
        layout.addWidget(name_label)
        layout.setSpacing(0)
        layout.setContentsMargins(5, 5, 5, 5)
        
        self.setLayout(layout)
        
    def update_style(self, checked: bool):
        if checked:
            self.setStyleSheet("""
                QPushButton {
                    background-color: #4f46e5;
                    border: 2px solid #3730a3;
                    border-radius: 10px;
                    color: white;
                }
                QPushButton:hover {
                    background-color: #4338ca;
                }
            """)
        else:
            self.setStyleSheet("""
                QPushButton {
                    background-color: white;
                    border: 2px solid #e5e7eb;
                    border-radius: 10px;
                    color: #374151;
                }
                QPushButton:hover {
                    background-color: #f9fafb;
                    border-color: #d1d5db;
                }
            """)


class NumberDisplay(QLabel):
    """Виджет для отображения числа"""
    
    def __init__(self):
        super().__init__()
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("""
            QLabel {
                font-size: 72px;
                font-weight: bold;
                color: #1f2937;
                background-color: #f8fafc;
                border: 3px solid #e5e7eb;
                border-radius: 15px;
                padding: 20px;
                margin: 10px;
            }
        """)
        self.setText("0")
        
    def set_number(self, num: int):
        """Установить число с красивым форматированием"""
        if num >= 1000:
            formatted = f"{num:,}".replace(",", " ")
        else:
            formatted = str(num)
        self.setText(formatted)


class ResultDisplay(QTextEdit):
    """Виджет для отображения результата"""
    
    def __init__(self):
        super().__init__()
        self.setReadOnly(True)
        self.setFixedHeight(120)
        self.setStyleSheet("""
            QTextEdit {
                font-size: 18px;
                font-weight: 500;
                color: #111827;
                background-color: #f0f9ff;
                border: 2px solid #bae6fd;
                border-radius: 10px;
                padding: 15px;
                margin: 10px;
                selection-background-color: #93c5fd;
            }
        """)


class NumPadButton(QPushButton):
    """Кнопка цифровой клавиатуры"""
    
    def __init__(self, text: str):
        super().__init__(text)
        self.setFixedSize(70, 70)
        self.setStyleSheet("""
            QPushButton {
                font-size: 24px;
                font-weight: bold;
                background-color: white;
                border: 2px solid #d1d5db;
                border-radius: 35px;
                color: #374151;
            }
            QPushButton:hover {
                background-color: #f3f4f6;
                border-color: #9ca3af;
            }
            QPushButton:pressed {
                background-color: #e5e7eb;
            }
        """)


class HistoryItem(QWidget):
    """Элемент истории"""
    
    def __init__(self, number: int, language: str, result: str):
        super().__init__()
        
        layout = QHBoxLayout()
        
        # Число
        num_label = QLabel(f"{number:,}".replace(",", " "))
        num_label.setStyleSheet("font-weight: bold; font-size: 16px; color: #4f46e5;")
        num_label.setFixedWidth(100)
        
        # Язык
        lang_label = QLabel(language)
        lang_label.setStyleSheet("font-size: 14px; color: #6b7280;")
        lang_label.setFixedWidth(80)
        
        # Результат
        result_label = QLabel(result)
        result_label.setStyleSheet("font-size: 14px;")
        result_label.setWordWrap(True)
        
        layout.addWidget(num_label)
        layout.addWidget(lang_label)
        layout.addWidget(result_label)
        layout.addStretch()
        
        self.setLayout(layout)
        self.setStyleSheet("""
            QWidget {
                background-color: #f9fafb;
                border: 1px solid #e5e7eb;
                border-radius: 8px;
                padding: 10px;
                margin: 2px;
            }
            QWidget:hover {
                background-color: #f3f4f6;
            }
        """)


class MainWindow(QMainWindow):
    """Главное окно приложения"""
    
    def __init__(self):
        super().__init__()
        
        self.translator = NumberTranslator()
        self.history = []  # История переводов
        self.current_language = 'ru'
        self.current_style = 'modern'
        
        self.setup_ui()
        self.setup_menu()
        
    def setup_ui(self):
        """Настройка интерфейса"""
        self.setWindowTitle("🔤 NumLingua - Конвертер чисел в слова")
        self.setGeometry(100, 100, 900, 700)
        
        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Основной вертикальный layout
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # ===== ЗАГОЛОВОК =====
        title_label = QLabel("🔤 NumLingua")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                font-size: 36px;
                font-weight: bold;
                color: #4f46e5;
                padding: 20px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4f46e5, stop:0.5 #7c3aed, stop:1 #ec4899);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }
        """)
        main_layout.addWidget(title_label)
        
        subtitle_label = QLabel("Конвертер чисел в слова на разных языках")
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("font-size: 14px; color: #6b7280; margin-bottom: 20px;")
        main_layout.addWidget(subtitle_label)
        
        # ===== ОСНОВНАЯ ОБЛАСТЬ =====
        content_layout = QHBoxLayout()
        
        # Левая панель (ввод и настройки)
        left_panel = QFrame()
        left_panel.setFrameStyle(QFrame.StyledPanel)
        left_panel.setStyleSheet("QFrame { background-color: #ffffff; border-radius: 15px; }")
        left_layout = QVBoxLayout()
        
        # Отображение числа
        self.number_display = NumberDisplay()
        left_layout.addWidget(self.number_display)
        
        # Цифровая клавиатура
        numpad_layout = QGridLayout()
        numpad_layout.setSpacing(10)
        
        # Создаем кнопки цифровой клавиатуры
        buttons = [
            ('7', 0, 0), ('8', 0, 1), ('9', 0, 2),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2),
            ('1', 2, 0), ('2', 2, 1), ('3', 2, 2),
            ('±', 3, 0), ('0', 3, 1), ('⌫', 3, 2)
        ]
        
        self.numpad_buttons = {}
        for text, row, col in buttons:
            btn = NumPadButton(text)
            btn.clicked.connect(self.on_numpad_clicked)
            numpad_layout.addWidget(btn, row, col)
            self.numpad_buttons[text] = btn
        
        left_layout.addLayout(numpad_layout)
        
        # Кнопки управления
        control_layout = QHBoxLayout()
        
        clear_btn = QPushButton("Очистить")
        clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #ef4444;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #dc2626;
            }
        """)
        clear_btn.clicked.connect(self.clear_number)
        
        random_btn = QPushButton("🎲 Случайное")
        random_btn.setStyleSheet("""
            QPushButton {
                background-color: #8b5cf6;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #7c3aed;
            }
        """)
        random_btn.clicked.connect(self.generate_random)
        
        control_layout.addWidget(clear_btn)
        control_layout.addWidget(random_btn)
        left_layout.addLayout(control_layout)
        
        left_panel.setLayout(left_layout)
        content_layout.addWidget(left_panel, 1)
        
        # Правая панель (языки и результат)
        right_panel = QFrame()
        right_panel.setFrameStyle(QFrame.StyledPanel)
        right_panel.setStyleSheet("QFrame { background-color: #ffffff; border-radius: 15px; }")
        right_layout = QVBoxLayout()
        
        # Выбор языка
        lang_label = QLabel("🌍 Выберите язык:")
        lang_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #1f2937;")
        right_layout.addWidget(lang_label)
        
        # Кнопки языков
        self.language_buttons = {}
        lang_grid = QGridLayout()
        lang_grid.setSpacing(10)
        
        languages = [
            ('ru', 'Русский', '🇷🇺', 0, 0),
            ('en', 'English', '🇺🇸', 0, 1),
            ('eo', 'Esperanto', '🟢', 1, 0),
            ('la', 'Latin', '🏛️', 1, 1)
        ]
        
        for code, name, emoji, row, col in languages:
            btn = LanguageButton(code, name, emoji)
            btn.clicked.connect(lambda checked, c=code: self.select_language(c))
            lang_grid.addWidget(btn, row, col)
            self.language_buttons[code] = btn
        
        right_layout.addLayout(lang_grid)
        
        # Стиль для латыни
        self.style_group = QGroupBox("🎭 Стиль латыни:")
        self.style_group.setStyleSheet("QGroupBox { font-weight: bold; color: #4b5563; }")
        style_layout = QHBoxLayout()
        
        self.modern_radio = QRadioButton("Современная")
        self.modern_radio.setChecked(True)
        self.roman_radio = QRadioButton("Римские цифры")
        
        self.modern_radio.toggled.connect(self.on_style_changed)
        self.roman_radio.toggled.connect(self.on_style_changed)
        
        style_layout.addWidget(self.modern_radio)
        style_layout.addWidget(self.roman_radio)
        style_layout.addStretch()
        
        self.style_group.setLayout(style_layout)
        right_layout.addWidget(self.style_group)
        self.style_group.setVisible(False)  # Скрыто по умолчанию
        
        # Кнопка перевода
        translate_btn = QPushButton("🚀 Перевести")
        translate_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4f46e5, stop:1 #ec4899);
                color: white;
                border: none;
                border-radius: 10px;
                padding: 15px;
                font-size: 18px;
                font-weight: bold;
                margin: 10px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4338ca, stop:1 #db2777);
            }
        """)
        translate_btn.clicked.connect(self.translate_number)
        right_layout.addWidget(translate_btn)
        
        # Результат
        result_label = QLabel("📝 Результат:")
        result_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #1f2937; margin-top: 10px;")
        right_layout.addWidget(result_label)
        
        self.result_display = ResultDisplay()
        right_layout.addWidget(self.result_display)
        
        # Примеры
        examples_label = QLabel("🎯 Примеры для теста:")
        examples_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #1f2937; margin-top: 10px;")
        right_layout.addWidget(examples_label)
        
        examples_layout = QGridLayout()
        examples = [
            ('0', 0, 0), ('7', 0, 1), ('13', 0, 2),
            ('42', 1, 0), ('100', 1, 1), ('2023', 1, 2),
            ('7777', 2, 0), ('-5', 2, 1), ('1000000', 2, 2)
        ]
        
        for text, row, col in examples:
            btn = QPushButton(text)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #f3f4f6;
                    border: 1px solid #d1d5db;
                    border-radius: 6px;
                    padding: 8px;
                    color: #4b5563;
                }
                QPushButton:hover {
                    background-color: #e5e7eb;
                }
            """)
            btn.clicked.connect(lambda checked, t=text: self.set_example_number(t))
            examples_layout.addWidget(btn, row, col)
        
        right_layout.addLayout(examples_layout)
        
        right_panel.setLayout(right_layout)
        content_layout.addWidget(right_panel, 1)
        
        main_layout.addLayout(content_layout)
        
        # ===== ИСТОРИЯ =====
        history_label = QLabel("📜 История переводов:")
        history_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #1f2937; margin-top: 20px;")
        main_layout.addWidget(history_label)
        
        # Прокручиваемая область истории
        self.history_scroll = QScrollArea()
        self.history_scroll.setWidgetResizable(True)
        self.history_scroll.setFixedHeight(150)
        self.history_scroll.setStyleSheet("""
            QScrollArea {
                border: 2px solid #e5e7eb;
                border-radius: 10px;
                background-color: white;
            }
            QScrollArea > QWidget > QWidget {
                background-color: white;
            }
        """)
        
        self.history_widget = QWidget()
        self.history_layout = QVBoxLayout()
        self.history_widget.setLayout(self.history_layout)
        
        self.history_scroll.setWidget(self.history_widget)
        main_layout.addWidget(self.history_scroll)
        
        # Статусная строка
        self.status_label = QLabel("Готов к работе")
        self.status_label.setStyleSheet("color: #6b7280; font-size: 12px; padding: 5px;")
        main_layout.addWidget(self.status_label)
        
        # Устанавливаем русский язык по умолчанию
        self.select_language('ru')
        
    def setup_menu(self):
        """Настройка меню"""
        menubar = self.menuBar()
        
        # Меню Файл
        file_menu = menubar.addMenu("Файл")
        
        export_action = QAction("📤 Экспорт истории...", self)
        export_action.triggered.connect(self.export_history)
        file_menu.addAction(export_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Выход", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Меню Настройки
        settings_menu = menubar.addMenu("Настройки")
        
        theme_action = QAction("🎨 Сменить тему", self)
        theme_action.triggered.connect(self.toggle_theme)
        settings_menu.addAction(theme_action)
        
        # Меню Помощь
        help_menu = menubar.addMenu("Помощь")
        
        about_action = QAction("О программе", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
    # ===== ОБРАБОТЧИКИ СОБЫТИЙ =====
    
    def on_numpad_clicked(self):
        """Обработка нажатия кнопки цифровой клавиатуры"""
        sender = self.sender()
        text = sender.text()
        current_text = self.number_display.text().replace(" ", "")
        
        if text == '⌫':  # Backspace
            if len(current_text) > 1 and current_text != '0':
                new_text = current_text[:-1]
            else:
                new_text = '0'
        elif text == '±':  # Смена знака
            if current_text != '0':
                if current_text[0] == '-':
                    new_text = current_text[1:]
                else:
                    new_text = '-' + current_text
            else:
                new_text = '0'
        else:  # Цифра
            if current_text == '0' or current_text == '-0':
                new_text = text
                if current_text == '-0':
                    new_text = '-' + text
            else:
                new_text = current_text + text
        
        # Ограничиваем длину числа
        if len(new_text.replace('-', '')) <= 12:
            self.update_display(new_text)
    
    def select_language(self, lang_code: str):
        """Выбор языка"""
        self.current_language = lang_code
        
        # Обновляем кнопки
        for code, btn in self.language_buttons.items():
            btn.setChecked(code == lang_code)
            btn.update_style(code == lang_code)
        
        # Показываем/скрываем выбор стиля для латыни
        self.style_group.setVisible(lang_code == 'la')
        
        # Автоматически переводим текущее число
        self.translate_number()
    
    def on_style_changed(self):
        """Изменение стиля латыни"""
        if self.modern_radio.isChecked():
            self.current_style = 'modern'
        else:
            self.current_style = 'roman'
        
        # Автоматически переводим если выбран латинский
        if self.current_language == 'la':
            self.translate_number()
    
    def translate_number(self):
        """Перевод текущего числа"""
        try:
            num_text = self.number_display.text().replace(" ", "")
            number = int(num_text)
            
            result = self.translator.translate(
                number, 
                self.current_language, 
                self.current_style
            )
            
            self.result_display.setPlainText(result)
            
            # Добавляем в историю
            self.add_to_history(number, self.current_language, result)
            
            self.status_label.setText(f"✓ Переведено: {number:,}".replace(",", " "))
            
        except ValueError:
            self.result_display.setPlainText("Ошибка: некорректное число")
            self.status_label.setText("✗ Ошибка: некорректное число")
        except Exception as e:
            self.result_display.setPlainText(f"Ошибка: {str(e)}")
            self.status_label.setText(f"✗ Ошибка: {str(e)}")
    
    def set_example_number(self, number_str: str):
        """Установить примерное число"""
        self.update_display(number_str)
        self.translate_number()
    
    def clear_number(self):
        """Очистить число"""
        self.update_display("0")
        self.result_display.clear()
        self.status_label.setText("Число очищено")
    
    def generate_random(self):
        """Сгенерировать случайное число"""
        import random
        
        # Выбираем диапазон в зависимости от вероятности
        rand = random.random()
        
        if rand < 0.3:  # 30% - маленькие числа
            number = random.randint(-999, 999)
        elif rand < 0.6:  # 30% - средние числа
            number = random.randint(-9999, 9999)
        elif rand < 0.8:  # 20% - большие числа
            number = random.randint(-999999, 999999)
        else:  # 20% - очень большие числа
            number = random.randint(-999999999, 999999999)
        
        self.update_display(str(number))
        self.translate_number()
        self.status_label.setText(f"🎲 Сгенерировано случайное число")
    
    def update_display(self, number_str: str):
        """Обновить отображение числа"""
        try:
            number = int(number_str)
            
            # Форматируем с пробелами для тысяч
            if abs(number) >= 1000:
                formatted = f"{number:,}".replace(",", " ")
            else:
                formatted = str(number)
            
            self.number_display.setText(formatted)
            
        except ValueError:
            self.number_display.setText("0")
    
    def add_to_history(self, number: int, language: str, result: str):
        """Добавить перевод в историю"""
        # Ограничиваем историю 10 элементами
        if len(self.history) >= 10:
            self.history.pop(0)
            # Удаляем старый виджет
            old_widget = self.history_layout.takeAt(0).widget()
            old_widget.deleteLater()
        
        # Добавляем в список
        lang_name = self.translator.language_names.get(language, language)
        self.history.append((number, lang_name, result))
        
        # Создаем виджет для истории
        item = HistoryItem(number, lang_name, result)
        self.history_layout.addWidget(item)
    
    def export_history(self):
        """Экспорт истории в файл"""
        if not self.history:
            QMessageBox.information(self, "Экспорт", "История пуста!")
            return
        
        filename, _ = QFileDialog.getSaveFileName(
            self, "Экспорт истории", "", "Text Files (*.txt);;JSON Files (*.json)"
        )
        
        if filename:
            try:
                if filename.endswith('.json'):
                    data = [
                        {
                            'number': num,
                            'language': lang,
                            'translation': trans
                        }
                        for num, lang, trans in self.history
                    ]
                    with open(filename, 'w', encoding='utf-8') as f:
                        json.dump(data, f, ensure_ascii=False, indent=2)
                else:
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write("История переводов NumLingua\n")
                        f.write("=" * 40 + "\n\n")
                        for num, lang, trans in self.history:
                            f.write(f"🔢 {num:,}\n".replace(",", " "))
                            f.write(f"🌍 {lang}\n")
                            f.write(f"📝 {trans}\n")
                            f.write("-" * 30 + "\n")
                
                QMessageBox.information(self, "Успех", f"История экспортирована в:\n{filename}")
                self.status_label.setText(f"✓ История экспортирована")
                
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось экспортировать: {str(e)}")
    
    def toggle_theme(self):
        """Переключение темы"""
        reply = QMessageBox.question(
            self, "Смена темы",
            "Переключить на темную тему?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #1f2937;
                }
                QLabel {
                    color: #f9fafb;
                }
                QFrame {
                    background-color: #374151;
                }
                QTextEdit {
                    background-color: #4b5563;
                    color: #f9fafb;
                }
                QPushButton {
                    color: #f9fafb;
                }
            """)
            self.status_label.setText("Тема: темная")
        else:
            self.setStyleSheet("")  # Сброс к стандартной теме
            self.status_label.setText("Тема: светлая")
    
    def show_about(self):
        """Показать окно 'О программе'"""
        about_text = """
        <h2>🔤 NumLingua</h2>
        <p><b>Конвертер чисел в слова на разных языках</b></p>
        
        <p>Версия 1.0.0</p>
        
        <p>Поддерживаемые языки:</p>
        <ul>
            <li>🇷🇺 Русский</li>
            <li>🇺🇸 Английский</li>
            <li>🟢 Эсперанто (международный)</li>
            <li>🏛️ Латынь (современная и римские цифры)</li>
        </ul>
        
        <p>Особенности:</p>
        <ul>
            <li>Поддержка больших чисел (до миллиардов)</li>
            <li>Отрицательные числа</li>
            <li>История переводов</li>
            <li>Цифровая клавиатура</li>
            <li>Экспорт результатов</li>
        </ul>
        
        <p>© 2024 NumLingua Project</p>
        <p>Лицензия: MIT</p>
        """
        
        QMessageBox.about(self, "О программе", about_text)


# ============ ЗАПУСК ПРИЛОЖЕНИЯ ============

def main():
    """Точка входа в приложение"""
    app = QApplication(sys.argv)
    app.setApplicationName("NumLingua")
    app.setStyle("Fusion")  # Современный стиль
    
    # Устанавливаем иконку (если есть)
    try:
        app.setWindowIcon(QIcon("icon.png"))
    except:
        pass
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()