#!/usr/bin/env python
"""Module that contains interactive functionality for library management"""

from app import storage
from app.models.book import Book
import cmd
import shlex


class ManageLibrary(cmd.Cmd):
    """Class that provides CLI for library management"""
    prompt = "(Nizami) "
    intro = (
        "Welcome to Nizami library management system. Type help or "
        "? to list commands. \n"
    )

    def do_list(self, arg: str) -> None:
        "List all books: list"
        try:
            if arg:
                raise ValueError(
                    "`list` command doesn't take an argument.\nUsage: list"
                )
            else:
                print(10 * "=" + " List of All Books " + 10 * "=")
                for book in storage.books:
                    print(book)
        except ValueError as e:
            print(e)

    def do_add(self, arg: str) -> None:
        "Adds new book: add <title> <author> <year>"
        try:
            arguments: list[str] = shlex.split(arg)

            if len(arguments) != 3:
                raise ValueError(
                    "Invalid number of arguments. "
                    "Usage: add <title> <author> <year>"
                )

            title, author, year = arguments

            if not year.isdigit():
                raise ValueError("<year> must be an integer.")

            storage.add_book(title, author, int(year))
            storage.save()
        except ValueError as e:
            print(e)

    def do_delete(self, arg: str) -> None:
        "Deletes the book: delete <id_of_the_book>"
        try:
            if len(arg.split()) != 1:
                raise ValueError(
                    "Invalid number of arguments. "
                    "Usage: delete <id_of_the_book>"
                )
            id: str = arg

            if not id.isdigit():
                raise ValueError("<id_of_the_book> must be an integer.")

            storage.delete_book(int(id))
            storage.save()
        except ValueError as e:
            print(e)

    def do_update_status(self, arg: str) -> None:
        (
            "Changes the status of the book: update_status <id_of_the_book> "
            "<status>"
            "\nstatus: 'в наличии' or 'выдана'"
        )
        try:
            args: list[str] = shlex.split(arg)
            if len(args) != 2:
                raise ValueError(
                    "Invalid number of arguments. "
                    "Usage: update_status <id_of_the_book> <status>"
                )
            id, status = args

            if not id.isdigit():
                raise ValueError("<id_of_the_book> must be an integer.")

            if status not in ["в наличии", "выдана"]:
                raise ValueError(
                    "<status> must be either 'в наличии' or 'выдана'"
                )

            storage.change_status(int(id), status)
            storage.save()
        except ValueError as e:
            print(e)

    def do_search(self, arg: str) -> None:
        (
            "Searches for books: search <option> <value>\n"
            "Options\n"
            "\t-title: search by title\n"
            "\t-author: search by author\n"
            "\t-year: search by year"
        )
        options: list[str] = ["-title", "-author", "-year"]
        args: list[str] = shlex.split(arg)
        args_len: int = len(args)

        search_details = {}

        try:
            if args_len < 2:
                raise ValueError(
                    "search command requires at least one option with the "
                    "value\n"
                    "Usage: search <option> <value>"
                )

            if args_len > 6:
                raise ValueError(
                    "search command requires at most three option with the "
                    "corresponding value\n"
                    "Usage: search <option> <value> <option> <value> <option> "
                    "<value>"
                )

            for i in range(0, args_len, 2):
                if args[i] in options:
                    key = args[i][1:]  # remove `-` prefix from option
                    search_details[key] = args[i + 1]
                else:
                    raise ValueError(f"Invalid argument: {args[i]}\n"
                                     "Type `help search` to see correct usage")

            books: list[Book] = storage.search_book(**search_details)

            print(10 * "=" + " Search Results " + 10 * "=")
            print(f"{len(books)} {'books' if len(books) > 1 else 'book'} "
                  "was found\n")

            for book in books:
                print(book)
        except ValueError as e:
            print(e)
        except IndexError:
            print("Value is missing for <option>\n"
                  "Type `help search` to see correct usage")

    def do_EOF(self, arg):
        'Handle EOF (Ctrl+D on Unix, Ctrl+Z on Windows) to exit the CLI.'
        print('Bye ...')
        return True


if __name__ == "__main__":
    try:
        ManageLibrary().cmdloop()
    except KeyboardInterrupt:
        print("Bye ...")
