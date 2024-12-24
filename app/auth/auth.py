from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user

from .forms import LoginForm, Newpassword, Userpass
from ..main import db
from ..models import User
import requests

auth_bp = Blueprint('auth', __name__, template_folder='templates', static_folder='static')


@auth_bp.route('/user_data', methods=['GET', 'POST'])
def user_data():
    if current_user.is_authenticated:
        return render_template('user_data.html', user=current_user)
    else:
        return redirect(url_for('error.not_found_error'))


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.username.data).first()
        print('*' * 20)
        print(user)
        if user is None or not user.check_password(form.pasword.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)

        return redirect(url_for('home.index'))
    return render_template('login_enter.html', form=form)


@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home.index'))


@auth_bp.route('/user_reg', methods=['GET', 'POST'])
def user_reg():
    form3 = LoginForm()
    if form3.validate_on_submit():
        print(form3)
        name = form3.username.data
        data = User(name=form3.username.data, is_active=False)
        data.set_password(form3.pasword.data)

        db.session.add(data)
        db.session.commit()
        flash('ПОЛЬЗОВАТЕЛЬ ' + name + ' ЗАРЕГИСТРИРОВАН')
        MONGO_APP_URL = f"http://flask_mongo:5001/add/{form3.username.data}/{form3.pasword.data}"
        response = requests.post(MONGO_APP_URL)

        return redirect(url_for('home.index'))
    return render_template('user_reg.html', form2=form3)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    upassform = Userpass()
    if upassform.validate_on_submit():
        user = User.query.filter_by(name=upassform.username.data).first()
        if user:
            return redirect(url_for('auth.recover_password'))
        else:
            flash('нет такого пользователя')
            return redirect(url_for('auth.user_reg'))

    return render_template('recover_password.html', upassform=upassform)



@auth_bp.route('/recover_password', methods=['GET', 'POST'])
def recover_password():
    newpassform = Newpassword()
    if newpassform.validate_on_submit():
        user = User.query.filter_by(name=newpassform.username.data).first()
        if user:
            user.password = newpassform.new_pass.data
            db.session.commit()
            return redirect(url_for('auth.login'))


    return render_template('refresh_pass.html', newpassform=newpassform)
