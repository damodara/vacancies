from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
import requests


class VacancyAPI(ABC):
    """
    Абстрактный класс для работы с API сервисов с вакансиями.
    Определяет интерфейс для получения вакансий с различных платформ.
    """

    def __init__(self):
        """Инициализация базового класса."""
        self._base_url: str = ""  # Базовый URL сервиса
        self._headers: Dict[str, str] = {}  # Заголовки для запросов
        self._params: Dict[str, Any] = {}  # Параметры для запросов

    @abstractmethod
    def _connect_to_api(self) -> bool:
        """
        Приватный метод для проверки доступности API.

        Returns:
            bool: True если соединение успешно установлено, иначе False
        """
        pass

    @abstractmethod
    def get_vacancies(self, keyword: str) -> List[Dict[str, Any]]:
        """
        Получение списка вакансий по указанному ключевому слову.

        Args:
            keyword (str): Ключевое слово для поиска вакансий

        Returns:
            List[Dict[str, Any]]: Список вакансий в формате словарей
        """
        pass


class HeadHunterAPI(VacancyAPI):
    """
    Класс для работы с API HeadHunter.
    Наследуется от абстрактного класса VacancyAPI.
    """

    def __init__(self):
        """
        Инициализирует экземпляр класса HeadHunterAPI.
        Устанавливает необходимые заголовки и параметры для запросов.
        """
        super().__init__()
        self._base_url = "https://api.hh.ru/vacancies"
        self._headers = {"User-Agent": "HH-User-Agent"}  # Используемые заголовки
        self._params = {
            "text": "",
            "page": 0,
            "per_page": 100  # Количество результатов на странице
        }

    def _connect_to_api(self) -> bool:
        """
        Проверяет доступность API HeadHunter путём отправки тестового запроса.

        Returns:
            bool: True если API доступен, иначе False
        """
        try:
            response = requests.get(self._base_url, headers=self._headers, timeout=10)
            return response.status_code == 200
        except requests.RequestException as e:
            print(f"Произошла ошибка при проверке связи с API: {e}")
            return False

    def get_vacancies(self, keyword: str) -> List[Dict[str, Any]]:
        """
        Получает список вакансий с HeadHunter по заданному ключевому слову.

        Args:
            keyword (str): Поисковый запрос

        Raises:
            ConnectionError: Если невозможно установить соединение с API

        Returns:
            List[Dict[str, Any]]: Список вакансий в формате словарей
        """
        if not self._connect_to_api():
            raise ConnectionError("Ошибка соединения с API HeadHunter.")

        self._params["text"] = keyword  # Устанавливаем искомый термин
        self._params["page"] = 0  # Начинаем с первой страницы
        vacancies: List[Dict[str, Any]] = []  # Результат поиска

        total_pages: int = 0  # Всего страниц для просмотра
        current_page: int = 0  # Текущая страница

        while current_page <= min(total_pages, 20):  # Ограничиваем просмотр максимум 20-ю страницами
            try:
                response = requests.get(
                    self._base_url,
                    headers=self._headers,
                    params=self._params,
                    timeout=10,
                )

                if response.status_code != 200:
                    break

                data = response.json()
                page_vacancies = data.get("items", [])  # Извлекаем список вакансий

                if len(page_vacancies) > 0:
                    vacancies.extend(page_vacancies)
                    total_pages = data.get("pages", 0)  # Максимальное число страниц
                    current_page += 1
                    self._params["page"] = current_page
                else:
                    break

            except requests.RequestException as e:
                print(f"Произошла ошибка при получении данных: {e}")
                break

        return vacancies