import pandas as pd
from datetime import datetime as dt

curr_search_id = ''

raw_search_weather_dict = {
'search_id': '',
    'city': '',
    'address': '',
    'latitude': 0,
    'longitude': 0,
    'timezone': '',
    'tzoffset': 0,
    'description': '',
    'user_id': 0
}


search_weather_schema = {
    'search_id': str,
    'city': str,
    'address': str,
    'latitude': float,
    'longitude': float,
    'timezone': str,
    'tzoffset': float,
    'description': str,
    'user_id': int
}


def search_weather_decode(key, value, user_id):
    try:

        src_id = str(dt.now().strftime('%Y-%m-%d_%H%M%S'))
        global curr_search_id

        if key == 'address' and len(value) > 0:
            raw_search_weather_dict['search_id'] = src_id + '_' + value.strip().upper().replace(' ', '_')
            raw_search_weather_dict['city'] = value
            curr_search_id = src_id + '_' + value.strip().upper().replace(' ', '_')
            raw_search_weather_dict['user_id'] = user_id

        if key == 'resolvedAddress' and len(value) > 0:
            raw_search_weather_dict['address'] = value

        if key == 'latitude' and len(value) > 0:
            raw_search_weather_dict['latitude'] = value

        if key == 'longitude' and len(value) > 0:
            raw_search_weather_dict['longitude'] = value

        if key == 'timezone' and len(value) > 0:
            raw_search_weather_dict['timezone'] = value

        if key == 'tzoffset' and len(value) > 0 :
            raw_search_weather_dict['tzoffset'] = value

        if key == 'description' and len(value) > 0:
            raw_search_weather_dict['description'] = value


    except Exception as e:
        print('Error in search_weather_decode()', e)

    return raw_search_weather_dict


daily_weather_schema = {
    'day_id': str,
    'search_id': str,
    'day_datetime': 'datetime64',
    'temp_max': float,
    'temp_min': float,
    'temp': float,
    'feels_like': float,
    'dew': float,
    'humidity': float,
    'precip': float,
    'precip_prob': float,
    'precip_cover': float,
    'precip_type': str,
    'snow': float,
    'snowd_depth': float,
    'wind_gust': float,
    'wind_speed': float,
    'wind_dir': float,
    'pressure': float,
    'cloud_cover': float,
    'visibility': float,
    'solar_radiation': float,
    'solar_energy': float,
    'uv_index': float,
    'severe_risk': float,
    'sun_rise': str,
    'sun_set': str,
    'conditions': str,
    'description': str,
}


