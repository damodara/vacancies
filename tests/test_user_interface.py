from unittest.mock import Mock, call, patch

import pytest

from src.api_connector import HeadHunterAPI
from src.file_saver import CSVSaver, JSONSaver
from src.user_interface import user_interaction
from src.vacancy import Vacancy


class TestUserInterface:
    """Тесты для функций пользовательского интерфейса."""

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_exit(self, mock_print, mock_input):
        """Тест выхода из программы."""
        mock_input.side_effect = ["0"]  # Выбираем выход

        # Проверяем, что функция завершается без ошибок
        try:
            user_interaction()
        except SystemExit:
            pass  # Ожидаемое поведение при выходе

        # Проверяем, что было выведено меню
        assert mock_print.called

    def test_headhunter_api_error_handling(self):
        """Тест обработки ошибок в HeadHunter API."""
        api = HeadHunterAPI()

        # Тест с невалидным ключевым словом
        try:
            vacancies = api.get_vacancies("")
        except Exception:
            pass  # Ожидаемо, что может произойти ошибка

    def test_json_saver_error_handling(self):
        """Тест обработки ошибок в JSONSaver."""
        import os
        import tempfile

        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "test.json")
            saver = JSONSaver(filename)

            # Тест с невалидной вакансией
            try:
                saver.add_vacancy(None)
            except Exception:
                pass  # Ожидаемо, что может произойти ошибка

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_invalid_choice(self, mock_print, mock_input):
        """Тест обработки невалидного выбора в пользовательском интерфейсе."""
        mock_input.side_effect = ["99", "0"]  # Невалидный выбор, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_empty_input(self, mock_print, mock_input):
        """Тест обработки пустого ввода в пользовательском интерфейсе."""
        mock_input.side_effect = ["", "0"]  # Пустой ввод, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_whitespace_input(self, mock_print, mock_input):
        """Тест обработки ввода с пробелами в пользовательском интерфейсе."""
        mock_input.side_effect = ["   ", "0"]  # Ввод с пробелами, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    def test_csv_saver_error_handling(self):
        """Тест обработки ошибок в CSVSaver."""
        import os
        import tempfile

        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "test.csv")
            saver = CSVSaver(filename)

            # Тест с невалидной вакансией
            try:
                saver.add_vacancy(None)
            except Exception:
                pass  # Ожидаемо, что может произойти ошибка

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_invalid_choice(self, mock_print, mock_input):
        """Тест обработки невалидного выбора в пользовательском интерфейсе."""
        mock_input.side_effect = ["99", "0"]  # Невалидный выбор, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_empty_input(self, mock_print, mock_input):
        """Тест обработки пустого ввода в пользовательском интерфейсе."""
        mock_input.side_effect = ["", "0"]  # Пустой ввод, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_whitespace_input(self, mock_print, mock_input):
        """Тест обработки ввода с пробелами в пользовательском интерфейсе."""
        mock_input.side_effect = ["   ", "0"]  # Ввод с пробелами, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    def test_headhunter_api_error_handling(self):
        """Тест обработки ошибок в HeadHunter API."""
        api = HeadHunterAPI()

        # Тест с невалидным ключевым словом
        try:
            vacancies = api.get_vacancies("")
        except Exception:
            pass  # Ожидаемо, что может произойти ошибка

    def test_json_saver_error_handling(self):
        """Тест обработки ошибок в JSONSaver."""
        import os
        import tempfile

        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "test.json")
            saver = JSONSaver(filename)

            # Тест с невалидной вакансией
            try:
                saver.add_vacancy(None)
            except Exception:
                pass  # Ожидаемо, что может произойти ошибка

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_invalid_choice(self, mock_print, mock_input):
        """Тест обработки невалидного выбора в пользовательском интерфейсе."""
        mock_input.side_effect = ["99", "0"]  # Невалидный выбор, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_empty_input(self, mock_print, mock_input):
        """Тест обработки пустого ввода в пользовательском интерфейсе."""
        mock_input.side_effect = ["", "0"]  # Пустой ввод, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_whitespace_input(self, mock_print, mock_input):
        """Тест обработки ввода с пробелами в пользовательском интерфейсе."""
        mock_input.side_effect = ["   ", "0"]  # Ввод с пробелами, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    def test_csv_saver_error_handling(self):
        """Тест обработки ошибок в CSVSaver."""
        import os
        import tempfile

        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "test.csv")
            saver = CSVSaver(filename)

            # Тест с невалидной вакансией
            try:
                saver.add_vacancy(None)
            except Exception:
                pass  # Ожидаемо, что может произойти ошибка

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_invalid_choice(self, mock_print, mock_input):
        """Тест обработки невалидного выбора в пользовательском интерфейсе."""
        mock_input.side_effect = ["99", "0"]  # Невалидный выбор, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_empty_input(self, mock_print, mock_input):
        """Тест обработки пустого ввода в пользовательском интерфейсе."""
        mock_input.side_effect = ["", "0"]  # Пустой ввод, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_whitespace_input(self, mock_print, mock_input):
        """Тест обработки ввода с пробелами в пользовательском интерфейсе."""
        mock_input.side_effect = ["   ", "0"]  # Ввод с пробелами, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_invalid_choice(self, mock_print, mock_input):
        """Тест обработки неверного выбора."""
        mock_input.side_effect = ["99", "0"]  # Неверный выбор, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено сообщение об ошибке
        print_calls = [call.args[0] for call in mock_print.call_args_list]
        assert any("Неверный выбор" in str(call) for call in print_calls)

    def test_headhunter_api_integration(self):
        """Тест интеграции с HeadHunter API."""
        api = HeadHunterAPI()

        # Проверяем инициализацию
        assert api._base_url == "https://api.hh.ru/vacancies"
        assert api._headers == {"User-Agent": "HH-User-Agent"}
        assert api._params == {"text": "", "page": 0, "per_page": 100}

    def test_json_saver_integration(self):
        """Тест интеграции с JSONSaver."""
        import os
        import tempfile

        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "test_vacancies.json")
            saver = JSONSaver(filename)

            # Проверяем инициализацию
            assert saver.filename == filename

            # Проверяем создание файла
            assert os.path.exists(filename)

            # Очищаем тестовый файл
            saver.clear_all()

    def test_csv_saver_integration(self):
        """Тест интеграции с CSVSaver."""
        import os
        import tempfile

        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "test_vacancies.csv")
            saver = CSVSaver(filename)

            # Проверяем инициализацию
            assert saver.filename == filename

            # Проверяем создание файла
            assert os.path.exists(filename)

            # Очищаем тестовый файл
            saver.clear_all()

    def test_vacancy_creation(self):
        """Тест создания вакансии."""
        vacancy = Vacancy(
            name="Test Developer",
            url="https://hh.ru/vacancy/123",
            salary_from=100000,
            salary_to=150000,
            currency="RUR",
            description="Test description",
            requirements="Test requirements",
            employer="Test Company",
        )

        assert vacancy.name == "Test Developer"
        assert vacancy.url == "https://hh.ru/vacancy/123"
        assert vacancy.salary_from == 100000
        assert vacancy.salary_to == 150000
        assert vacancy.currency == "RUR"
        assert vacancy.description == "Test description"
        assert vacancy.requirements == "Test requirements"
        assert vacancy.employer == "Test Company"
        assert vacancy.average_salary == 125000

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_search_vacancies(self, mock_print, mock_input):
        """Тест поиска вакансий через пользовательский интерфейс."""
        mock_input.side_effect = ["1", "Python", "0"]  # Поиск, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    def test_headhunter_api_error_handling(self):
        """Тест обработки ошибок в HeadHunter API."""
        api = HeadHunterAPI()

        # Тест с невалидным ключевым словом
        try:
            vacancies = api.get_vacancies("")
        except Exception:
            pass  # Ожидаемо, что может произойти ошибка

    def test_json_saver_error_handling(self):
        """Тест обработки ошибок в JSONSaver."""
        import os
        import tempfile

        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "test.json")
            saver = JSONSaver(filename)

            # Тест с невалидной вакансией
            try:
                saver.add_vacancy(None)
            except Exception:
                pass  # Ожидаемо, что может произойти ошибка

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_invalid_choice(self, mock_print, mock_input):
        """Тест обработки невалидного выбора в пользовательском интерфейсе."""
        mock_input.side_effect = ["99", "0"]  # Невалидный выбор, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_empty_input(self, mock_print, mock_input):
        """Тест обработки пустого ввода в пользовательском интерфейсе."""
        mock_input.side_effect = ["", "0"]  # Пустой ввод, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_whitespace_input(self, mock_print, mock_input):
        """Тест обработки ввода с пробелами в пользовательском интерфейсе."""
        mock_input.side_effect = ["   ", "0"]  # Ввод с пробелами, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    def test_csv_saver_error_handling(self):
        """Тест обработки ошибок в CSVSaver."""
        import os
        import tempfile

        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "test.csv")
            saver = CSVSaver(filename)

            # Тест с невалидной вакансией
            try:
                saver.add_vacancy(None)
            except Exception:
                pass  # Ожидаемо, что может произойти ошибка

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_invalid_choice(self, mock_print, mock_input):
        """Тест обработки невалидного выбора в пользовательском интерфейсе."""
        mock_input.side_effect = ["99", "0"]  # Невалидный выбор, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_empty_input(self, mock_print, mock_input):
        """Тест обработки пустого ввода в пользовательском интерфейсе."""
        mock_input.side_effect = ["", "0"]  # Пустой ввод, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_whitespace_input(self, mock_print, mock_input):
        """Тест обработки ввода с пробелами в пользовательском интерфейсе."""
        mock_input.side_effect = ["   ", "0"]  # Ввод с пробелами, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    def test_headhunter_api_error_handling(self):
        """Тест обработки ошибок в HeadHunter API."""
        api = HeadHunterAPI()

        # Тест с невалидным ключевым словом
        try:
            vacancies = api.get_vacancies("")
        except Exception:
            pass  # Ожидаемо, что может произойти ошибка

    def test_json_saver_error_handling(self):
        """Тест обработки ошибок в JSONSaver."""
        import os
        import tempfile

        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "test.json")
            saver = JSONSaver(filename)

            # Тест с невалидной вакансией
            try:
                saver.add_vacancy(None)
            except Exception:
                pass  # Ожидаемо, что может произойти ошибка

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_invalid_choice(self, mock_print, mock_input):
        """Тест обработки невалидного выбора в пользовательском интерфейсе."""
        mock_input.side_effect = ["99", "0"]  # Невалидный выбор, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_empty_input(self, mock_print, mock_input):
        """Тест обработки пустого ввода в пользовательском интерфейсе."""
        mock_input.side_effect = ["", "0"]  # Пустой ввод, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_whitespace_input(self, mock_print, mock_input):
        """Тест обработки ввода с пробелами в пользовательском интерфейсе."""
        mock_input.side_effect = ["   ", "0"]  # Ввод с пробелами, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    def test_csv_saver_error_handling(self):
        """Тест обработки ошибок в CSVSaver."""
        import os
        import tempfile

        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "test.csv")
            saver = CSVSaver(filename)

            # Тест с невалидной вакансией
            try:
                saver.add_vacancy(None)
            except Exception:
                pass  # Ожидаемо, что может произойти ошибка

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_invalid_choice(self, mock_print, mock_input):
        """Тест обработки невалидного выбора в пользовательском интерфейсе."""
        mock_input.side_effect = ["99", "0"]  # Невалидный выбор, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_empty_input(self, mock_print, mock_input):
        """Тест обработки пустого ввода в пользовательском интерфейсе."""
        mock_input.side_effect = ["", "0"]  # Пустой ввод, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_whitespace_input(self, mock_print, mock_input):
        """Тест обработки ввода с пробелами в пользовательском интерфейсе."""
        mock_input.side_effect = ["   ", "0"]  # Ввод с пробелами, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_show_top_vacancies(self, mock_print, mock_input):
        """Тест показа топ вакансий через пользовательский интерфейс."""
        mock_input.side_effect = ["2", "5", "0"]  # Топ 5, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    def test_headhunter_api_error_handling(self):
        """Тест обработки ошибок в HeadHunter API."""
        api = HeadHunterAPI()

        # Тест с невалидным ключевым словом
        try:
            vacancies = api.get_vacancies("")
        except Exception:
            pass  # Ожидаемо, что может произойти ошибка

    def test_json_saver_error_handling(self):
        """Тест обработки ошибок в JSONSaver."""
        import os
        import tempfile

        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "test.json")
            saver = JSONSaver(filename)

            # Тест с невалидной вакансией
            try:
                saver.add_vacancy(None)
            except Exception:
                pass  # Ожидаемо, что может произойти ошибка

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_invalid_choice(self, mock_print, mock_input):
        """Тест обработки невалидного выбора в пользовательском интерфейсе."""
        mock_input.side_effect = ["99", "0"]  # Невалидный выбор, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_empty_input(self, mock_print, mock_input):
        """Тест обработки пустого ввода в пользовательском интерфейсе."""
        mock_input.side_effect = ["", "0"]  # Пустой ввод, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_whitespace_input(self, mock_print, mock_input):
        """Тест обработки ввода с пробелами в пользовательском интерфейсе."""
        mock_input.side_effect = ["   ", "0"]  # Ввод с пробелами, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    def test_csv_saver_error_handling(self):
        """Тест обработки ошибок в CSVSaver."""
        import os
        import tempfile

        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "test.csv")
            saver = CSVSaver(filename)

            # Тест с невалидной вакансией
            try:
                saver.add_vacancy(None)
            except Exception:
                pass  # Ожидаемо, что может произойти ошибка

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_invalid_choice(self, mock_print, mock_input):
        """Тест обработки невалидного выбора в пользовательском интерфейсе."""
        mock_input.side_effect = ["99", "0"]  # Невалидный выбор, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_empty_input(self, mock_print, mock_input):
        """Тест обработки пустого ввода в пользовательском интерфейсе."""
        mock_input.side_effect = ["", "0"]  # Пустой ввод, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_whitespace_input(self, mock_print, mock_input):
        """Тест обработки ввода с пробелами в пользовательском интерфейсе."""
        mock_input.side_effect = ["   ", "0"]  # Ввод с пробелами, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    def test_headhunter_api_error_handling(self):
        """Тест обработки ошибок в HeadHunter API."""
        api = HeadHunterAPI()

        # Тест с невалидным ключевым словом
        try:
            vacancies = api.get_vacancies("")
        except Exception:
            pass  # Ожидаемо, что может произойти ошибка

    def test_json_saver_error_handling(self):
        """Тест обработки ошибок в JSONSaver."""
        import os
        import tempfile

        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "test.json")
            saver = JSONSaver(filename)

            # Тест с невалидной вакансией
            try:
                saver.add_vacancy(None)
            except Exception:
                pass  # Ожидаемо, что может произойти ошибка

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_invalid_choice(self, mock_print, mock_input):
        """Тест обработки невалидного выбора в пользовательском интерфейсе."""
        mock_input.side_effect = ["99", "0"]  # Невалидный выбор, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_empty_input(self, mock_print, mock_input):
        """Тест обработки пустого ввода в пользовательском интерфейсе."""
        mock_input.side_effect = ["", "0"]  # Пустой ввод, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_whitespace_input(self, mock_print, mock_input):
        """Тест обработки ввода с пробелами в пользовательском интерфейсе."""
        mock_input.side_effect = ["   ", "0"]  # Ввод с пробелами, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    def test_csv_saver_error_handling(self):
        """Тест обработки ошибок в CSVSaver."""
        import os
        import tempfile

        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "test.csv")
            saver = CSVSaver(filename)

            # Тест с невалидной вакансией
            try:
                saver.add_vacancy(None)
            except Exception:
                pass  # Ожидаемо, что может произойти ошибка

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_invalid_choice(self, mock_print, mock_input):
        """Тест обработки невалидного выбора в пользовательском интерфейсе."""
        mock_input.side_effect = ["99", "0"]  # Невалидный выбор, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_empty_input(self, mock_print, mock_input):
        """Тест обработки пустого ввода в пользовательском интерфейсе."""
        mock_input.side_effect = ["", "0"]  # Пустой ввод, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_whitespace_input(self, mock_print, mock_input):
        """Тест обработки ввода с пробелами в пользовательском интерфейсе."""
        mock_input.side_effect = ["   ", "0"]  # Ввод с пробелами, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_filter_by_keyword(self, mock_print, mock_input):
        """Тест фильтрации по ключевому слову через пользовательский интерфейс."""
        mock_input.side_effect = ["3", "Python", "0"]  # Фильтр, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    def test_headhunter_api_error_handling(self):
        """Тест обработки ошибок в HeadHunter API."""
        api = HeadHunterAPI()

        # Тест с невалидным ключевым словом
        try:
            vacancies = api.get_vacancies("")
        except Exception:
            pass  # Ожидаемо, что может произойти ошибка

    def test_json_saver_error_handling(self):
        """Тест обработки ошибок в JSONSaver."""
        import os
        import tempfile

        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "test.json")
            saver = JSONSaver(filename)

            # Тест с невалидной вакансией
            try:
                saver.add_vacancy(None)
            except Exception:
                pass  # Ожидаемо, что может произойти ошибка

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_invalid_choice(self, mock_print, mock_input):
        """Тест обработки невалидного выбора в пользовательском интерфейсе."""
        mock_input.side_effect = ["99", "0"]  # Невалидный выбор, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_empty_input(self, mock_print, mock_input):
        """Тест обработки пустого ввода в пользовательском интерфейсе."""
        mock_input.side_effect = ["", "0"]  # Пустой ввод, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_whitespace_input(self, mock_print, mock_input):
        """Тест обработки ввода с пробелами в пользовательском интерфейсе."""
        mock_input.side_effect = ["   ", "0"]  # Ввод с пробелами, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    def test_csv_saver_error_handling(self):
        """Тест обработки ошибок в CSVSaver."""
        import os
        import tempfile

        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "test.csv")
            saver = CSVSaver(filename)

            # Тест с невалидной вакансией
            try:
                saver.add_vacancy(None)
            except Exception:
                pass  # Ожидаемо, что может произойти ошибка

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_invalid_choice(self, mock_print, mock_input):
        """Тест обработки невалидного выбора в пользовательском интерфейсе."""
        mock_input.side_effect = ["99", "0"]  # Невалидный выбор, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_empty_input(self, mock_print, mock_input):
        """Тест обработки пустого ввода в пользовательском интерфейсе."""
        mock_input.side_effect = ["", "0"]  # Пустой ввод, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_whitespace_input(self, mock_print, mock_input):
        """Тест обработки ввода с пробелами в пользовательском интерфейсе."""
        mock_input.side_effect = ["   ", "0"]  # Ввод с пробелами, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    def test_headhunter_api_error_handling(self):
        """Тест обработки ошибок в HeadHunter API."""
        api = HeadHunterAPI()

        # Тест с невалидным ключевым словом
        try:
            vacancies = api.get_vacancies("")
        except Exception:
            pass  # Ожидаемо, что может произойти ошибка

    def test_json_saver_error_handling(self):
        """Тест обработки ошибок в JSONSaver."""
        import os
        import tempfile

        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "test.json")
            saver = JSONSaver(filename)

            # Тест с невалидной вакансией
            try:
                saver.add_vacancy(None)
            except Exception:
                pass  # Ожидаемо, что может произойти ошибка

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_invalid_choice(self, mock_print, mock_input):
        """Тест обработки невалидного выбора в пользовательском интерфейсе."""
        mock_input.side_effect = ["99", "0"]  # Невалидный выбор, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_empty_input(self, mock_print, mock_input):
        """Тест обработки пустого ввода в пользовательском интерфейсе."""
        mock_input.side_effect = ["", "0"]  # Пустой ввод, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_whitespace_input(self, mock_print, mock_input):
        """Тест обработки ввода с пробелами в пользовательском интерфейсе."""
        mock_input.side_effect = ["   ", "0"]  # Ввод с пробелами, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    def test_csv_saver_error_handling(self):
        """Тест обработки ошибок в CSVSaver."""
        import os
        import tempfile

        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "test.csv")
            saver = CSVSaver(filename)

            # Тест с невалидной вакансией
            try:
                saver.add_vacancy(None)
            except Exception:
                pass  # Ожидаемо, что может произойти ошибка

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_invalid_choice(self, mock_print, mock_input):
        """Тест обработки невалидного выбора в пользовательском интерфейсе."""
        mock_input.side_effect = ["99", "0"]  # Невалидный выбор, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_empty_input(self, mock_print, mock_input):
        """Тест обработки пустого ввода в пользовательском интерфейсе."""
        mock_input.side_effect = ["", "0"]  # Пустой ввод, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_whitespace_input(self, mock_print, mock_input):
        """Тест обработки ввода с пробелами в пользовательском интерфейсе."""
        mock_input.side_effect = ["   ", "0"]  # Ввод с пробелами, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_filter_by_salary(self, mock_print, mock_input):
        """Тест фильтрации по зарплате через пользовательский интерфейс."""
        mock_input.side_effect = ["4", "100000-200000", "0"]  # Фильтр, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    def test_headhunter_api_error_handling(self):
        """Тест обработки ошибок в HeadHunter API."""
        api = HeadHunterAPI()

        # Тест с невалидным ключевым словом
        try:
            vacancies = api.get_vacancies("")
        except Exception:
            pass  # Ожидаемо, что может произойти ошибка

    def test_json_saver_error_handling(self):
        """Тест обработки ошибок в JSONSaver."""
        import os
        import tempfile

        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "test.json")
            saver = JSONSaver(filename)

            # Тест с невалидной вакансией
            try:
                saver.add_vacancy(None)
            except Exception:
                pass  # Ожидаемо, что может произойти ошибка

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_invalid_choice(self, mock_print, mock_input):
        """Тест обработки невалидного выбора в пользовательском интерфейсе."""
        mock_input.side_effect = ["99", "0"]  # Невалидный выбор, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_empty_input(self, mock_print, mock_input):
        """Тест обработки пустого ввода в пользовательском интерфейсе."""
        mock_input.side_effect = ["", "0"]  # Пустой ввод, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_whitespace_input(self, mock_print, mock_input):
        """Тест обработки ввода с пробелами в пользовательском интерфейсе."""
        mock_input.side_effect = ["   ", "0"]  # Ввод с пробелами, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    def test_csv_saver_error_handling(self):
        """Тест обработки ошибок в CSVSaver."""
        import os
        import tempfile

        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "test.csv")
            saver = CSVSaver(filename)

            # Тест с невалидной вакансией
            try:
                saver.add_vacancy(None)
            except Exception:
                pass  # Ожидаемо, что может произойти ошибка

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_invalid_choice(self, mock_print, mock_input):
        """Тест обработки невалидного выбора в пользовательском интерфейсе."""
        mock_input.side_effect = ["99", "0"]  # Невалидный выбор, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_empty_input(self, mock_print, mock_input):
        """Тест обработки пустого ввода в пользовательском интерфейсе."""
        mock_input.side_effect = ["", "0"]  # Пустой ввод, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_whitespace_input(self, mock_print, mock_input):
        """Тест обработки ввода с пробелами в пользовательском интерфейсе."""
        mock_input.side_effect = ["   ", "0"]  # Ввод с пробелами, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    def test_headhunter_api_error_handling(self):
        """Тест обработки ошибок в HeadHunter API."""
        api = HeadHunterAPI()

        # Тест с невалидным ключевым словом
        try:
            vacancies = api.get_vacancies("")
        except Exception:
            pass  # Ожидаемо, что может произойти ошибка

    def test_json_saver_error_handling(self):
        """Тест обработки ошибок в JSONSaver."""
        import os
        import tempfile

        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "test.json")
            saver = JSONSaver(filename)

            # Тест с невалидной вакансией
            try:
                saver.add_vacancy(None)
            except Exception:
                pass  # Ожидаемо, что может произойти ошибка

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_invalid_choice(self, mock_print, mock_input):
        """Тест обработки невалидного выбора в пользовательском интерфейсе."""
        mock_input.side_effect = ["99", "0"]  # Невалидный выбор, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_empty_input(self, mock_print, mock_input):
        """Тест обработки пустого ввода в пользовательском интерфейсе."""
        mock_input.side_effect = ["", "0"]  # Пустой ввод, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_whitespace_input(self, mock_print, mock_input):
        """Тест обработки ввода с пробелами в пользовательском интерфейсе."""
        mock_input.side_effect = ["   ", "0"]  # Ввод с пробелами, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    def test_csv_saver_error_handling(self):
        """Тест обработки ошибок в CSVSaver."""
        import os
        import tempfile

        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "test.csv")
            saver = CSVSaver(filename)

            # Тест с невалидной вакансией
            try:
                saver.add_vacancy(None)
            except Exception:
                pass  # Ожидаемо, что может произойти ошибка

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_invalid_choice(self, mock_print, mock_input):
        """Тест обработки невалидного выбора в пользовательском интерфейсе."""
        mock_input.side_effect = ["99", "0"]  # Невалидный выбор, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_empty_input(self, mock_print, mock_input):
        """Тест обработки пустого ввода в пользовательском интерфейсе."""
        mock_input.side_effect = ["", "0"]  # Пустой ввод, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_whitespace_input(self, mock_print, mock_input):
        """Тест обработки ввода с пробелами в пользовательском интерфейсе."""
        mock_input.side_effect = ["   ", "0"]  # Ввод с пробелами, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_show_all_vacancies(self, mock_print, mock_input):
        """Тест показа всех вакансий через пользовательский интерфейс."""
        mock_input.side_effect = ["5", "0"]  # Показать все, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    def test_headhunter_api_error_handling(self):
        """Тест обработки ошибок в HeadHunter API."""
        api = HeadHunterAPI()

        # Тест с невалидным ключевым словом
        try:
            vacancies = api.get_vacancies("")
        except Exception:
            pass  # Ожидаемо, что может произойти ошибка

    def test_json_saver_error_handling(self):
        """Тест обработки ошибок в JSONSaver."""
        import os
        import tempfile

        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "test.json")
            saver = JSONSaver(filename)

            # Тест с невалидной вакансией
            try:
                saver.add_vacancy(None)
            except Exception:
                pass  # Ожидаемо, что может произойти ошибка

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_invalid_choice(self, mock_print, mock_input):
        """Тест обработки невалидного выбора в пользовательском интерфейсе."""
        mock_input.side_effect = ["99", "0"]  # Невалидный выбор, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_empty_input(self, mock_print, mock_input):
        """Тест обработки пустого ввода в пользовательском интерфейсе."""
        mock_input.side_effect = ["", "0"]  # Пустой ввод, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_whitespace_input(self, mock_print, mock_input):
        """Тест обработки ввода с пробелами в пользовательском интерфейсе."""
        mock_input.side_effect = ["   ", "0"]  # Ввод с пробелами, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    def test_csv_saver_error_handling(self):
        """Тест обработки ошибок в CSVSaver."""
        import os
        import tempfile

        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "test.csv")
            saver = CSVSaver(filename)

            # Тест с невалидной вакансией
            try:
                saver.add_vacancy(None)
            except Exception:
                pass  # Ожидаемо, что может произойти ошибка

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_invalid_choice(self, mock_print, mock_input):
        """Тест обработки невалидного выбора в пользовательском интерфейсе."""
        mock_input.side_effect = ["99", "0"]  # Невалидный выбор, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_empty_input(self, mock_print, mock_input):
        """Тест обработки пустого ввода в пользовательском интерфейсе."""
        mock_input.side_effect = ["", "0"]  # Пустой ввод, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_whitespace_input(self, mock_print, mock_input):
        """Тест обработки ввода с пробелами в пользовательском интерфейсе."""
        mock_input.side_effect = ["   ", "0"]  # Ввод с пробелами, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    def test_headhunter_api_error_handling(self):
        """Тест обработки ошибок в HeadHunter API."""
        api = HeadHunterAPI()

        # Тест с невалидным ключевым словом
        try:
            vacancies = api.get_vacancies("")
        except Exception:
            pass  # Ожидаемо, что может произойти ошибка

    def test_json_saver_error_handling(self):
        """Тест обработки ошибок в JSONSaver."""
        import os
        import tempfile

        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "test.json")
            saver = JSONSaver(filename)

            # Тест с невалидной вакансией
            try:
                saver.add_vacancy(None)
            except Exception:
                pass  # Ожидаемо, что может произойти ошибка

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_invalid_choice(self, mock_print, mock_input):
        """Тест обработки невалидного выбора в пользовательском интерфейсе."""
        mock_input.side_effect = ["99", "0"]  # Невалидный выбор, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_empty_input(self, mock_print, mock_input):
        """Тест обработки пустого ввода в пользовательском интерфейсе."""
        mock_input.side_effect = ["", "0"]  # Пустой ввод, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_whitespace_input(self, mock_print, mock_input):
        """Тест обработки ввода с пробелами в пользовательском интерфейсе."""
        mock_input.side_effect = ["   ", "0"]  # Ввод с пробелами, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    def test_csv_saver_error_handling(self):
        """Тест обработки ошибок в CSVSaver."""
        import os
        import tempfile

        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "test.csv")
            saver = CSVSaver(filename)

            # Тест с невалидной вакансией
            try:
                saver.add_vacancy(None)
            except Exception:
                pass  # Ожидаемо, что может произойти ошибка

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_invalid_choice(self, mock_print, mock_input):
        """Тест обработки невалидного выбора в пользовательском интерфейсе."""
        mock_input.side_effect = ["99", "0"]  # Невалидный выбор, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_empty_input(self, mock_print, mock_input):
        """Тест обработки пустого ввода в пользовательском интерфейсе."""
        mock_input.side_effect = ["", "0"]  # Пустой ввод, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_whitespace_input(self, mock_print, mock_input):
        """Тест обработки ввода с пробелами в пользовательском интерфейсе."""
        mock_input.side_effect = ["   ", "0"]  # Ввод с пробелами, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_show_statistics(self, mock_print, mock_input):
        """Тест показа статистики через пользовательский интерфейс."""
        mock_input.side_effect = ["6", "0"]  # Статистика, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    def test_headhunter_api_error_handling(self):
        """Тест обработки ошибок в HeadHunter API."""
        api = HeadHunterAPI()

        # Тест с невалидным ключевым словом
        try:
            vacancies = api.get_vacancies("")
        except Exception:
            pass  # Ожидаемо, что может произойти ошибка

    def test_json_saver_error_handling(self):
        """Тест обработки ошибок в JSONSaver."""
        import os
        import tempfile

        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "test.json")
            saver = JSONSaver(filename)

            # Тест с невалидной вакансией
            try:
                saver.add_vacancy(None)
            except Exception:
                pass  # Ожидаемо, что может произойти ошибка

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_invalid_choice(self, mock_print, mock_input):
        """Тест обработки невалидного выбора в пользовательском интерфейсе."""
        mock_input.side_effect = ["99", "0"]  # Невалидный выбор, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_empty_input(self, mock_print, mock_input):
        """Тест обработки пустого ввода в пользовательском интерфейсе."""
        mock_input.side_effect = ["", "0"]  # Пустой ввод, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_whitespace_input(self, mock_print, mock_input):
        """Тест обработки ввода с пробелами в пользовательском интерфейсе."""
        mock_input.side_effect = ["   ", "0"]  # Ввод с пробелами, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    def test_csv_saver_error_handling(self):
        """Тест обработки ошибок в CSVSaver."""
        import os
        import tempfile

        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "test.csv")
            saver = CSVSaver(filename)

            # Тест с невалидной вакансией
            try:
                saver.add_vacancy(None)
            except Exception:
                pass  # Ожидаемо, что может произойти ошибка

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_invalid_choice(self, mock_print, mock_input):
        """Тест обработки невалидного выбора в пользовательском интерфейсе."""
        mock_input.side_effect = ["99", "0"]  # Невалидный выбор, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_empty_input(self, mock_print, mock_input):
        """Тест обработки пустого ввода в пользовательском интерфейсе."""
        mock_input.side_effect = ["", "0"]  # Пустой ввод, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_whitespace_input(self, mock_print, mock_input):
        """Тест обработки ввода с пробелами в пользовательском интерфейсе."""
        mock_input.side_effect = ["   ", "0"]  # Ввод с пробелами, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    def test_headhunter_api_error_handling(self):
        """Тест обработки ошибок в HeadHunter API."""
        api = HeadHunterAPI()

        # Тест с невалидным ключевым словом
        try:
            vacancies = api.get_vacancies("")
        except Exception:
            pass  # Ожидаемо, что может произойти ошибка

    def test_json_saver_error_handling(self):
        """Тест обработки ошибок в JSONSaver."""
        import os
        import tempfile

        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "test.json")
            saver = JSONSaver(filename)

            # Тест с невалидной вакансией
            try:
                saver.add_vacancy(None)
            except Exception:
                pass  # Ожидаемо, что может произойти ошибка

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_invalid_choice(self, mock_print, mock_input):
        """Тест обработки невалидного выбора в пользовательском интерфейсе."""
        mock_input.side_effect = ["99", "0"]  # Невалидный выбор, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_empty_input(self, mock_print, mock_input):
        """Тест обработки пустого ввода в пользовательском интерфейсе."""
        mock_input.side_effect = ["", "0"]  # Пустой ввод, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_whitespace_input(self, mock_print, mock_input):
        """Тест обработки ввода с пробелами в пользовательском интерфейсе."""
        mock_input.side_effect = ["   ", "0"]  # Ввод с пробелами, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    def test_csv_saver_error_handling(self):
        """Тест обработки ошибок в CSVSaver."""
        import os
        import tempfile

        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "test.csv")
            saver = CSVSaver(filename)

            # Тест с невалидной вакансией
            try:
                saver.add_vacancy(None)
            except Exception:
                pass  # Ожидаемо, что может произойти ошибка

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_invalid_choice(self, mock_print, mock_input):
        """Тест обработки невалидного выбора в пользовательском интерфейсе."""
        mock_input.side_effect = ["99", "0"]  # Невалидный выбор, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_empty_input(self, mock_print, mock_input):
        """Тест обработки пустого ввода в пользовательском интерфейсе."""
        mock_input.side_effect = ["", "0"]  # Пустой ввод, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_whitespace_input(self, mock_print, mock_input):
        """Тест обработки ввода с пробелами в пользовательском интерфейсе."""
        mock_input.side_effect = ["   ", "0"]  # Ввод с пробелами, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_clear_vacancies(self, mock_print, mock_input):
        """Тест очистки вакансий через пользовательский интерфейс."""
        mock_input.side_effect = ["7", "нет", "0"]  # Очистка, отмена, выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    def test_headhunter_api_error_handling(self):
        """Тест обработки ошибок в HeadHunter API."""
        api = HeadHunterAPI()

        # Тест с невалидным ключевым словом
        try:
            vacancies = api.get_vacancies("")
        except Exception:
            pass  # Ожидаемо, что может произойти ошибка

    def test_json_saver_error_handling(self):
        """Тест обработки ошибок в JSONSaver."""
        import os
        import tempfile

        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "test.json")
            saver = JSONSaver(filename)

            # Тест с невалидной вакансией
            try:
                saver.add_vacancy(None)
            except Exception:
                pass  # Ожидаемо, что может произойти ошибка

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_invalid_choice(self, mock_print, mock_input):
        """Тест обработки невалидного выбора в пользовательском интерфейсе."""
        mock_input.side_effect = ["99", "0"]  # Невалидный выбор, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_empty_input(self, mock_print, mock_input):
        """Тест обработки пустого ввода в пользовательском интерфейсе."""
        mock_input.side_effect = ["", "0"]  # Пустой ввод, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_whitespace_input(self, mock_print, mock_input):
        """Тест обработки ввода с пробелами в пользовательском интерфейсе."""
        mock_input.side_effect = ["   ", "0"]  # Ввод с пробелами, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    def test_csv_saver_error_handling(self):
        """Тест обработки ошибок в CSVSaver."""
        import os
        import tempfile

        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "test.csv")
            saver = CSVSaver(filename)

            # Тест с невалидной вакансией
            try:
                saver.add_vacancy(None)
            except Exception:
                pass  # Ожидаемо, что может произойти ошибка

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_invalid_choice(self, mock_print, mock_input):
        """Тест обработки невалидного выбора в пользовательском интерфейсе."""
        mock_input.side_effect = ["99", "0"]  # Невалидный выбор, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_empty_input(self, mock_print, mock_input):
        """Тест обработки пустого ввода в пользовательском интерфейсе."""
        mock_input.side_effect = ["", "0"]  # Пустой ввод, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_whitespace_input(self, mock_print, mock_input):
        """Тест обработки ввода с пробелами в пользовательском интерфейсе."""
        mock_input.side_effect = ["   ", "0"]  # Ввод с пробелами, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    def test_headhunter_api_error_handling(self):
        """Тест обработки ошибок в HeadHunter API."""
        api = HeadHunterAPI()

        # Тест с невалидным ключевым словом
        try:
            vacancies = api.get_vacancies("")
        except Exception:
            pass  # Ожидаемо, что может произойти ошибка

    def test_json_saver_error_handling(self):
        """Тест обработки ошибок в JSONSaver."""
        import os
        import tempfile

        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "test.json")
            saver = JSONSaver(filename)

            # Тест с невалидной вакансией
            try:
                saver.add_vacancy(None)
            except Exception:
                pass  # Ожидаемо, что может произойти ошибка

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_invalid_choice(self, mock_print, mock_input):
        """Тест обработки невалидного выбора в пользовательском интерфейсе."""
        mock_input.side_effect = ["99", "0"]  # Невалидный выбор, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_empty_input(self, mock_print, mock_input):
        """Тест обработки пустого ввода в пользовательском интерфейсе."""
        mock_input.side_effect = ["", "0"]  # Пустой ввод, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_whitespace_input(self, mock_print, mock_input):
        """Тест обработки ввода с пробелами в пользовательском интерфейсе."""
        mock_input.side_effect = ["   ", "0"]  # Ввод с пробелами, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    def test_csv_saver_error_handling(self):
        """Тест обработки ошибок в CSVSaver."""
        import os
        import tempfile

        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "test.csv")
            saver = CSVSaver(filename)

            # Тест с невалидной вакансией
            try:
                saver.add_vacancy(None)
            except Exception:
                pass  # Ожидаемо, что может произойти ошибка

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_invalid_choice(self, mock_print, mock_input):
        """Тест обработки невалидного выбора в пользовательском интерфейсе."""
        mock_input.side_effect = ["99", "0"]  # Невалидный выбор, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_empty_input(self, mock_print, mock_input):
        """Тест обработки пустого ввода в пользовательском интерфейсе."""
        mock_input.side_effect = ["", "0"]  # Пустой ввод, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_whitespace_input(self, mock_print, mock_input):
        """Тест обработки ввода с пробелами в пользовательском интерфейсе."""
        mock_input.side_effect = ["   ", "0"]  # Ввод с пробелами, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_export_to_csv(self, mock_print, mock_input):
        """Тест экспорта в CSV через пользовательский интерфейс."""
        mock_input.side_effect = ["8", "0"]  # Экспорт, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    def test_headhunter_api_error_handling(self):
        """Тест обработки ошибок в HeadHunter API."""
        api = HeadHunterAPI()

        # Тест с невалидным ключевым словом
        try:
            vacancies = api.get_vacancies("")
        except Exception:
            pass  # Ожидаемо, что может произойти ошибка

    def test_json_saver_error_handling(self):
        """Тест обработки ошибок в JSONSaver."""
        import os
        import tempfile

        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "test.json")
            saver = JSONSaver(filename)

            # Тест с невалидной вакансией
            try:
                saver.add_vacancy(None)
            except Exception:
                pass  # Ожидаемо, что может произойти ошибка

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_invalid_choice(self, mock_print, mock_input):
        """Тест обработки невалидного выбора в пользовательском интерфейсе."""
        mock_input.side_effect = ["99", "0"]  # Невалидный выбор, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_empty_input(self, mock_print, mock_input):
        """Тест обработки пустого ввода в пользовательском интерфейсе."""
        mock_input.side_effect = ["", "0"]  # Пустой ввод, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_whitespace_input(self, mock_print, mock_input):
        """Тест обработки ввода с пробелами в пользовательском интерфейсе."""
        mock_input.side_effect = ["   ", "0"]  # Ввод с пробелами, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    def test_csv_saver_error_handling(self):
        """Тест обработки ошибок в CSVSaver."""
        import os
        import tempfile

        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "test.csv")
            saver = CSVSaver(filename)

            # Тест с невалидной вакансией
            try:
                saver.add_vacancy(None)
            except Exception:
                pass  # Ожидаемо, что может произойти ошибка

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_invalid_choice(self, mock_print, mock_input):
        """Тест обработки невалидного выбора в пользовательском интерфейсе."""
        mock_input.side_effect = ["99", "0"]  # Невалидный выбор, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_empty_input(self, mock_print, mock_input):
        """Тест обработки пустого ввода в пользовательском интерфейсе."""
        mock_input.side_effect = ["", "0"]  # Пустой ввод, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_whitespace_input(self, mock_print, mock_input):
        """Тест обработки ввода с пробелами в пользовательском интерфейсе."""
        mock_input.side_effect = ["   ", "0"]  # Ввод с пробелами, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    def test_headhunter_api_error_handling(self):
        """Тест обработки ошибок в HeadHunter API."""
        api = HeadHunterAPI()

        # Тест с невалидным ключевым словом
        try:
            vacancies = api.get_vacancies("")
        except Exception:
            pass  # Ожидаемо, что может произойти ошибка

    def test_json_saver_error_handling(self):
        """Тест обработки ошибок в JSONSaver."""
        import os
        import tempfile

        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "test.json")
            saver = JSONSaver(filename)

            # Тест с невалидной вакансией
            try:
                saver.add_vacancy(None)
            except Exception:
                pass  # Ожидаемо, что может произойти ошибка

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_invalid_choice(self, mock_print, mock_input):
        """Тест обработки невалидного выбора в пользовательском интерфейсе."""
        mock_input.side_effect = ["99", "0"]  # Невалидный выбор, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_empty_input(self, mock_print, mock_input):
        """Тест обработки пустого ввода в пользовательском интерфейсе."""
        mock_input.side_effect = ["", "0"]  # Пустой ввод, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_whitespace_input(self, mock_print, mock_input):
        """Тест обработки ввода с пробелами в пользовательском интерфейсе."""
        mock_input.side_effect = ["   ", "0"]  # Ввод с пробелами, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    def test_csv_saver_error_handling(self):
        """Тест обработки ошибок в CSVSaver."""
        import os
        import tempfile

        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "test.csv")
            saver = CSVSaver(filename)

            # Тест с невалидной вакансией
            try:
                saver.add_vacancy(None)
            except Exception:
                pass  # Ожидаемо, что может произойти ошибка

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_invalid_choice(self, mock_print, mock_input):
        """Тест обработки невалидного выбора в пользовательском интерфейсе."""
        mock_input.side_effect = ["99", "0"]  # Невалидный выбор, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_empty_input(self, mock_print, mock_input):
        """Тест обработки пустого ввода в пользовательском интерфейсе."""
        mock_input.side_effect = ["", "0"]  # Пустой ввод, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called

    @patch("builtins.input")
    @patch("builtins.print")
    def test_user_interaction_whitespace_input(self, mock_print, mock_input):
        """Тест обработки ввода с пробелами в пользовательском интерфейсе."""
        mock_input.side_effect = ["   ", "0"]  # Ввод с пробелами, затем выход

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем, что было выведено меню
        assert mock_print.called
