from csv import DictReader
import time

from sklearn.utils import column_or_1d

from services.anomaly_data_service import AnomalyDataService
from services.synthesize_data import Data_Synthesizer
import pandas as pd

class SynthesizeDataManager:
    """Used as a  data source that periodically yields timeseries data points

    """
    def __init__(self):
        self.range = [0,1]


    def csv_line_reader(self, file_name, col_name, speed_up):
        """Use data from a csv to periodically yield a row of data

        :param file_name: Name of csv file as source of data
        :param col_name:  Name of column to extract
        :return: none
        ..notes:: This static method has no return.  Instead, it yields a row of data that has been read from
        a data source.
        """
        with open(file_name, 'r') as read_obj:
            dict_reader = DictReader(read_obj)
            pandas_df = pd.read_csv(file_name)
            self.range = [pandas_df[col_name].min(), pandas_df[col_name].max()]
            for row in dict_reader:
                
                # print("row in reader: {}".format(row))
                sleep_period = (1/10) / float(speed_up)
                time.sleep(sleep_period)
                yield [row[pandas_df.columns[0]], row[col_name]]

    def load_sensor(self, col_name, speed_up):
        
        query = AnomalyDataService
        df_data = query.get_all_data()
        df_data = df_data.sort_values(by=df_data.columns[0],ascending=True)
        df_data['timestamp'] = df_data[df_data.columns[0]].apply(str)
        print(df_data['timestamp'])
        if col_name not in list(df_data.columns):
            col_name =  df_data.columns[1]
        df_sensor = df_data[['timestamp', col_name]]
        self.range = [df_sensor[col_name].min(), df_sensor[col_name].max()]

        for index in df_sensor.index:
                # print("row in reader: {}".format(row))
                row = df_sensor.loc[index,:]
                sleep_period = (1/10) / float(speed_up)
                time.sleep(sleep_period)
                yield [row['timestamp'], row[col_name]]

    def synthesize_data(self, col_name, speed_up):
        generator = Data_Synthesizer
        df_data = generator.synthesize_data(col_name)

        df_sensor = df_data[['timestamp', col_name]]
        self.range = [df_sensor[col_name].min(), df_sensor[col_name].max()]

        for index in df_sensor.index:
                # print("row in reader: {}".format(row))
                row = df_sensor.loc[index,:]
                sleep_period = (1/10) / float(speed_up)
                time.sleep(sleep_period)

                yield [row['timestamp'], row[col_name]]

    def return_range(self):
        return self.range
