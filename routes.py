from flask import render_template, url_for, flash, redirect, request
import pandas as pd
from weathereval.db_connector import get_searched_history, check_login, get_cities, get_record_data
from weathereval import app
from weathereval.forms import RegisterForm, LoginForm, SearchWeather, EvaluationWeather ,RecordWeather
from weathereval.models import User, Weather, Weather_Evaluation
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime as dt
import plotly
import plotly.express as px
import json

logged_user = {'user_id': 0 , 'email_id': ''}
searched_city = ''
session_weather_obj = Weather()
mrs_list=['temp_max','temp_min','temp','feels_like','dew','humidity','precip','precip_prob','precip_cover','snow','snowd_depth','wind_gust','wind_speed','wind_dir','pressure','cloud_cover','visibility','solar_radiation','solar_energy','uv_index','severe_risk']

# login () function use to handle user login activity
@app.route("/", methods=['GET', 'POST'])
@app.route("/login", methods=['GET', 'POST'])
def login():
    global logged_user, session_weather_obj
    login_form = LoginForm()
    user = User()
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if login_form.validate_on_submit() and request.method == "POST":
        user_entry = check_login(login_form.email.data)
        if login_form.email.data in user_entry and login_form.password.data in user_entry:
            user.user_id = user_entry[0]
            user.first_name = user_entry[1]
            user.last_name = user_entry[2]
            user.email_id = user_entry[3]
            login_user(user)
            logged_user['user_id'] = user_entry[0]
            logged_user['email_id'] = user_entry[3]
            # setting user id in weather object
            session_weather_obj.user_id = user_entry[0]
            flash('You have been logged in !', category='success')

            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password !', category='danger')
    return render_template("login.html", form=login_form, title='Login')


@app.route("/register", methods=['GET', 'POST'])
def register():
    user_dict = {
        'first_name': str,
        'last_name': str,
        'email_id': str,
        'password': str
    }
    # created variable for Register form
    reg_form = RegisterForm()
    if reg_form.validate_on_submit():
        if reg_form.user_validation() == 1:
            flash('Digit is present in first name', category='danger')

        elif reg_form.user_validation() == 2:
            flash('Digit is present in last name', category='danger')
        else:
            user_dict['first_name'] = str(reg_form.first_name.data).capitalize()
            user_dict['last_name'] = str(reg_form.last_name.data).capitalize()
            user_dict['email_id'] = str(reg_form.email.data)
            user_dict['password'] = str(reg_form.password.data)
            flag = User().create_user_account(pd.DataFrame([user_dict]))
            if flag:
                flash('Your account has been created', category='success')
                return redirect(url_for('login'))
            else:
                flash('Email address already registered. Please choose a different one', category='danger')
    return render_template("register.html", form=reg_form, title='Register')


# home  function will display page for search weather activity
@app.route("/home", methods=['GET', 'POST'])
@login_required
def home():
    global searched_city, session_weather_obj, logged_user
    # Object for Webpage
    src_form = SearchWeather()

    # searching weather for city when user clicks search button
    if request.form.get('search_submit') == "Search":
        searched_city = str(src_form.city_name.data).strip().capitalize()

        # getting data from internet
        status,city_data,curr_data, graph_data, past_data, future_data, bst_time_data,temp_min_max = session_weather_obj.search_weather(
            str(src_form.city_name.data).strip().capitalize())

        if status == 'Extracted':
            graph_df = graph_data[['hour', 'temp']]
            fig = px.line(graph_df, x='hour', y='temp', markers=True, title='Current Hourly Temperature',
                      line_shape='spline')
            graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
            return render_template("home.html", form=src_form, title='Home',
                               city = city_data.to_records(index=False)[0],
                               curr_data = json.loads(curr_data.to_json(orient='records'))[0],
                               past_data = json.loads(past_data.to_json(orient='records')),
                               future_data = json.loads(future_data.to_json(orient='records')),
							   bst_time = bst_time_data,
                               temp_min_max=json.loads(temp_min_max.to_json(orient='records'))[0],
                               graph=graphJSON)
        else:
            flash('Free query limit exceeded !! Try after 24 hrs', category='danger')
            return render_template("home.html", form=src_form, title='Home', city='',
                                   curr_data='',
                                   past_data='',
                                   future_data='',
								   bst_time = '',
                                   temp_min_max='',
                                   graph='')

    # saving weather data when user clicks save button
    elif request.form.get('save_submit') == "Save":
        status = session_weather_obj.record_weather()
        if status[0] == 0:
            flash('Weather data recorded successfully !!', category='success')
        else:
            flash('Failed to record !!', category='danger')

        return render_template("home.html", form=src_form, title='Home', city='',
                               curr_data='',
                               past_data='',
                               future_data='',
							   bst_time = '',
                               temp_min_max='',
                               graph='')
    else:
        return render_template("home.html", form=src_form, title='Home', city = '',
                               curr_data = '',
                               past_data = '',
                               future_data = '',
							   bst_time = '',
                               temp_min_max='',
                               graph= '')


