import random
import datetime

from flask import Flask, render_template, request, redirect
from pyexpat.errors import messages

from config import KEY_CSRF
from loginform import LoginForm
from registrationform import RegistrationForm
from data import db_session
from data.users import User
from data.jobs import Jobs
from flask_login import LoginManager, login_user, logout_user

app = Flask(__name__)
app.config['SECRET_KEY'] = KEY_CSRF

login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/')
def index():
    return render_template("index.html", username="Иванов", title="Миссия колонизации Марса")


temp = ""


@app.route('/registration_wtf', methods=['POST', 'GET'])
def registration_wtf():
    form = LoginForm()
    if form.validate_on_submit():
        temp = form
        return redirect('/success')
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/success')
def success():
    return render_template("success.html", form=temp)


@app.route('/registration', methods=['POST', 'GET'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template("registration.html", form=form, message="Такой пользователь уже существует!")
        user = User(name=form.name.data, email=form.email.data)

        user.set_password(form.password.data)

        session.add(user)
        session.commit()
        return redirect("/login")
    return render_template("registration.html", form=form)


list_profession = ["капитан", "пилот", "строитель", "врач"]


@app.route('/list_prof/<num>')
def list_prof(num):
    return render_template("list_prof.html", list_prof=list_profession, op=num)


@app.route('/logout')
def logout():
    logout_user()
    return redirect("/base")


@app.route('/training/<prof>')
def training(prof):
    if "инженер" in prof:
        return render_template("training.html", title2="Инженерные тренажеры", title="Миссия колонизации")
    return render_template("training.html", title2="Научные симуляторы", title="Миссия колонизации")


@app.route('/astronaut_selection')
def astronaut_selection():
    with open("templates/ttt.txt", encoding="utf-8") as file:
        return file.read()

    return render_template('index.html')


@app.route('/promotion')
def promotion():
    return "Человечество вырастает из детства.<br>Человечеству мала одна планета.<br>Мы сделаем обитаемыми безжизненные пока планеты.<br>И начнем с Марса!<br>Присоединяйся!"


@app.route('/image_mars')
def image_mars():
    return '''<html><title>Привет, Марс!</title><h1>Жди нас, Марс!</h1><img src="static/Images/mars.png" alt="Mars surface" width=500 height=500><br><br>Вот она красная планета!</html>'''


@app.route('/log_jobs')
def log_jobs():
    session = db_session.create_session()
    jobs = session.query(Jobs).all()
    print(len(jobs))
    return render_template('log_jobs.html', jobs=jobs)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


def init():
    session = db_session.create_session()
    job = Jobs()
    job.team_leader = 1
    job.work_size = 125
    job.collaborators = '15, 5'
    job.start_date = datetime.datetime.now()
    job.end_date = datetime.datetime.now()
    job.job = "решаем!!!"
    session.add(job)
    session.commit()


if __name__ == '__main__':
    db_session.global_init("db/mars_explorer.db")
    app.run(port=8080, host='127.0.0.1')
