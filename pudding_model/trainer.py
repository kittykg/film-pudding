import numpy as np
from random import shuffle

from .data_collector import DataCollector
from .data_processor import DataProcessor
from .model import FilmPuddingModel


class Trainer:
    def __init__(self, enable_data_collect=False):
        with open("pudding_model/secret_key", "r") as sk:
            self.API_KEY = sk.readline().splitlines().pop()
        sk.close()

        if enable_data_collect:
            dc = DataCollector(self.API_KEY, "pudding_model/ratings.csv")
            dc.collect("pudding_model/collected_data")

    def train_model(self):
        dp = DataProcessor(self.API_KEY, "pudding_model/collected_data.npy")
        x, y = dp.process_data()

        assert x.shape[0] == y.shape[0]
        assert x.shape[1] == 24

        print("Data ready...")

        dataset_size = len(y)
        data_label_pairs = list(zip(x, y))
        shuffle(data_label_pairs)

        x = [obs for obs, _ in data_label_pairs]
        y = [label for _, label in data_label_pairs]

        val_size = dataset_size // 10

        train_x = x[:(len(x) - 2 * val_size)]
        train_y = y[:(len(y) - 2 * val_size)]
        val_x = x[(len(x) - 2 * val_size): len(x) - val_size]
        val_y = y[(len(y) - 2 * val_size): len(y) - val_size]
        test_x = x[(len(x) - val_size): len(x)]
        test_y = y[(len(y) - val_size): len(y)]

        train_x = np.array(train_x)
        train_y = np.array(train_y)
        val_x = np.array(val_x)
        val_y = np.array(val_y)
        test_x = np.array(test_x)
        test_y = np.array(test_y)

        print("Datasets for training, validation and testing are ready...\n")

        fpm = FilmPuddingModel()

        fpm.fit(train_x, train_y, val_x, val_y)

        print("Training done...\n")

        print("Evaluation:")
        fpm.evaluate(test_x, test_y)

        return fpm
