from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo



#validation of forms
class SearchWeather(FlaskForm):
    city_name = StringField('City Name',
                            validators=[DataRequired(), Length(min=3, max=30)])
    search_submit = SubmitField('Search')
    save_submit = SubmitField('Save')

class EvaluationWeather(FlaskForm):
    eval_submit = SubmitField('Evaluate')
    select_city = SelectField('Select City')
    city_submit = SubmitField('Selected')
    current_day=''
    record_day =''
    recorded_day = SelectField('Select Recorded Day')



class RecordWeather(FlaskForm):
    select_src_id = SelectField('Select Search ID')
    rec_submit = SubmitField('Selected')




class RegisterForm(FlaskForm):
    first_name = StringField('First Name',
                             validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last Name',
                            validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email Address',
                        validators=[DataRequired(), Length(min=2, max=30), Email()])

    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=6, max=15)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), Length(min=6, max=15), EqualTo('password')])

    submit = SubmitField('Sign Up')

    # method to check digit in username
    def user_validation(self):
        if len([x for x in self.first_name.data if x.isdigit()]) > 0:
            return 1
        if len([x for x in self.last_name.data if x.isdigit()]) > 0:
            return 2


class LoginForm(FlaskForm):
    email = StringField('Email Address',
                        validators=[DataRequired(), Length(min=2, max=30), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=6, max=15)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')


