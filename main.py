import os
import sys
import logging
from triangle import calculate_triangle

def main():
    # Создаем директорию для логов, если её нет
    os.makedirs("logs", exist_ok=True)

    log_format = "%(asctime)s | [%(levelname)-7s] | %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    # Базовая настройка логирования
    logging.basicConfig(
        level=logging.DEBUG,
        format=log_format,
        datefmt=date_format,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("logs/file_txt.log", encoding="utf-8")
        ]
    )

    logging.info("Логгер успешно сконфигурирован")
    logging.info("Приложение запущено")

    # Бесконечный цикл для ручного ввода
    while True:
        try:
            user_input = input("\nВведите стороны a, b, c через пробел (или 'q' для выхода): ").strip()
            
            if user_input.lower() == 'q':
                print("Выход из программы. Логи сохранены в logs/file_txt.log.")
                logging.info("Приложение остановлено пользователем.")
                break
                
            parts = user_input.split()
            if len(parts) != 3:
                print("Ошибка: нужно ввести ровно три значения через пробел!")
                continue
                
            t_type, coords = calculate_triangle(parts[0], parts[1], parts[2])
            
            if t_type == "":
                print("Ошибка: введены нечисловые значения.")
            elif t_type == "не треугольник":
                print("Треугольник с такими сторонами не существует.")
            else:
                print(f"Тип треугольника: {t_type}")
                print(f"Координаты вершин: {coords}")

        except KeyboardInterrupt:
            print("\nПрограмма прервана с клавиатуры.")
            logging.info("Приложение завершено пользователем через Ctrl+C.")
            break

if __name__ == "__main__":
    main() 