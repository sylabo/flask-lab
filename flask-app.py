from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

# DEMO STUFF

@app.route('/')
def view_hello():
    return 'Hello World!'

@app.route('/demo-1')
def view_demo_1():
    return render_template('demo-1.html', name='Justin')

@app.route('/demo-2/<name>/')
def view_demo_2(name):
    return render_template('demo-1.html', name=name)

@app.route('/demo-3')
def view_demo_3():
    names = ['Alice', 'Bob', 'Charlie', 'Eva']
    return render_template('demo-3.html', salutation='Roll call', names=names)

# STUDENT DIRECTORY APP

class Student:
    def __init__(self, first_name, last_name, username, majors, advisor):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.majors = majors
        self.advisor = advisor

def get_data():
    students = []
    with open('students.csv') as fd:
        for line in fd.read().splitlines():
            name, username, majors, advisor = line.split('\t')
            last_name, first_name = name.split(', ')
            students.append(Student(first_name, last_name, username, majors, advisor))
    return sorted(students, key=(lambda s: s.username))

@app.route('/directory')
def view_directory():
    student_list = get_data()
    return render_template('directory.html', salutation='Student Directory',students=student_list)

@app.route('/directory/<username>')
def view_student(username):
    student_list = get_data()

    index = 0

    for student in student_list:
        if username == student.username:
            current_student = student

            if student_list.index(student) == 0:
                prev_student = student_list[len(student_list) - 1]
                next_student = student_list[1]
            elif student_list.index(student) == len(student_list) - 1:
                prev_student = student_list[student_list.index(student) - 1]
                next_student = student_list[0]
            else:
                prev_student = student_list[student_list.index(student) - 1]
                next_student = student_list[student_list.index(student) + 1]
    return render_template('student.html',student=current_student, prev_student=prev_student, next_student=next_student)

# DON'T TOUCH THE CODE BELOW THIS LINE

@app.route('/css/<file>')
def view_css(file):
    return send_from_directory('css', file)

if __name__ == '__main__':
    #print(get_data())
    app.run(debug=True)