def daily_weather_decode(day_list):
    try:
        filter_day_list = []
        key_list = list(day_list[0].keys())
        for day in day_list:
            raw_daily_weather_dict = {}
            if 'search_id' in key_list:
                raw_daily_weather_dict['day_id'] = str(day['datetime']) + '_' + day['search_id']
                raw_daily_weather_dict['search_id'] = day['search_id']

            if 'datetime' in key_list:
                raw_daily_weather_dict['day_datetime'] = day['datetime']

            if 'tempmax' in key_list and type(day['tempmax']) != str:
                raw_daily_weather_dict['temp_max'] = day['tempmax']
            else:
                raw_daily_weather_dict['temp_max'] = 0

            if 'tempmin' in key_list and type(day['tempmin']) != str:
                raw_daily_weather_dict['temp_min'] = day['tempmin']
            else:
                raw_daily_weather_dict['temp_min'] = 0

            if 'temp' in key_list and type(day['temp']) != str:
                raw_daily_weather_dict['temp'] = day['temp']
            else:
                raw_daily_weather_dict['temp'] = 0

            if 'feelslike' in key_list and type(day['feelslike']) != str:
                raw_daily_weather_dict['feels_like'] = day['feelslike']
            else:
                raw_daily_weather_dict['feels_like'] = 0

            if 'dew' in key_list and type(day['dew']) != str:
                raw_daily_weather_dict['dew'] = day['dew']
            else:
                raw_daily_weather_dict['dew'] = 0

            if 'humidity' in key_list and type(day['humidity']) != str:
                raw_daily_weather_dict['humidity'] = day['humidity']
            else:
                raw_daily_weather_dict['humidity'] = 0

            if 'precip' in key_list and type(day['precip']) != str:
                raw_daily_weather_dict['precip'] = day['precip']
            else:
                raw_daily_weather_dict['precip'] = 0

            if 'precipprob' in key_list and type(day['precipprob']) != str:
                raw_daily_weather_dict['precip_prob'] = day['precipprob']
            else:
                raw_daily_weather_dict['precip_prob'] = 0

            if 'precipcover' in key_list and type(day['precipcover']) != str:
                raw_daily_weather_dict['precip_cover'] = day['precipcover']
            else:
                raw_daily_weather_dict['precip_cover'] = 0

            if 'preciptype' in key_list :
                raw_daily_weather_dict['precip_type'] = day['preciptype']
            else:
                raw_daily_weather_dict['precip_type'] = '0'

            if 'snow' in key_list and type(day['snow']) != str:
                raw_daily_weather_dict['snow'] = day['snow']
            else:
                raw_daily_weather_dict['snow'] = 0

            if 'snowdepth' in key_list and type(day['snowdepth']) != str:
                raw_daily_weather_dict['snowd_depth'] = day['snowdepth']
            else:
                raw_daily_weather_dict['snowd_depth'] = 0

            if 'windgust' in key_list and type(day['windgust']) != str:
                raw_daily_weather_dict['wind_gust'] = day['windgust']
            else:
                raw_daily_weather_dict['wind_gust'] = 0

            if 'windspeed' in key_list and type(day['windspeed']) != str:
                raw_daily_weather_dict['wind_speed'] = day['windspeed']
            else:
                raw_daily_weather_dict['wind_speed'] = 0

            if 'winddir' in key_list and type(day['winddir']) != str:
                raw_daily_weather_dict['wind_dir'] = day['winddir']
            else:
                raw_daily_weather_dict['wind_dir'] = 0

            if 'pressure' in key_list and type(day['pressure']) != str:
                raw_daily_weather_dict['pressure'] = day['pressure']
            else:
                raw_daily_weather_dict['pressure'] = 0

            if 'cloudcover' in key_list and type(day['cloudcover']) != str:
                raw_daily_weather_dict['cloud_cover'] = day['cloudcover']
            else:
                raw_daily_weather_dict['cloud_cover'] = 0

            if 'visibility' in key_list and type(day['visibility']) != str:
                raw_daily_weather_dict['visibility'] = day['visibility']
            else:
                raw_daily_weather_dict['visibility'] = 0

            if 'solarradiation' in key_list and type(day['solarradiation']) != str:
                raw_daily_weather_dict['solar_radiation'] = day['solarradiation']
            else:
                raw_daily_weather_dict['solar_radiation'] = 0

            if 'solarenergy' in key_list and type(day['solarenergy']) != str:
                raw_daily_weather_dict['solar_energy'] = day['solarenergy']
            else:
                raw_daily_weather_dict['solar_energy'] = 0

            if 'uvindex' in key_list and type(day['uvindex']) != str:
                raw_daily_weather_dict['uv_index'] = day['uvindex']
            else:
                raw_daily_weather_dict['uv_index'] = 0

            if 'severerisk' in key_list and type(day['severerisk']) != str:
                raw_daily_weather_dict['severe_risk'] = day['severerisk']
            else:
                raw_daily_weather_dict['severe_risk'] = 0

            if 'sunrise' in key_list:
                raw_daily_weather_dict['sun_rise'] = day['sunrise']
            else:
                raw_daily_weather_dict['sun_rise'] = ''

            if 'sunset' in key_list:
                raw_daily_weather_dict['sun_set'] = day['sunset']
            else:
                raw_daily_weather_dict['sun_set'] = ''

            if 'conditions' in key_list:
                raw_daily_weather_dict['conditions'] = day['conditions']
            else:
                raw_daily_weather_dict['conditions'] = ''

            if 'description' in key_list:
                raw_daily_weather_dict['description'] = day['description']
            else:
                raw_daily_weather_dict['description'] = ''

            if 'hours' in key_list:
                raw_daily_weather_dict['hours'] = day['hours']

            filter_day_list.append(raw_daily_weather_dict)
        return filter_day_list

    except Exception as e:
        print('Error in daily_weather_decode()', str(e))


