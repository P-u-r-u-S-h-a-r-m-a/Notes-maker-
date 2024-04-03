from flask import Blueprint ,render_template, request,flash,redirect,url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user,login_required,logout_user,current_user
from website import views

auth=Blueprint('auth',__name__)

@auth.route('/login' ,methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        email=request.form.get('email')
        password=request.form.get('password')

        user=User.query.filter_by(email=email).first()
        if user:
           if check_password_hash(user.password, password):
                flash('login succesfull',category='success')
                login_user(user,remember=True)
                return redirect(url_for('views.home'))
           else:
               flash('check password',category='error')
        else:
            flash('user does not exist',category='error')


    return render_template("login.html",user=current_user)
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up',methods=['GET', 'POST'])
def signup():
    if request.method=='POST':
        email=request.form.get('email')
        firstname=request.form.get('firstname')
        password1=request.form.get('password1')
        password2=request.form.get('password2')
        user=User.query.filter_by(email=email).first()

        if user:
            flash('email already exist',category='error')
        elif len(email)<4:
            flash('Email must be greater than 4 characters' ,category='error')
        elif len(firstname)<1:
            flash('name must be greater than 2 characters' ,category='error')
        elif len(password1)<7:
            flash('Password too short' ,category='error')
        elif password1!=password2:
            flash('passwords dont\'t match' ,category='error')
        else:
            new_user=User(email=email,firstname=firstname,password=generate_password_hash(password1))
            db.session.add(new_user)
            db.session.commit()
            flash('Account created',category='success')
            login_user(new_user,remember=True)
            return redirect(url_for('views.home'))


    return render_template("sign-up.html",user=current_user)
