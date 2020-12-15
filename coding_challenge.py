import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import os


# 1. write a piece of code to extract the time-series data into a format that provides easier access to the data
consumption_values = pd.read_csv('consumption_values.csv')

channel = consumption_values['channmr']

start_time = consumption_values['startdatetime']

logdata_concat = consumption_values['logdata0']\
                 + consumption_values['logdata1']\
                 + consumption_values['logdata2']\
                 + consumption_values['logdata3']\
                 + consumption_values['logdata4']\
                 + consumption_values['logdata5']\
                 + consumption_values['logdata6']

cleaned_consumption_values = pd.DataFrame(columns=['channel', 'interval', 'start_time', 'logdata_value'])

df = pd.DataFrame({'channel': channel, 'start_time': start_time, 'logdata_concat': logdata_concat})

p = 0

for row in df.iterrows():
    channel_number = row[1]['channel']
    start_time = row[1]['start_time']
    time = datetime.fromtimestamp(start_time)
    logdata = row[1]['logdata_concat'].split(',')
    # need to add re to detect status code
    logdata_value = logdata[0].replace('A', '').replace('d2','')

    logdata_interval = logdata[1]

    first_data_point_dict = {'channel': channel_number, 'interval': logdata_interval, 'start_time': time, 'logdata_value': logdata_value}

    cleaned_consumption_values = cleaned_consumption_values.append(first_data_point_dict, ignore_index=True)

    i = 2
    interval = 60*30

    for i in range(2,len(logdata)):
        ts = interval * i
        ts = ts - interval
        time = datetime.fromtimestamp(start_time)
        data_point_ts = time + timedelta(0,ts)
        row_dict = {'channel': channel_number, 'interval': logdata_interval, 'start_time': data_point_ts, 'logdata_value': logdata[i]}
        cleaned_consumption_values = cleaned_consumption_values.append(row_dict, ignore_index=True)


# print(cleaned_consumption_values)
# cleaned_consumption_values.to_csv(os.path.join(path,r'cleaned_consumption_value.csv')


fig = px.line(cleaned_consumption_values,
              title="Cleaned Consumption Values",
              line_group="channel",
              color="channel",
              x="start_time",
              y="logdata_value"
              )

fig.update_xaxes(title_text='DateTime')
fig.update_yaxes(title_text='kWh')

fig.show()