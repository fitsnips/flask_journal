from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect, json
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '3932l3k3k39923k49kdksks'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"



def open_journal(jfile):
    # open the file, create if not present
    data = []

    try:
        with open( jfile, 'r+' ) as input:
            data = json.load( input )
    except OSError:
        print( 'Unable to open file {}'.format( jfile ) )

    return data


def write_journal(data, jfile):
    # print(json.dumps(data, sort_keys=True, indent=4, default=str ))
    try:
        with open( jfile, 'w' ) as outfile:
            json.dump( data, outfile, sort_keys=True, indent=4, default=str )
    except OSError:
        print( 'Unable to open file {}'.format( jfile ) )


journal_file = './data/journal.json'

journal_data = open_journal(journal_file)




@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html',entries=journal_data)

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'hardcodedpasswordsforthewin':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


if __name__ == '__main__':
    app.run(debug=True)