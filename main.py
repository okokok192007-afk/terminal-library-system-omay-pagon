import os
import hashlib
import datetime

USERS_FILE = "users.txt"
BOOKS_FILE = "books.txt"
BORROWERS_FILE = "borrowers.txt"
HISTORY_FILE = "borrowing_history.txt"

def initialize_files():
    files = [USERS_FILE, BOOKS_FILE, BORROWERS_FILE, HISTORY_FILE]
    for file in files:
        if not os.path.exists(file):
            with open(file, "w") as f:
                pass

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user():
    print("\n--- USER REGISTRATION ---")
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()
    role = input("Enter role (Admin/Staff): ").strip().capitalize()
    if not username or not password:
        print("Error: Username and password cannot be empty.")
        return
    if role not in ["Admin", "Staff"]:
        print("Error: Role must be Admin or Staff.")
        return
    hashed_pw = hash_password(password)
    with open(USERS_FILE, "a") as f:
        f.write(f"{username},{hashed_pw},{role}\n")
    print(f"User '{username}' registered successfully!")

def login_user():
    print("\n--- SYSTEM LOGIN ---")
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    hashed_pw = hash_password(password)
    if not os.path.exists(USERS_FILE):
        print("No users found. Please register first.")
        return None, None
    with open(USERS_FILE, "r") as f:
        for line in f:
            parts = line.strip().split(",")
            if len(parts) == 3:
                stored_user, stored_pw, role = parts
                if stored_user == username and stored_pw == hashed_pw:
                    print(f"Login successful! Welcome, {username} ({role}).")
                    return username, role
    print("Invalid username or password.")
    return None, None

def add_book():
    print("\n--- ADD NEW BOOK ---")
    book_id = input("Enter Book ID: ").strip()
    title = input("Enter Book Title: ").strip()
    author = input("Enter Author: ").strip()
    if not book_id or not title:
        print("Error: Book ID and Title are required.")
        return
    with open(BOOKS_FILE, "a") as f:
        f.write(f"{book_id},{title},{author},Available\n")
    print(f"Book '{title}' added successfully!")

def view_books():
    print("\n--- LIBRARY INVENTORY ---")
    if not os.path.exists(BOOKS_FILE) or os.path.getsize(BOOKS_FILE) == 0:
        print("No books found in the system.")
        return
    print(f"{'Book ID':<10} | {'Title':<25} | {'Author':<20} | {'Status'}")
    print("-" * 65)
    with open(BOOKS_FILE, "r") as f:
        for line in f:
            parts = line.strip().split(",")
            if len(parts) == 4:
                b_id, title, author, status = parts
                print(f"{b_id:<10} | {title:<25} | {author:<20} | {status}")

def add_borrower():
    print("\n--- REGISTER BORROWER ---")
    borrower_id = input("Enter Borrower ID: ").strip()
    name = input("Enter Borrower Name: ").strip()
    course = input("Enter Course/Section: ").strip()
    if not borrower_id or not name:
        print("Error: Borrower ID and Name are required.")
        return
    with open(BORROWERS_FILE, "a") as f:
        f.write(f"{borrower_id},{name},{course}\n")
    print(f"Borrower '{name}' registered successfully!")

def view_borrowers():
    print("\n--- BORROWERS LIST ---")
    if not os.path.exists(BORROWERS_FILE) or os.path.getsize(BORROWERS_FILE) == 0:
        print("No borrowers found.")
        return
    print(f"{'Borrower ID':<12} | {'Name':<25} | {'Course'}")
    print("-" * 60)
    with open(BORROWERS_FILE, "r") as f:
        for line in f:
            parts = line.strip().split(",")
            if len(parts) == 3:
                b_id, name, course = parts
                print(f"{b_id:<12} | {name:<25} | {course}")

def borrow_book():
    print("\n--- BORROW A BOOK ---")
    book_id = input("Enter Book ID to borrow: ").strip()
    borrower_id = input("Enter Borrower ID: ").strip()
    borrower_exists = False
    if os.path.exists(BORROWERS_FILE):
        with open(BORROWERS_FILE, "r") as f:
            for line in f:
                if line.startswith(f"{borrower_id},"):
                    borrower_exists = True
                    break
    if not borrower_exists:
        print("Error: Borrower ID not found. Please register the borrower first.")
        return
    books = []
    book_found = False
    is_available = False
    if os.path.exists(BOOKS_FILE):
        with open(BOOKS_FILE, "r") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) == 4:
                    b_id, title, author, status = parts
                    if b_id == book_id:
                        book_found = True
                        if status == "Available":
                            is_available = True
                            status = "Borrowed"
                    books.append(f"{b_id},{title},{author},{status}\n")
    if not book_found:
        print("Error: Book ID not found.")
        return
    if not is_available:
        print("Error: Book is already borrowed or unavailable.")
        return
    with open(BOOKS_FILE, "w") as f:
        f.writelines(books)
    date_borrowed = datetime.date.today().strftime("%Y-%m-%d")
    with open(HISTORY_FILE, "a") as f:
        f.write(f"{book_id},{borrower_id},{date_borrowed},Active\n")
    print(f"Book ID '{book_id}' successfully borrowed by Borrower '{borrower_id}'!")

def view_history():
    print("\n--- BORROWING HISTORY ---")
    if not os.path.exists(HISTORY_FILE) or os.path.getsize(HISTORY_FILE) == 0:
        print("No borrowing history found.")
        return
    print(f"{'Book ID':<10} | {'Borrower ID':<15} | {'Date Borrowed':<15} | {'Status'}")
    print("-" * 60)
    with open(HISTORY_FILE, "r") as f:
        for line in f:
            parts = line.strip().split(",")
            if len(parts) == 4:
                b_id, bor_id, date, status = parts
                print(f"{b_id:<10} | {bor_id:<15} | {date:<15} | {status}")

def main_dashboard(username, role):
    while True:
        print(f"\n=== LIBRARY DASHBOARD [{role}: {username}] ===")
        print("1. View Books")
        print("2. Add New Book")
        print("3. Register Borrower")
        print("4. View Borrowers")
        print("5. Borrow a Book")
        print("6. View Borrowing History")
        if role == "Admin":
            print("7. Register New User")
            print("8. Logout")
        else:
            print("7. Logout")
        choice = input("Select an option: ").strip()
        if choice == '1':
            view_books()
        elif choice == '2':
            add_book()
        elif choice == '3':
            add_borrower()
        elif choice == '4':
            view_borrowers()
        elif choice == '5':
            borrow_book()
        elif choice == '6':
            view_history()
        elif choice == '7':
            if role == "Admin":
                register_user()
            else:
                print("Logging out...")
                break
        elif choice == '8' and role == "Admin":
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")

def main():
    initialize_files()
    while True:
        print("\n=== WELCOME TO TERMINAL LIBRARY SYSTEM ===")
        print("1. Login")
        print("2. Register User")
        print("3. Exit")
        choice = input("Select an option (1-3): ").strip()
        if choice == '1':
            user, role = login_user()
            if user:
                main_dashboard(user, role)
        elif choice == '2':
            register_user()
        elif choice == '3':
            print("Exiting application. Goodbye!")
            break
        else:
            print("Invalid input. Please try again.")

if __name__ == "__main__":
    main()
