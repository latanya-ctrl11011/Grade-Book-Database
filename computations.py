import numpy as np
import tables
import sqlite3
import matplotlib.pyplot as plt


conn = sqlite3.connect('tables.db')
c = conn.cursor()
    
def avg_score(assignment_id):
    c.execute("SELECT AVG(score) AS average_score FROM Grades WHERE assignment_id = ?",  (assignment_id,))
    average_score = c.fetchone()[0]
    return average_score
    
def high_score(assignment_id):
    c.execute("SELECT MAX(score) AS highest_score FROM Grades WHERE assignment_id = ?",  (assignment_id,))
    highest_score = c.fetchone()[0]
    return highest_score
    
def low_score(assignment_id):
    c.execute("SELECT MIN(score) AS lowest_score FROM Grades WHERE assignment_id = ?",  (assignment_id,))
    lowest_score = c.fetchone()[0]
    return lowest_score
    
def students_in_bio(course_id):
    c.execute("""
        SELECT s.*
        FROM Student s
        JOIN Roster r ON s.student_id = r.student_id
        WHERE r.course_id = ?
    """, (course_id,))
    student_data = c.fetchall()
    rtn = ''
    for arr in student_data:
        rtn+=arr[1]
        rtn+=' '
        rtn+=arr[2]
        rtn+=', '
    return rtn
 
def students_in_course(course_id):
    c.execute("""
        SELECT Student.f_name, Student.l_name, Student.student_id, Assignment.assignment_id, Grades.score
        FROM Grades 
        INNER JOIN student ON grades.student_id = student.student_id 
        INNER JOIN assignment ON grades.assignment_id = assignment.assignment_id
        WHERE Grades.course_id = ?
    """, (course_id,))
    students = c.fetchall()
    return students
    
# add an assignment to a course
def add_assignment(assigment_id,category_id, course_id):
    c.execute("INSERT INTO Assignment (assignment_id, category_id, course_id) VALUES (?, ?, ?)", (21, 2, 1))
    c.fetchall()
# change the percentages of the categories for a course
def percent_change():
    c.execute("UPDATE Assignment SET percentage = ? WHERE category = ? AND course_id = ?", (30.0, 'Homework', 1))

# add 2 points to the score of each student on an assignment 
def score_update():
    c.execute("UPDATE Grades SET score = score + 2 WHERE assignment_id = ?", (3,))
    
# add 2 points just to those students whose last name contains a ‘Q'
def score_updateQ():
    for student_id in student_ids:
        c.execute("UPDATE Grades SET score = score + 2 WHERE student_id = ?", student_id)

# compute the grade for a student
def student_grade():
    c.execute("""
        SELECT s.f_name, s.l_name, SUM(a.percentage * g.score / 100) AS grade
        FROM Student s
        JOIN Grades g ON s.student_id = g.student_id
        JOIN Assignment a ON g.assignment_id = a.assignment_id
        WHERE s.student_id = ?
        GROUP BY s.f_name, s.l_name
    """)
    result = c.fetchall()
    return result
    
# compute the grade for a student, where the lowest score for a given category is dropped
def student_grade_lowest_dropped():
    c.execute("""
        SELECT s.first_name, s.last_name, SUM(a.percentage * (g.score - MIN(g.score)) / 100) AS grade
        FROM Student s
        JOIN Grades g ON s.student_id = g.student_id
        JOIN Assignment a ON g.assignment_id = a.assignment_id
        GROUP BY s.first_name, s.last_name
        HAVING s.student_id = 2;
    """)

# conn.close()
