from flask import Flask, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange
from flask_behind_proxy import FlaskBehindProxy


app = Flask(__name__)
proxied = FlaskBehindProxy(app)
app.config['SECRET_KEY'] = '81ccd8c605028899b10031520988c053'

class SearchInput(FlaskForm):
    villagerID = IntegerField('Search ID',
                           validators=[DataRequired(), NumberRange(min=1, max=391)])

    submit = SubmitField('Search')

@app.route("/")
def gome():
    form = SearchInput()
    if form.validate_on_submit(): # checks if entries are valid
        flash(f'Data successfully retrieved for {form.villagerID.data}!')
    return render_template('home.html', title='Home Search', form=form)
    

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")