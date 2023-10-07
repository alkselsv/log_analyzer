"""Запускает приложение"""
import argparse
from logger import init_stream_logger
from log_scanner import LogScanner
from preproccessor import Preprocessor
from predictor import Predictor


if __name__ == "__main__":
    # Парсинг аргументов командной строки
    parser = argparse.ArgumentParser(description="Log monitoring and processing")
    parser.add_argument(
        "--root_dir", type=str, default="users", help="Path to the root dir"
    )
    parser.add_argument(
        "--models_dir",
        type=str,
        default="models",
        help="Path to the classification models",
    )
    parser.add_argument(
        "--period",
        type=int,
        default=60,
        help="Log access period in seconds",
    )
    args = parser.parse_args()

    # Подключение логера
    logger = init_stream_logger()
    logger.info("App starts")

    # Установка путей
    root_dir = args.root_dir
    models_dir = args.models_dir
    # Определение периода
    period = args.period

    logger.info(f"Root dir: {root_dir}")
    logger.info(f"Models dir: {models_dir}")

    logger.info("Log scanning starts")
    scanner = LogScanner(root_dir=root_dir, logger=logger)
    scanner.scan()
    logger.info("Log scanning ends")

    preproccessor = Preprocessor(logger=logger)
    predictor = Predictor(
        scanner=scanner,
        preproccessor=preproccessor,
        models_dir=models_dir,
        period=period,
        logger=logger,
    )
    predictor.start()
