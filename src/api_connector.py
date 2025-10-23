from abc import ABC, abstractmethod
from typing import Any, Dict, List

import requests


class VacancyAPI(ABC):
    """
    Абстрактный класс для работы с API сервисов с вакансиями.
    Определяет интерфейс для получения вакансий с различных платформ.
    """

    def __init__(self):
        """Инициализация базового класса."""
        self._base_url = ""
        self._headers = {}
        self._params = {}

    @abstractmethod
    def _connect_to_api(self) -> bool:
        """
        Приватный метод для подключения к API.

        Returns:
            bool: True если подключение успешно, False в противном случае
        """
        pass

    @abstractmethod
    def get_vacancies(self, keyword: str) -> List[Dict[str, Any]]:
        """
        Получение вакансий по ключевому слову.

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
        Инициализация класса для работы с API HeadHunter.
        Устанавливает базовые параметры для запросов.
        """
        super().__init__()
        self._base_url = "https://api.hh.ru/vacancies"
        self._headers = {"User-Agent": "HH-User-Agent"}
        self._params = {"text": "", "page": 0, "per_page": 100}

    def _connect_to_api(self) -> bool:
        """
        Приватный метод для подключения к API HeadHunter.
        Проверяет доступность API путем отправки тестового запроса.

        Returns:
            bool: True если API доступен, False в противном случае
        """
        try:
            response = requests.get(self._base_url, headers=self._headers, timeout=10)
            return response.status_code == 200
        except requests.RequestException:
            return False

    def get_vacancies(self, keyword: str) -> List[Dict[str, Any]]:
        """
        Получение вакансий с HeadHunter по ключевому слову.

        Args:
            keyword (str): Ключевое слово для поиска вакансий

        Returns:
            List[Dict[str, Any]]: Список вакансий в формате словарей
        """
        if not self._connect_to_api():
            raise ConnectionError("Не удалось подключиться к API HeadHunter")

        self._params["text"] = keyword
        self._params["page"] = 0
        vacancies = []

        # Получаем вакансии с нескольких страниц (максимум 20 страниц)
        while self._params.get("page", 0) < 20:
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
                page_vacancies = data.get("items", [])

                if not page_vacancies:
                    break

                vacancies.extend(page_vacancies)
                self._params["page"] += 1

            except requests.RequestException:
                break

        return vacancies
