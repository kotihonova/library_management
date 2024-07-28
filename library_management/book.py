class Book:
    """Class representing a book in the library_management."""

    def __init__(self, book_id: int, title: str, author: str, year: int, status: str = 'available') -> None:
        self.book_id: int = book_id
        self.title: str = title
        self.author: str = author
        self.year: int = year
        self.status: str = status

    def __repr__(self) -> str:
        return (f"Book(id={self.book_id}, title='{self.title}', "
                f"author='{self.author}', year={self.year}, status='{self.status}')")