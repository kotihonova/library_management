import unittest
from unittest.mock import patch
import json
from library_management.library import Library
from library_management.errors import DuplicateBookError, BookNotFoundError


class TestLibrary(unittest.TestCase):

    def setUp(self) -> None:
        """Set up a fresh library_management for each test."""
        self.library = Library()

    def test_add_book(self):
        """Test adding a new book."""
        response = self.library.add_book("The Great Gatsby", "F. Scott Fitzgerald", 1925)
        self.assertEqual(response, "Book 'The Great Gatsby' by F. Scott Fitzgerald added with ID 1.")
        self.assertEqual(len(self.library.books), 1)

    def test_add_duplicate_book(self):
        """Test adding a duplicate book."""
        self.library.add_book("The Great Gatsby", "F. Scott Fitzgerald", 1925)
        with self.assertRaises(DuplicateBookError):
            self.library.add_book("The Great Gatsby", "F. Scott Fitzgerald", 1925)

    def test_delete_book(self):
        """Test deleting a book."""
        self.library.add_book("The Great Gatsby", "F. Scott Fitzgerald", 1925)
        response = self.library.delete_book(1)
        self.assertEqual(response, "Book with ID 1 has been deleted.")
        self.assertEqual(len(self.library.books), 0)

    def test_delete_nonexistent_book(self):
        """Test deleting a nonexistent book."""
        with self.assertRaises(BookNotFoundError):
            self.library.delete_book(1)

    def test_edit_status(self):
        """Test editing the status of a book."""
        self.library.add_book("The Great Gatsby", "F. Scott Fitzgerald", 1925)
        response = self.library.edit_status(1, "checked out")
        self.assertEqual(response, "Status of book with ID 1 has been updated to 'checked out'.")
        self.assertEqual(self.library.books[0].status, "checked out")

    def test_edit_status_nonexistent_book(self):
        """Test editing the status of a nonexistent book."""
        with self.assertRaises(BookNotFoundError):
            self.library.edit_status(1, "checked out")

    def test_find_books_by_title(self):
        """Test finding books by title."""
        self.library.add_book("The Great Gatsby", "F. Scott Fitzgerald", 1925)
        found_books = self.library.find_books("The Great Gatsby")
        self.assertEqual(len(found_books), 1)
        self.assertEqual(found_books[0].title, "The Great Gatsby")

    def test_find_books_by_author(self):
        """Test finding books by author."""
        self.library.add_book("1984", "George Orwell", 1949)
        found_books = self.library.find_books("George Orwell")
        self.assertEqual(len(found_books), 1)
        self.assertEqual(found_books[0].author, "George Orwell")

    def test_find_books_by_year(self):
        """Test finding books by year."""
        self.library.add_book("To Kill a Mockingbird", "Harper Lee", 1960)
        found_books = self.library.find_books("1960")
        self.assertEqual(len(found_books), 1)
        self.assertEqual(found_books[0].year, 1960)

    def test_find_books_no_results(self):
        """Test finding books with no results."""
        with self.assertRaises(BookNotFoundError):
            self.library.find_books("Nonexistent Book")

    def test_list_books(self):
        """Test listing all books."""
        self.library.add_book("The Great Gatsby", "F. Scott Fitzgerald", 1925)
        books = self.library.list_books()
        self.assertEqual(len(books), 1)
        self.assertEqual(books[0].title, "The Great Gatsby")

    def test_list_books_empty(self):
        """Test listing books when library_management is empty."""
        response = self.library.list_books()
        self.assertEqual(response, "No books in the library_management.")

    def test_save_library(self):
        """Test saving the library_management to a JSON file."""
        self.library.add_book("The Great Gatsby", "F. Scott Fitzgerald", 1925)
        with patch('builtins.open', unittest.mock.mock_open()) as mocked_file:
            response = self.library.save_library("library_management.json")
            self.assertEqual(response, "Library saved to library_management.json")
            mocked_file().write.assert_called_once_with(json.dumps(
                [book.__dict__ for book in self.library.books], indent=4))

    def test_load_library(self):
        """Test loading the library_management from a JSON file."""
        book_data = [{"book_id": 1, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "year": 1925, "status": "available"}]
        with patch('builtins.open', unittest.mock.mock_open(read_data=json.dumps(book_data))):
            response = self.library.load_library("library_management.json")
            self.assertEqual(response, "Library loaded from library_management.json")
            self.assertEqual(len(self.library.books), 1)
            self.assertEqual(self.library.books[0].title, "The Great Gatsby")

    def test_load_library_file_not_found(self):
        """Test loading the library_management from a nonexistent file."""
        with patch('builtins.open', side_effect=FileNotFoundError):
            response = self.library.load_library("nonexistent.json")
            self.assertEqual(response, "No library_management file found at nonexistent.json. Starting with an empty library_management.")
            self.assertEqual(len(self.library.books), 0)


if __name__ == "__main__":
    unittest.main()
