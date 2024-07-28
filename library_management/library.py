import json
from typing import List, Union
from book import Book
from errors import DuplicateBookError, InvalidStatusError, BookNotFoundError, LibraryFileError


class Library:
    """Class representing a library_management that manages a collection of books."""

    def __init__(self) -> None:
        self.books: List[Book] = []
        self.next_id: int = 1

    def add_book(self, title: str, author: str, year: int) -> str:
        """
        Adds a new book to the library_management.

        Args:
            title (str): The title of the book.
            author (str): The author of the book.
            year (int): The year the book was published.

        Returns:
            str: A message confirming the addition of the book.

        Raises:
            DuplicateBookError: If the book already exists in the library_management.
        """
        if any(book.title == title and book.author == author and book.year == year for book in self.books):
            raise DuplicateBookError(title, author, year)
        book = Book(self.next_id, title, author, year)
        self.books.append(book)
        self.next_id += 1
        return f"Book '{title}' by {author} added with ID {book.book_id}."

    def delete_book(self, book_id: int) -> str:
        """
        Deletes a book from the library_management by its ID.

        Args:
            book_id (int): The ID of the book to delete.

        Returns:
            str: A message confirming the deletion of the book.

        Raises:
            BookNotFoundError: If the book with the specified ID is not found.
        """
        book = self._find_book_by_id(book_id)
        self.books.remove(book)
        return f"Book with ID {book_id} has been deleted."

    def edit_status(self, book_id: int, new_status: str) -> str:
        """
        Edits the status of a book by its ID.

        Args:
            book_id (int): The ID of the book.
            new_status (str): The new status of the book.

        Returns:
            str: A message confirming the status update.

        Raises:
            BookNotFoundError: If the book with the specified ID is not found.
            InvalidStatusError: If the new status is not valid.
        """
        if new_status not in ['available', 'checked out']:
            raise InvalidStatusError(new_status)
        book = self._find_book_by_id(book_id)
        book.status = new_status
        return f"Status of book with ID {book_id} has been updated to '{new_status}'."

    def find_books(self, search_term: str) -> List[Book]:
        """
        Finds books by title, author, or year.

        Args:
            search_term (str): The search term (title, author, or year).

        Returns:
            List[Book]: A list of books matching the search term.

        Raises:
            BookNotFoundError: If no books are found.
        """
        found_books = [
            book for book in self.books
            if search_term in book.title or search_term in book.author or search_term == str(book.year)
        ]
        if not found_books:
            raise BookNotFoundError(-1)  # ID -1 indicates no specific book was being searched for
        return found_books

    def list_books(self) -> Union[List[Book], str]:
        """
        Lists all books in the library_management.

        Returns:
            Union[List[Book], str]: A list of all books or a message if the library_management is empty.
        """
        if not self.books:
            return "No books in the library_management."
        return self.books

    def save_library(self, filename: str) -> str:
        """
        Saves the library_management to a JSON file.

        Args:
            filename (str): The name of the file to save the library_management to.

        Returns:
            str: A message confirming the library_management was saved.

        Raises:
            LibraryFileError: If there is an issue writing to the file.
        """
        try:
            with open(filename, 'w') as file:
                json.dump([book.__dict__ for book in self.books], file, indent=4)
            return f"Library saved to {filename}"
        except IOError as e:
            raise LibraryFileError(filename, str(e))

    def load_library(self, filename: str) -> str:
        """
        Loads the library_management from a JSON file.

        Args:
            filename (str): The name of the file to load the library_management from.

        Returns:
            str: A message confirming the library_management was loaded.

        Raises:
            LibraryFileError: If there is an issue reading from the file.
        """
        try:
            with open(filename, 'r') as file:
                book_dicts = json.load(file)
                self.books = [Book(**book_dict) for book_dict in book_dicts]
            return f"Library loaded from {filename}"
        except FileNotFoundError:
            return f"No library_management file found at {filename}. Starting with an empty library_management."
        except (IOError, json.JSONDecodeError) as e:
            raise LibraryFileError(filename, str(e))

    def _find_book_by_id(self, book_id: int) -> Book:
        """
        Finds a book by its ID.

        Args:
            book_id (int): The ID of the book.

        Returns:
            Book: The book with the specified ID.

        Raises:
            BookNotFoundError: If the book with the specified ID is not found.
        """
        for book in self.books:
            if book.book_id == book_id:
                return book
        raise BookNotFoundError(book_id)
