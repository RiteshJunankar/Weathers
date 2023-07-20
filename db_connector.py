from typing import Union, Any

import weathereval.json_decoder as jsd
import pyodbc
import json
import pandas as pd
import warnings

warnings.filterwarnings('ignore')
#use to connect the database

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=DESKTOP-8VH721P\SQLEXPRESS;'
                      'Database=Weather_Eval_DB;'
                      'Trusted_Connection=yes;')

cursor = conn.cursor()

def create_new_user(user_df):
    try:
        cursor = conn.cursor()
        insert_sql = "Insert into user_accounts(" + ",".join([str(col) for col in list(user_df.columns)]) + \
                     ") values (?,?,?,?)"
        cursor.execute(insert_sql, tuple(user_df.values[0]))
        print('Account created !!')
        cursor.commit()
        cursor.close()
    except Exception as e:
        print('Error in create_new_user()', str(e))


def check_user(email):
    global cursor
    try:
        flag = True
        cursor = conn.cursor()
        select_sql = "Select email_id from user_accounts where email_id  = '" + email + "'"
        cursor.execute(select_sql)
        if len(cursor.fetchall()) > 0:
            flag = False
            raise Exception('Email Id already registered')
        return flag
    except Exception as e:
        print(e)
    finally:
        cursor.close()


def check_login(email):
    try:
        select_sql = "Select user_id, first_name, last_name ,email_id, password from user_accounts where email_id  like '" + email + "'"
        row_df = pd.read_sql(select_sql, conn)
        return list(row_df.iloc[0])
    except Exception as e:
        print(e)


def get_user_id(email):
    try:
        select_sql = "Select user_id from user_accounts where email_id  like '" + email + "'"
        row_df = pd.read_sql(select_sql, conn)
        return list(row_df.iloc[0])
    except Exception as e:
        print(e)

def truncate_old_records(uid, src_id):
    cursor = conn.cursor()
    try:
        # cleanup for duplicate searches
        select_sql ="select top 1 search_id from search_weather where user_id = " + str(uid) + \
                    " and SUBSTRING(search_id, 0,11) = '" + src_id.split('_')[0] + \
                    "' and search_id like '%" + src_id.split('_')[2] +"'order by created_datetime desc"

        old_src_id =  tuple(pd.read_sql(select_sql, conn)['search_id'])
        if len(old_src_id)>0:
            sql_4 = "delete from current_weather where search_id = '" + old_src_id[0] + "'"
            sql_3 = "delete from hourly_weather where search_id = '" + old_src_id[0] + "'"
            sql_2 = "delete from daily_weather where search_id = '" + old_src_id[0] + "'"
            sql_1 = "delete from search_weather where search_id = '" + old_src_id[0] + "'"
            cursor.execute(sql_4)
            cursor.execute(sql_2)
            cursor.execute(sql_1)
            cursor.execute(sql_3)
            cursor.commit()

    except Exception as e:
        cursor.rollback()
        print('Error in truncate_old_records :' , e)
    finally:
        cursor.close()

def load_search_weather(search_weather_df):
    cursor = conn.cursor()
    try:
        # loading search city data
        insert_sql = "Insert into search_weather (" + ",".join(
            [str(col) for col in jsd.raw_search_weather_dict.keys()]) + \
                 ") values (?,?,?,?,?,?,?,?,?)"
        cursor.execute(insert_sql, tuple(search_weather_df.values[0]))
        cursor.commit()
    except Exception as e:
        cursor.rollback()
        print('Error in load_search_weather : ',e)
    finally:
        cursor.close()

def load_daily_weather(daily_weather_df):
    cursor = conn.cursor()
    try:
        # loading daily weather data
        insert_sql = "Insert into daily_weather (" + ",".join([str(col) for col in jsd.daily_weather_schema.keys()]) + \
                     ") values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"

        for index, row in daily_weather_df.iterrows():
            cursor.execute(insert_sql, tuple(row.values))
        cursor.commit()
    except Exception as e:
        cursor.rollback()
        print('Error in load_daily_weather :',e)
    finally:
        cursor.close()

def load_hourly_weather(hourly_weather_df):
    cursor = conn.cursor()
    try:
        # loading hourly weather data
        insert_sql = "Insert into hourly_weather (" + ",".join([str(col) for col in jsd.hourly_weather_schema.keys()]) + \
                     ") values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"

        for index, row in hourly_weather_df.iterrows():
            cursor.execute(insert_sql, tuple(row.values))
        cursor.commit()

    except Exception as e:
        cursor.rollback()
        print('Error in load_hourly_weather :',e)
    finally:
        cursor.close()

def load_current_weather(curr_weather_df):
    cursor = conn.cursor()
    try:
        # loading current weather data
        insert_sql = "Insert into current_weather (" + ",".join([str(col) for col in jsd.curr_weather_schema.keys()]) + \
                     ") values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"

        for index, row in curr_weather_df.iterrows():
            cursor.execute(insert_sql, tuple(row.values))
        cursor.commit()

    except Exception as e:
        cursor.rollback()
        print(e)
    finally:
        cursor.close()

def load_weather_data(uid, src_id ,search_weather_df, daily_weather_df, hourly_weather_df, curr_weather_df):
    try:
        truncate_old_records(uid, src_id)
        load_search_weather(search_weather_df)
        load_daily_weather(daily_weather_df)
        load_hourly_weather(hourly_weather_df)
        load_current_weather(curr_weather_df)

        return [0, 'Weather data recorded !!']

    except Exception as e:
        print('Error in DB_connector', e)
        return [1, 'Error in recording weather data !!']

