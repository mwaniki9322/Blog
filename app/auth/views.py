from flask import render_template,url_for,redirect
from . import auth
from .forms import RegistrationForm
from ..models import User
from .. import db

@auth.route('/login')
def login():
    return render_template('auth/login.html')

@auth.route('/register', methods = ["GET","POST"])
def register():
    form =RegistrationForm
    if form.validate_on_submit():
      user=User(form.email.data,form.username.data,form.password.data)
      db.session.add(user)
      db.session.commit()
      return redirect(url_for('auth.login'))
      title='New Account'
    return render_template('auth/register.html',registration_form = form)