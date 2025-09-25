import mysql.connector 

# Connecting to your MySQL server
db = mysql.connector.connect(
    host="localhost",       
    user="root",            
    password="MySql@1234",  
    database="triveni"   
)

# Creating a cursor to execute queries
cursor = db.cursor()


def admin_login(cursor):
    uname = input("Enter Admin Username: ")
    pwd = input("Enter Admin Password: ")

    cursor.execute("SELECT * FROM admins WHERE usernames=%s AND passwords=%s", (uname, pwd))
    result = cursor.fetchone()

    if result:
        print(" Admin Login Successful!")
        return True
    else:
        print(" Invalid Admin Credentials.")
        return False
        
def user_login_or_register(cursor, conn):
    uname = input("Enter Your Name: ").strip().title()

    # Validating mobile number
    while True:
        mobile = input("Enter Mobile Number: ").strip()
        if not mobile.isdigit() or len(mobile) != 10 or mobile[0] not in "6789":
            print(" Invalid input. Mobile must be 10 digits starting with 6/7/8/9.")
            continue
        else:
            break

    # Check for duplicate username and mobile
    cursor.execute("SELECT * FROM users WHERE username = %s AND mobile_number = %s", (uname, mobile))
    if cursor.fetchone():
        print(f" Welcome back, {uname}! You are already registered.")
        return uname, mobile

    # Register new user
    try:
        cursor.execute(
            "INSERT INTO users (username, mobile_number, technology, score, quiz_time) VALUES (%s, %s, %s, %s, %s)",
            (uname, mobile, '', 0, None)
        )
        conn.commit()
        print(f" User Registered Successfully: {uname}")
        return uname, mobile
    except Exception as e:
        print(" Error during registration:", e)
        return None, None
        

def admin_menu(cursor, conn):
    while True:
        print("\n******* *Admin Menu *************")
        print("1. Add Question")
        print("2. View All Questions")
        print("3. Delete Question")
        print("4. Logout")
        choice = input("Enter choice: ")

        if choice == '1':
            tech = input("Enter Technology (Python/MySQL): ")
            
            def get_multiline_input(prompt):
                print(prompt)
                lines = []
                while True:
                    line = input()
                    if line.strip() == "":  # empty line to stop
                        break
                    lines.append(line)
                return "\n".join(lines)

# Use multiline input for question
            q = get_multiline_input("Enter Question (Press Enter twice to finish):")

            a = input("Option A: ")
            b = input("Option B: ")
            c = input("Option C: ")
            d = input("Option D: ")
            ans = input("Correct Option (A/B/C/D): ").upper()

            cursor.execute("""
    INSERT INTO questions (technology, question_text, option_a, option_b, option_c, option_d, correct_option)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
""", (tech, q, a, b, c, d, ans))
            conn.commit()
            print("Question Added Successfully!")


        elif choice == '2':
            cursor.execute("SELECT q_id, technology, question_text, option_a, option_b, option_c, option_d, correct_option FROM questions")
            for qid, tech, qtext, a, b, c, d, correct in cursor.fetchall():
                print(f"\nQuestion ID: {qid}  |  Technology: {tech}")
                print(f"Q: {qtext}")
                print(f"A. {a}")
                print(f"B. {b}")
                print(f"C. {c}")
                print(f"D. {d}")
                print(f"(Correct Answer: {correct})")  

        elif choice == '3':
            qid = input("Enter Question ID to delete: ")
            cursor.execute("DELETE FROM questions WHERE question_id = %s", (qid,))
            conn.commit()
            print(" Question Deleted")

        elif choice == '4':
            break
        else:
            print(" Invalid Choice.")
        
import datetime

def user_take_quiz(cursor, conn, uname, mobile):
    tech = input("Select Technology (Python/MySQL): ")
    cursor.execute("SELECT * FROM questions WHERE technology = %s", (tech,))
    questions = cursor.fetchall()

    if not questions:
        print("No questions available for selected technology.")
        return

    score = 0
    for q in questions:
        print("Q.no:",q[7])
        print("Q:", q[1])
        print("A.", q[2])
        print("B.", q[3])
        print("C.", q[4])
        print("D.", q[5])
        ans = input("Your Answer (A/B/C/D): ").upper()
        if ans not in ['A','B','C','D']:
            print("Invalid choice ..,choose correct in options")
        #continue
        if ans == q[6]:
            score += 1

    #print(f"\n Quiz Completed! Your Score: {score}/{len(questions)}")
    cursor.execute("""
        UPDATE users SET technology = %s, score = %s, quiz_time = %s
        WHERE username = %s AND mobile_number = %s
    """, (tech, score, datetime.datetime.now(), uname, mobile))
    percentage = (score / len(questions)) * 100
    if percentage >= 80:
        remark = " Excellent!"
    elif percentage >= 50:
        remark = " Good Job!"
    else:
        remark = " Try Again!"

    print(f"\n Quiz Completed! Your Score: {score}/{len(questions)}")
    print(f"Percentage: {percentage:.2f}%")
    print(f" Remark: {remark}")
    # Save result to main users table
    cursor.execute("""
        UPDATE users SET technology = %s, score = %s, quiz_time = %s
        WHERE username = %s AND mobile_number = %s
    """, (tech, score, datetime.datetime.now(), uname, mobile))
    conn.commit()

    # Optional: Save to user_results table
    
    
    choice = input("\nDo you want to retake the quiz? (yes/no): ").lower()
    if choice == "yes":
        user_take_quiz(cursor, conn, uname, mobile)

    conn.commit()
def main_menu(cursor, conn):
    while True:
        print("\n=== QUIZ SYSTEM ===")
        print("1. Admin Login")
        print("2. User Login")
        print("3.Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            if admin_login(cursor):
                admin_menu(cursor, conn)

        elif choice == '2':
            uname, mobile = user_login_or_register(cursor, conn)
            if uname and mobile:
                user_take_quiz(cursor, conn, uname, mobile)
        elif choice=='3':
            print("exiting the quiz.")
            break

        else:
            print("Invalid choice.")

main_menu(cursor, db)

# After finishing
cursor.close()
db.close()


    
