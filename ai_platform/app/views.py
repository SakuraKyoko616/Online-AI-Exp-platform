import os

from flask import render_template, redirect, session, request, url_for, make_response,jsonify
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
import requests,json
from app import app, db
from .models import School, Student, Teacher, Exp_Course, Experiment, Course, Class, Comment, platform_Manager

e = []
@app.route(('/'), methods=['GET', 'POST'])
def login():
    session['log'] = 'logout'
    if request.method == 'POST':
        if 'log_in' in request.form:
            ID = request.form['ID']
            pwd = request.form['password']
            s_check = Student.query.filter_by(student_ID=ID).first()
            t_check = Teacher.query.filter_by(teacher_ID=ID).first()

            if t_check:
                if t_check.password == pwd:
                        session['username'] = ID
                        session['log'] = 'login'
                        course_ID = Teacher.query.filter_by(teacher_ID=session['username']).first().course_ID
                        course = Course.query.filter_by(course_ID=course_ID).first()
                        exps = course.Exps
                        response = make_response(render_template('teacher_system.html', exps=exps, flag=0, username=ID))
                        response.set_cookie('username', ID)
                        return response
                else:
                    return render_template('index.html', flag=1)
            elif s_check:
                if s_check.password == pwd:
                        session['username'] = ID
                        session['log'] = 'login'
                        teacher_ID = Student.query.filter_by(student_ID=session['username']).first().teacher_ID
                        course_ID = Teacher.query.filter_by(teacher_ID=teacher_ID).first().course_ID
                        course = Course.query.filter_by(course_ID=course_ID).first()
                        exps = course.Exps
                        response = make_response(render_template('student_system.html', exps=exps, flag=0, username=ID))
                        response.set_cookie('username', ID)
                        return response
                else:
                    return render_template('index.html', flag=1)
            else:
                 return render_template('index.html', flag=1)

        if 'pm_log_in' in request.form:
            ID = request.form['pm_ID']
            pwd = request.form['pm_password']
            pm_check = platform_Manager.query.filter_by(pm_ID = ID).first()

            if not pm_check:
                return render_template('index.html', flag=1)
            if pm_check.password == pwd:
                session['username'] = ID
                session['log'] = 'login'
                teachers = Teacher.query.all()
                response = make_response(render_template('pm_system.html', teachers=teachers, flag=0, username=ID))
                response.set_cookie('username', ID)
                return response
            else:
                return render_template('index.html', flag=1)
        return render_template('index.html')

@app.route('/change_pwd', methods=['GET', 'POST'])
def change_pwd():
    if session['log'] == 'login':
        if request.method == 'POST':
            pwd = request.form['Opwd']
            Npwd = request.form['Npwd']
            s_check = Student.query.filter_by(student_ID=session['username']).first()
            t_check = Teacher.query.filter_by(teacher_ID=session['username']).first()
            if t_check:
                if t_check.password == pwd:
                    t_check.password = Npwd
                    db.session.commit()
                    session['log'] = 'logout'

                    return redirect(url_for('login'))
                else:
                    return render_template('change_pwd.html', flag=1)
            elif s_check:
                if s_check.password == pwd:
                    s_check.password = Npwd
                    db.session.commit()
                    session['log'] = 'logout'

                    return redirect(url_for('login'))
                else:
                    return render_template('change_pwd.html', flag=1)
        return render_template('change_pwd.html')
    return render_template('index.html', flag=5)

@app.route('/stu_exps', methods=['GET', 'POST'])
def stu_exps():
        temp = []
        teacher_ID = Student.query.filter_by(student_ID=session['username']).first().teacher_ID
        course_ID = Teacher.query.filter_by(teacher_ID=teacher_ID).first().course_ID
        course = Course.query.filter_by(course_ID=course_ID).first()
        # if request.method == 'POST':
        #     search = request.form['search']
        #     if search:
        #         exps = course.Exps
        #         for exp in exps:
        #             if search in exp.exp_Name:
        #                 temp.append(exp)
        #     return render_template('student_system.html', exps=temp, username=session['username'])
        exps = course.Exps
        return render_template('student_system.html', exps=exps, username=session['username'])

@app.route('/teacher_list', methods=['GET', 'POST'])
def teacher_list():
        teachers = Teacher.query.all()
        return render_template('pm_system.html', teachers=teachers, username=session['username'])

@app.route('/teacher_exps', methods=['GET', 'POST'])
def teacher_exps():
    if session['log'] == 'login':
        temp = []
        course_ID = Teacher.query.filter_by(teacher_ID=session['username']).first().course_ID
        course = Course.query.filter_by(course_ID=course_ID).first()
        # if request.method == 'POST':
        #     search = request.form['search']
        #     if search:
        #         exps = course.Exps
        #         for exp in exps:
        #             if search in exp.exp_Name:
        #                 temp.append(exp)
        #     return render_template('teacher_system.html', exps=temp, username=session['username'])
        exps = course.Exps
        return render_template('teacher_system.html', exps=exps, username=session['username'])
    else:
        return render_template('index.html', flag=5)


