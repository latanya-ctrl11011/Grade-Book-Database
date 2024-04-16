import sqlite3
# Connect to SQLite database (create a new database if it doesn't exist)
conn = sqlite3.connect('tables.db')
c = conn.cursor()

# Execute SQL statements

# Create tables
c.execute("""DROP TABLE IF EXISTS Course""")
c.execute('''
    CREATE TABLE Course (
        course_id INTEGER PRIMARY KEY,
        department TEXT,
        course_number INTEGER,
        course_name TEXT,
        semester TEXT,
        year INTEGER
    )
''')

c.execute("""DROP TABLE IF EXISTS Student""")
c.execute('''
    CREATE TABLE Student (
        student_id INTEGER PRIMARY KEY,
        f_name TEXT,
        l_name TEXT
    )
''')
c.execute("""DROP TABLE IF EXISTS Category""")
c.execute('''
    CREATE TABLE Category (
        category_id INTEGER PRIMARY KEY,
        category_name TEXT,
        weight INTEGER
    )
''')

c.execute("""DROP TABLE IF EXISTS Assignment""")
c.execute('''
    CREATE TABLE Assignment (
        assignment_id INTEGER PRIMARY KEY,
        category_id INTEGER,
        course_id INTEGER,
        FOREIGN KEY (course_id) REFERENCES Course(course_id),
        FOREIGN KEY (category_id) REFERENCES Category(category_id)
    )
''')
c.execute('''
    CREATE TRIGGER enforce_category_id_constraint
        BEFORE INSERT ON Assignment
            FOR EACH ROW
                 WHEN NEW.category_id >= 5
                    BEGIN
                        SELECT RAISE(ABORT, 'category_id must be less than 5');
                    END;
''')

c.execute("""DROP TABLE IF EXISTS Grades""")
c.execute('''
    CREATE TABLE Grades (
        course_id INTEGER,
        student_id INTEGER,
        assignment_id INTEGER,
        score DECIMAL(5, 2),
        FOREIGN KEY (course_id) REFERENCES Student(course_id),
        FOREIGN KEY (student_id) REFERENCES Student(student_id),
        FOREIGN KEY (assignment_id) REFERENCES Assignment(assignment_id)
    )
''')

c.execute("""DROP TABLE IF EXISTS Roster""")
c.execute('''
    CREATE TABLE Roster (
        course_id INTEGER,
        student_id INTEGER,
        FOREIGN KEY (course_id) REFERENCES Student(course_id),
        FOREIGN KEY (student_id) REFERENCES Student(student_id)
    )
''')

# Commit the transaction
conn.commit()

print("Tables created successfully.")

# Insert values into tables 
c.executemany("INSERT INTO Course (course_id, department, course_number, course_name, semester, year) VALUES (?, ?, ?, ?, ?, ?)", [
    (1, 'Computer Science', 100, 'Intro to Computer Science', 'Fall', 2023),
    (2, 'Mathematics', 201, 'Calculus I', 'Spring', 2024),
    (3, 'Biology', 101, 'General Biology Lec/Lab', 'Fall', 2023),
    (4, 'Computer Science', 120, 'Explorations in Computer Science', 'Fall', 2023),
    (5, 'English', 103, 'Persuasive Writing & Research', 'Spring', 2024)
])

c.executemany("INSERT INTO Student (student_id, f_name, l_name) VALUES (?, ?, ?)", [
    (1234, 'Diana', 'Ekechukwu'),
    (2345, 'Latanya', 'KhissyBeyniouah'),
    (3456, 'Ivy', 'Lee'),
    (4567, 'Khendra', 'Phillips'),
    (5678, 'Imaan', 'Adam')
])

c.executemany("INSERT INTO Roster (course_id, student_id) VALUES (?, ?)", [
    (1, 1234),
    (1, 5678),
    (2, 1234),
    (2, 2345),
    (2, 4567),
    (3, 2345),
    (3, 3456),
    (4, 3456),
    (5, 4567),
    (5, 5678)
])

