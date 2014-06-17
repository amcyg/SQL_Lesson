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
            #make_new_project(*args)

    CONN.close()

if __name__ == "__main__":
    main()
