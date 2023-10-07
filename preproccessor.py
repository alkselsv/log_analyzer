"""Определение класса Preprocessor"""
import os
from datetime import datetime
import warnings
import pandas as pd

warnings.filterwarnings("ignore")


class Preprocessor:
    """Предобработчик данных"""

    def __init__(self, logger=None):

        self.logger = logger

        # Имена всех признаков
        self.columns = [
            "type",
            "host",
            "auto",
            "cTm",
            "date",
            "remote_addr",
            "session",
            "page",
            "http_referer",
            "http_user_agent",
            "access.status",
            "access.request_time",
            "access.bytes_sent",
            "access.request",
            "metrik.action",
            "metrik.param",
            "metrik.cookieEnabled",
            "metrik.language",
            "metrik.isMobile",
            "metrik.platform",
        ]

        # Правила агрегации признаков (имя признака : агрегация)
        self.aggs = {
            "remote_addr": "unique",
            "page": list,
            "http_referer": "unique",
            "http_user_agent": "unique",
            "access.status": "unique",
            "access.request_time": "mean",
            "access.bytes_sent": "sum",
            "access.request": list,
            "metrik.action": "unique",
        }

        # Имена признаков, которые будут отброшены после постобработки
        self.columns_to_drop = [
            "remote_addr",
            "session",
            "time_round",
            "page",
            "http_referer",
            "http_user_agent",
            "access.status",
            "access.request",
            "metrik.action",
        ]

        self.last_file_positions = {}
        self.last_file_sizes = {}

    def __read_data__(self, file):
        """Загружает данные в DataFrame pandas"""

        with open(file, 'r') as f:
            current_file_size = os.path.getsize(file)
            last_file_position = self.last_file_positions.get(file, 0)
            if current_file_size < self.last_file_sizes.get(file, 0):
                last_file_position = 0
                self.last_file_positions[file] = 0
            self.last_file_sizes[file] = current_file_size
            f.seek(last_file_position)
            dataframe = pd.read_csv(f, sep=";", names=self.columns, on_bad_lines="skip")
            self.last_file_positions[file] = f.tell()
            dataframe["datetime"] = pd.to_datetime(dataframe["date"])
            dataframe = dataframe[dataframe["type"]
                                  == "METRIK"]  # Оставляет строки с метрикой
            self.logger.debug(f"New records for predictions: {len(dataframe)}")
            return dataframe

    def __make_group__(self, dataframe):
        """Выполняет операцию группирования по двум столбцам session и time_round"""

        return (
            dataframe.groupby(["session", "time_round"])
            .aggregate(self.aggs)
            .reset_index()
        )

    @staticmethod
    def __remove_nan__(coll):
        """Удаляет NaN из переданной коллекции элементов"""

        arr = coll[~pd.isna(coll)]  # noqa: E1130
        return arr

    def __preproccess_data__(self, dataframe):
        """Выполняет предобаботку данных"""

        dataframe["time_round"] = dataframe["datetime"].apply(
            lambda x: datetime(
                x.year, x.month, x.day, x.hour, x.minute, (x.second // 20) * 20
            )
        )
        return self.__make_group__(dataframe)

    def __postproccess_data__(self, dataframe):
        """Выполняет создание новых признаков"""

        # подсчёт числа посещённых страниц
        dataframe["page_count"] = dataframe["page"].apply(len)

        dataframe["was_404"] = dataframe["access.status"].apply(
            lambda x: 1 if 404 in x else 0
        )  # флаг 404 кода в результатах
        dataframe["was_200"] = dataframe["access.status"].apply(
            lambda x: 1 if 200 in x else 0
        )  # флаг 200 кода в результатах

        dataframe["http_referer"] = dataframe["http_referer"].apply(
            self.__remove_nan__
        )  # удаляем nan из http_referer
        dataframe["http_referer"] = dataframe["http_referer"].apply(
            lambda x: x[x != "-"]
        )  # удаляем '-' из http_referer
        dataframe["http_referer_is_empty"] = dataframe["http_referer"].apply(
            lambda x: int(len(x) == 0)
        )  # флаг отсутствия рефереров

        dataframe["metrik.action"] = dataframe["metrik.action"].apply(
            self.__remove_nan__
        )  # удаляем NaN из metrik.action
        dataframe["was_action_ready"] = dataframe["metrik.action"].apply(
            lambda x: int("ready" in x)
        )  # флаг наличия действия ready в metrik.action
        dataframe["was_action_scroll"] = dataframe["metrik.action"].apply(
            lambda x: int("scroll" in x)
        )  # флаг наличия действия scroll в metrik.action
        dataframe["was_action_click"] = dataframe["metrik.action"].apply(
            lambda x: int("click" in x)
        )  # флаг наличия действия click в metrik.action

        timestamps = dataframe["time_round"].values
        ip_addrs = [remote_addr[0] for remote_addr in dataframe["remote_addr"].values]
        sessions = dataframe["session"].values
        user_agents = [
            user_agent[0] for user_agent in dataframe["http_user_agent"].values
        ]
        dataframe.drop(self.columns_to_drop, axis=1, inplace=True)
        return dataframe, timestamps, ip_addrs, sessions, user_agents

    def proccess_data(self, file):
        """Запускает процесс обработки данных"""

        dataframe = self.__read_data__(file)
        dataframe = self.__preproccess_data__(dataframe)
        (
            dataframe,
            timestamps,
            ip_addrs,
            sessions,
            user_agents,
        ) = self.__postproccess_data__(dataframe)
        return dataframe, timestamps, ip_addrs, sessions, user_agents
