from flask import Flask, render_template, url_for, request, flash, session, redirect
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange
from flask_behind_proxy import FlaskBehindProxy
from flask_sqlalchemy import SQLAlchemy
import git


app = Flask(__name__)
proxied = FlaskBehindProxy(app)
app.config['SECRET_KEY'] = '81ccd8c605028899b10031520988c053'
app.config['SESSION_TYPE'] = 'filesystem'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class search(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  villagerID = db.Column(db.Integer, nullable=False)

  def __repr__(self):
    return f"search('{self.villagerID}')"

class SearchInput(FlaskForm):
    villagerID = IntegerField('Search ID',
                           validators=[DataRequired(), NumberRange(min=1, max=391)])

    submit = SubmitField('Search')

with app.app_context():
  db.create_all()

@app.route("/", methods=['GET', 'POST'])
def home():
    form = SearchInput()
    if form.validate_on_submit(): # checks if entries are valid
        new_search = search(villagerID=form.villagerID.data)
        db.session.add(new_search)
        db.session.commit()
        flash("success")
        return redirect(url_for('home'))
    return render_template('home.html', title='Home Search', form=form)

@app.route("/update_server", methods=['POST'])
def webhook():
    if request.method == 'POST':
        repo = git.Repo('/home/IzMo2000/flask_test')
        origin = repo.remotes.origin
        origin.pull()
        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400
    

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")