hourly_weather_schema = {'hour_id': str,
                         'search_id': str,
                         'day_id': str,
                         'hour_no': str,
                         'hour': str,
                         'temp': float,
                         'feels_like': float,
                         'humidity': float,
                         'dew': float,
                         'precip': float,
                         'precip_prob': float,
                         'snow': float,
                         'snow_depth': float,
                         'precip_type': str,
                         'wind_gust': float,
                         'wind_speed': float,
                         'wind_dir': float,
                         'pressure': float,
                         'visibility': float,
                         'cloud_cover': float,
                         'solar_radiation': float,
                         'solar_energy': float,
                         'uv_index': float,
                         'severe_risk': float,
                         'conditions': str,
                         'icon': str,
                         'stations': str,
                         'source': str}

final_hrs_list = []


def hourly_weather_decode(day):
    try:
        for hour in day['hours']:
            raw_hrs_weather = {}
            if 'datetime' in hour.keys():
                raw_hrs_weather['hour_id'] = hour['hour_id']
                raw_hrs_weather['search_id'] = hour['search_id']
                raw_hrs_weather['day_id'] = hour['day_id']
                raw_hrs_weather['hour_no'] = str(hour['datetime']).split(':')[0]
                raw_hrs_weather['hour'] = hour['datetime']

            if 'temp' in hour.keys():
                raw_hrs_weather['temp'] = hour['temp']

            if 'feelslike' in hour.keys() and type(hour['feelslike']) != str:
                raw_hrs_weather['feels_like'] = hour['feelslike']
            else:
                raw_hrs_weather['feels_like'] = 0

            if 'humidity' in hour.keys() and type(hour['humidity']) != str:
                raw_hrs_weather['humidity'] = hour['humidity']
            else:
                raw_hrs_weather['humidity'] = 0

            if 'dew' in hour.keys() and type(hour['dew']) != str:
                raw_hrs_weather['dew'] = hour['dew']
            else:
                raw_hrs_weather['dew'] = 0

            if 'precip' in hour.keys() and type(hour['precip']) != str:
                raw_hrs_weather['precip'] = hour['precip']
            else:
                raw_hrs_weather['precip'] = 0

            if 'precipprob' in hour.keys() and type(hour['precipprob']) != str:
                raw_hrs_weather['precip_prob'] = hour['precipprob']
            else:
                raw_hrs_weather['precip_prob'] = 0

            if 'snow' in hour.keys() and type(hour['snow']) != str:
                raw_hrs_weather['snow'] = hour['snow']
            else:
                raw_hrs_weather['snow'] = 0

            if 'snowdepth' in hour.keys() and type(hour['snowdepth']) != str:
                raw_hrs_weather['snow_depth'] = hour['snowdepth']
            else:
                raw_hrs_weather['snow_depth'] = 0

            if 'preciptype' in hour.keys() :
                raw_hrs_weather['precip_type'] = hour['preciptype']
            else:
                raw_hrs_weather['precip_type'] = '0'

            if 'windgust' in hour.keys() and type(hour['windgust']) != str:
                raw_hrs_weather['wind_gust'] = hour['windgust']
            else:
                raw_hrs_weather['wind_gust'] = 0

            if 'windspeed' in hour.keys() and type(hour['windspeed']) != str:
                raw_hrs_weather['wind_speed'] = hour['windspeed']
            else:
                raw_hrs_weather['wind_speed'] = 0

            if 'winddir' in hour.keys() and type(hour['winddir']) != str:
                raw_hrs_weather['wind_dir'] = hour['winddir']
            else:
                raw_hrs_weather['wind_dir'] = 0

            if 'pressure' in hour.keys() and type(hour['pressure']) != str:
                raw_hrs_weather['pressure'] = hour['pressure']
            else:
                raw_hrs_weather['pressure'] = 0

            if 'visibility' in hour.keys() and type(hour['visibility']) != str:
                raw_hrs_weather['visibility'] = hour['visibility']
            else:
                raw_hrs_weather['visibility'] = 0

            if 'cloudcover' in hour.keys() and type(hour['cloudcover']) != str:
                raw_hrs_weather['cloud_cover'] = hour['cloudcover']
            else:
                raw_hrs_weather['cloud_cover'] = 0

            if 'solarradiation' in hour.keys() and type(hour['solarradiation']) != str:
                raw_hrs_weather['solar_radiation'] = hour['solarradiation']
            else:
                raw_hrs_weather['solar_radiation'] = 0

            if 'solarenergy' in hour.keys() and type(hour['solarenergy']) != str:
                raw_hrs_weather['solar_energy'] = hour['solarenergy']
            else:
                raw_hrs_weather['solar_energy'] = 0

            if 'uvindex' in hour.keys() and type(hour['uvindex']) != str:
                raw_hrs_weather['uv_index'] = hour['uvindex']
            else:
                raw_hrs_weather['uv_index'] = 0

            if 'severerisk' in hour.keys() and type(hour['severerisk']) != str:
                raw_hrs_weather['severe_risk'] = hour['severerisk']
            else:
                raw_hrs_weather['severe_risk'] = 0

            if 'conditions' in hour.keys():
                raw_hrs_weather['conditions'] = hour['conditions']
            else:
                raw_hrs_weather['conditions'] = ''

            if 'icon' in hour.keys():
                raw_hrs_weather['icon'] = hour['icon']
            else:
                raw_hrs_weather['icon'] = ''

            if 'stations' in hour.keys():
                raw_hrs_weather['stations'] = hour['stations']
            else:
                raw_hrs_weather['stations'] = ''

            if 'source' in hour.keys():
                raw_hrs_weather['source'] = hour['source']
            else:
                raw_hrs_weather['source'] = ''

            final_hrs_list.append(raw_hrs_weather)

        return final_hrs_list
    except Exception as e:
        print('Error in hourly_weather_decode()', str(e))


