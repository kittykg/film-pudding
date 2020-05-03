import os
from data_collector import DataCollector
from data_processor import DataProcessor

API_KEY = os.environ["TMDB_API_KEY"]

# dc = DataCollector(API_KEY, "ratings.csv")
# dc.collect("collected_data")

dp = DataProcessor(API_KEY, "collected_data.npy")
data = dp.process_data()

print("Writing to files")
dp.write_to_file(data)