def get_recorded_weather(user_id):
    try:
        get_sql = "select src.search_id as search_id, src.city as city_name, src.address as address, src.latitude as latitude,src.longitude as longitude, " \
                  "src.timezone as timezone, src.tzoffset as tzoffset, src.description as description, dlw.day_datetime as day_datetime, dlw.temp as curr_temp " \
                  "from search_weather src inner join daily_weather dlw " \
                  "on src.search_id= dlw.search_id " \
                  "where src.user_id= '" + user_id + "'"
        rows_df = pd.read_sql(get_sql, conn)
        if len(rows_df) != 0:
            return rows_df

    except Exception as e:
        print(e)


def set_searched_history(search_weather_df):
    try:
        cursor = conn.cursor()
        insert_sql = "Insert into search_history (search_id, user_id, city_name) " \
                     "values (?,?,?)"
        cursor.execute(insert_sql, tuple(search_weather_df[['search_id', 'user_id', 'city']].values[0]))
        cursor.commit()
    except Exception as e:
        print(e)


def get_searched_history(user_id):
    try:
        get_sql = "select usr.email_id as user_name ,upper(hist.city_name),hist.created_datetime from " \
                  "user_accounts usr  inner join search_history hist " \
                  "on usr.user_id = hist.user_id where usr.user_id like '" + str(user_id) + "'"
        rows_df = pd.read_sql(get_sql, conn, parse_dates=True)
        if len(rows_df) != 0:
            return rows_df
        else:
            return None

    except Exception as e:
        print(e)


# function to get recorded daily weather for evaluation page
def get_cities(user_id):
    try:
        get_sql = "select distinct city from search_weather where user_id like '" + str(user_id)+ "'"
        rows_df = pd.read_sql(get_sql, conn)
        if len(rows_df) != 0:
            return tuple(rows_df['city'])

    except Exception as e:
        print(e)


def get_recorded_daily_weather(user_id, city):
    try:
        data_list = []

        # Part-1 get data for current day
        curr_data_sql = "select distinct day_datetime as curr_day , dw.*  from search_weather sw inner join  daily_weather dw " \
                        "on sw.search_id = dw.search_id  inner join hourly_weather hrs on hrs.search_id = sw.search_id and hrs.day_id = dw.day_id    where " \
                        "dw.day_datetime = cast(getdate() as date) " \
                        "and sw.user_id like '" + str(user_id) + \
                        "' and sw.city like '" + city + "'"

        curr_data_df = pd.read_sql(curr_data_sql, conn, parse_dates=True)
        data_list.append(curr_data_df.to_dict(orient='list'))
        data_list.append(curr_data_df)

        # Part-2 get data for recorded days
        rec_data_sql = "select distinct day_datetime as  rec_day, dw.* from search_weather sw inner join  daily_weather dw " \
                       "on sw.search_id = dw.search_id inner join hourly_weather hrs on hrs.search_id = sw.search_id and hrs.day_id = dw.day_id where " \
                       "dw.day_datetime != cast(getdate() as date) " \
                       "and sw.user_id like '" + str(user_id) + \
                       "' and sw.city like '" + city + "'"

        rec_data_df = pd.read_sql(rec_data_sql, conn, parse_dates=True)
        data_list.append(rec_data_df.to_dict(orient='list'))
        data_list.append(rec_data_df)

        # sql query to load recorded field on evaluation page
        get_sql = "select distinct day_datetime as  filter_day from search_weather sw inner join  daily_weather dw " \
                  "on sw.search_id = dw.search_id  inner join hourly_weather hrs on hrs.search_id = sw.search_id and hrs.day_id = dw.day_id where dw.day_datetime != cast(getdate() as date) " \
                  "and sw.user_id like '" + str(user_id) + \
                  "' and sw.city like '" + city + "'"

        rec_days_filter_df = pd.read_sql(get_sql, conn, parse_dates=True)
        data_list.append(rec_days_filter_df.to_dict(orient='list'))


        # sql query for graph
        get_sql = "select distinct dw.day_datetime, hrs.temp , hrs.hour  from  search_weather sw inner join  daily_weather dw on sw.search_id = dw.search_id " \
                  "inner join hourly_weather hrs on hrs.search_id = sw.search_id " \
                  "and dw.day_id = hrs.day_id where sw.user_id like '" + str(user_id) + "' and sw.city like '" + city + "' order by hour asc"
        hourly_df = pd.read_sql(get_sql, conn, parse_dates=True)
        #data_list.append(rec_days_filter_df.to_dict(orient='list'))
        data_list.append(hourly_df)
        return data_list

    except Exception as e:
        print(e)


def get_record_data(user_id):
    try:
        get_sql = "select distinct sw.search_id, sw.city, dw.day_datetime, hw.hour, hw.temp  from search_weather sw inner join daily_weather dw  " \
                  "on sw.search_id = dw.search_id inner join hourly_weather hw " \
                  "on sw.search_id = hw.search_id and dw.day_id = hw.day_id" \
                  " where sw.user_id  like '"+str(user_id)+"'"
        rows_df = pd.read_sql(get_sql, conn)
        if len(rows_df) != 0:
            return rows_df

    except Exception as e:
        print(e)

#print(get_cities(1))

'''
s = get_recorded_daily_weather(1, 'Pune')
print(s[0]['search_id'][0].split('_')[2])
curr_df = s[1]
rec_df = s[3]
rec_df = rec_df[rec_df['day_datetime'] == '2023-01-18']

diff_df = rec_df[['temp_max','temp_min','temp','feels_like','dew','humidity','precip','precip_prob','precip_cover','snow','snowd_depth','wind_gust','wind_speed','wind_dir','pressure','cloud_cover','visibility','solar_radiation','solar_energy','uv_index','severe_risk']]

for col in mrs_list:
    diff_df[col] = float(curr_df[col]) - float(rec_df[col])
print(diff_df)'''