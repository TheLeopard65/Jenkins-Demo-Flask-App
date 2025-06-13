from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, Length
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import bleach, os

app = Flask(__name__)
app.config.from_object('config.Config')
os.makedirs(os.path.join(app.root_path, 'instance'), exist_ok=True)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
load_dotenv()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

class UserForm(FlaskForm):
    name = StringField('Name', validators=[ DataRequired(), Length(max=80)])
    email = StringField('Email', validators=[ DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Password', validators=[ DataRequired(), Length(min=8, max=128) ])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = UserForm()
    if form.validate_on_submit():
        clean_name = bleach.clean(form.name.data)
        clean_email = bleach.clean(form.email.data)
        pw_hash = bcrypt.generate_password_hash(form.password.data).decode()
        user = User(name=clean_name, email=clean_email, password_hash=pw_hash)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('index'))
    users = User.query.all()
    return render_template('index.html', form=form, users=users)

@app.route('/delete/<int:id>')
def delete(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    user = User.query.get_or_404(id)
    form = UserForm(obj=user)
    if form.validate_on_submit():
        user.name = bleach.clean(form.name.data)
        user.email = bleach.clean(form.email.data)
        user.password_hash = bcrypt.generate_password_hash(form.password.data).decode()
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('update.html', form=form, user=user)

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=False)
