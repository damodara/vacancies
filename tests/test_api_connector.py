from unittest.mock import Mock, patch

import pytest
import requests

from src.api_connector import HeadHunterAPI, VacancyAPI


class TestVacancyAPI:
    """Тесты для абстрактного класса VacancyAPI."""

    def test_init(self):
        """Тест инициализации базового класса."""

        # Создаем конкретную реализацию для тестирования
        class ConcreteAPI(VacancyAPI):
            def _connect_to_api(self):
                return True

            def get_vacancies(self, keyword):
                return []

        api = ConcreteAPI()
        assert api._base_url == ""
        assert api._headers == {}
        assert api._params == {}


class TestHeadHunterAPI:
    """Тесты для класса HeadHunterAPI."""

    def test_init(self):
        """Тест инициализации HeadHunterAPI."""
        api = HeadHunterAPI()
        assert api._base_url == "https://api.hh.ru/vacancies"
        assert api._headers == {"User-Agent": "HH-User-Agent"}
        assert api._params == {"text": "", "page": 0, "per_page": 100}

    @patch("requests.get")
    def test_connect_to_api_success(self, mock_get):
        """Тест успешного подключения к API."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        api = HeadHunterAPI()
        result = api._connect_to_api()

        assert result is True
        mock_get.assert_called_once()

    @patch("requests.get")
    def test_connect_to_api_failure(self, mock_get):
        """Тест неудачного подключения к API."""
        mock_get.side_effect = requests.RequestException()

        api = HeadHunterAPI()
        result = api._connect_to_api()

        assert result is False

    @patch("requests.get")
    def test_get_vacancies_success(self, mock_get):
        """Тест успешного получения вакансий."""
        # Мокаем ответы API
        mock_response1 = Mock()
        mock_response1.status_code = 200
        mock_response1.json.return_value = {
            "items": [
                {
                    "id": "1",
                    "name": "Test Vacancy",
                    "alternate_url": "https://hh.ru/vacancy/1",
                    "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
                    "snippet": {
                        "requirement": "Test requirements",
                        "responsibility": "Test description",
                    },
                    "employer": {"name": "Test Company"},
                }
            ]
        }

        mock_response2 = Mock()
        mock_response2.status_code = 200
        mock_response2.json.return_value = {"items": []}

        # Первый вызов для проверки подключения, затем два вызова для получения данных
        mock_get.side_effect = [mock_response1, mock_response1, mock_response2]

        api = HeadHunterAPI()
        vacancies = api.get_vacancies("Python")

        assert len(vacancies) == 1
        assert vacancies[0]["name"] == "Test Vacancy"

    @patch("requests.get")
    def test_get_vacancies_connection_error(self, mock_get):
        """Тест ошибки подключения при получении вакансий."""
        mock_get.side_effect = requests.RequestException()

        api = HeadHunterAPI()

        with pytest.raises(ConnectionError):
            api.get_vacancies("Python")

    @patch("requests.get")
    def test_get_vacancies_non_200_status(self, mock_get):
        """Тест получения вакансий с не-200 статусом."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        api = HeadHunterAPI()

        with pytest.raises(ConnectionError):
            api.get_vacancies("Python")

    @patch("requests.get")
    def test_get_vacancies_request_exception_in_loop(self, mock_get):
        """Тест исключения RequestException в цикле получения вакансий."""
        # Первый вызов для проверки подключения успешен
        mock_response1 = Mock()
        mock_response1.status_code = 200

        # Второй вызов в цикле вызывает исключение
        mock_get.side_effect = [mock_response1, requests.RequestException()]

        api = HeadHunterAPI()
        vacancies = api.get_vacancies("Python")

        # Должен вернуть пустой список
        assert vacancies == []

    @patch("requests.get")
    def test_get_vacancies_non_200_status_in_loop(self, mock_get):
        """Тест получения не-200 статуса в цикле получения вакансий."""
        # Первый вызов для проверки подключения успешен
        mock_response1 = Mock()
        mock_response1.status_code = 200

        # Второй вызов в цикле возвращает не-200 статус
        mock_response2 = Mock()
        mock_response2.status_code = 404

        mock_get.side_effect = [mock_response1, mock_response2]

        api = HeadHunterAPI()
        vacancies = api.get_vacancies("Python")

        # Должен вернуть пустой список
        assert vacancies == []

    @patch("requests.get")
    def test_get_vacancies_empty_items(self, mock_get):
        """Тест получения пустого списка items."""
        # Первый вызов для проверки подключения успешен
        mock_response1 = Mock()
        mock_response1.status_code = 200

        # Второй вызов возвращает пустой список items
        mock_response2 = Mock()
        mock_response2.status_code = 200
        mock_response2.json.return_value = {"items": []}

        mock_get.side_effect = [mock_response1, mock_response2]

        api = HeadHunterAPI()
        vacancies = api.get_vacancies("Python")

        # Должен вернуть пустой список
        assert vacancies == []

    @patch("requests.get")
    def test_get_vacancies_missing_items_key(self, mock_get):
        """Тест получения ответа без ключа items."""
        # Первый вызов для проверки подключения успешен
        mock_response1 = Mock()
        mock_response1.status_code = 200

        # Второй вызов возвращает ответ без ключа items
        mock_response2 = Mock()
        mock_response2.status_code = 200
        mock_response2.json.return_value = {"data": []}  # Нет ключа 'items'

        mock_get.side_effect = [mock_response1, mock_response2]

        api = HeadHunterAPI()
        vacancies = api.get_vacancies("Python")

        # Должен вернуть пустой список
        assert vacancies == []
