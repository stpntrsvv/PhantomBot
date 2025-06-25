class Resin:
    def __init__(self, name, price, density):
        # Материал и стоимость
        self.material_type = name  # Тип смолы
        self.material_price_per_kg = price  # Цена за кг смолы (в руб/долл/евро)
        self.density = density  # Плотность смолы (г/см³)


waterwash = Resin("waterwash", 2000, 1.15)
