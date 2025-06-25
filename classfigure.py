import numpy as np
from stl import mesh
import os
from classresin import Resin

class Figure:
    def __init__(self, name, id, notes, supcoeff, files, postproc, margin, height):
        # Идентификаторы и название
        self.name = name  # Название модели (например, "Дракон")
        self.model_id = id  # Уникальный ID модели (если нужно)
        self.stl_files = files  # Список путей к STL-файлам (если несколько частей)

        # Геометрические параметры
        self.support_coefficient = supcoeff
        self.volume = 0.0  # Объём модели в см³
        self.volume_with_supports = 0.0  # Объём поддержек (если нужны)
        self.height = height
        self.wanted_height = 0

        # Время и дополнительные расходы
        self.print_time_coefficient = 0.06  # Время печати (часы)
        self.postprocessing_hours = postproc  # Доп. обработка (покраска и т. д.)
        self.profit_margin = margin  # Наценка

        # Прочее
        self.price = 0
        self.notes = notes  # Примечания (например, "Хрупкая, нужны поддержки")

    def calculate_volume(self):
        """Вычисляет объём моделей"""
        abs_volume = 0
        for i in self.stl_files:
            model = mesh.Mesh.from_file(i)
            total = 0.0
            for v0, v1, v2 in model.vectors:
                total += np.dot(v0, np.cross(v1, v2)) / 6.0
            abs_volume += abs(total)
        mil_volume = abs_volume * (0.1 ** 3)
        self.volume = mil_volume
        if self.wanted_height != self.height:
            height_coeff = (self.wanted_height / self.height)**3
            self.volume = self.volume * height_coeff
        self.volume_with_supports = self.volume * self.support_coefficient
        return None

    def calculate_price(Figura, Resin):
        Figura.price = ((Figura.volume_with_supports * Resin.density)/1000 * Resin.material_price_per_kg + (Figura.volume_with_supports*Figura.print_time_coefficient+7)*25 + Figura.postprocessing_hours * 500) * Figura.profit_margin
        return None

    def get_model_info(self):
            """Возвращает строку с описанием модели (для отправки пользователю)."""
            info = [str(self.name), self.model_id, str(self.price), str(self.volume), str(self.volume_with_supports), self.notes]
            return info