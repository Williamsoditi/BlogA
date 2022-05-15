from . import main
from flask import render_template,abort,redirect,url_for,request,flash
from flask_login import login_required,current_user
from ..models import User,Blog,Comment,Upvote,Downvote,Delete
from .. import db,photos
from .forms import UpdateProfile, BlogForm,CommentForm
from ..requests import get_quote

#Application views
@main.route('/')
def index():
    '''
    View root page function that returns the index page and its data
    '''
    title = 'BlogA'
    user = User.query.all()
    quotes = get_quote
    blogs = Blog.query.all()

    return render_template('index.html', blogs = blogs, quotes = quotes, user = user, title = title)