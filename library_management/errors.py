class BookNotFoundError(Exception):
    """
    Exception raised when a book is not found in the library_management.

    Attributes:
        book_id (int): The ID of the book that was not found.
    """

    def __init__(self, book_id: int) -> None:
        self.book_id: int = book_id
        super().__init__(f"Book with ID {book_id} not found.")

    def __str__(self) -> str:
        return f"BookNotFoundError: {self.args[0]}"


class DuplicateBookError(Exception):
    """
    Exception raised when attempting to add a duplicate book to the library_management.

    Attributes:
        title (str): The title of the duplicate book.
        author (str): The author of the duplicate book.
        year (int): The publication year of the duplicate book.
    """

    def __init__(self, title: str, author: str, year: int) -> None:
        self.title: str = title
        self.author: str = author
        self.year: int = year
        super().__init__(f"Book '{title}' by {author} ({year}) already exists in the library_management.")

    def __str__(self) -> str:
        return f"DuplicateBookError: {self.args[0]}"


class InvalidStatusError(Exception):
    """
    Exception raised when an invalid status is provided.

    Attributes:
        status (str): The invalid status provided.
    """

    def __init__(self, status: str) -> None:
        self.status: str = status
        super().__init__(f"Invalid status: '{status}'. Valid statuses are 'available' and 'checked out'.")

    def __str__(self) -> str:
        return f"InvalidStatusError: {self.args[0]}"


class LibraryFileError(Exception):
    """
    Exception raised when there is an issue with the library_management file.

    Attributes:
        filename (str): The name of the file where the error occurred.
        message (str): A description of the error.
    """

    def __init__(self, filename: str, message: str) -> None:
        self.filename: str = filename
        self.message: str = message
        super().__init__(f"File '{filename}': {message}")

    def __str__(self) -> str:
        return f"LibraryFileError: {self.args[0]}"


class BookSearchError(Exception):
    """
    Exception raised when no books are found matching the search criteria.

    Attributes:
        search_term (str): The term used for the search that resulted in no matches.
    """

    def __init__(self, search_term: str) -> None:
        self.search_term: str = search_term
        super().__init__(f"No books found matching the search term '{search_term}'.")

    def __str__(self) -> str:
        return f"BookSearchError: {self.args[0]}"


class InvalidChoiceError(Exception):
    """Exception raised when an invalid choice is made in the menu."""

    def __init__(self, choice: str) -> None:
        self.choice: str = choice
        super().__init__(f"Invalid menu choice: '{choice}'")

    def __str__(self) -> str:
        return f"InvalidChoiceError: {self.args[0]}"