curr_weather_schema = {'curr_weather_id': str,
                       'search_id': str,
                       'search_hour': str,
                       'temp': float,
                       'feels_like': float,
                       'humidity': float,
                       'dew': float,
                       'precip': float,
                       'precip_prob': float,
                       'snow': float,
                       'snow_depth': float,
                       'precip_type': str,
                       'wind_gust': float,
                       'wind_speed': float,
                       'wind_dir': float,
                       'pressure': float,
                       'visibility': float,
                       'cloud_cover': float,
                       'solar_radiation': float,
                       'solar_energy': float,
                       'uv_index': float,
                       'severe_risk': float,
                       'conditions': str,
                       'icon': str,
                       'stations': str,
                       'source': str,
                       'sun_rise': str,
                       'sun_set': str}


def current_weather_decode(curr_dict):
    try:
        global curr_search_id
        raw_curr_weather = {}
        raw_curr_weather['curr_weather_id'] = curr_dict['datetime'].replace(':', '-') + '_' + curr_search_id
        raw_curr_weather['search_id'] = curr_search_id
        raw_curr_weather['search_hour'] = curr_dict['datetime']

        if 'temp' in curr_dict.keys() and type(curr_dict['temp']) != str:
            raw_curr_weather['temp'] = curr_dict['temp']
        else:
            raw_curr_weather['temp'] = 0

        if 'feelslike' in curr_dict.keys() and type(curr_dict['feelslike']) != str:
            raw_curr_weather['feels_like'] = curr_dict['feelslike']
        else:
            raw_curr_weather['feels_like'] = 0

        if 'humidity' in curr_dict.keys() and type(curr_dict['humidity']) != str:
            raw_curr_weather['humidity'] = curr_dict['humidity']
        else:
            raw_curr_weather['humidity'] = 0

        if 'dew' in curr_dict.keys() and type(curr_dict['dew']) != str:
            raw_curr_weather['dew'] = curr_dict['dew']
        else:
            raw_curr_weather['dew'] = 0

        if 'precip' in curr_dict.keys() and type(curr_dict['precip']) != str:
            raw_curr_weather['precip'] = curr_dict['precip']
        else:
            raw_curr_weather['precip'] = 0

        if 'precipprob' in curr_dict.keys() and type(curr_dict['precipprob']) != str:
            raw_curr_weather['precip_prob'] = curr_dict['precipprob']
        else:
            raw_curr_weather['precip_prob'] = 0

        if 'snow' in curr_dict.keys() and type(curr_dict['snow']) != str:
            raw_curr_weather['snow'] = curr_dict['snow']
        else:
            raw_curr_weather['snow'] = 0

        if 'snowdepth' in curr_dict.keys() and type(curr_dict['snowdepth']) != str:
            raw_curr_weather['snow_depth'] = curr_dict['snowdepth']
        else:
            raw_curr_weather['snow_depth'] = 0

        if 'preciptype' in curr_dict.keys() :
            raw_curr_weather['precip_type'] = curr_dict['preciptype']
        else:
            raw_curr_weather['precip_type'] = '0'

        if 'windgust' in curr_dict.keys() and type(curr_dict['windgust']) != str :
            raw_curr_weather['wind_gust'] = curr_dict['windgust']
        else:
            raw_curr_weather['wind_gust'] = 0

        if 'windspeed' in curr_dict.keys() and type(curr_dict['windspeed']) != str:
            raw_curr_weather['wind_speed'] = curr_dict['windspeed']
        else:
            raw_curr_weather['wind_speed'] = 0

        if 'winddir' in curr_dict.keys() and type(curr_dict['winddir']) != str:
            raw_curr_weather['wind_dir'] = curr_dict['winddir']
        else:
            raw_curr_weather['wind_dir'] = 0

        if 'pressure' in curr_dict.keys() and type(curr_dict['pressure']) != str:
            raw_curr_weather['pressure'] = curr_dict['pressure']
        else:
            raw_curr_weather['pressure'] = 0


        if 'visibility' in curr_dict.keys() and type(curr_dict['visibility']) != str:
            raw_curr_weather['visibility'] = curr_dict['visibility']
        else:
            raw_curr_weather['visibility'] = 0

        if 'cloudcover' in curr_dict.keys() and type(curr_dict['cloudcover']) != str:
            raw_curr_weather['cloud_cover'] = curr_dict['cloudcover']
        else:
            raw_curr_weather['cloud_cover'] = 0

        if 'solarradiation' in curr_dict.keys() and type(curr_dict['solarradiation']) != str:
            raw_curr_weather['solar_radiation'] = curr_dict['solarradiation']
        else:
            raw_curr_weather['solar_radiation'] = 0

        if 'solarenergy' in curr_dict.keys() and type(curr_dict['solarenergy']) != str:
            raw_curr_weather['solar_energy'] = curr_dict['solarenergy']
        else:
            raw_curr_weather['solar_energy'] = 0

        if 'uvindex' in curr_dict.keys() and type(curr_dict['uvindex']) != str:
            raw_curr_weather['uv_index'] = curr_dict['uvindex']
        else:
            raw_curr_weather['uv_index'] = 0

        if 'severerisk' in curr_dict.keys() and type(curr_dict['severerisk']) != str:
            raw_curr_weather['severe_risk'] = curr_dict['severerisk']
        else:
            raw_curr_weather['severe_risk'] = 0

        if 'conditions' in curr_dict.keys():
            raw_curr_weather['conditions'] = curr_dict['conditions']
        else:
            raw_curr_weather['conditions'] = ''

        if 'icon' in curr_dict.keys():
            raw_curr_weather['icon'] = curr_dict['icon']
        else:
            raw_curr_weather['icon'] = ''

        if 'stations' in curr_dict.keys():
            raw_curr_weather['stations'] = curr_dict['stations']
        else:
            raw_curr_weather['stations'] = ''

        if 'source' in curr_dict.keys():
            raw_curr_weather['source'] = curr_dict['source']
        else:
            raw_curr_weather['source'] = ''

        if 'sunrise' in curr_dict.keys():
            raw_curr_weather['sun_rise'] = curr_dict['sunrise']
        else:
            raw_curr_weather['sun_rise'] = ''

        if 'sunset' in curr_dict.keys():
            raw_curr_weather['sun_set'] = curr_dict['sunset']
        else:
            raw_curr_weather['sun_set'] = ''

        return raw_curr_weather
    except Exception as e:
        print('Error in current_weather_decode()', str(e))


