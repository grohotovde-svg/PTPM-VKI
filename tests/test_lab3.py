import unittest
from unittest.mock import MagicMock, patch
import os

from src.triangle import TriangleCalculator
from src.db_service import DatabaseService
from src.ui_service import ConsoleUI
from src.external_service import EmailNotificationService
from src.controller import Controller


class TestLab3Integration(unittest.TestCase):
    TEST_DB = "test_triangles.db"

    def setUp(self):
        """Подготовка изолированной тестовой базы данных перед каждым тестом."""
        self.db = DatabaseService(db_path=self.TEST_DB)
        self.calculator = TriangleCalculator()
        self.ui = ConsoleUI()
        self.external = EmailNotificationService()

    def tearDown(self):
        """Удаление временной БД после каждого теста."""
        if os.path.exists(self.TEST_DB):
            os.remove(self.TEST_DB)

    # --- ИНТЕГРАЦИОННЫЙ ТЕСТ 1: Первичный расчет и запись в БД ---
    @patch('src.external_service.EmailNotificationService.send_notification')
    @patch('builtins.input', side_effect=["3", "4", "5"])
    def test_integration_first_run_calculates_and_saves_to_db(self, mock_input, mock_external):
        """Интеграция: ввод -> расчёт -> запись в БД -> отправка на внешний сервер."""
        mock_external.return_value = True
        controller = Controller(self.calculator, self.db, self.ui, self.external)

        result = controller.process_request()

        # 1. Проверяем возвращаемое значение
        self.assertIn("разносторонний", result)
        # 2. Проверяем, что запись действительно сохранилась в БД
        record_in_db = self.db.get_record("3", "4", "5")
        self.assertIsNotNone(record_in_db)
        self.assertEqual(record_in_db["triangle_type"], "разносторонний")
        # 3. Проверяем вызов стороннего сервиса
        mock_external.assert_called_once()

    # --- ИНТЕГРАЦИОННЫЙ ТЕСТ 2: Повторный запрос берет данные из БД (КЭШ) ---
    @patch('src.external_service.EmailNotificationService.send_notification')
    @patch('builtins.input', side_effect=["5", "5", "5"])
    def test_integration_second_run_uses_db_cache(self, mock_input, mock_external):
        """Интеграция: если данные уже есть в БД, расчётчик НЕ вызывается повторно."""
        # Заранее кладём данные в БД
        self.db.add_record("5", "5", "5", "равносторонний", [(0,0), (5,0), (2,4)], "")

        # Создаем шпион (Spy/Mock) для калькулятора, чтобы проверить, вызывается ли он
        spy_calculator = TriangleCalculator()
        spy_calculator.calculate = MagicMock()

        controller = Controller(spy_calculator, self.db, self.ui, self.external)
        result = controller.process_request()

        # Проверяем, что данные взяты из БД, а калькулятор НЕ вызвался
        self.assertIn("равносторонний", result)
        spy_calculator.calculate.assert_not_called()
        mock_external.assert_called_once()

    # --- ИНТЕГРАЦИОННЫЙ ТЕСТ 3: Обработка нечисловой ошибки через заглушку ---
    @patch('src.external_service.EmailNotificationService.send_notification')
    @patch('builtins.input', side_effect=["abc", "4", "5"])
    def test_integration_invalid_input_saves_error_to_db(self, mock_input, mock_external):
        """Интеграция: при ошибке ввода сообщение об ошибке фиксируется и сохраняется в БД."""
        controller = Controller(self.calculator, self.db, self.ui, self.external)

        result = controller.process_request()

        self.assertIn("Ошибка: Нечисловые данные", result)
        record = self.db.get_record("abc", "4", "5")
        self.assertIsNotNone(record)
        self.assertEqual(record["error_message"], "Нечисловые данные")

    # --- ЮНИТ-ТЕСТ 4: Проверка работы метода удаления в БД ---
    def test_unit_db_delete_record(self):
        """Юнит-тест изолированной работы метода delete_record в БД."""
        self.db.add_record("7", "7", "7", "равносторонний", [], "")
        self.assertIsNotNone(self.db.get_record("7", "7", "7"))

        deleted = self.db.delete_record("7", "7", "7")
        self.assertTrue(deleted)
        self.assertIsNone(self.db.get_record("7", "7", "7"))

    # --- ЮНИТ-ТЕСТ 5: Изолированная проверка стороннего сервиса ---
    def test_unit_external_service_notification(self):
        """Юнит-тест сторонней зависимости."""
        external = EmailNotificationService()
        res = external.send_notification("Тестовое сообщение")
        self.assertTrue(res)


if __name__ == "__main__":
    unittest.main()