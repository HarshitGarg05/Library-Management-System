Library Management System 📚

This is a Flask-based Library Management System that allows users to add, edit, and delete books in a MySQL database. The system provides a simple web interface with a sidebar for easy navigation and a dropdown selection to manage books efficiently.

🚀 Features
✅ Add Books – Users can add new books with a title, author, and ISBN.
✅ Edit Books – Select a book by its unique ID and update its details.
✅ Delete Books – Remove books from the database with a confirmation prompt.
✅ MySQL Database Integration – Uses MySQL to store and manage book records.
✅ Flash Messages – Provides user-friendly success/error notifications.
✅ Responsive UI – A clean and simple interface for easy book management.

🛠️ Tech Stack
Backend: Flask (Python)

Frontend: HTML, CSS, Bootstrap

Database: MySQL

📂 Project Structure
/library_management
│── app.py                # Flask backend logic
│── templates/
│   ├── edit_book.html    # Edit/Delete book UI
│   ├── add_book.html     # Add book UI
│── static/
│   ├── styles.css        # Custom styling
│── requirements.txt      # Dependencies
│── README.md             # Project documentation

🎯 How to Run
Clone the repository

git clone https://github.com/yourusername/library-management.git
cd library-management
Install dependencies

pip install -r requirements.txt
Set up the MySQL database


CREATE DATABASE library_db;
USE library_db.sql in SQL in phpmyadmin

Run the Flask app

python app.py
Open in browser

Navigate to http://127.0.0.1:5000/

🛠️ Contributing
Feel free to fork the repository, create a new branch, and submit a pull request. Contributions are welcome!

📜 License
This project is open-source under the MIT License.

🚀 Happy Coding! 🎉
