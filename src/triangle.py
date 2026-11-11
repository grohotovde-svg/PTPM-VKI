import math
from typing import Tuple, List


class TriangleCalculator:
    """Класс вычислений и валидации треугольника."""

    def calculate(self, str_a: str, str_b: str, str_c: str) -> Tuple[str, List[Tuple[int, int]], str]:
        """
        Возвращает: (тип_треугольника, список_координат, сообщение_об_ошибке)
        """
        try:
            a = float(str_a)
            b = float(str_b)
            c = float(str_c)
        except (ValueError, TypeError):
            return "", [(-2, -2), (-2, -2), (-2, -2)], "Нечисловые данные"

        epsilon = 1e-9

        if a <= 0 or b <= 0 or c <= 0 or not (a + b > c + epsilon and a + c > b + epsilon and b + c > a + epsilon):
            return "не треугольник", [(-1, -1), (-1, -1), (-1, -1)], "Некорректные стороны для треугольника"

        if abs(a - b) < epsilon and abs(b - c) < epsilon:
            t_type = "равносторонний"
        elif abs(a - b) < epsilon or abs(b - c) < epsilon or abs(a - c) < epsilon:
            t_type = "равнобедренный"
        else:
            t_type = "разносторонний"

        try:
            max_side = max(a, b, c)
            scale = 70.0 / max_side if max_side > 0 else 1.0
            sa, sb, sc = a * scale, b * scale, c * scale

            x1, y1 = 10, 80
            x2 = int(x1 + sa)
            y2 = 80

            cos_val = (sb ** 2 + sc ** 2 - sa ** 2) / (2 * sb * sc) if (sb * sc) > 0 else 0
            cos_val = max(-1.0, min(1.0, cos_val))
            sin_val = math.sqrt(1.0 - cos_val ** 2)

            x3 = int(x1 + sb * cos_val)
            y3 = int(y1 - sb * sin_val)

            coords = [
                (max(0, min(100, x1)), max(0, min(100, y1))),
                (max(0, min(100, x2)), max(0, min(100, y2))),
                (max(0, min(100, x3)), max(0, min(100, y3)))
            ]
        except Exception as ex:
            return t_type, [(-1, -1), (-1, -1), (-1, -1)], f"Ошибка расчета координат: {ex}"

        return t_type, coords, ""