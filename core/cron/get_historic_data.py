from datetime import datetime
import pathlib
import pandas

CURRENT_PATH = pathlib.Path(__file__).parent.absolute()
DATA_PATH = pathlib.Path(CURRENT_PATH.parent, 'data')
UNREASONABLE_FAR_DATE = '12/12/40'
TOTAL_DATA = {
        'url': 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv',
        'local_path': pathlib.Path(DATA_PATH, 'total_history.csv'),
}
DEATHS_DATA = {
        'url': 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv',
        'local_path': pathlib.Path(DATA_PATH, 'deaths_history.csv'),
}
RECOVERIES_DATA = {
        'url': 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv',
        'local_path': pathlib.Path(DATA_PATH, 'recovered_history.csv'),
}

def get_dataframe(url):
    return pandas.read_csv(url)

def remove_unused_columns(dataframe):
    del dataframe['Lat']
    del dataframe['Long']
    del dataframe['Province/State']

def reindex(dataframe):
    dataframe.index.name = 'date'
    dataframe.reset_index(inplace=True)

def get_index(arr):
    try:
        return next(x for x, val in enumerate(arr) if val > 0)
    except:
        return len(arr)-1

def row_to_append(dataframe):
    row = [UNREASONABLE_FAR_DATE]

    for (column_name, column_data) in dataframe.iteritems():
        if not (column_name == "date"): row.append(dataframe['date'].values[get_index(column_data.values)])

    return row

def insert_dates_row(dataframe):
    dataframe.loc[-1] = row_to_append(dataframe)
    dataframe.index += 1
    dataframe.sort_index(inplace=True)

def append_today_row(dataframe):
    row = [datetime.now().strftime("%-m/%-d/%y")]
    row += list(dataframe.loc[dataframe.shape[0]-1].values)[1:]
    dataframe = dataframe.append(pandas.DataFrame([row], columns=dataframe.columns))
    return dataframe

def missing_today_data(dataframe):
    return not dataframe.iloc[-1]['date'] == datetime.now().strftime("%-m/%-d/%y")

def restructure_and_save_data(dataframe, local_path):
    remove_unused_columns(dataframe)

    dataframe['Country/Region'] = [x.lower() for x in dataframe['Country/Region'].values]
    dataframe = dataframe.groupby(dataframe['Country/Region']).sum().transpose()

    reindex(dataframe)

    insert_dates_row(dataframe)

    if missing_today_data(dataframe): dataframe = append_today_row(dataframe)

    dataframe.to_csv(local_path, index=False)

def download_and_restructure_cases_data():
    dataframe = get_dataframe(TOTAL_DATA['url'])
    restructure_and_save_data(dataframe, TOTAL_DATA['local_path'])

def download_and_restructure_deaths_data():
    dataframe = get_dataframe(DEATHS_DATA['url'])
    restructure_and_save_data(dataframe, DEATHS_DATA['local_path'])

def download_and_restructure_recoveries_data():
    dataframe = get_dataframe(RECOVERIES_DATA['url'])
    restructure_and_save_data(dataframe, RECOVERIES_DATA['local_path'])

download_and_restructure_cases_data()
download_and_restructure_deaths_data()
download_and_restructure_recoveries_data()
