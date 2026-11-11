from src.triangle import TriangleCalculator
from src.db_service import DatabaseService
from src.ui_service import ConsoleUI
from src.external_service import EmailNotificationService
from src.controller import Controller


def main():
    calculator = TriangleCalculator()
    db_service = DatabaseService()
    ui_service = ConsoleUI()
    external_service = EmailNotificationService()

    controller = Controller(calculator, db_service, ui_service, external_service)

    print("=== ЗАПУСК ПРИЛОЖЕНИЯ (ЛР3) ===")
    result = controller.process_request()
    print(f"\n[Итоговый результат работы контроллера]: {result}")


if __name__ == "__main__":
    main()