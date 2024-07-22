from collections import UserDict
import re


class Field:
    """Клас довільного поля, з чого складаються записи для контактної книги"""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    """Поле імені"""

    def __init__(self, value):
        if value is '':
            raise ValueError("Name cannot be empty")
        else:
            super().__init__(value)


class Phone(Field):
    """Поле телефонного номера"""

    def __init__(self, value):
        # Верифікація номера (має складатися з 10 цифр)
        if re.match(r'\d{10}', value):
            super().__init__(value)
        else:
            raise ValueError("Incorrect phone number")


class Record:
    """Клас запису, з яких складатиметься контактна книга"""

    def __init__(self, name):
        # Обов'язкове поле ім'я та список телефонних номерів
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        """Додавання номера телефона до запису

        Параметри:
            phone (str): Номер телефону
        """

        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        """Видалення номера телефона із запису

        Параметри:
            phone (str): Номер телефону
        """

        # Змінна для збереження конкретного об'єкта зі списку для видалення (інакше - змінювати метод __eq__)
        phone_to_remove = None
        for p in self.phones:
            if p.value == phone:
                phone_to_remove = p
                break
        if phone_to_remove:
            self.phones.remove(phone_to_remove)
        else:
            raise ValueError(f"Phone number {phone} not found")

    def edit_phone(self, phone_old, phone_new):
        """Редагування номера телефона у записі

        Параметри:
            phone_old (str): Попередній номер телефону
            phone_new (str): Новий номер телефону
        """

        # Ітерація по значеннях Phone об'єктів у списку
        if phone_old in [phone.value for phone in self.phones]:
            self.remove_phone(phone_old)
            self.add_phone(phone_new)
        else:
            raise ValueError(f"Phone number {phone_old} not found")

    def find_phone(self, phone):
        """Пошук номера телефона в записі

        Параметри:
            phone (str): Номер телефону
        """

        for phone_obj in self.phones:
            if phone_obj.value == phone:
                return phone_obj
        return None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    """Клас контактної книги"""

    def add_record(self, record: Record):
        """Додавання нового запису до контактної книги

        Параметри:
            record (Record): Запис для додавання
        """

        self.data[record.name.value] = record

    def delete(self, name):
        """Видалення запису з контактної книги

        Параметри:
            name (str): ім'я контакту для видалення
        """

        if name in self.data:
            del self.data[name]
        else:
            raise ValueError(f"Contact with name {name} not found")

    def find(self, name):
        """Пошук запису з контактної книги

        Параметри:
            name (str): ім'я контакту для пошуку
        """

        return self.data.get(name, None)

    def __str__(self):
        decoration = '-'*max([len(str(record)) for record in self.data.values()])
        return decoration + '\n' + "\n".join(str(record) for record in self.data.values()) + '\n' + decoration

