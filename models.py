import pandas as pd
import weathereval.db_connector as db_conn
import weathereval.json_decoder as jsd
import json
from weathereval import login_manager
from flask_login import UserMixin
from datetime import datetime, timedelta
import requests
import bs4



#api_key = 'BR32A7TJWPYSM2WPMJT945QFT'
api_key = 'RFL6U9LVLWTVSQDP2MPLUSXQ9'
#api_key ='84PD9E38NYQBB4TWYVZWUGFD2'

@login_manager.user_loader
def user_loader(email):
    user = User()
    user.id = email
    return user

class User(UserMixin):
    id =''
    user_id = ''
    first_name = ''
    last_name = ''
    email_id = ''

    def create_user_account(self, user_df):
        flag = 0
        if db_conn.check_user(user_df.iloc[0]['email_id']):
            db_conn.create_new_user(user_df)
            flag = 1
        else:
            flag = 0
        return flag


class Weather():
    def __init__(self):
        self.user_id = 0
        self.api_key = api_key
        self.raw_json = None
        self.data = None

    def search_weather(self, city_name=''):
        # creating start_date and end_date for getting +2 -2 days weather details from
        # search date
        days_count = 2
        search_date = datetime.strptime(datetime.now().strftime('%Y-%m-%d'), '%Y-%m-%d')
        start_date = str(search_date + timedelta(days=-2)).split(' ')[0]
        end_date = str(search_date + timedelta(days=2)).split(' ')[0]
        try:
            api_link = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/' \
                       + city_name + '/' + start_date + '/' + end_date + '?unitGroup=metric&key=' + self.api_key +'&contentType=json'


            resp = requests.get(api_link)
            bst_time = requests.get('https://google.com/search?q=' + "best time to visit " + city_name)
            if resp.status_code == 200:
                self.raw_json = resp.json()

                soup = bs4.BeautifulSoup(bst_time.text, "html.parser")
                bst_time_data = soup.find("div", class_="BNeawe s3v9rd AP7Wnd").text

                #with open('curr_data.txt', 'w') as f:
                #    f.write(json.dumps(self.raw_json))

                # Decoding JSON data
                self.data = jsd.decode_raw_json(self.raw_json, self.user_id)

                # inserting record in history table for searched city
                db_conn.set_searched_history(self.data['search_city'])

                # returning decoded weather json data to home page
                city_data = self.data['search_city'][['city', 'address', 'timezone', 'tzoffset', 'description']]
                curr_data = self.data['current_weather']


                # getting data for past 2 and future 2 days
                daily_data = self.data['daily_weather']
                past_data = daily_data[daily_data['day_datetime'] < pd.to_datetime(search_date)]
                #past_data = daily_data[daily_data['day_datetime'] < pd.to_datetime('2022-12-16 00:00:00')]

                temp_min_max = daily_data[daily_data['day_datetime'] == pd.to_datetime(search_date)][
                    ['temp_min', 'temp_max']]

                future_data = daily_data[daily_data['day_datetime'] > pd.to_datetime(search_date)]
                #future_data = daily_data[daily_data['day_datetime'] > pd.to_datetime('2022-12-16 00:00:00')]


                graph_data = self.data['hourly_weather']
                graph_data_df = graph_data[graph_data['day_id'].str.match(str(search_date).split(' ')[0]+'_'+self.data['search_id'])]
                return 'Extracted', city_data,curr_data, graph_data_df, past_data, future_data, bst_time_data,temp_min_max
                
            else:
                return 'Failed'


            ################## for testing ###################
            '''
            with open('curr_data.txt', 'r') as fptr:
                self.raw_json = json.load(fptr)

            # Decoding JSON data
            self.data = jsd.decode_raw_json(self.raw_json, self.user_id)

            # inserting record in history table for searched city
            db_conn.set_searched_history(self.data['search_city'])

            # returning decoded weather json data to home page
            city_data = self.data['search_city'][['city', 'address','latitude','longitude','timezone','tzoffset', 'description']]
            curr_data = self.data['current_weather']
            
            # getting data for past 2 and future 2 days
            daily_data = self.data['daily_weather']
            #past_data = daily_data[daily_data['day_datetime'] < pd.to_datetime(search_date)]
            past_data = daily_data[daily_data['day_datetime'] < pd.to_datetime('2023-01-03 00:00:00')]

            #future_data = daily_data[daily_data['day_datetime'] > pd.to_datetime(search_date)]
            future_data = daily_data[daily_data['day_datetime'] > pd.to_datetime('2023-01-03 00:00:00')]

            graph_data = self.data['hourly_weather']
            #graph_data_df = graph_data[graph_data['day_id'].str.match(str(search_date).split(' ')[0]+'_'+self.data['search_id'])]
            graph_data_df = graph_data[graph_data['day_id'].str.match(str('2023-01-03').split(' ')[0]+'_'+self.data['search_id']) ]

            return 'Extracted', city_data,curr_data, graph_data_df, past_data, future_data

            #############################################################'''

        except Exception as e:
            print('Error in search_weather() method in Weather class', e)

    def record_weather(self):
        try:
            # Saving weather data into database for future comparison
            result = db_conn.load_weather_data(self.user_id,self.data['search_id'],self.data['search_city'], self.data['daily_weather'],
                                                     self.data['hourly_weather'], self.data['current_weather'])
            self.data = None
            return result

        except Exception as e:
            print('Error in recorded', e)

    def recored_days(self):
        try:
            print()


        except Exception as e:
            print('Error in recorded', e)


class Weather_Evaluation:
    def __init__(self, user_id ):
        self.user_id = user_id

    # to load weather data for evaluation page
    def load_recorded_daily_weather(self, city):
        data_dict = dict()
        data_dict['city'] = city
        rec_data_list = db_conn.get_recorded_daily_weather(self.user_id, city)
        data_dict['data'] = rec_data_list

        return data_dict






#s = Weather()
#s.user_id=1
#data = s.search_weather('Pune')
#s.data['hourly_weather'].to_csv('hrs.txt' )




#data['hourly_weather'].to_csv('hrd_2.txt')


#s = Weather_Evaluation(3)
#print(s.load_recorded_daily_weather('Pune')['data'][0]['curr_day'])




