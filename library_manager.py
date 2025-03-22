#Import required modules for file handling and type hints
import json
from typing import List, Dict, Any
import os

class LibraryManager:
    def __init__(self):
        # Initialize an empty list to store book dictionaries
        # This implements the requirement: "Use a list of dictionaries to store the books"
        self.books: List[Dict[str, Any]] = []
        self.filename = "library.json"
        self.backup_filename = "library_backup.json"
        self.load_library()

    def add_book(self) -> None:
        """Add a new book to the library."""
        print("\n=== Add New Book ===")
        # Get user input and strip whitespace
        # This implements string manipulation for input handling
        title = input("Enter book title: ").strip()
        author = input("Enter author name: ").strip()
        
        # Input validation and type casting for year
        # This implements the requirement: "Use type casting to convert user input to appropriate data types"
        while True:
            try:
                year = int(input("Enter publication year: "))
                if 1800 <= year <= 2024:
                    break
                print("Please enter a valid year between 1800 and 2024.")
            except ValueError:
                print("Please enter a valid number for the year.")
        
        genre = input("Enter genre: ").strip()
        # Convert string input to boolean using string manipulation
        read_status = input("Have you read this book? (yes/no): ").lower().strip() == "yes"
        
        # Create a dictionary for the book
        # This implements the requirement: "Use a list of dictionaries to store the books"
        book = {
            "title": title,
            "author": author,
            "year": year,
            "genre": genre,
            "read": read_status
        }
        
        # Add book to the list and save to file
        self.books.append(book)
        self.save_library()
        # Use string formatting for output
        print(f"\nSuccessfully added '{title}' to your library!")

    def remove_book(self) -> None:
        """Remove a book from the library."""
        # Check if library is empty
        if not self.books:
            print("\nYour library is empty!")
            return

        print("\n=== Remove Book ===")
        title = input("Enter the title of the book to remove: ").strip()
        
        # Loop through books to find and remove the matching title
        # This implements the requirement: "Use loops and conditionals"
        for i, book in enumerate(self.books):
            if book["title"].lower() == title.lower():
                removed_book = self.books.pop(i)
                self.save_library()
                print(f"\nSuccessfully removed '{removed_book['title']}' from your library!")
                return
        
        print(f"\nBook with title '{title}' not found in your library.")

    def search_books(self) -> None:
        """Search for books by title or author."""
        if not self.books:
            print("\nYour library is empty!")
            return

        print("\n=== Search Books ===")
        # Get search term and convert to lowercase for case-insensitive search
        search_term = input("Enter search term (title or author): ").strip().lower()
        
        # Use list comprehension and string manipulation for search
        found_books = []
        for book in self.books:
            if search_term in book["title"].lower() or search_term in book["author"].lower():
                found_books.append(book)
        
        if found_books:
            print("\nFound books:")
            self._display_books(found_books)
        else:
            print(f"\nNo books found matching '{search_term}'")

    def display_all_books(self) -> None:
        """Display all books in the library."""
        if not self.books:
            print("\nYour library is empty!")
            return

        print("\n=== Your Library ===")
        self._display_books(self.books)

    def display_statistics(self) -> None:
        """Display library statistics."""
        if not self.books:
            print("\nYour library is empty!")
            return

        # Calculate statistics using list operations
        total_books = len(self.books)
        read_books = sum(1 for book in self.books if book["read"])
        percentage_read = (read_books / total_books) * 100 if total_books > 0 else 0

        # Format and display statistics
        print("\n=== Library Statistics ===")
        print(f"Total books: {total_books}")
        print(f"Books read: {read_books}")
        print(f"Percentage read: {percentage_read:.1f}%")

        # Calculate genre statistics using dictionary
        genres = {}
        for book in self.books:
            genre = book["genre"]
            genres[genre] = genres.get(genre, 0) + 1

        print("\nBooks by genre:")
        for genre, count in genres.items():
            print(f"{genre}: {count}")

    def _display_books(self, books: List[Dict[str, Any]]) -> None:
        """Helper method to display a list of books."""
        # Use enumerate for numbered display
        for i, book in enumerate(books, 1):
            # Use string manipulation for status indicator
            status = "✓" if book["read"] else "✗"
            # Format output using f-strings
            print(f"{i}. {book['title']} by {book['author']} ({book['year']})")
            print(f"   Genre: {book['genre']} | Read: {status}")

    def save_library(self) -> None:
        """
        Save the library to a JSON file.
        Creates a backup file before saving to prevent data loss.
        """
        try:
            # Create a backup of the existing file if it exists
            if os.path.exists(self.filename):
                try:
                    with open(self.filename, 'r', encoding='utf-8') as src:
                        with open(self.backup_filename, 'w', encoding='utf-8') as dst:
                            dst.write(src.read())
                except Exception as e:
                    print(f"Warning: Could not create backup file: {e}")

            # Save the current library
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(self.books, f, indent=4, ensure_ascii=False)
                print(f"\nLibrary successfully saved to {self.filename}")
        except Exception as e:
            print(f"Error saving library: {e}")
            # Try to recover from backup if save failed
            if os.path.exists(self.backup_filename):
                try:
                    with open(self.backup_filename, 'r', encoding='utf-8') as src:
                        with open(self.filename, 'w', encoding='utf-8') as dst:
                            dst.write(src.read())
                    print("Recovered from backup file.")
                except Exception as backup_e:
                    print(f"Error recovering from backup: {backup_e}")

    def load_library(self) -> None:
        """
        Load the library from a JSON file.
        Attempts to load from backup if the main file is corrupted.
        """
        loaded = False
        
        # Try loading from the main file
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Validate the loaded data
                    if isinstance(data, list):
                        self.books = data
                        loaded = True
                        print(f"\nLibrary loaded successfully from {self.filename}")
                        print(f"Total books loaded: {len(self.books)}")
                    else:
                        print("Error: Invalid data format in library file")
            except json.JSONDecodeError:
                print("Error: Library file is corrupted")
            except Exception as e:
                print(f"Error loading library: {e}")

        # Try loading from backup if main load failed
        if not loaded and os.path.exists(self.backup_filename):
            try:
                with open(self.backup_filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        self.books = data
                        loaded = True
                        print(f"\nLibrary loaded successfully from backup file")
                        print(f"Total books loaded: {len(self.books)}")
                    else:
                        print("Error: Invalid data format in backup file")
            except Exception as e:
                print(f"Error loading from backup: {e}")

        # Initialize empty library if both loads failed
        if not loaded:
            self.books = []
            print("\nStarting with an empty library")

    def export_to_txt(self, filename: str = "library_export.txt") -> None:
        """
        Export the library to a human-readable text file.
        This provides an additional backup in a readable format.
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("=== Personal Library Export ===\n\n")
                f.write(f"Total Books: {len(self.books)}\n")
                f.write("=" * 50 + "\n\n")
                
                for i, book in enumerate(self.books, 1):
                    f.write(f"Book #{i}:\n")
                    f.write(f"Title: {book['title']}\n")
                    f.write(f"Author: {book['author']}\n")
                    f.write(f"Year: {book['year']}\n")
                    f.write(f"Genre: {book['genre']}\n")
                    f.write(f"Read: {'Yes' if book['read'] else 'No'}\n")
                    f.write("-" * 30 + "\n\n")
                
                print(f"\nLibrary exported to {filename}")
        except Exception as e:
            print(f"Error exporting library to text file: {e}")

def main():
    library = LibraryManager()
    
    # Main menu loop
    # This implements the requirement: "Use loops and conditionals to implement the menu system"
    while True:
        print("\n=== Personal Library Manager ===")
        print("1. Add a book")
        print("2. Remove a book")
        print("3. Search books")
        print("4. Display all books")
        print("5. Display statistics")
        print("6. Export to text file")
        print("7. Exit")
        
        # Get user input and handle menu choices
        choice = input("\nEnter your choice (1-7): ").strip()
        
        # Use conditionals to handle different menu options
        if choice == "1":
            library.add_book()
        elif choice == "2":
            library.remove_book()
        elif choice == "3":
            library.search_books()
        elif choice == "4":
            library.display_all_books()
        elif choice == "5":
            library.display_statistics()
        elif choice == "6":
            library.export_to_txt()
        elif choice == "7":
            print("\nSaving library before exit...")
            library.save_library()
            print("\nThank you for using Personal Library Manager!")
            break
        else:
            print("\nInvalid choice. Please try again.")

if __name__ == "__main__":
    main()
