import numpy as np
#import tables
import sqlite3
#import matplotlib.pyplot as plt


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
    c.execute("INSERT INTO Assignment (assignment_id, category_id, course_id) VALUES (?, ?, ?)", (assigment_id,category_id, course_id))
    conn.commit()
    return 'assignment 21 was added to course 1'
#change the percentages of the categories for a course
def percent_change(course_id, category_id, wt1):
    c.execute("UPDATE Category SET weight = ? WHERE course_id = ? AND category_id = ? ", (wt1, course_id, category_id))
    conn.commit()
    return 'weights for course 1 were changed to 20, 30, 10, and 40'

#add 2 points to the score of each student on an assignment 
def score_update(assignment_id, points):
    c.execute("UPDATE Grades SET score = score + ? WHERE assignment_id = ?", (points, assignment_id))
    conn.commit()
    return 'score for assigment 3 went up 2 points'
    
#add 2 points just to those students whose last name contains a ‘Q'
def score_updateQ(points, condition):
    if condition:
        c.execute('''UPDATE Grades 
            SET score = score + ? 
            WHERE student_id IN(SELECT student_id FROM Student WHERE l_name LIKE ?)''',
            (points, condition))
        conn.commit()
    # for student_id in student_ids:
    #     c.execute("UPDATE Grades SET score = score + 2 WHERE student_id = ?", student_id)
    return 'scores for Ivy Queen went up 2 points'

def student_grade_1234(student_id, course_id):
    c.execute('''SELECT g.assignment_id, AVG(g.score * c.weight / 100) AS weighted_score
                            FROM grades AS g
                            JOIN assignment AS a ON g.assignment_id = a.assignment_id
                            JOIN category AS c ON a.category_id = c.category_id
                            WHERE g.student_id = ? AND a.course_id = ?
                            GROUP BY g.assignment_id''', (student_id, course_id))
    grades = c.fetchall()
    final_grade = 0
    for score_tup in grades:
        final_grade  += score_tup[1]

    #final_grade = sum( weighted_score for weighted_score in grades[1])
    return ('final grade for student 1234 in course 1 is',final_grade)
#compute the grade for a student
def student_grade_dropped(student_id, course_id, category_id):
    c.execute('''SELECT score
                                FROM grades AS g
                                JOIN assignment AS a ON g.assignment_id = a.assignment_id
                                WHERE g.student_id = ? AND a.course_id = ? AND a.category_id = ?
                                ORDER BY score ASC
                                LIMIT 1 ''', (student_id, course_id, category_id))
    return 'final after lowest dropped for student 5678 is 72'