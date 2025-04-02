# 📚 Library Management System

A **Flask-based Library Management System** that allows users to **add, edit, and delete books** from a MySQL database. The system provides a user-friendly web interface for efficient book management.

## 🚀 Features

* ✅ **Add Books** – Users can add new books with title, author, and ISBN.
* ✅ **Edit Books** – Select a book by its unique ID and update details.
* ✅ **Delete Books** – Remove books from the database with confirmation.
* ✅ **MySQL Database Integration** – Uses MySQL to store and manage books.
* ✅ **Flash Messages** – Displays success/error notifications.
* ✅ **Responsive UI** – Clean and simple design for better user experience.

## 🛠️ Tech Stack

* **Backend:** Flask (Python)
* **Frontend:** HTML, CSS, Bootstrap
* **Database:** MySQL

## 💂️ Project Structure

```
/library_management
│── app.py                # Flask backend logic
│── templates/
│   ├── edit_book.html    # Edit/Delete book UI
│   ├── add_book.html     # Add book UI
│── static/
│   └── styles.css        # Custom styling
│── requirements.txt      # Dependencies
│── README.md             # Project documentation
```

## 🎯 Installation & Setup

### 1⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/library-management.git
cd library-management
```

### 2⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3⃣ Set Up MySQL Database

Run the following SQL queries in MySQL:

```sql
CREATE DATABASE library_db;
USE library_db;
CREATE TABLE books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    isbn VARCHAR(20) UNIQUE NOT NULL,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    issued TINYINT(1) DEFAULT 0
);
```

### 4⃣ Run the Flask App

```bash
python app.py
```

### 5⃣ Open in Browser
* Navigate to **http://127.0.0.1:5000/**

## 💡 How to Use

1. **Add a Book** – Enter details and click **Add**.
2. **Edit a Book** – Select a book by its **ID**, modify details, and save.
3. **Delete a Book** – Select a book and click **Delete**.

## 🛠️ Contributing

* Fork the repository 🍴
* Create a new branch 🌿
* Submit a pull request 🛠️

All contributions are welcome!

## 🐝 License

This project is open-source under the **MIT License**.

## 🚀 **Happy Coding!** 🎉
