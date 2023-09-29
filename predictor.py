"""Определение класса Predictor"""
import os
import time
import multiprocessing as mp
import pickle
import random  # Для тестирования
import numpy as np
import pandas as pd


class Predictor:
    """Возвращает предсказания модели"""

    def __init__(self, scanner, preproccessor, model_dir="models"):
        self.scanner = scanner
        self.preproccessor = preproccessor
        self.model_dir = model_dir

    def __predict__(self, model, log_file, min_bound):
        """Выполняет предсказание"""

        print(model)
        print(min_bound)

        while True:

            data, timestamps, ip_addrs, sessions, user_agents = self.preproccessor.proccess_data(
                log_file)
            df_out = pd.DataFrame(columns=["timestamp", "ip_addr", "prob", "session"])
            df_out["timestamp"] = timestamps
            df_out["ip_addr"] = ip_addrs
            df_out["session"] = sessions
            df_out["user_agent"] = user_agents
            print(len(data))

            if model is not None and len(data):
                predictions = [
                    int(y) for y in model.predict_proba(data)[:, 1] > 0.004]
                df_out["prob"] = np.round(predictions, 2)

                # Для тестирования
                # predictions = [random.random()
                #                for _ in range(len(data))]
                # predictions_filtered = [
                #     predict for predict in predictions if predict > min_bound
                # ]

                df_out_filtered = df_out[df_out["prob"] > min_bound]

                if len(df_out_filtered) > 0:
                    out_file = os.path.join(
                        os.path.dirname(log_file), "out.csv.log"
                    )
                    df_out_filtered.to_csv(out_file, mode='a', index=False, header=False)

            time.sleep(20)

    def __worker__(self, args):
        """Вспомогательная функция, которая разбирает аргументы"""

        model_name, log_file, min_bound = args
        model_path = os.path.join(self.model_dir, model_name + ".pkl")
        with open(model_path, "rb") as file:
            model = pickle.load(file)
        return self.__predict__(model, log_file, min_bound)

    def start(self):
        """Запускает процесс предсказания"""

        models_names = self.scanner.get_models()
        log_files = self.scanner.get_log_files()
        min_bounds = self.scanner.get_min_bounds()

        pool = mp.Pool(mp.cpu_count())
        pool.map(self.__worker__, zip(models_names, log_files, min_bounds))
        pool.close()
