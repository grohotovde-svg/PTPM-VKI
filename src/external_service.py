from abc import ABC, abstractmethod


class BaseExternalService(ABC):
    """Абстрактный интерфейс стороннего сервиса (например, отправка на сервер/email)."""

    @abstractmethod
    def send_notification(self, data_str: str) -> bool:
        """Отправка строки-результата стороннему сервису."""
        pass


class EmailNotificationService(BaseExternalService):
    """Имитация внешней службы отправки уведомлений."""

    def send_notification(self, data_str: str) -> bool:
        # Имитация отправки пакета по сети
        print(f"[Внешний Сервер]: Уведомление успешно отправлено -> '{data_str}'")
        return True