"""
Этот код представляет собой программу для управления телефонной книгой.
Он позволяет пользователю выполнять различные операции с записями в телефонной книге,
такие как добавление, редактирование, удаление и поиск записей.

"""

import csv
import re

class PhoneBook:
    """
    Класс для представления телефонной книги.

    """
    def __init__(self, file_name):
        self.file_name = file_name
        self.phone_book = self.load_phone_book()

    def load_phone_book(self):
        """
        Загружает данные из файла в телефонную книгу.

        :return:Список словарей, представляющих записи в телефонной книге.
        """
        phone_book = []
        try:
            with open(self.file_name, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    phone_book.append(row)
        except FileNotFoundError:
            phone_book = []
        return phone_book

    def save_phone_book(self):
        """
        Сохраняет текущее состояние телефонной книги в файл.

        """
        with open(self.file_name, mode='w', newline='', encoding='utf-8') as file:
            fieldnames = ['Фамилия', 'Имя', 'Отчество', 'Организация', 'Рабочий телефон', 'Личный телефон']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.phone_book)

class Menu:
    """
     Класс для представления меню управления телефонной книгой.
    """

    def __init__(self, phone_book):
        self.phone_book = phone_book

    def display_menu(self):
        """
            Отображает меню операций на экране.
        """
        print("\nВыберите действие:")
        print("1. Вывести записи из справочника")
        print("2. Добавить новую запись")
        print("3. Редактировать запись")
        print("4. Поиск записей")
        print("5. Удалить запись")
        print("6. Выйти")

    def delete_record(self):
        """
        Удаляет запись из телефонной книги на основе фамилии.
        """
        last_name = input("Введите фамилию записи, которую хотите удалить: ").title()
        found_records = [record for record in self.phone_book.phone_book if record['Фамилия'] == last_name]

        if not found_records:
            print("Запись не найдена.")
            return

        print("Найденные записи:")
        for i, record in enumerate(found_records):
            print(f"{i + 1}. {record}")

        while True:
            try:
                choice = int(input("Введите номер записи, которую хотите удалить: ")) - 1
                if 0 <= choice < len(found_records):
                    break
                else:
                    print("Неверный номер записи. Попробуйте снова.")
            except ValueError:
                print("Введите номер записи цифрами.")

        record = found_records[choice]
        self.phone_book.phone_book.remove(record)
        print("Запись удалена.")
        self.phone_book.save_phone_book()

    def run(self):
        """
            Запускает цикл меню для взаимодействия с пользователем.
        """
        while True:
            self.display_menu()
            choice = input("Введите номер выбранного действия: ")
            if choice == "1":
                self.display_phone_book()
            elif choice == "2":
                self.add_record()
            elif choice == "3":
                self.edit_record()
            elif choice == "4":
                self.search_records()
            elif choice == "5":
                self.delete_record()
            elif choice == "6":
                self.exit_program()
            else:
                print("Неверный выбор. Попробуйте снова.")

    def display_phone_book(self):
        """
        Отображает все записи в телефонной книге.
        """
        for record in self.phone_book.phone_book:
            print(record)

    def is_valid_name(self, name: str) -> str:
        """
        Проверяет допустимость имени.
        :param name: Имя для проверки.
        :return: True, если имя допустимо, иначе False.
        """

        return name.isalpha()

    def is_valid_phone(self, phone: str) -> bool:
        """
                Проверяет допустимость номера телефона.
                :param Номер телефона для проверки..
                :return: True, если номер телефона допустим, иначе False.
                """
        return re.match(r'^\(\d{3,5}\) \d{3}-\d{2}-\d{2}$', phone)

    def get_valid_input(self, prompt: str, validator: callable)->str:
        """
        Запрашивает допустимый ввод у пользователя
        :param prompt: Подсказка для ввода
        :param validator: функция-валидатор для проверки ввода
        :return: Допустимый ввод пользователя
        """

        while True:
            user_input = input(prompt)
            if validator(user_input):
                return user_input
            else:
                print("Неверный формат. Попробуйте снова.")

    def add_record(self):
        """
            Добавляет новую запись в телефонную книгу.
        """
        record = {}
        record['Фамилия'] = self.get_valid_input("Введите фамилию: ", self.is_valid_name)
        record['Имя'] = self.get_valid_input("Введите имя: ", self.is_valid_name)
        record['Отчество'] = self.get_valid_input("Введите отчество: ", self.is_valid_name)
        record['Организация'] = input("Введите название организации: ").title()
        record['Рабочий телефон'] = self.get_valid_input("Введите рабочий телефон в формате (ХХХ) ХХХ-ХХ-ХХ: ", self.is_valid_phone)
        record['Личный телефон'] = self.get_valid_input("Введите личный телефон в формате (ХХХ) ХХХ-ХХ-ХХ: ", self.is_valid_phone)
        self.phone_book.phone_book.append(record)
        print("Запись добавлена.")
        self.phone_book.save_phone_book()

    def edit_record(self):
        """
            Редактирует существующую запись в телефонной книге.
        """
        last_name = input("Введите фамилию записи, которую хотите редактировать: ").title()
        found_records = [record for record in self.phone_book.phone_book if record['Фамилия'] == last_name]

        if not found_records:
            print("Запись не найдена.")
            return

        print("Найденные записи:")
        for i, record in enumerate(found_records):
            print(f"{i + 1}. {record}")

        while True:
            try:
                choice = int(input("Введите номер записи, которую хотите редактировать: ")) - 1
                if 0 <= choice < len(found_records):
                    break
                else:
                    print("Неверный номер записи. Попробуйте снова.")
            except ValueError:
                print("Введите номер записи цифрами.")

        record = found_records[choice]
        print(f"Редактируемая запись: {record}")

        fields = ['Фамилия', 'Имя', 'Отчество', 'Организация', 'Рабочий телефон', 'Личный телефон']

        for field in fields:
            new_value = input(f"Введите новое значение для '{field}' (оставьте пустым для без изменений): ")
            if new_value:
                record[field] = new_value.strip()

        print("Запись отредактирована.")
        self.phone_book.save_phone_book()

    def search_records(self):
        """
            Выполняет поиск записей в телефонной книге по ключевым словам.
        """
        query = input(
            "Введите запрос для строгого поиска (Фамилия, Имя, Отчество, Организация, Рабочий телефон, Личный телефон), разделяя характеристики запятыми: ").lower()
        keywords = [keyword.strip() for keyword in query.split(",")]

        results = []

        for record in self.phone_book.phone_book:
            found = True  # Изначально считаем запись подходящей

            for keyword in keywords:
                keyword_found = False

                for key, value in record.items():
                    if keyword in value.lower():
                        keyword_found = True
                        break

                # Если характеристика не найдена, запись не подходит
                if not keyword_found:
                    found = False
                    break

            # Если все характеристики найдены, добавляем запись в результаты
            if found:
                results.append(record)

        if results:
            print("Результаты строгого поиска:")
            for i, result in enumerate(results):
                print(f"{i + 1}. {result}")
        else:
            print("Ничего не найдено.")

    def exit_program(self):
        """
            Сохраняет изменения и завершает программу.
        """
        self.phone_book.save_phone_book()
        print("Справочник сохранен. До свидания!")
        exit()

if __name__ == "__main__":
    file_name = "phone_book.csv"
    phone_book = PhoneBook(file_name)
    menu = Menu(phone_book)

    while True:
        menu.run()