@app.route("/evaluation", methods=['GET', 'POST'])
@login_required
def evaluation():
    global logged_user , searched_city, mrs_list
    # object for webpage form
    eval_form = EvaluationWeather()
    session_eval_obj = Weather_Evaluation(logged_user['user_id'])
    cities = get_cities(logged_user['user_id'])
    eval_form.select_city.choices = cities

    # initial loading of data
    if cities !=None:
        data_dict = session_eval_obj.load_recorded_daily_weather(cities[0])
        eval_form.recorded_day.choices = data_dict['data'][4]['filter_day']
        eval_form.record_day = str(eval_form.recorded_day.choices[0])
        eval_form.current_day = str(dt.strptime(dt.now().strftime('%Y-%m-%d'), '%Y-%m-%d'))


        curr_df = data_dict['data'][1]
        rec_df = data_dict['data'][3]
        rec_df = rec_df[rec_df['day_datetime'] == eval_form.recorded_day.choices[0]]
        diff_df = rec_df[mrs_list]
        for col in mrs_list:
            diff_df[col] = float(curr_df[col].values[0]) - float(rec_df[col].values[0])

        graph_data = data_dict['data'][5]
        graph_data = graph_data[graph_data['day_datetime'].isin([str(eval_form.current_day).split(' ')[0], str(eval_form.recorded_day.choices[0]).split(' ')[0]])]
        graph_data['day_datetime'] = graph_data['day_datetime'].astype(str)
        graph_data.rename(columns={'day_datetime': 'Day', 'hour':'Hours' ,'temp':'Temp' }, inplace=True)

        fig = px.line(graph_data[['Hours', 'Temp', 'Day']], x='Hours', y='Temp', color='Day', markers=True, title='Hourly Temperature Comparison',
                      line_shape='spline')

        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        return render_template("evaluation.html", title='Evaluation',
                               form=eval_form,
                               city_name = cities[0],
                               curr_data=json.loads(curr_df.to_json(orient='records'))[0],
                               rec_data=json.loads(rec_df.to_json(orient='records'))[0],
                               diff_data=json.loads(diff_df.to_json(orient='records'))[0],
                               graph=graphJSON)

    '''if request.form.get('city_submit') == 'Selected':
        # getting data after city selected
        data_dict = session_eval_obj.load_recorded_daily_weather(eval_form.select_city.data)
        eval_form.recorded_day.choices = data_dict['data'][4]['filter_day']'''


    if request.form.get('eval_submit') == 'Evaluate':
        data_dict = session_eval_obj.load_recorded_daily_weather(eval_form.select_city.data)
        eval_form.recorded_day.choices = data_dict['data'][4]['filter_day']
        eval_form.record_day = str(eval_form.recorded_day.data)
        curr_df = data_dict['data'][1]
        rec_df  = data_dict['data'][3]
        rec_df  = rec_df[rec_df['day_datetime'] == eval_form.recorded_day.data]
        diff_df = rec_df[mrs_list]
        for col in mrs_list:
            diff_df[col] = float(curr_df[col].values[0]) - float(rec_df[col].values[0])

        graph_data = data_dict['data'][5]

        graph_data = graph_data[graph_data['day_datetime'].isin([str(eval_form.current_day).split(' ')[0], eval_form.recorded_day.data.split(' ')[0]])]
        graph_data['day_datetime'] = graph_data['day_datetime'].astype(str)
        graph_data.rename(columns={'day_datetime': 'Day', 'hour':'Hours' ,'temp':'Temp' }, inplace=True)

        fig = px.line(graph_data[['Hours', 'Temp', 'Day']], x='Hours', y='Temp', color='Day', markers=True, title='Hourly Temperature Comparison',
                      line_shape='spline')

        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return render_template("evaluation.html", title='Evaluation',
                               form=eval_form,
                               city_name = data_dict['data'][0]['search_id'][0].split('_')[2].capitalize(),
                               curr_data=json.loads(curr_df.to_json(orient='records'))[0],
                               rec_data=json.loads(rec_df.to_json(orient='records'))[0],
                               diff_data=json.loads(diff_df.to_json(orient='records'))[0],
                               graph=graphJSON)
    return render_template("evaluation.html", title='Evaluation',
                           form=eval_form,
                           city_name='',
                           curr_data='',
                           rec_data='',
                           diff_data='',
                           graph='')

@app.route("/record", methods=['GET', 'POST'])
@login_required
def record():
    rec_form = RecordWeather()
    data_dict = get_record_data(logged_user['user_id'])
    rec_form.select_src_id.choices = list(set(data_dict['search_id']))

    if request.form.get('rec_submit') == 'Selected':
        selected_data = data_dict[data_dict['search_id'] == rec_form.select_src_id.data]
        graph_data = selected_data[['day_datetime', 'hour', 'temp']]
        graph_data['day_datetime'] = graph_data['day_datetime'].astype(str)
        graph_data.rename(columns={'day_datetime': 'Day', 'hour': 'Hours', 'temp': 'Temp'}, inplace=True)

        fig = px.line(graph_data[['Hours', 'Temp', 'Day']], x='Hours', y='Temp', color='Day', markers=True,
                      title='Hourly Temperature Comparison',
                      line_shape='spline')

        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        data_dict = get_record_data(logged_user['user_id'])
        rec_form.select_src_id.choices = list(set(data_dict['search_id']))
        return render_template("record.html", form=rec_form, graph=graphJSON,title='Records')

    return render_template("record.html", form=rec_form, title='Record')


@app.route("/history" ,methods=['GET', 'POST'])
@login_required
def history():
    src_hist = get_searched_history(logged_user['user_id'])
    if len(src_hist) >0 :
        return render_template("history.html", hist=src_hist.to_records(index=False), title='History')
    return render_template("history.html", hist='', title='History')


@app.route("/about")
@login_required
def about():
    return render_template("about.html", title='About')

@app.route("/place")
@login_required
def place():
    return render_template("place.html", title='Place')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