@app.route('/logout/')
def log_out():
    session['log'] = 'logout'
    session.pop('username')
    return redirect(url_for('login'))

@app.route('/delete/<exp_ID>')
def delete_Exp(exp_ID):
    course_ID = Teacher.query.filter_by(teacher_ID=session['username']).first().course_ID
    course = Course.query.filter_by(course_ID=course_ID).first()
    exps = course.Exps
    for exp in exps:
        if str(exp.exp_ID) == str(exp_ID):
            exps.remove(exp)
            db.session.delete(exp)
            db.session.commit()
    return redirect(url_for('teacher_exps'))

@app.route('/student_list')
def student_list():
    if session['log'] == 'login':
        student_list = Student.query.filter_by(teacher_ID=session['username']).all()
        return render_template('check_students.html', students=student_list,username=session['username'])
    return render_template('index.html', flag=5)

@app.route('/comment/<exp_ID>', methods=['GET', 'POST'])
def comment(exp_ID):
    if session['log'] == 'login':
        if request.method == 'POST':
            stu_comment = request.form['comment']
            new_comment = Comment(comment = stu_comment, student_ID= session['username'], exp_ID=exp_ID)
            db.session.add(new_comment)
            db.session.commit()
            return redirect(url_for('stu_exps'))
        return render_template('comment_on_EXPs.html',username=session['username'])
    return render_template('index.html', flag=5)

@app.route('/check_comment')
def check_comment():
    if session['log'] == 'login':
        comments = []
        students = Student.query.filter_by(teacher_ID=session['username']).all()
        temps = Comment.query.all()
        for temp in temps:
            for student in students:
                if temp.student_ID == student.student_ID:
                    comments.append(temp)
        return render_template('check_comments.html', comments = comments,username=session['username'])
    return render_template('index.html', flag=5)

@app.route('/add_exp', methods=['POST', 'GET'])
def add_exp():
    if request.method == 'POST':
        f = request.files['file']
        exp_Name = request.form['exp_Name']
        time_Limit = request.form['time_Limit']
        basepath = '/home/kyokoz/data/' + str(exp_Name)
        new_exp = Experiment(exp_Name = exp_Name, timeLimit = time_Limit)
        if not os.path.exists(basepath):
            os.makedirs(basepath)
        upload_path = os.path.join(basepath,secure_filename(f.filename))
        f.save(upload_path)
        db.session.add(new_exp)
        course_ID = Teacher.query.filter_by(teacher_ID=session['username']).first().course_ID
        course = Course.query.filter_by(course_ID=course_ID).first()
        exp = Experiment.query.filter_by(exp_Name = exp_Name).first()
        exps = course.Exps
        exps.append(exp)
        db.session.commit()
        return render_template('teacher_system.html', exps=exps, username=session['username'])
    return render_template('add_experiment.html')

@app.route('/start/<exp_Name>')
def start(exp_Name):
    if exp_Name == "ML:CNN_recognize_hand_writing_numbers":
        req = requests.get('http://localhost:8080/api/v1/namespaces/default/pods/ml/log').text
        temp = json.dumps(req)
        print(temp[(temp.find('http://ml:8888/?token=') + 22):temp.find('http://ml:8888/?token=') + 70])
        token = temp[(temp.find('http://ml:8888/?token=') + 22):temp.find('http://ml:8888/?token=') + 70]
        return redirect("http://192.168.100.101:10000/?token="+token)
    elif exp_Name == "NLP:CHN_ENG_translation":
        req = requests.get('http://localhost:8080/api/v1/namespaces/default/pods/nlp/log').text
        temp = json.dumps(req)
        print(temp[(temp.find('http://nlp:8888/?token=') + 23):temp.find('http://nlp:8888/?token=') + 71])
        token = temp[(temp.find('http://nlp:8888/?token=') + 23):temp.find('http://nlp:8888/?token=') + 71]
        return redirect("http://192.168.100.101:10001/?token="+token)
    else:
        req = requests.get('http://localhost:8080/api/v1/namespaces/default/pods/test/log').text
        temp = json.dumps(req)
        print(temp[(temp.find('http://test:8888/?token=') + 24):temp.find('http://test:8888/?token=') + 72])
        token = temp[(temp.find('http://test:8888/?token=') + 24):temp.find('http://test:8888/?token=') + 72]
        return redirect("http://192.168.100.101:10002/?token=" + token)

@app.route('/to_dashboard')
def to_dashboard():
    return redirect('http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/')