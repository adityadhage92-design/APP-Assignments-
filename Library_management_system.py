"""
Library Management System
Advanced Python - Assignment 01

Implements the provided problem statement using OOP:
books, patrons, adding books, registering patrons,
issuing books, returning books, availability, and borrowing records.
"""


class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.available = True

    def __str__(self):
        status = "Available" if self.available else "Borrowed"
        return f"{self.title} by {self.author} - {status}"


class Patron:
    def __init__(self, name):
        self.name = name
        self.borrowed_books = []

    def borrow_book(self, book):
        self.borrowed_books.append(book)

    def return_book(self, book):
        if book in self.borrowed_books:
            self.borrowed_books.remove(book)

    def __str__(self):
        borrowed = ", ".join(book.title for book in self.borrowed_books)
        return f"{self.name} - Borrowed Books: {borrowed or 'None'}"


class Library:
    def __init__(self):
        self.books = []
        self.patrons = []

    def add_book(self, title, author):
        book = Book(title, author)
        self.books.append(book)
        return book

    def register_patron(self, name):
        patron = Patron(name)
        self.patrons.append(patron)
        return patron

    def issue_book(self, title, patron_name):
        book = self._find_book(title)
        patron = self._find_patron(patron_name)

        if book is None:
            raise ValueError(f"Book '{title}' not found.")
        if patron is None:
            raise ValueError(f"Patron '{patron_name}' not found.")
        if not book.available:
            raise ValueError(f"Book '{title}' is currently unavailable.")

        book.available = False
        patron.borrow_book(book)
        return True

    def return_book(self, title, patron_name):
        book = self._find_book(title)
        patron = self._find_patron(patron_name)

        if book is None:
            raise ValueError(f"Book '{title}' not found.")
        if patron is None:
            raise ValueError(f"Patron '{patron_name}' not found.")
        if book not in patron.borrowed_books:
            raise ValueError(
                f"Patron '{patron_name}' has not borrowed '{title}'."
            )

        patron.return_book(book)
        book.available = True
        return True

    def _find_book(self, title):
        for book in self.books:
            if book.title.lower() == title.lower():
                return book
        return None

    def _find_patron(self, name):
        for patron in self.patrons:
            if patron.name.lower() == name.lower():
                return patron
        return None

    def display_books(self):
        print("\nBooks:")
        if not self.books:
            print("No books available.")
            return
        for book in self.books:
            print(f"- {book}")

    def display_patrons(self):
        print("\nPatrons:")
        if not self.patrons:
            print("No patrons registered.")
            return
        for patron in self.patrons:
            print(f"- {patron}")


if __name__ == "__main__":
    library = Library()

    library.add_book("Python Programming", "John Smith")
    library.add_book("Object-Oriented Python", "Jane Doe")
    library.add_book("Advanced Python", "Alex Brown")

    library.register_patron("Rahul")
    library.register_patron("Priya")

    library.display_books()
    library.display_patrons()

    print("\n--- Issuing Books ---")
    library.issue_book("Python Programming", "Rahul")
    library.issue_book("Advanced Python", "Priya")

    library.display_books()
    library.display_patrons()

    print("\n--- Returning Book ---")
    library.return_book("Python Programming", "Rahul")

    library.display_books()
    library.display_patrons()
