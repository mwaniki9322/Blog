
from app.requests import get_quotes, repeat_get_quotes
from ..models import Blog, Comment, User,Upvote,Downvote,Quote
from flask import render_template,abort,redirect,url_for
from .forms import BlogForm, CommentForm, UpdateProfile
from flask_login import login_required,current_user
from .. import db
from . import main


@main.route('/')
@login_required
def index():
    '''
    view function for index page
    '''
   
    blogs=Blog.query.all()
    social=Blog.query.filter_by(category='Social').all()
    festival=Blog.query.filter_by(category='Festival').all()
    concert=Blog.query.filter_by(category='Concert').all()

    return render_template('index.html', social=social,festival=festival, blogs=blogs,concert=concert,quotes=quotes)

@main.route('/quotes')
@login_required
def quotes():
    '''
    view function for quotes
    '''
    quote= get_quotes
    quotes= repeat_get_quotes(10, get_quotes)

    return render_template('quotes.html',quotes=quotes)


@main.route('/create_new',methods = ['POST','GET'])
@login_required
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
    return render_template('create_blog.html', form = form)



@main.route('/comment/<int:blog_id>',methods =['POST','GET'])
@login_required
def comment(blog_id):
    form=CommentForm()
    blog=Blog.query.get(blog_id)
    all_comments= Comment.query.filter_by(blog_id=blog_id).all()

    if form.validate_on_submit():
        comment=form.comment.data
        blog_id=blog_id
        user_id=current_user._get_current_object().id
        new_comment=Comment(comment=comment,user_id=user_id,blog_id=blog_id)
        new_comment.save_comment()
        return redirect(url_for('.comment',blog_id=blog_id))
    return render_template('comment.html',form=form,blog=blog,all_comments=all_comments)


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


@main.route('/like/<int:id>',methods = ['POST','GET'])
@login_required
def like(id):
    get_blogs = Upvote.get_upvotes(id)
    valid_string = f'{current_user.id}:{id}'
    for blog in get_blogs:
        to_str = f'{blog}'
        print(valid_string+" "+to_str)
        if valid_string == to_str:
            return redirect(url_for('main.index',id=id))
        else:
            continue
    new_vote = Upvote(user = current_user, blog_id=id)
    new_vote.save()
    return redirect(url_for('main.index',id=id))

@main.route('/dislike/<int:id>',methods = ['POST','GET'])
@login_required
def dislike(id):
    blog = Downvote.get_downvotes(id)
    valid_string = f'{current_user.id}:{id}'
    for blo in blog:
        to_str = f'{blo}'
        print(valid_string+" "+to_str)
        if valid_string == to_str:
            return redirect(url_for('main.index',id=id))
        else:
            continue
    new_downvote = Downvote(user = current_user, blog_id=id)
    new_downvote.save()
    return redirect(url_for('main.index',id = id))