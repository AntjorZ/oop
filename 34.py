import os
import pickle
from abc import ABC, abstractmethod

#МОДЕЛИ

class Book:
    def __init__(self, title, author, is_available=True):
        self.__title = title
        self.__author = author
        self.__is_available = is_available  # Инкапсуляция

    # Геттеры
    def get_title(self):
        return self.__title

    def get_author(self):
        return self.__author

    def is_available(self):
        return self.__is_available

    # Сеттер
    def set_available(self, status):
        self.__is_available = status

    # Сохранение в файл
    def to_file_string(self):
        return f"{self.__title};{self.__author};{self.__is_available}"

    @staticmethod
    def from_file_string(line):
        title, author, status = line.strip().split(";")
        return Book(title, author, status == "True")

    def __str__(self):
        status = "Доступна" if self.__is_available else "Выдана"
        return f"{self.__title} - {self.__author} ({status})"


#АБСТРАКЦИЯ 
class Person(ABC):
    def __init__(self, name):
        self._name = name  # protected

    def get_name(self):
        return self._name

    @abstractmethod
    def get_role(self):
        pass


#ПОЛЬЗОВАТЕЛЬ
class User(Person):
    def __init__(self, name):
        super().__init__(name)
        self.__borrowed_books = []  # Инкапсуляция

    def get_role(self):
        return "Пользователь"

    def get_borrowed_books(self):
        return self.__borrowed_books

    def borrow_book(self, title):
        self.__borrowed_books.append(title)

    def return_book(self, title):
        if title in self.__borrowed_books:
            self.__borrowed_books.remove(title)

    def to_file_string(self):
        books_str = ",".join(self.__borrowed_books)
        return f"{self._name};{books_str}"

    @staticmethod
    def from_file_string(line):
        parts = line.strip().split(";")
        user = User(parts[0])
        if len(parts) > 1 and parts[1]:
            user._User__borrowed_books = parts[1].split(",")
        return user





#БИБЛИОТЕКА
class Library:
    def __init__(self):
        self.__books = []
        self.__users = []
        self.load_data()

 #PICKLE
    def load_data(self):
        if os.path.exists("library.pkl"):
            with open("library.pkl", "rb") as f:
                data = pickle.load(f)
                self.__books = data["books"]
                self.__users = data["users"]
                print("Данные загружены из файла.")
        else:
            print("Файл данных не найден. Создана новая библиотека.")

    def save_data(self):
        with open("library.pkl", "wb") as f:
            data = {
                "books": self.__books,
                "users": self.__users
            }
            pickle.dump(data, f)
            print("Данные сохранены в файл.")

    


    # ФУНКЦИИ БИБЛИОТЕКАРЯ
    def add_book(self, title, author):
        self.__books.append(Book(title, author))
        print("Книга добавлена.")

    def remove_book(self, title):
     for book in self.__books:
        if book.get_title() == title:
            if not book.is_available():  # проверка статуса
                print("Невозможно удалить книгу — она уже выдана!")
                return
            self.__books.remove(book)
            print("Книга удалена.")
            return
    print("Книга не найдена.")

    def register_user(self, name):
        self.__users.append(User(name))
        print("Пользователь зарегистрирован.")

    def show_all_users(self):
        for user in self.__users:
            print(user.get_name())

    def show_all_books(self):
        for book in self.__books:
            print(book)

#ФУНКЦИИ ПОЛЬЗОВАТЕЛЯ
    def show_available_books(self):
        for book in self.__books:
            if book.is_available():
                print(book)

    def borrow_book(self, user_name, title):
        user = self.find_user(user_name)
        book = self.find_book(title)

        if not user:
            print("Пользователь не найден.")
            return

        if not book:
            print("Книга не найдена.")
            return

        if not book.is_available():
            print("Книга уже выдана.")
            return

        book.set_available(False)
        user.borrow_book(title)
        print("Книга успешно выдана.")

    def return_book(self, user_name, title):
        user = self.find_user(user_name)
        book = self.find_book(title)

        if user and book:
            book.set_available(True)
            user.return_book(title)
            print("Книга возвращена.")

    def show_user_books(self, user_name):
        user = self.find_user(user_name)
        if user:
            for book in user.get_borrowed_books():
                print(book)


#ВСПОМОГАТЕЛЬНЫЕ
    def find_user(self, name):
        for user in self.__users:
            if user.get_name() == name:
                return user
        return None

    def find_book(self, title):
        for book in self.__books:
            if book.get_title() == title:
                return book
        return None

#МЕНЮ
def main():
    library = Library()

    print("Выберите роль:")
    print("1 - Библиотекарь")
    print("2 - Пользователь")

    choice = input("Введите номер: ")

    if choice == "1":
        while True:
            print("\n1 Добавить книгу")
            print("2 Удалить книгу")
            print("3 Зарегистрировать пользователя")
            print("4 Список пользователей")
            print("5 Список книг")
            print("0 Выход")

            cmd = input("Выберите действие: ")

            if cmd == "1":
                title = input("Название: ")
                author = input("Автор: ")
                library.add_book(title, author)

            elif cmd == "2":
                title = input("Название книги: ")
                library.remove_book(title)

            elif cmd == "3":
                name = input("Имя пользователя: ")
                library.register_user(name)

            elif cmd == "4":
                library.show_all_users()

            elif cmd == "5":
                library.show_all_books()

            elif cmd == "0":
                break

    elif choice == "2":
        name = input("Введите ваше имя: ")

        while True:
            print("\n1 Доступные книги")
            print("2 Взять книгу")
            print("3 Вернуть книгу")
            print("4 Мои книги")
            print("0 Выход")

            cmd = input("Выберите действие: ")

            if cmd == "1":
                library.show_available_books()

            elif cmd == "2":
                title = input("Название книги: ")
                library.borrow_book(name, title)

            elif cmd == "3":
                title = input("Название книги: ")
                library.return_book(name, title)

            elif cmd == "4":
                library.show_user_books(name)

            elif cmd == "0":
                break

    library.save_data()
    print("Данные сохранены")


if __name__ == "__main__":
    main()
