import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import re


def plot_cleaned_csv(cleaned_consumption_values):
    fig = px.line(cleaned_consumption_values,
                  title="Cleaned Consumption Values",
                  line_group="channel",
                  color="channel",
                  x="datetime",
                  y="logdata_value"
                  )

    fig.update_xaxes(title_text='DateTime')
    fig.update_yaxes(title_text='kWh')

    fig.show()

def clean_and_plot_csv(consumption_values_csv):
    # Import the source data
    consumption_values = pd.read_csv(consumption_values_csv)

    # Build temporary dataframe for parsing
    channel = consumption_values['channmr']
    start_time = consumption_values['startdatetime']

    logdata_concat = consumption_values['logdata0']\
                 + consumption_values['logdata1']\
                 + consumption_values['logdata2']\
                 + consumption_values['logdata3']\
                 + consumption_values['logdata4']\
                 + consumption_values['logdata5']\
                 + consumption_values['logdata6']

    parsing_df = pd.DataFrame({'channel': channel, 'start_time': start_time, 'logdata_concat': logdata_concat})

    # Cleaned output dataframe
    cleaned_consumption_values = pd.DataFrame(columns=['channel', 'interval', 'datetime', 'logdata_value'])

    for row in parsing_df.iterrows():

        channel = row[1]['channel']
        logdata = row[1]['logdata_concat'].split(',')

        current_timestamp = int(row[1]['start_time'])
        current_interval = 0

        for i in range(1,len(logdata)):

            logdata_entry = logdata[i]

            # Check if logdata_entry is an interval (ie 30M, 180M)
            interval_match = re.match("[0-9]+M", logdata_entry)
            if interval_match:
                interval_string = re.match("[0-9]+", logdata_entry)
                current_interval = int(interval_string.group())

            else:

                # Check for a float (ie logdata value)
                float_match = re.match('[0-9]+\.[0-9]+', logdata_entry)
                if float_match:
                    logdata_value = float(float_match.group())

                    # Calculate the next/current timestamp from previous & convert to datetime
                    current_timestamp = current_timestamp + (current_interval * 60)
                    current_datetime = datetime.fromtimestamp(current_timestamp)

                    # Build the dictionary to append to cleaned dataframe
                    row_dict = {'channel': channel, 'interval': current_interval, 'datetime': current_datetime, 'logdata_value': logdata_value}
                    cleaned_consumption_values = cleaned_consumption_values.append(row_dict, ignore_index=True)

    plot_cleaned_csv(cleaned_consumption_values)

# Call function, parsing relevant .csv file
clean_and_plot_csv('consumption_values.csv')