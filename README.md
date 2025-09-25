Quiz System (Python + MySQL)

This is a command-line quiz system built with Python and MySQL.
It supports Admin and User functionalities, including user registration, quiz attempts, result storage, and question management.

🚀 Features
👨‍💻 Admin

Secure login with username and password.

Add quiz questions with multiple options (supports Python/MySQL categories).

View all questions (with correct answers).

Delete questions by ID.

Logout to return to the main menu.

🙋 User

Register with Name and Mobile Number (validated for 10 digits starting with 6/7/8/9).

Prevents duplicate registration (based on name & mobile number).

Take quizzes based on selected technology (Python/MySQL).

Immediate result evaluation with:

Score

Percentage

Performance remark (Excellent/Good Job/Try Again)

Option to retake quiz.

🛠️ Technologies Used

Python 3.11

MySQL (via mysql-connector-python)

⚡ Installation & Setup

Clone the repository

git clone https://github.com/your-username/quiz-system.git
cd quiz-system


Install dependencies

pip install mysql-connector-python


Create database in MySQL

CREATE DATABASE database name;
USE database name;


Create tables
Run the provided SQL queries from Database Schema
.

Insert Admin Credentials

INSERT INTO admins (usernames, passwords) VALUES ('admin', 'admin123');


Update Database Config
In main.py, update MySQL connection details:

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your db password",
    database="your database"
)


Run the program

python main.py

🎮 Usage
Main Menu:
=== QUIZ SYSTEM ===
1. Admin Login
2. User Login
3. Exit


Admins can manage questions.

Users can register/login and attempt quizzes.

📊 Sample Output

User Taking Quiz:

Select Technology (Python/MySQL): Python
Q.no: 1
Q: What is Python?
A. Programming Language
B. Snake
C. Coffee
D. None
Your Answer (A/B/C/D): A

Quiz Completed! Your Score: 1/1
Percentage: 100.00%
Remark: Excellent!

📌 Notes

To stop adding a multiline question, press Enter twice.

Admin credentials must exist in the admins table before login.

User results update after every quiz attempt.

🧑‍💻 Author

Developed by [Triveni]
