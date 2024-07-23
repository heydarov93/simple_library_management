""" This module contains a FileStorage class that represents a file storage for books.

The class provides methods for reading and writing books to a file.
"""
import json

from typing import Any
from .book import Book


class FileStorage:
    """ This class represents a file storage for books

    description:
        With the help of this class we can read all books from the file,
        update books, add new books and delete books. Finally we can save
        all books to the file.

    Attributes:
        file_name: The name of the file where books are stored
    """
    filename: str = "books.json"
    books: list[Book] = []

    def __init__(self):
        """ Initializes a file storage object

        description:
            Triggers the reload method to read all books from the file
            when app starts.
        """

        self.reload()

    def reload(self) -> None:
        """ Reads all books from the file and stores them in the books list """

        data: dict[str, Any] = {}
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                data = json.load(file)

            Book.id = data["lastId"]

            for book_dict in data["books"]:
                # initialize a book object from the dictionary
                book: Book = Book(**book_dict)
                self.books.append(book)
        except FileNotFoundError:
            print(f"File ({self.filename}) not found")

    def save(self) -> None:
        """ Saves books into a file """

        data: dict[str, list[dict] | int] = {
            "books": [book.to_dict() for book in self.books],
            "lastId": Book.id
        }
        try:
            with open(self.filename, "w+", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        except:
            pass

    def add_book(self, title: str, author: str, year: int) -> None:
        """ Adds a new book into the books list """

        book: Book = Book(title, author, year)
        self.books.append(book)

    def delete_book(self, id: int) -> None:
        """ Finds the book whose ID matches the id argument.
        Deletes it from the books list """

        try:
            isInList: bool = False
            for book in self.books:
                if book.id == id:
                    self.books.remove(book)
                    del book
                    isInList = True
                    break

            if not isInList:
                raise ValueError("Book not found")
        except ValueError as e:
            print(e)

    def search_book(self, **kwargs) -> list[Book]:
        """ Searches books by title, author and year. """
        year = kwargs.get("year")

        try:
            if year:
                if year.isdigit():
                    kwargs["year"] = int(year)
                else:
                    raise TypeError("Year must be an integer")

            books: list[Book] = self.books[:]

            for key, value in kwargs.items():
                def filter_books(x): return x.__dict__[key] == value
                books = list(filter(filter_books, books))
        except ValueError as e:
            print(e)

        return books

    def change_status(self, id: int, status: str) -> None:
        """ Finds the book whose ID matches the id argument.
        Changes the status of the book by calling the change_status method of
        the book object. """

        try:
            isInList: bool = False
            for book in self.books:
                if book.id == id:
                    book.change_status(status)
                    isInList = True
                    break

            if not isInList:
                raise ValueError("Book not found")
        except ValueError as e:
            print(e)
