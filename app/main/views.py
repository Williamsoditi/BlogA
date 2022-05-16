from . import main
from flask import render_template,abort,redirect,url_for,request,flash
from flask_login import login_required
from ..models import User,Blog,Comment,Upvote,Downvote
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

    return render_template ('index.html',title=title,blogs=blogs,quotes=quotes,user=user)

@main.route('/user/<name>')
def profile(name):
    user = User.query.filter_by(username = name).first()

    if user is None:
        abort(404)
    else:
        return render_template('profile/profile.html', user = user)

@main.route('/user/<name>/update/pic',methods= ['POST'])
@login_required
def update_pic(name):
    user = User.query.filter_by(username = name).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.avatar = path
        db.session.commit()
    return redirect(url_for('main.profile',name = name))

@main.route('/user/<name>/update',methods = ['GET','POST'])
@login_required
def update_profile(name):
    user = User.query.filter_by(username = name).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',name = user.username))

    return render_template('profile/update.html',form =form)

@main.route('/create_new',methods = ['GET','POST'])
@login_required
def new_blog():
    form = BlogForm()

    if form.validate_on_submit():
        category = form.category.data
        context = form.context.data
        new_blog = Blog(category=category,context=context)
        
        db.session.add(new_blog)
        db.session.commit()
        return redirect(url_for('main.index'))
    else:
        all_blogs = Blog.query.order_by(Blog.posted)

    return render_template('blog.html',blog_form = form,blogs=all_blogs)

@main.route('/comment/<int:blog_id>', methods = ['POST','GET'])
def comment(blog_id):
    form = CommentForm()
    blog = Blog.query.get(blog_id)
    all_comments = Comment.query.filter_by(blog_id = blog_id).all()
    if form.validate_on_submit():
        comment = form.comment.data 
        blog_id = blog_id
        new_comment = Comment(comment=comment,blog_id = blog_id)
        db.session.add(new_comment)
        db.session.commit()
        return redirect(url_for('.comment', blog_id = blog_id))
    return render_template('comment.html',comment_form =form, blog = blog,all_comments=all_comments)

@main.route('/like/<int:id>', methods=['GET', 'POST'])
def like(id):
    blog = Blog.query.get(id)
    if blog is None:
        abort(404)
    like = Upvote.query.filter_by(blog_id=id).first()
    if like is not None:
        db.session.add(like)
        db.session.commit()
    new_like = Upvote(blog_id=id)
    db.session.add(new_like)
    db.session.commit()
    return redirect(url_for('main.index'))


@main.route('/dislike/<int:id>', methods=['GET', 'POST'])
def dislike(id):
    blog = Blog.query.get(id)
    if blog is None:
        abort(404)
    
    dislike = Downvote.query.filter_by(blog_id=id).first()
    
    if dislike is not None:   
        db.session.add(dislike)
        db.session.commit()

    new_dislike = Downvote(blog_id=id)
    db.session.add(new_dislike)
    db.session.commit()
    
    return redirect(url_for('main.index'))

@main.route('/delete_blog/<int:id>',methods = ['GET','POST'])
@login_required
def delete(id):
    blog= Blog.query.get(id)
    db.session.delete(blog)
    db.session.commit()

    return redirect(url_for('main.index'))

@main.route("/delete_comment/<int:id>")
@login_required
def delete_comment(id):
    comment = Comment.query.get(id)
    db.session.delete(comment)
    db.session.commit()

    return redirect(url_for('main.index'))

    