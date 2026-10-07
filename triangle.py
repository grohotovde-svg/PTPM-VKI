import logging
import math
from typing import Tuple, List

def calculate_triangle(str_a: str, str_b: str, str_c: str) -> Tuple[str, List[Tuple[int, int]]]:
    logging.info(f"Получены входные данные: A={str_a}, B={str_b}, C={str_c}")
    
    # 1. Проверка на числовой ввод
    try:
        a = float(str_a)
        b = float(str_b)
        c = float(str_c)
    except (ValueError, TypeError):
        logging.error("Ошибка: переданы нечисловые (невалидные) данные.")
        logging.exception("Детали ошибки конвертации:")
        return "", [(-2, -2), (-2, -2), (-2, -2)]

    epsilon = 1e-9

    # 2. Проверка существования треугольника с учетом точности epsilon
    if a <= 0 or b <= 0 or c <= 0 or not (a + b > c + epsilon and a + c > b + epsilon and b + c > a + epsilon):
        logging.warning(f"Некорректные размеры сторон для треугольника: A={a}, B={b}, C={c}")
        return "не треугольник", [(-1, -1), (-1, -1), (-1, -1)]

    # 3. Определение типа треугольника
    if abs(a - b) < epsilon and abs(b - c) < epsilon:
        t_type = "равносторонний"
    elif abs(a - b) < epsilon or abs(b - c) < epsilon or abs(a - c) < epsilon:
        t_type = "равнобедренный"
    else:
        t_type = "разносторонний"
    
    logging.info(f"Определен тип треугольника: {t_type}")

    # 4. Расчет координат с масштабированием под поле 100x100
    try:
        max_side = max(a, b, c)
        scale = 70.0 / max_side if max_side > 0 else 1.0
        sa = a * scale
        sb = b * scale
        sc = c * scale

        x1, y1 = 10, 80
        x2 = int(x1 + sa)
        y2 = 80

        cos_val = (sb**2 + sc**2 - sa**2) / (2 * sb * sc) if (sb * sc) > 0 else 0
        cos_val = max(-1.0, min(1.0, cos_val))
        sin_val = math.sqrt(1.0 - cos_val**2)

        x3 = int(x1 + sb * cos_val)
        y3 = int(y1 - sb * sin_val)

        coords = [
            (max(0, min(100, x1)), max(0, min(100, y1))),
            (max(0, min(100, x2)), max(0, min(100, y2))),
            (max(0, min(100, x3)), max(0, min(100, y3)))
        ]
        logging.info(f"Рассчитаны координаты вершин: {coords}")
    except Exception as ex:
        logging.error("Ошибка при расчете координат.")
        logging.exception(ex)
        coords = [(-1, -1), (-1, -1), (-1, -1)]

    return t_type, coords