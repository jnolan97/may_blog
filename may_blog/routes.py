from may_blog import app, db, Message, mail
from flask import render_template, request, redirect, url_for
from may_blog.forms import UserInfoForm, PostForm, LoginForm

from may_blog.models import User, Post, check_password_hash

from flask_login import login_required,login_user,current_user,logout_user


#Home Route
@app.route('/')
def home():
    # customer_name = 'Jack'
    # order_number = 1
    # item_dict = {1: "Ice cream", 2:"Bread",3:"Lemons",4:"Cereal"}
    posts = Post.query.all()
    return render_template("home.html",posts = posts)
#Register route
@app.route('/register', methods=['GET','POST'])
def register():
    form = UserInfoForm()
    if request.method == 'POST' and form.validate():
        # Get info
        username = form.username.data
        password = form.password.data
        email = form.email.data
        print("\n",username,password,email)
        #create instance of user
        user = User(username,email,password)
        # open and insert into db and then save info
        db.session.add(user)
        db.session.commit()
        #Flask Email Sender
        msg = Message(f'Thanks for Signing up! {email}', recipients=[email])
        msg.body =('Congrats on signing up! Looking forward to your posts!')
        msg.html = ('<h1> Welcome to May_Blog! </h1>' '<p> This will be fun! </p>')
        mail.send(msg)
    return render_template('register.html',form = form)
# Post Submission
@app.route('/posts',methods=['GET','POST'])
@login_required
def posts():
    post = PostForm()
    if request.method == 'POST' and post.validate():
        title = post.title.data
        content = post.content.data
        user_id = current_user.id
        print("\n",title,content)
        post = Post(title,content,user_id)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('posts'))
    return render_template('posts.html',post = post)

#Login Route
@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        email = form.email.data
        password = form.password.data
        logged_user = User.query.filter(User.email == email).first()
        if logged_user and check_password_hash(logged_user.password,password):
            login_user(logged_user)
            return redirect(url_for('home'))
        else:
            return redirect(url_for('login'))
    return render_template('login.html',form=form)

@app.route('/posts/<int:post_id>')
@login_required
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post_detail.html',post = post)

@app.route('/posts/update/<int:post_id>',methods = ['GET','POST'])
@login_required
def post_update(post_id):
    post = Post.query.get_or_404(post_id)
    update_form = PostForm()

    if request.method == 'POST' and update_form.validate():
        title = update_form.title.data
        content = update_form.content.data
        user_id = current_user.id 
        print(title,content,user_id)
        
        post.title = title
        post.content = content
        post.user_id = user_id
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('post_update.html',update_form = update_form)

@app.route('/posts/delete/<int:post_id>',methods = ['POST'])
@login_required
def post_delete(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))
