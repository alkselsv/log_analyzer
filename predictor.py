"""Определение класса Predictor"""
import os
import time
from threading import Thread
import random  # только для отладки
import pandas as pd
import joblib


class Predictor:
    """Возвращает предсказания модели"""

    def __init__(self, scanner, preproccessor, model_dir="models"):
        self.scanner = scanner
        self.preproccessor = preproccessor
        self.model_dir = model_dir
        self.models = {}
        self.load_models()

    def load_models(self):
        """Загружает модели в память"""

        for model_name in self.scanner.get_models():
            model_file = os.path.join(self.model_dir, model_name + ".joblib")
            print(model_file)
            if os.path.isfile(model_file):
                self.models[model_name] = joblib.load(model_file)

    def predict(self):
        """Выполняет предсказание"""

        while True:
            for idx, log_file in enumerate(self.scanner.get_log_files()):
                data = self.preproccessor.proccess_data(
                    log_file)
                print(len(data))
                model_name = self.scanner.get_models()[idx]
                model = self.models.get(model_name)
                print(model)
                if model is not None and len(data):
                    # predictions = model.predict(data)
                    predictions = [random.random()
                                   for _ in range(len(data))]

                    min_bound = self.scanner.get_min_bounds()[idx]
                    print(min_bound)
                    predictions_filtered = [
                        predict for predict in predictions if predict > min_bound
                    ]

                    if len(predictions_filtered) > 0:
                        out_file = os.path.join(
                            os.path.dirname(log_file), "out.csv.log"
                        )
                        pd.DataFrame(predictions_filtered).to_csv(
                            out_file, mode="a", header=False
                        )
            time.sleep(20)

    def start(self):
        """Запускает процесс предсказания"""

        Thread(target=self.predict).start()
