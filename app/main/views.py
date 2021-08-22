from operator import pos
from ..models import Blog, User
from flask import render_template,abort,redirect,url_for
from .forms import BlogForm, UpdateProfile
from flask_login import login_required,current_user
from .. import db
from . import main


@main.route('/')
def index():
    '''
    view function for index page
    '''
    blogs=Blog.query.all()
    social=Blog.query.filter_by(category='Social Events').all()
    festival=Blog.query.filter_by(category='Festivals').all()
    concert=Blog.query.filter_by(category='Concerts').all()

    return render_template('index.html',social=social,festival=festival,concert=concert)


@main.route('/create_new',methods = ['POST','GET'])
def new_blog():
    form=BlogForm()
    if form.validate_on_submit():
        title=form.title.data
        post=form.post.data
        category=form.category.data
        user_id=current_user

        new_blog_object=Blog(post=post,user_id=current_user._get_current_object().id,category=category,title=title)

        new_blog_object.save_blog()
        return redirect(url_for('main.index'))



















@main.route('/user/<uname>')
def profile(uname):
    user=User.query.filter_by(username=uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)















@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)