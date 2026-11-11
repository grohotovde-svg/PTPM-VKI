from src.triangle import TriangleCalculator
from src.db_service import DatabaseService
from src.ui_service import BaseUI
from src.external_service import BaseExternalService


class Controller:
    """Контроллер бизнес-логики сквозного сценария."""

    def __init__(
            self,
            calculator: TriangleCalculator,
            db_service: DatabaseService,
            ui_service: BaseUI,
            external_service: BaseExternalService
    ):
        self.calculator = calculator
        self.db = db_service
        self.ui = ui_service
        self.external = external_service

    def process_request(self) -> str:  # <-- Добавлен 'self'
        """
        Сквозной сценарий:
        1. Ввод данных от пользователя.
        2. Проверка наличия записи в БД.
        3. Если есть -> взять из БД. Если нет -> вычислить и записать в БД.
        4. Отправить результат сторонней зависимости.
        5. Возвратить итоговую строку.
        """
        # 1. Запрос данных у пользователя
        a, b, c = self.ui.get_user_input()

        # 2. Проверка базы данных
        cached_record = self.db.get_record(a, b, c)

        if cached_record:
            self.ui.show_message("Данные найдены в базе данных (КЭШ).")
            t_type = cached_record["triangle_type"]
            coords = cached_record["coords"]
            error_msg = cached_record["error_message"]
        else:
            self.ui.show_message("Данные отсутствуют в БД. Выполняется расчет...")
            t_type, coords, error_msg = self.calculator.calculate(a, b, c)
            # Сохранение в БД
            self.db.add_record(a, b, c, t_type, coords, error_msg)

        # Формирование итогового ответа
        if error_msg:
            result_str = f"Ошибка: {error_msg} (Координаты: {coords})"
        else:
            result_str = f"Тип: {t_type}, Координаты: {coords}"

        # 4. Отправка сторонней зависимости
        self.external.send_notification(result_str)

        return result_str