import sqlite3

DB = None
CONN = None

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
    query = """INSERT into Students values (?, ?, ?)"""
    DB.execute(query, (first_name, last_name, github))
    CONN.commit()
    print "Successfully added student: %s %s" % (first_name, last_name)

def get_project_title(title): # query by project title
    query = """SELECT first_name, last_name, github 
        FROM Students 
        INNER JOIN Grades ON (Students.github = Grades.student_github)
        WHERE project_title = ?"""
    DB.execute(query, (title,))
    row = DB.fetchone()
    print """\
Student: %s %s
Github account: %s"""%(row[0], row[1], row[2])

def make_new_project(title, max_grade, description):
    query = """ INSERT INTO Projects (title, max_grade, description) VALUES (?, ?, ?)"""
    DB.execute(query, (title, max_grade, description))
    CONN.commit()
    print "Successfully added project: %s" % (title)

def get_grade(project_title):
    query = """SELECT first_name, last_name, Grades.grade
        FROM Students
        INNER JOIN Grades ON (Grades.student_github = Students.github)
        WHERE project_title =?"""
    DB.execute(query, (project_title,))
    row = DB.fetchone()
    print """\
Student: %s %s 
Grade: %d""" % (row[0],row[1],row[2])

def show_all_grades(student_github):
    query = """ SELECT * FROM Grades WHERE student_github = ?"""
    DB.execute(query, (student_github,))
    row = DB.fetchall()
    count = 0
    for index in row:
        print """ \
            Student Github: %s
            Project Name: %s
            Grade: %d""" % (row[count][0], row[count][1], row[count][2])
        count += 1
        

    

def give_grade(student_github, project_title, grade):
    query = """ INSERT INTO Grades (student_github, project_title, grade) VALUES (?, ?, ?)"""
    DB.execute(query, (student_github, project_title, grade))
    CONN.commit()
    print "Successfully added grade to: %s" % (project_title)

def main():
    connect_to_db()
    command = None
    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split()
        command = tokens[0]
        args = tokens[1:]

        if command == "student":
            get_student_by_github(*args) 
        elif command == "new_student":
            make_new_student(*args)
        elif command == "project_title":
            get_project_title(*args)
        elif command == "add_project":
            make_new_project(args[0], args[1], " ".join(args[2:]))
        elif command == "get_grade":
            get_grade(*args)
        elif command == "give_grade":
            give_grade(*args)
        elif command == "show_all_grades":
            show_all_grades(*args)
            

    CONN.close()

if __name__ == "__main__":
    main()
