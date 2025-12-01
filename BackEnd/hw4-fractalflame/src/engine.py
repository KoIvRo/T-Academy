import multiprocessing as mp
import random

from config import Config
from histogram import Histogram
from logger_config import logger
from measure import measure_time
from models import Color, Point
from transform import TransformationSystem


class FractalEngine:
    """Класс для генерирования."""

    def __init__(self, config: Config) -> None:
        self.config = config
        self.transform = TransformationSystem(config.functions, config.affine_params)

    def generate(self) -> Histogram:
        """Точка входа в генерацию."""
        try:
            if self.config.threads == 1:
                return self._single_thread_generate()
            return self._multi_thread_generate()
        except (ValueError, AttributeError, ArithmeticError) as e:
            logger.critical(f"Гистограмма не была создана: {e}")

    @measure_time("Гистограмма создана.")
    def _single_thread_generate(self) -> Histogram:
        hist = Histogram(
            self.config.width,
            self.config.height,
            self.config.gamma,
            self.config.symmetry_level,
        )
        random.seed(self.config.seed)
        point = Point(random.uniform(-1, 1), random.uniform(-1, 1))
        color = Color(0, 0, 0)

        for _ in range(self.config.iteration_count):
            point, color = self.transform.transform_point(point, color)

            hist.add_point(point, color)

        return hist

    def _multi_thread_generate(self) -> Histogram:
        try:
            worker_args = self._create_worker_args()

            logger.info(f"Созданно {self.config.threads} процесса")

            # Запускаем нужное число процессов - _worker
            with mp.Pool(processes=self.config.threads) as pool:
                workers = pool.map(self._worker, worker_args)

            return self._merge_histograms(workers)
        except (mp.TimeoutError, mp.ProcessError, MemoryError) as e:
            logger.critical(e)

    def _create_worker_args(self) -> list[tuple]:
        worker_iter = self.config.iteration_count // self.config.threads

        return [(worker_id, worker_iter) for worker_id in range(self.config.threads)]

    @measure_time("Один из процессов выполнил свою работу.")
    def _worker(self, args: tuple) -> Histogram:
        """Независмый генератор."""
        worker_id, iter_count = args
        local_hist = Histogram(
            self.config.width,
            self.config.height,
            self.config.gamma,
            self.config.symmetry_level,
        )

        random.seed(self.config.seed + worker_id)

        point = Point(random.uniform(-1, 1), random.uniform(-1, 1))
        color = Color(0, 0, 0)

        for _ in range(iter_count):
            point, color = self.transform.transform_point(point, color)

            local_hist.add_point(point, color)

        return local_hist

    @measure_time("Гистограммы обедединены.")
    def _merge_histograms(self, histograms: list) -> Histogram:
        merged_hist = histograms[0]

        for hist in histograms[1:]:
            for (x, y), data in hist.data.items():
                if (x, y) in merged_hist.data:
                    # Суммируем count и color
                    merged_hist.data[(x, y)]["count"] += data["count"]
                    old_color = merged_hist.data[(x, y)]["color"]
                    merged_hist.data[(x, y)]["color"] = (
                        old_color[0] + data["color"][0],
                        old_color[1] + data["color"][1],
                        old_color[2] + data["color"][2],
                    )
                else:
                    # Копируем данные
                    merged_hist.data[(x, y)] = {
                        "count": data["count"],
                        "color": data["color"],
                    }

        return merged_hist
