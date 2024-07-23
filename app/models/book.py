"""This module contains a Book class that represents a book."""
from typing import Any


class Book:
    """This class represents a book."""
    id: int = 0

    def __init__(self, *args: Any,
                 **kwargs: dict[str, Any]) -> None:
        """ Initializes a book object 

        Args:
            *args: Arbitrary positional arguments
            **kwargs: Arbitrary keyword arguments
        """
        if kwargs:
            for key, value in kwargs.items():
                setattr(self, key, value)
        else:
            Book.id += 1
            self.id: int = Book.id
            self.status: str = "в наличии"
            self.title = args[0]
            self.author = args[1]
            self.year = args[2]

    def __str__(self) -> str:
        """ Returns a string representation of the book """
        title_str: str = f"{self.title} {10 * '_'}\n"
        id_str: str = f"id: {self.id}\n"
        author_str: str = f"author: {self.author}\n"
        year_str: str = f"year: {self.year}\n"
        status_str: str = f"status: {self.status}\n\n"
        return title_str + id_str + author_str + year_str + status_str

    def change_status(self, status: str) -> None:
        """ Changes books' status """
        if status in ["в наличии", "выдана"]:
            self.status = status
        else:
            raise ValueError("Invalid status, must be 'в наличии' or 'выдана'")

    def to_dict(self) -> dict:
        """ Returns a dictionary representation of the book """

        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "status": self.status
        }
