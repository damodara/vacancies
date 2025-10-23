from unittest.mock import patch

from src.utils import (
    filter_vacancies,
    get_statistics,
    get_top_vacancies,
    get_vacancies_by_keyword,
    get_vacancies_by_salary,
    print_statistics,
    print_vacancies,
    remove_duplicates,
    sort_vacancies,
)
from src.vacancy import Vacancy


class TestUtils:
    """Тесты для вспомогательных функций."""

    def test_filter_vacancies(self):
        """Тест фильтрации вакансий по ключевым словам."""
        vacancies = [
            Vacancy(
                name="Python Developer",
                url="https://hh.ru/vacancy/1",
                description="Python job",
            ),
            Vacancy(
                name="Java Developer",
                url="https://hh.ru/vacancy/2",
                description="Java job",
            ),
            Vacancy(
                name="Frontend Developer",
                url="https://hh.ru/vacancy/3",
                description="JavaScript job",
            ),
        ]

        filtered = filter_vacancies(vacancies, ["Python"])
        assert len(filtered) == 1
        assert filtered[0].name == "Python Developer"

        filtered = filter_vacancies(vacancies, ["Developer"])
        assert len(filtered) == 3

        filtered = filter_vacancies(vacancies, [])
        assert len(filtered) == 3

    def test_get_vacancies_by_salary(self):
        """Тест фильтрации вакансий по зарплате."""
        vacancies = [
            Vacancy(
                name="Test1",
                url="https://hh.ru/vacancy/1",
                salary_from=100000,
                salary_to=150000,
            ),
            Vacancy(
                name="Test2",
                url="https://hh.ru/vacancy/2",
                salary_from=200000,
                salary_to=250000,
            ),
            Vacancy(
                name="Test3",
                url="https://hh.ru/vacancy/3",
                salary_from=50000,
                salary_to=80000,
            ),
        ]

        filtered = get_vacancies_by_salary(vacancies, "100000-200000")
        assert len(filtered) == 1
        assert filtered[0].name == "Test1"  # Только Test1 попадает в диапазон

        filtered = get_vacancies_by_salary(vacancies, "150000")
        assert len(filtered) == 1
        assert filtered[0].name == "Test2"

        filtered = get_vacancies_by_salary(vacancies, "")
        assert len(filtered) == 3

    def test_sort_vacancies(self):
        """Тест сортировки вакансий по зарплате."""
        vacancies = [
            Vacancy(
                name="Test1",
                url="https://hh.ru/vacancy/1",
                salary_from=100000,
                salary_to=150000,
            ),
            Vacancy(
                name="Test2",
                url="https://hh.ru/vacancy/2",
                salary_from=200000,
                salary_to=250000,
            ),
            Vacancy(
                name="Test3",
                url="https://hh.ru/vacancy/3",
                salary_from=50000,
                salary_to=80000,
            ),
        ]

        sorted_vacancies = sort_vacancies(vacancies)
        assert sorted_vacancies[0].name == "Test2"  # Самая высокая зарплата
        assert sorted_vacancies[1].name == "Test1"
        assert sorted_vacancies[2].name == "Test3"  # Самая низкая зарплата

        sorted_vacancies = sort_vacancies(vacancies, reverse=False)
        assert sorted_vacancies[0].name == "Test3"  # Самая низкая зарплата
        assert sorted_vacancies[2].name == "Test2"  # Самая высокая зарплата

    def test_get_top_vacancies(self):
        """Тест получения топ N вакансий."""
        vacancies = [
            Vacancy(
                name="Test1",
                url="https://hh.ru/vacancy/1",
                salary_from=100000,
                salary_to=150000,
            ),
            Vacancy(
                name="Test2",
                url="https://hh.ru/vacancy/2",
                salary_from=200000,
                salary_to=250000,
            ),
            Vacancy(
                name="Test3",
                url="https://hh.ru/vacancy/3",
                salary_from=50000,
                salary_to=80000,
            ),
        ]

        top_vacancies = get_top_vacancies(vacancies, 2)
        assert len(top_vacancies) == 2
        assert top_vacancies[0].name == "Test2"
        assert top_vacancies[1].name == "Test1"

        top_vacancies = get_top_vacancies(vacancies, 0)
        assert len(top_vacancies) == 0

        top_vacancies = get_top_vacancies(vacancies, 10)
        assert len(top_vacancies) == 3

    def test_get_vacancies_by_keyword(self):
        """Тест поиска вакансий по ключевому слову."""
        vacancies = [
            Vacancy(
                name="Python Developer",
                url="https://hh.ru/vacancy/1",
                description="Python job",
            ),
            Vacancy(
                name="Java Developer",
                url="https://hh.ru/vacancy/2",
                description="Java job",
            ),
            Vacancy(
                name="Frontend Developer",
                url="https://hh.ru/vacancy/3",
                description="JavaScript job",
            ),
        ]

        filtered = get_vacancies_by_keyword(vacancies, "Python")
        assert len(filtered) == 1
        assert filtered[0].name == "Python Developer"

        filtered = get_vacancies_by_keyword(vacancies, "Developer")
        assert len(filtered) == 3

        filtered = get_vacancies_by_keyword(vacancies, "")
        assert len(filtered) == 3

    def test_remove_duplicates(self):
        """Тест удаления дубликатов."""
        vacancies = [
            Vacancy(name="Test1", url="https://hh.ru/vacancy/1"),
            Vacancy(name="Test2", url="https://hh.ru/vacancy/2"),
            Vacancy(name="Test3", url="https://hh.ru/vacancy/1"),  # Дубликат URL
        ]

        unique_vacancies = remove_duplicates(vacancies)
        assert len(unique_vacancies) == 2
        assert unique_vacancies[0].name == "Test1"
        assert unique_vacancies[1].name == "Test2"

    def test_get_statistics(self):
        """Тест получения статистики."""
        vacancies = [
            Vacancy(
                name="Test1",
                url="https://hh.ru/vacancy/1",
                salary_from=100000,
                salary_to=150000,
                employer="Company1",
            ),
            Vacancy(
                name="Test2",
                url="https://hh.ru/vacancy/2",
                salary_from=200000,
                salary_to=250000,
                employer="Company2",
            ),
            Vacancy(name="Test3", url="https://hh.ru/vacancy/3", employer="Company1"),
            Vacancy(
                name="Test4",
                url="https://hh.ru/vacancy/4",
                salary_from=50000,
                salary_to=80000,
                employer="Company1",
            ),
        ]

        stats = get_statistics(vacancies)

        assert stats["total_count"] == 4
        assert stats["with_salary"] == 3
        assert stats["without_salary"] == 1
        assert stats["avg_salary"] == 138333  # (125000 + 225000 + 65000) / 3 = 138333
        assert stats["min_salary"] == 65000
        assert stats["max_salary"] == 225000
        assert stats["employers"]["Company1"] == 3
        assert stats["employers"]["Company2"] == 1

    def test_get_statistics_empty_list(self):
        """Тест получения статистики для пустого списка."""
        stats = get_statistics([])

        assert stats["total_count"] == 0
        assert stats["with_salary"] == 0
        assert stats["without_salary"] == 0
        assert stats["avg_salary"] == 0
        assert stats["min_salary"] == 0
        assert stats["max_salary"] == 0
        assert stats["employers"] == {}

    def test_get_vacancies_by_salary_invalid_format(self):
        """Тест фильтрации с неверным форматом зарплаты."""
        vacancies = [
            Vacancy(
                name="Test1",
                url="https://hh.ru/vacancy/1",
                salary_from=100000,
                salary_to=150000,
            )
        ]

        # Неверный формат должен вернуть все вакансии
        filtered = get_vacancies_by_salary(vacancies, "invalid-format")
        assert len(filtered) == 1

        # Пустая строка должна вернуть все вакансии
        filtered = get_vacancies_by_salary(vacancies, "")
        assert len(filtered) == 1

    def test_get_vacancies_by_salary_no_salary(self):
        """Тест фильтрации вакансий без зарплаты."""
        vacancies = [
            Vacancy(name="Test1", url="https://hh.ru/vacancy/1"),  # Без зарплаты
            Vacancy(name="Test2", url="https://hh.ru/vacancy/2", salary_from=100000),
        ]

        filtered = get_vacancies_by_salary(vacancies, "50000")
        assert len(filtered) == 1
        assert filtered[0].name == "Test2"

    def test_sort_vacancies_with_none_salary(self):
        """Тест сортировки вакансий с None зарплатой."""
        vacancies = [
            Vacancy(name="Test1", url="https://hh.ru/vacancy/1", salary_from=100000),
            Vacancy(name="Test2", url="https://hh.ru/vacancy/2"),  # Без зарплаты
            Vacancy(name="Test3", url="https://hh.ru/vacancy/3", salary_from=200000),
        ]

        sorted_vacancies = sort_vacancies(vacancies)
        assert sorted_vacancies[0].name == "Test3"  # Самая высокая зарплата
        assert sorted_vacancies[1].name == "Test1"
        assert sorted_vacancies[2].name == "Test2"  # Без зарплаты в конце

    @patch("builtins.print")
    def test_print_vacancies_empty_list(self, mock_print):
        """Тест вывода пустого списка вакансий."""
        print_vacancies([])

        # Проверяем, что был вызван print с сообщением о том, что вакансии не найдены
        mock_print.assert_called_with("Вакансии не найдены.")

    @patch("builtins.print")
    def test_print_vacancies_with_data(self, mock_print):
        """Тест вывода вакансий с данными."""
        vacancies = [
            Vacancy(
                name="Test Developer",
                url="https://hh.ru/vacancy/1",
                salary_from=100000,
                salary_to=150000,
                currency="RUR",
                description="Test description",
                requirements="Test requirements",
                employer="Test Company",
            )
        ]

        print_vacancies(vacancies)

        # Проверяем, что print был вызван несколько раз
        assert mock_print.call_count > 1

        # Проверяем, что в выводах есть название вакансии
        print_calls = [call.args[0] for call in mock_print.call_args_list]
        assert any("Test Developer" in str(call) for call in print_calls)

    @patch("builtins.print")
    def test_print_statistics(self, mock_print):
        """Тест вывода статистики."""
        vacancies = [
            Vacancy(
                name="Test1",
                url="https://hh.ru/vacancy/1",
                salary_from=100000,
                salary_to=150000,
                employer="Company1",
            ),
            Vacancy(
                name="Test2",
                url="https://hh.ru/vacancy/2",
                salary_from=200000,
                salary_to=250000,
                employer="Company2",
            ),
            Vacancy(name="Test3", url="https://hh.ru/vacancy/3", employer="Company1"),
        ]

        print_statistics(vacancies)

        # Проверяем, что print был вызван несколько раз
        assert mock_print.call_count > 1

        # Проверяем, что в выводах есть статистика
        print_calls = [call.args[0] for call in mock_print.call_args_list]
        assert any("СТАТИСТИКА ПО ВАКАНСИЯМ" in str(call) for call in print_calls)
        assert any("Всего вакансий: 3" in str(call) for call in print_calls)
