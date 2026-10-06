import json
from typing import List


class Book:
    def __init__(self, title: str, author: str, isbn: str, available: bool = True):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.available = available

    def __repr__(self):
        status = "Available" if self.available else "Checked Out"

        return (
            f"Book(title='{self.title}', "
            f"author='{self.author}', "
            f"isbn='{self.isbn}', "
            f"status='{status}')"
        )


class Library:
    def __init__(self):
        self.books = {}

    def add_book(self, book: Book):
        if book.isbn in self.books:
            raise ValueError(
                f"Book with ISBN '{book.isbn}' already exists."
            )

        self.books[book.isbn] = book

    def search_by_title(self, keyword: str) -> List[Book]:
        keyword = keyword.lower()

        return [
            book
            for book in self.books.values()
            if keyword in book.title.lower()
        ]

    def checkout(self, isbn: str) -> bool:
        if isbn not in self.books:
            return False

        book = self.books[isbn]

        if not book.available:
            return False

        book.available = False
        return True

    def return_book(self, isbn: str) -> bool:
        if isbn not in self.books:
            return False

        book = self.books[isbn]

        if book.available:
            return False

        book.available = True
        return True

    def save_to_file(self, path: str):
        data = []

        for book in self.books.values():
            data.append({
                "title": book.title,
                "author": book.author,
                "isbn": book.isbn,
                "available": book.available
            })

        with open(path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    @classmethod
    def load_from_file(cls, path: str):
        library = cls()

        try:
            with open(path, "r", encoding="utf-8") as file:
                data = json.load(file)

            for item in data:
                book = Book(
                    item["title"],
                    item["author"],
                    item["isbn"],
                    item["available"]
                )

                library.add_book(book)

        except FileNotFoundError:
            print("No existing catalog found. Starting with an empty library.")

        return library


if __name__ == "__main__":

    # Load existing catalog or start with an empty library
    library = Library.load_from_file("library.json")

    # Add three distinct books
    books_to_add = [
        Book(
            "Python Crash Course",
            "Eric Matthes",
            "9781593279288"
        ),
        Book(
            "Clean Code",
            "Robert C. Martin",
            "9780132350884"
        ),
        Book(
            "The Pragmatic Programmer",
            "Andrew Hunt",
            "9780135957059"
        )
    ]

    for book in books_to_add:
        try:
            library.add_book(book)
            print(f"Added: {book.title}")
        except ValueError:
            print(f"Already exists: {book.title}")

    # Search by title
    print("\nSearch results for 'python':")

    results = library.search_by_title("python")

    for book in results:
        print(book)

    # Checkout a book
    isbn = "9781593279288"

    print("\nChecking out Python Crash Course:")

    first_checkout = library.checkout(isbn)
    print("First checkout:", first_checkout)

    # Attempt to checkout the same book again
    second_checkout = library.checkout(isbn)
    print("Second checkout:", second_checkout)

    # Return the book
    returned = library.return_book(isbn)
    print("Book returned:", returned)

    # Save catalog
    library.save_to_file("library.json")

    print("\nLibrary catalog saved successfully.")