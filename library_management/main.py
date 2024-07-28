import sys
from typing import Dict, Tuple
from library import Library
from errors import InvalidChoiceError, BookNotFoundError, DuplicateBookError, InvalidStatusError, BookSearchError


def quit_app() -> None:
    """Quits the application."""
    print("Quitting the application...")
    sys.exit()


menu_options: Dict[str, Tuple[str, str]] = {
    'a': ("Add a book", 'add_book'),
    'd': ("Delete a book", 'delete_book'),
    'e': ("Edit status", 'edit_status'),
    's': ("Find a book", 'find_book'),
    'l': ("List of all books", 'list_books'),
    'q': ("Quit", quit_app),
}


def show_menu() -> None:
    """Displays the menu to user."""
    print("Welcome to your library_management!")
    for key, (description, _) in menu_options.items():
        print(f"'{key}' - {description}")


def add_book(library: 'Library') -> None:
    """Handles adding a new book to the library."""
    title = input("Enter title: ").strip()
    author = input("Enter author: ").strip()
    try:
        year = int(input("Enter year: ").strip())
        print(library.add_book(title, author, year))
    except ValueError:
        print("Invalid input for year. Please enter a valid number.")
    except DuplicateBookError as e:
        print(e)


def delete_book(library: 'Library') -> None:
    """Handles deleting a book from the library."""
    try:
        book_id = int(input("Enter book ID to delete: ").strip())
        print(library.delete_book(book_id))
    except ValueError:
        print("Invalid input for book ID. Please enter a valid number.")
    except BookNotFoundError as e:
        print(e)


def edit_status(library: 'Library') -> None:
    """Handles editing the status of a book."""
    try:
        book_id = int(input("Enter book ID to edit status: ").strip())
        new_status = input("Enter new status (available/checked out): ").strip()
        print(library.edit_status(book_id, new_status))
    except ValueError:
        print("Invalid input for book ID. Please enter a valid number.")
    except InvalidStatusError as e:
        print(e)
    except BookNotFoundError as e:
        print(e)


def find_book(library: 'Library') -> None:
    """Handles finding a book in the library."""
    search_term = input("Enter title, author, or year to search: ").strip()
    try:
        found_books = library.find_books(search_term)
        for book in found_books:
            print(book)
    except BookSearchError as e:
        print(e)


def list_books(library: 'Library') -> None:
    """Handles listing all books in the library."""
    books = library.list_books()
    if isinstance(books, str):
        print(books)
    else:
        for book in books:
            print(book)


def handle_choice(choice: str, library: 'Library') -> None:
    """Handles the user's menu choice."""
    if choice not in menu_options:
        raise InvalidChoiceError(choice)

    description, action = menu_options.get(choice)
    if callable(action):
        if action == quit_app:
            action()
        else:
            action(library)
    else:
        raise InvalidChoiceError(choice)


def main():
    """Main function to run the library console application."""
    library = Library()
    while True:
        show_menu()
        choice = input("Choose an option: ").strip().lower()
        try:
            handle_choice(choice, library)
        except InvalidChoiceError as e:
            print(e)


if __name__ == "__main__":
    main()
