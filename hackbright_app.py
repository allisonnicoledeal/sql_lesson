import sqlite3

DB = None
CONN = None

import inspect

def get_num_args(fn):
    return len(inspect.getargspec(fn).args)

def get_student_by_github(github):
    query = """SELECT first_name, last_name, github FROM Students WHERE github = ?"""
    DB.execute(query, (github,))
    row = DB.fetchone()
    print """\
Student: %s %s
Github account: %s"""%(row[0], row[1], row[2])

def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("hackbright.db")
    DB = CONN.cursor()

def make_new_student(first_name, last_name, github):
    query = """INSERT into Students values (?,?,?)"""%first_name
    DB.execute(query, (first_name, last_name, github))
    CONN.commit()
    print "Successfully added student: %s %s"%(first_name, last_name)

def get_project_by_title(project_title):
    query = """SELECT title, description FROM Projects WHERE title = ?"""
    DB.execute(query, (project_title,))
    row = DB.fetchone()
    print "The project %s is: %s"%(row[0], row[1])

def make_new_project(title, description, max_grade):
    query = """INSERT into Projects values (?, ?, ?)"""
    DB.execute(query, (title, description, max_grade))
    CONN.commit()
    print "Successfully added project: %s"%(title)

def get_grade_by_project(title, github):
    print 'test'
    query = """SELECT first_name, grade, project_title FROM Students
            JOIN Grades on (github = student_github) 
            WHERE project_title = ? and github = ?"""
    DB.execute(query, (title, github))
    row = DB.fetchone()
   
    print "%s's grade is %d for their project: %s"%(row[0], row[1], row[2])

def make_grade_for_student(github, project_title, grade):
    query = """INSERT into Grades VALUES(?,?,?)"""
    DB.execute(query, (github, project_title, grade))
    CONN.commit
    print "Successfully added grade for %s on project: %s"%(github, project_title)

def show_grades(github):
    query = """SELECT first_name, last_name, project_title, grade FROM Students 
            JOIN Grades ON (github = student_github)
            WHERE github = ? """
    DB.execute(query, (github,))
    #results have multiple rows. Use fetchall instead of fetchone
    rows = DB.fetchall()

    for row in rows:
        print "%s %s's grade for %s: %d"%(row[0], row[1], row[2], row[3])

def main():
    connect_to_db()
    command = None
    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split('; ')
        command = tokens[0]
        args = tokens[1:]

        try:
            if command == "student":   
                get_student_by_github(*args) 
            elif command == "new_student":
                make_new_student(*args)
            elif command == "project":
                get_project_by_title(*args)
            elif command == "new_project":
                make_new_project(*args)
            elif command == "project_grade":
                get_grade_by_project(*args)
            elif command == "make_grade":
                make_grade_for_student(*args)
            elif command == "show_grades":
                show_grades(*args)
            else:
                print "Use an available command, with arguments separated by semi-colons: student, \n\
                    new_student, project, new_project, project_grade, make_grade"
        except TypeError, e:
            print "Error: wrong number of arguments to %s or entry not valid"%command
            print e
    CONN.close()

if __name__ == "__main__":
    main()
