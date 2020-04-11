import pathlib
import pandas

LOCAL_COUNTRY = 'peru'
CURRENT_PATH = pathlib.Path(__file__).parent.absolute()
LOCAL_DATAFILE_PATH = pathlib.Path(CURRENT_PATH, 'data', '{}.csv'.format(LOCAL_COUNTRY))
DATAFILE_PATH = pathlib.Path(CURRENT_PATH, 'data', 'total_history.csv')

def modify_with_local_data():
    local_dataframe = pandas.read_csv(LOCAL_DATAFILE_PATH)
    dataframe = pandas.read_csv(DATAFILE_PATH)

    if dataframe.shape[0] > local_dataframe.shape[0]: return

    dataframe[LOCAL_COUNTRY] = local_dataframe[LOCAL_COUNTRY]
    dataframe.to_csv(DATAFILE_PATH, index=False)

modify_with_local_data()
