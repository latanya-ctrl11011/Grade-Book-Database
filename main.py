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
        category_id INTEGER,
        course_id INTEGER,
        category_name TEXT,
        weight INTEGER,
        PRIMARY KEY(category_id, course_id),
        FOREIGN KEY (course_id) REFERENCES Course(course_id)
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
    (3456, 'Ivy', 'Queen'),
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

c.executemany("INSERT INTO Category (category_id, course_id, category_name, weight) VALUES (?, ?, ?, ?)", [
    (1, 1, 'Participation', 10),
    (2, 1, 'Homework', 20),
    (3, 1, 'Test', 50),
    (4, 1, 'Project', 20),
    (1, 2, 'Participation', 15),
    (2, 2, 'Homework', 15),
    (3, 2, 'Test', 50),
    (4, 2, 'Project', 20),
    (1, 3, 'Participation', 10),
    (2, 3, 'Homework', 20),
    (3, 3, 'Test', 45),
    (4, 3, 'Project', 25),
    (1, 4, 'Participation', 10),
    (2, 4, 'Homework', 10),
    (3, 4, 'Test', 50),
    (4, 4, 'Project', 30),
    (1, 5, 'Participation', 10),
    (2, 5, 'Homework', 20),
    (3, 5, 'Test', 50),
    (4, 5, 'Project', 20)
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
    (3, 2345,  9, 92),
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
    (2, 4567,  5, 91),
    (2, 4567,  6, 69),
    (2, 4567,  7, 66),
    (2, 4567,  8, 67),
    (5, 4567,  17, 39),
    (5, 4567,  18, 73),
    (5, 4567,  19, 69),
    (5, 4567,  20, 92),
    (1, 5678,  1, 99),
    (1, 5678,  2, 43),
    (1, 5678,  3, 56),
    (1, 5678,  4, 68),
    (5, 5678,  9, 76),
    (5, 5678,  10, 62),
    (5, 5678,  11, 90),
    (5, 5678,  12, 90)
])

#print(computations.add_assignment(21, 2, 1))

c.execute("UPDATE Category SET weight = ? WHERE category_id = ? AND category_name = ?", (2, 'Homework', 20))
c.execute("UPDATE Grades SET score = score + 2 WHERE assignment_id = ?", (3,))
conn.commit()
print("Values added successfully.")




#run functions:
import computations
print("\nTASK 4")
average_score = computations.avg_score(7)
print("The average score for this assignment is ", average_score)

highest_score = computations.high_score(7)
print("The highest score for this assignment is ", highest_score)

lowest_score = computations.low_score(7)
print("The lowest score for this assignment is ", lowest_score)
print("\nTASK 5")
stu_in_bio = computations.students_in_bio(3)
print("Students in Bio 101 are ", stu_in_bio)
print("\nTASK 6")
stu_in_cs = computations.students_in_course(1)
print("The grades on each assignment for all students in CS 100 are ", stu_in_cs)

print("\nTASK 7")
#print(computations.add_assignment(21, 2, 1))

print("\nTASK 8")
print(computations.percent_change(1, 1, 20))
print(computations.percent_change(1, 2, 30))
print(computations.percent_change(1, 3, 10))
print(computations.percent_change(1, 4, 40))

print("\nTASK 9")
print(computations.score_update(3, 2))

print("\nTASK 10")
print(computations.score_updateQ(2, '%Q%'))

print("\nTASK 11")
print(computations.student_grade_1234(1234, 1))

print("\nTASK 12")
print(computations.student_grade_dropped(1234, 1, 2))

# Close the connection
conn.close()

