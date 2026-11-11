from abc import ABC, abstractmethod
from typing import Tuple


class BaseUI(ABC):
    """Абстрактный базовый класс для взаимодействия с пользователем."""

    @abstractmethod
    def get_user_input(self) -> Tuple[str, str, str]:
        """Получение трех сторон от пользователя."""
        pass

    @abstractmethod
    def show_message(self, message: str) -> None:
        """Вывод сообщения пользователю."""
        pass


class ConsoleUI(BaseUI):
    """Реализация консольного взаимодействия."""

    def get_user_input(self) -> Tuple[str, str, str]:
        print("\n--- Ввод данных треугольника ---")
        a = input("Введите сторону A: ").strip()
        b = input("Введите сторону B: ").strip()
        c = input("Введите сторону C: ").strip()
        return a, b, c

    def show_message(self, message: str) -> None:
        print(f"[UI]: {message}")