c.executemany("INSERT INTO Category (category_id, category_name, weight) VALUES (?, ?, ?)", [
    (1, 'Participation', 10),
    (2, 'Homework', 20),
    (3, 'Test', 50),
    (4, 'Project', 20)
])
c.executemany("INSERT INTO Assignment (assignment_id, category_id, course_id) VALUES (?, ?, ?)", [
    (1, 1, 1),
    (2, 2,  1),
    (3, 3,  1),
    (4, 4, 1),
    
    (5, 1, 2),
    (6, 2,  2),
    (7, 3,  2),
    (8, 4, 2),
    
    (9, 1, 3),
    (10, 2,  3),
    (11, 3, 3),
    (12, 4, 3),
    
    (13, 1, 3),
    (14, 2, 3),
    (15, 3, 3),
    (16, 4, 3),
    
    (17, 1, 4),
    (18, 2,  4),
    (19, 3,  4),
    (20, 4,4)
])

c.executemany("INSERT INTO Grades (course_id, student_id, assignment_id, score) VALUES (?, ?, ?, ?)", [
    (1, 1234,  1, 72),
    (1, 1234,  2, 48),
    (1, 1234,  3, 23),
    (1, 1234,  4, 70),
    (2, 1234,  5, 85),
    (2, 1234,  6, 67),
    (2, 1234,  7, 78),
    (2, 1234,  8, 28),
    (2, 2345,  5, 98),
    (2, 2345,  6, 39),
    (2, 2345,  7, 27),
    (2, 2345,  8, 90),
    (3, 2345,  9, 100),
    (3, 2345,  10, 92),
    (3, 2345,  11, 39),
    (3, 2345,  12, 50),
    (3, 3456,  9, 74),
    (3, 3456,  10, 99),
    (3, 3456,  11, 29),
    (3, 3456,  12, 30),
    (4, 3456,  13, 40),
    (4, 3456,  14, 40),
    (4, 3456,  15, 28),
    (4, 3456,  16, 30),
    (2, 4567,  5, 100),
    (2, 4567,  6, 69),
    (2, 4567,  7, 66),
    (2, 4567,  8, 67),
    (5, 4567,  17, 39),
    (5, 4567,  18, 73),
    (5, 4567,  19, 69),
    (5, 4567,  20, 100),
    (1, 5678,  1, 99),
    (1, 5678,  2, 43),
    (1, 5678,  3, 56),
    (1, 5678,  4, 68),
    (5, 5678,  9, 76),
    (5, 5678,  10, 62),
    (5, 5678,  11, 100),
    (5, 5678,  12, 100)
])
conn.commit()
print("Values added successfully.")

# # Write table contents to a file in a human-readable format
# with open("tables_data.txt", "w") as f:
#     # Query and write Course table data
#     f.write("Course Table:\n")
#     c.execute("SELECT * FROM Course")
#     for row in c.fetchall():
#         f.write(f"Course ID: {row[0]}, Department: {row[1]}, Course Number: {row[2]}, Course Name: {row[3]}, Semester: {row[4]}, Year: {row[5]}\n")
#     f.write("\n")
    
#     # Query and write Student table data
#     f.write("Student Table:\n")
#     c.execute("SELECT * FROM Student")
#     for row in c.fetchall():
#         f.write(f"Student ID: {row[0]}, First Name: {row[1]}, Last Name: {row[2]}, Course ID: {row[3]}\n")
#     f.write("\n")  
    
#     # Query and write Assignment table data
#     f.write("Assignment Table:\n")
#     c.execute("SELECT * FROM Assignment")
#     for row in c.fetchall():
#         f.write(f"Assignment ID: {row[0]}, Category: {row[1]}, Percentage: {row[2]}, Course ID: {row[3]}\n")
#     f.write("\n")
    
#     # Query and write Grades table data
#     f.write("Grades Table:\n")
#     c.execute("SELECT * FROM Grades")
#     for row in c.fetchall():
#         f.write(f"Grade ID: {row[0]}, Student ID: {row[1]}, Assignment ID: {row[2]}, Score: {row[3]}\n")
#     f.write("\n")

# print("Table data written to 'tables_data.txt' successfully.")



#run functions:
import computations

average_score = computations.avg_score(7)
print("The average score for this assignment is ", average_score)

highest_score = computations.high_score(7)
print("The highest score for this assignment is ", highest_score)

lowest_score = computations.low_score(7)
print("The lowest score for this assignment is ", lowest_score)

stu_in_bio = computations.students_in_bio(3)
print("Students in Bio 101 are ", stu_in_bio)

stu_in_cs = computations.students_in_course(1)
print("The grades on each assignment for all students in CS 100 are ", stu_in_cs)

computations.add_assignment(21,2,1)
# Commit the transaction

# Close the connection
conn.close()

