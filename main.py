import os
from data_processor import DataProcessor

API_KEY = os.environ["TMDB_API_KEY"]

dp = DataProcessor(API_KEY, "test.csv")
data = dp.processe_data()
dp.write_to_file(data)
