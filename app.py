from flask import Flask, render_template
import pandas as pd
import folium
from datetime import datetime, timedelta
from urllib.error import HTTPError

app = Flask(__name__)


def get_raw_data():
    """
    This function gets daily covid-19 data from JHU
    :return: utc_date, raw_data and data_url
    """
    # get utc date
    utc_datetime = datetime.utcnow()
    utc_date = utc_datetime.strftime('%m-%d-%Y')
    print(f'🌟{utc_date}')

    # construct url
    data_url = f'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/{utc_date}.csv'

    # try except url
    try:
        # run this code
        raw_data = pd.read_csv(data_url)
    except HTTPError as e:
        print(f'🌟{e}')
        # run the following if there is an error
        try:
            utc_date = (utc_datetime - timedelta(days=1)).strftime('%m-%d-%Y')
            data_url = f'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/{utc_date}.csv'
            raw_data = pd.read_csv(data_url)
            print('🌟cannot get today, gotten yesterday')
        except HTTPError as er:
            print(f'🌟 second {er}')
            utc_date = (utc_datetime - timedelta(days=2)).strftime('%m-%d-%Y')
            data_url = f'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/{utc_date}.csv'
            raw_data = pd.read_csv(data_url)
            print('🌟cannot get today, gotten DAY BEFORE yesterday')
    else:
        # no error? run this
        raw_data = pd.read_csv(data_url)
        print('🌟can get today, gotten today')

    # return utc_date, dataframe and url
    return utc_date, raw_data, data_url


def world_total(original_df):
    """
    This function sums up cases of confirmed, active, deaths, recovered
    all over the world.

    :param original_df: raw, unprocessed pandas dataframe
    :return: confirmed, active, deaths, recovered. all int
    """
    all_sum = original_df.sum()

    confirmed = format(int(all_sum['Confirmed']), ',')
    active = format(int(all_sum['Active']), ',')
    deaths = format(int(all_sum['Deaths']), ',')
    recovered = format(int(all_sum['Recovered']), ',')

    return confirmed, active, deaths, recovered


def top_ten(original_df):
    """
    Takes raw data and returns a list of top ten countries by confirmed cases
    :param original_df: raw, unprocessed pandas dataframe
    :return: pandas dataframe of top ten countries by confirmed cases
    """
    top_ten_df = original_df.groupby('Country_Region') \
        .sum()[['Confirmed']] \
        .sort_values(by=['Confirmed'], ascending=False) \
        .nlargest(10, 'Confirmed')

    # format numbers
    top_ten_df['Confirmed'] = top_ten_df.apply(lambda x: "{:,}".format(x['Confirmed']), axis=1)

    # convert dataframe to html table
    top_ten_table = top_ten_df.to_html()

    tbody_start_index = top_ten_table.index('</thead>') + 8
    html_table_body = top_ten_table[tbody_start_index:]

    return html_table_body


def add_bubble(bubble_map, data):
    """
    Adds bubbles to map object based on data passed in.
    :param bubble_map: this is a folium Map object
    :param data: this is a list of [location name, latitude, longitude, confirmed cases]
    """
    folium.Circle(location=[data[1], data[2]],
                  radius=float(data[3]) * 1,
                  popup=f'{data[0]}\nConfirmed cases: {data[3]}',
                  color='#3186cc', fill=True, fill_color='#3186cc').add_to(bubble_map)


def create_map(original_df):
    """
    This function creates a dataframe with required columns from original_df (raw data).
    The new dataframe will be used to create a bubble map chart.
    :param original_df: a pandas dataframe of raw data
    :return: folium map object
    """

    # get required data
    new_df = original_df[['Combined_Key', 'Lat', 'Long_', 'Confirmed']].dropna()

    # create folium map object
    bubble_map = folium.Map(tiles='Stamen toner')
    new_df.apply(lambda x: add_bubble(bubble_map, x), axis=1)
    html_bubble_map = bubble_map._repr_html_()

    return html_bubble_map


@app.route('/')
def home():
    utc_date, raw_data, data_url = get_raw_data()
    confirmed, active, deaths, recovered = world_total(raw_data)
    top_tbody = top_ten(raw_data)
    bubble_map = create_map(raw_data)

    return render_template('index.html', utc_date=utc_date, data_url=data_url,
                           confirmed=confirmed, active=active, deaths=deaths, recovered=recovered,
                           top_tbody=top_tbody,
                           bubble_map=bubble_map)


if __name__ == '__main__':
    app.run(debug=True)
