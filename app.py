from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'library_secret_key'  # Required for flash messages

# Database Connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # Change this to your MySQL password
        database="library_db"
    )

# Initialize database tables
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create Books Table if not exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            isbn VARCHAR(20) PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            author VARCHAR(255) NOT NULL,
            issued BOOLEAN DEFAULT FALSE
        )
    ''')
    
    # Create Issued Books Table if not exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS issued_books (
            issue_id INT AUTO_INCREMENT PRIMARY KEY,
            isbn VARCHAR(20) NOT NULL,
            student_id VARCHAR(50) NOT NULL,
            student_name VARCHAR(100) NOT NULL,
            issue_date DATE NOT NULL,
            return_date DATE,
            FOREIGN KEY (isbn) REFERENCES books(isbn)
        )
    ''')
    
    conn.commit()
    cursor.close()
    conn.close()

# Initialize database on startup
init_db()

# @app.route('/')
# def home():
#     conn = get_db_connection()
#     cursor = conn.cursor(dictionary=True)
#     cursor.execute("SELECT * FROM books")
#     books = cursor.fetchall()
#     cursor.close()
#     conn.close()
#     return render_template('home.html', books=books)

@app.route('/')
def home():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    conn.close()
    
    return render_template('home.html', books=books)


@app.route('/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        isbn = request.form['isbn']
        title = request.form['title']
        author = request.form['author']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("INSERT INTO books (isbn, title, author) VALUES (%s, %s, %s)", 
                          (isbn, title, author))
            conn.commit()
            flash('Book added successfully!', 'success')
        except mysql.connector.IntegrityError:
            flash('Book with this ISBN already exists!', 'danger')
        
        cursor.close()
        conn.close()
        return redirect(url_for('home'))
    
    return render_template('add.html')

@app.route('/issue', methods=['GET', 'POST'])
def issue_book():
    if request.method == 'POST':
        isbn = request.form['isbn']
        student_id = request.form['student_id']
        student_name = request.form['student_name']
        issue_date = request.form['issue_date']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if book exists and is available
        cursor.execute("SELECT * FROM books WHERE isbn = %s AND issued = FALSE", (isbn,))
        book = cursor.fetchone()
        
        if not book:
            flash('Book is either already issued or not found!', 'danger')
            cursor.close()
            conn.close()
            return redirect(url_for('issue_book'))
        
        # Mark book as issued
        cursor.execute("UPDATE books SET issued = TRUE WHERE isbn = %s", (isbn,))
        
        # Record the issuance
        cursor.execute("""
            INSERT INTO issued_books (isbn, student_id, student_name, issue_date) 
            VALUES (%s, %s, %s, %s)
        """, (isbn, student_id, student_name, issue_date))
        
        conn.commit()
        flash('Book issued successfully!', 'success')
        
        cursor.close()
        conn.close()
        return redirect(url_for('view_issued_books'))
    
    return render_template('issue.html')

@app.route('/return', methods=['GET', 'POST'])
def return_book():
    if request.method == 'POST':
        isbn = request.form['isbn']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Update books table
        cursor.execute("UPDATE books SET issued = FALSE WHERE isbn = %s AND issued = TRUE", (isbn,))
        
        if cursor.rowcount == 0:
            flash('Book is either not issued or not found!', 'danger')
            cursor.close()
            conn.close()
            return redirect(url_for('return_book'))
        
        # Update issued_books table
        today = datetime.now().strftime('%Y-%m-%d')
        cursor.execute("""
            UPDATE issued_books 
            SET return_date = %s 
            WHERE isbn = %s AND return_date IS NULL
        """, (today, isbn))
        
        conn.commit()
        flash('Book returned successfully!', 'success')
        
        cursor.close()
        conn.close()
        return redirect(url_for('home'))
    
    return render_template('return.html')

@app.route('/search', methods=['GET', 'POST'])
def search_book():
    books = None
    
    if request.method == 'POST':
        search_query = request.form['search_query']
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT * FROM books 
            WHERE title LIKE %s OR author LIKE %s OR isbn LIKE %s
        """, ('%' + search_query + '%', '%' + search_query + '%', '%' + search_query + '%'))
        
        books = cursor.fetchall()
        
        cursor.close()
        conn.close()
    
    return render_template('search.html', books=books)

@app.route('/view_issued')
def view_issued_books():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("""
        SELECT ib.issue_id, ib.student_name, ib.student_id, ib.issue_date, ib.return_date, 
               b.isbn, b.title, b.author
        FROM issued_books ib
        JOIN books b ON ib.isbn = b.isbn
        ORDER BY ib.return_date IS NULL DESC, ib.issue_date DESC
    """)
    
    issued_books = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('view_issued.html', issued_books=issued_books)

def get_available_books():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='password',  # Use your MySQL credentials
        database='library_db'
    )
    
    cursor = connection.cursor(dictionary=True)
    
    # Query to fetch available books
    cursor.execute("SELECT * FROM books WHERE available = 1")  # Assuming `available` is a column indicating availability
    books = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    return books

@app.route('/edit_book', methods=['GET', 'POST'])
def edit_book():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    conn.close()
    
    message = None
    
    if request.method == 'POST':
        if 'delete' in request.form:  # Check if delete button was clicked
            book_id = request.form['book_id']
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''
                DELETE FROM books 
                WHERE id = %s
            ''', (book_id,))
            conn.commit()
            conn.close()
            flash("Book deleted updated successfully!", "success") 
            return redirect(url_for('edit_book', message=message))

        # Handle form submission for updating book details
        book_id = request.form['book_id']
        title = request.form['title']
        author = request.form['author']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE books 
            SET title = %s, author = %s 
            WHERE id = %s
        ''', (title, author, book_id))
        conn.commit()
        conn.close()
        flash("Book details updated successfully!", "success") 
        return redirect(url_for('edit_book', message=message))

    return render_template('edit_book.html', books=books, message=message)

@app.route('/delete_book/<int:id>', methods=['POST'])
def delete_book(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE id = %s", (id,))
    conn.commit()
    conn.close()
    flash("Book details updated successfully!", "success") 
    return redirect(url_for('available_books'))


if __name__ == '__main__':
    app.run(debug=True)