from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:fS2mbWR@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = '2Xe$vHjVr1&G'


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    body = db.Column(db.String(1000))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50),unique=True)
    password = db.Column(db.String(50))
    blogs = db.relationship('Blog', backref='owner')


    def __init__(self, username, password):
        self.username = username 
        self.password = password
       
@app.route('/')
def index():
    return render_template('index.html', title="blog users!")

@app.before_request
def require_login():
    allowed routes = ['login','blog','index','signup']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method =='POST':
        username = request.form('username')
        password = request.form('password')
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            flash("Logged in")
            return redirect('/')
        else:
            flash('User password incorrect or user does not exist','error') 

@app.route('/signup', methods=['GET','POST'])
def signup():

    username = request.form['username'] 
    username_error = ''

    if len(username) < 3 or len(username) > 20:
        username_error = "Username must be between 3 and 20 characters"
    if ' ' in username:
        username_error = "Not a valid username"   

    password = request.form['password'] 
    password_error = ''
    verify = request.form['verify']
    verify_error = ''
    
    if len(password) < 3 or len(password) > 20:
        password_error = "Password must be between 3 and 20 characters"
        password = ''
    if ' ' in password:
        password_error = "Not a valid password"
        password = ''
    if verify != password or len(verify) == 0:
        verify_error = "Passwords do not match"
        verify = ''

    if not username_error and not password_error and not verify_error:
        return render_template('index.html')
    else:
        return render_template('index.html', username = username, username_error = username_error, password_error = password_error, verify_error = verify_error, email = email, email_error = email_error)




@app.route('/blog')
def blog():
    blogs = Blog.query.order_by(Blog.id.desc()).all()
    return render_template('blog.html',title="" blogs=blogs)

@app.route('/singleblog')
def single_blog():
    id = int(request.args.get('id'))
    blog = Blog.query.filter_by(id=id).first()
    return render_template('single_blog.html', title="", id=id, blog=blog)
    
     
@app.route('/newpost', methods=['GET', 'POST'])
def new_post():
    if request.method == 'GET':
        return render_template('new_post.html')

    if request.method == 'POST':
        blog_title = request.form['blog_title']
        blog_body = request.form['blog_body']
       
        title_error = ''
        blog_body_error = ''

        if blog_title == "":
            title_error = "Please enter a title for your blog"

        if blog_body == "":
            blog_body_error = "Please enter content for your blog"

        if blog_body_error or title_error:
            return render_template('new_post.html', blog_title=blog_title, blog_body=blog_body, title_error=title_error, blog_body_error=blog_body_error)
        else: 
            blog = Blog(blog_title, blog_body)
            db.session.add(blog)
            db.session.commit()
            return render_template('single_blog.html', blog=blog, blog_title=blog_title, blog_body=blog_body)    


if __name__ == '__main__':
    app.run()

