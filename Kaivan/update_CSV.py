# Source: https://towardsdatascience.com/collect-your-own-fitbit-data-with-python-ff145fa10873
# Getting familiar with fitbit API
# Kaivan Taylor

import fitbit
import gather_keys_oauth2 as Oauth2
from secret import fb_CLIENT_ID,fb_CLIENT_SECRET
import pandas as pd
import datetime
import os

CLIENT_ID = fb_CLIENT_ID
CLIENT_SECRET = fb_CLIENT_SECRET

def update_heartrate():
    server = Oauth2.OAuth2Server(CLIENT_ID, CLIENT_SECRET)
    server.browser_authorize()

    ACCESS_TOKEN = str(server.fitbit.client.session.token['access_token'])
    REFRESH_TOKEN = str(server.fitbit.client.session.token['refresh_token'])

    auth2_client = fitbit.Fitbit(CLIENT_ID, CLIENT_SECRET, oauth2=True, access_token=ACCESS_TOKEN, refresh_token=REFRESH_TOKEN)

    yesterday = str((datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y%m%d"))
    yesterday2 = str((datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d"))
    today = str(datetime.datetime.now().strftime("%Y%m%d"))

    fit_statsHR = auth2_client.intraday_time_series('activities/heart')

    stime_list = []
    sval_list = []
    for i in fit_statsHR['activities-heart-intraday']['dataset']:
        stime_list.append(i['time'])
        sval_list.append(i['value'])

    heartdf = pd.DataFrame({'Heart Rate':sval_list,
                         'Time':stime_list})

    print(os.getcwd())
    os.chdir("C:/Users/speedykai/Desktop/hophacks2019/kaivan/CSV")
    heartdf.to_csv('heartrate_'+ \
                   yesterday+'.csv', \
                   columns=['Time','Heart Rate'], header=True, \
                   index = False)