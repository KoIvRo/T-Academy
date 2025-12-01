import argparse
import json
from pathlib import Path

from logger_config import logger


class Config:
    """Класс с конфигом для отрисовки."""

    def __init__(self) -> None:
        """Инициализируем значениями по умолчанию."""
        self.width = 1920
        self.height = 1080
        self.seed = 5.1234
        self.iteration_count = 250000
        self.output_path = "result.png"
        self.threads = 1
        self.functions = [
            {"name": "swirl", "weight": 1.0},
            {"name": "horseshoe", "weight": 0.8},
        ]
        self.affine_params = {
            "a": 0.6,
            "b": 0.6,
            "c": 0.6,
            "d": 0.6,
            "e": 0.6,
            "f": 0.6,
        }
        self.gamma = 2.2
        self.symmetry_level = 1

    def load_with_priority(self) -> None:
        """Приоритетная загрузка конфига."""
        args = self._parse_cli_args()

        if args.config:
            try:
                json_config = self._read_json(args.config)
            except (FileNotFoundError, PermissionError) as e:
                logger.warning(f"Файл не найден: {e}")
            else:
                self._apply_json(json_config)

        self._apply_cli_args(args)

    @staticmethod
    def _parse_cli_args() -> argparse.Namespace:
        """Парсер аргументов."""
        parser = argparse.ArgumentParser()

        parser.add_argument(
            "-W", "--width", type=int, help="Ширина изображения", default=None
        )
        parser.add_argument(
            "-H", "--height", type=int, help="Высота изображения", default=None
        )

        parser.add_argument(
            "-s",
            "--seed",
            type=float,
            help="Начальное значение генератора",
            default=None,
        )

        parser.add_argument(
            "-i",
            "--iteration-count",
            type=int,
            help="Количество иетраций",
            default=None,
        )

        parser.add_argument(
            "-o",
            "--output-path",
            type=str,
            help="Путь для реузльтат",
            default=None,
        )

        parser.add_argument(
            "-t", "--threads", type=int, help="Количество потоков", default=None
        )

        parser.add_argument(
            "-ap",
            "--affine-params",
            type=str,
            help="""
                a - масштаб/вращение X, double, например - 0.1;\n
                b - сдвиг-смешивание X от Y, double, например - 0.1;\n
                c - сдвиг по X, double, например - 0.1;\n
                d - смешивание Y от X, double, например - 0.1;\n
                e - масштаб/вращение Y, double, например - 0.1;\n
                f - сдвиг по Y, double, например - 0.1;
                """,
            default=None,
        )

        parser.add_argument(
            "-f",
            "--functions",
            help="""Строка, конфигурация применяемых методов трансформации формата\n
            <функция_N>:<вес_функции>,<функция_N>:<вес_функции>""",
            default=None,
        )

        parser.add_argument(
            "-g", "--gamma", type=float, help="Гамма коррекция", default=None
        )

        parser.add_argument(
            "-S", "--symmetry-level", type=int, help="Уровень симметрий", default=None
        )

        parser.add_argument(
            "-c",
            "--config",
            help="Путь до файла с конфигом",
        )

        return parser.parse_args()

    def _apply_cli_args(self, cli_args: argparse.Namespace) -> None:
        """Применяет CLI аргументы (высший приоритет)."""
        args = [
            "width",
            "height",
            "seed",
            "iteration_count",
            "output_path",
            "threads",
            "gamma",
            "symmetry_level",
        ]
        for attr in args:
            value = getattr(cli_args, attr, None)
            if value is not None:
                setattr(self, attr, value)

        if cli_args.functions is not None:
            self.functions = self._parse_functions(cli_args.functions)
        if cli_args.affine_params is not None:
            self.affine_params = self._parse_affine_params(cli_args.affine_params)

    @staticmethod
    def _parse_affine_params(params_str: str) -> dict:
        """Парсинг строки аффинных параметров."""
        count_params = 6
        params = [float(x.strip()) for x in params_str.split(",")]
        if len(params) != count_params:
            logger.critical("Недостаточное число -ap аргументов")
            raise ValueError

        return {
            "a": params[0],
            "b": params[1],
            "c": params[2],
            "d": params[3],
            "e": params[4],
            "f": params[5],
        }

    @staticmethod
    def _parse_functions(functions_str: str) -> list:
        """Парсинг строки функций."""
        functions = []
        for func_str in functions_str.split(","):
            if ":" in func_str:
                name, weight = func_str.split(":", 1)
                functions.append(
                    {"name": name.strip(), "weight": float(weight.strip())}
                )
        return functions

    @staticmethod
    def _read_json(file: str) -> dict:
        """Парсинг JSON конфигурации."""
        with Path.open(file, encoding="utf-8") as f:
            return json.load(f)

    def _apply_json(self, json_config: dict) -> None:
        """Применяем конфигурацию из JSON."""
        try:
            if "size" in json_config:
                self.width = json_config["size"].get("width", self.width)
                self.height = json_config["size"].get("height", self.height)
            else:
                self.width = json_config.get("width", self.width)
                self.height = json_config.get("height", self.height)

            self.seed = json_config.get("seed", self.seed)
            self.iteration_count = json_config.get(
                "iteration_count", self.iteration_count
            )
            self.output_path = json_config.get("output_path", self.output_path)
            self.threads = json_config.get("threads", self.threads)

            if "functions" in json_config:
                self.functions = json_config["functions"]
            if "affine_params" in json_config:
                self.affine_params = json_config["affine_params"]
            if "gamma" in json_config:
                self.gamma = json_config["gamma"]
            if "symmetry_level" in json_config:
                self.symmetry_level = json_config["symmetry_level"]
        except (AttributeError, ValueError, KeyError, TypeError) as e:
            logger.warning(f"Ошибка json конфига: {e}")