def decode_raw_json(raw_data, user_id):
    try:
        filtered_weather_data = {
            'user_id': "",
            'search_id': "",
            'src_city': "",
            'daily_weather': "",
            'hourly_weather': "",
            'current_weather': ""
        }
        src_weather_dict = {}
        # PART : 1 decoding main weather json
        # to create search_id
        for key, value in raw_data.items():
            if key != 'days':
                src_weather_dict = search_weather_decode(key, str(value), user_id)

        # setting search_id
        search_id = src_weather_dict['search_id']

        # converting return dict into dataframe and applying schema for type changed
        search_weather_df = pd.DataFrame([src_weather_dict]).astype(search_weather_schema)

        # PART : 2 Decoding daily weather json
        # decoding daily weather json and adding search_id
        for i in range(len(raw_data['days'])):
            raw_data['days'][i]['search_id'] = search_id

        filter_day_list = daily_weather_decode(raw_data['days'])

        # creating dataframe from raw day weather
        daily_weather_df = pd.DataFrame(filter_day_list, columns=list(daily_weather_schema.keys())).astype(
            daily_weather_schema)
        daily_weather_df.fillna(value=0, inplace=True)

        # PART : 3
        # created hours list to store hourly weather details
        for day in filter_day_list:
            for hour in day['hours']:
                hour['hour_id'] = hour['datetime'] + '_' + day['day_id']
                hour['search_id'] = search_id
                hour['day_id'] = day['day_id']
                hour['hour_no'] = str(hour['datetime'].split(':')[0])

        hours_list = []
        for day in filter_day_list:
            hours_list = hourly_weather_decode(day)

        # converting hours_list into dataframe
        hourly_weather_df = pd.DataFrame(hours_list, columns=list(hourly_weather_schema.keys())).astype(
            hourly_weather_schema)
        hourly_weather_df.fillna(value=0, inplace=True)
        hourly_weather_df.drop_duplicates(inplace=True)

        # setting current weather details
        curr_weather_df = current_weather_decode(raw_data['currentConditions'])
        curr_weather_df = pd.DataFrame([curr_weather_df]).astype(curr_weather_schema)
        curr_weather_df.fillna(value=0, inplace=True)

        filtered_weather_data['user_id'] = user_id
        filtered_weather_data['search_id'] = search_id
        filtered_weather_data['search_city'] = search_weather_df
        filtered_weather_data['daily_weather'] = daily_weather_df
        filtered_weather_data['hourly_weather'] = hourly_weather_df
        filtered_weather_data['current_weather'] = curr_weather_df

        return filtered_weather_data
    except Exception as e:
        print('Error in decode_raw_json()',e)
