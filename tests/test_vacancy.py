import pytest

from src.vacancy import Vacancy


class TestVacancy:
    """Тесты для класса Vacancy."""

    def test_init_valid_data(self):
        """Тест инициализации с валидными данными."""
        vacancy = Vacancy(
            name="Python Developer",
            url="https://hh.ru/vacancy/123",
            salary_from=100000,
            salary_to=150000,
            currency="RUR",
            description="Test description",
            requirements="Test requirements",
            employer="Test Company",
        )

        assert vacancy.name == "Python Developer"
        assert vacancy.url == "https://hh.ru/vacancy/123"
        assert vacancy.salary_from == 100000
        assert vacancy.salary_to == 150000
        assert vacancy.currency == "RUR"
        assert vacancy.description == "Test description"
        assert vacancy.requirements == "Test requirements"
        assert vacancy.employer == "Test Company"

    def test_init_invalid_name(self):
        """Тест инициализации с невалидным названием."""
        with pytest.raises(ValueError):
            Vacancy(name="", url="https://hh.ru/vacancy/123")

        with pytest.raises(ValueError):
            Vacancy(name="   ", url="https://hh.ru/vacancy/123")

    def test_init_invalid_url(self):
        """Тест инициализации с невалидным URL."""
        with pytest.raises(ValueError):
            Vacancy(name="Test", url="")

        with pytest.raises(ValueError):
            Vacancy(name="Test", url="invalid-url")

    def test_salary_validation(self):
        """Тест валидации зарплаты."""
        vacancy = Vacancy(
            name="Test", url="https://hh.ru/vacancy/123", salary_from=-1000
        )
        assert vacancy.salary_from is None

        vacancy = Vacancy(
            name="Test", url="https://hh.ru/vacancy/123", salary_from="invalid"
        )
        assert vacancy.salary_from is None

    def test_average_salary(self):
        """Тест расчета средней зарплаты."""
        vacancy1 = Vacancy(
            name="Test",
            url="https://hh.ru/vacancy/123",
            salary_from=100000,
            salary_to=150000,
        )
        assert vacancy1.average_salary == 125000

        vacancy2 = Vacancy(
            name="Test", url="https://hh.ru/vacancy/123", salary_from=100000
        )
        assert vacancy2.average_salary == 100000

        vacancy3 = Vacancy(
            name="Test", url="https://hh.ru/vacancy/123", salary_to=150000
        )
        assert vacancy3.average_salary == 150000

        vacancy4 = Vacancy(name="Test", url="https://hh.ru/vacancy/123")
        assert vacancy4.average_salary is None

    def test_comparison_methods(self):
        """Тест методов сравнения."""
        vacancy1 = Vacancy(
            name="Test1",
            url="https://hh.ru/vacancy/1",
            salary_from=100000,
            salary_to=150000,
        )
        vacancy2 = Vacancy(
            name="Test2",
            url="https://hh.ru/vacancy/2",
            salary_from=200000,
            salary_to=250000,
        )
        vacancy3 = Vacancy(name="Test3", url="https://hh.ru/vacancy/3")

        assert vacancy1 < vacancy2
        assert vacancy2 > vacancy1
        assert vacancy1 <= vacancy2
        assert vacancy2 >= vacancy1
        assert vacancy1 != vacancy2

        # Сравнение с вакансией без зарплаты
        assert vacancy3 < vacancy1
        assert vacancy1 > vacancy3

    def test_to_dict(self):
        """Тест преобразования в словарь."""
        vacancy = Vacancy(
            name="Test",
            url="https://hh.ru/vacancy/123",
            salary_from=100000,
            salary_to=150000,
            currency="RUR",
            description="Test description",
            requirements="Test requirements",
            employer="Test Company",
        )

        data = vacancy.to_dict()

        assert data["name"] == "Test"
        assert data["url"] == "https://hh.ru/vacancy/123"
        assert data["salary_from"] == 100000
        assert data["salary_to"] == 150000
        assert data["currency"] == "RUR"
        assert data["description"] == "Test description"
        assert data["requirements"] == "Test requirements"
        assert data["employer"] == "Test Company"

    def test_from_dict(self):
        """Тест создания из словаря."""
        data = {
            "name": "Test",
            "url": "https://hh.ru/vacancy/123",
            "salary_from": 100000,
            "salary_to": 150000,
            "currency": "RUR",
            "description": "Test description",
            "requirements": "Test requirements",
            "employer": "Test Company",
        }

        vacancy = Vacancy.from_dict(data)

        assert vacancy.name == "Test"
        assert vacancy.url == "https://hh.ru/vacancy/123"
        assert vacancy.salary_from == 100000
        assert vacancy.salary_to == 150000
        assert vacancy.currency == "RUR"
        assert vacancy.description == "Test description"
        assert vacancy.requirements == "Test requirements"
        assert vacancy.employer == "Test Company"

    def test_from_hh_data(self):
        """Тест создания из данных HeadHunter API."""
        hh_data = {
            "name": "Python Developer",
            "alternate_url": "https://hh.ru/vacancy/123",
            "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
            "snippet": {
                "requirement": "Test requirements",
                "responsibility": "Test description",
            },
            "employer": {"name": "Test Company"},
        }

        vacancy = Vacancy.from_hh_data(hh_data)

        assert vacancy.name == "Python Developer"
        assert vacancy.url == "https://hh.ru/vacancy/123"
        assert vacancy.salary_from == 100000
        assert vacancy.salary_to == 150000
        assert vacancy.currency == "RUR"
        assert vacancy.description == "Test description"
        assert vacancy.requirements == "Test requirements"
        assert vacancy.employer == "Test Company"

    def test_cast_to_object_list(self):
        """Тест преобразования списка данных в список объектов."""
        hh_data_list = [
            {
                "name": "Python Developer",
                "alternate_url": "https://hh.ru/vacancy/1",
                "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
                "snippet": {
                    "requirement": "Test requirements",
                    "responsibility": "Test description",
                },
                "employer": {"name": "Test Company"},
            },
            {
                "name": "Java Developer",
                "alternate_url": "https://hh.ru/vacancy/2",
                "salary": {"from": 120000, "to": 180000, "currency": "RUR"},
                "snippet": {
                    "requirement": "Java requirements",
                    "responsibility": "Java description",
                },
                "employer": {"name": "Another Company"},
            },
        ]

        vacancies = Vacancy.cast_to_object_list(hh_data_list)

        assert len(vacancies) == 2
        assert vacancies[0].name == "Python Developer"
        assert vacancies[1].name == "Java Developer"

    def test_str_representation(self):
        """Тест строкового представления."""
        vacancy = Vacancy(
            name="Test",
            url="https://hh.ru/vacancy/123",
            salary_from=100000,
            salary_to=150000,
            currency="RUR",
            description="Test description",
            requirements="Test requirements",
            employer="Test Company",
        )

        str_repr = str(vacancy)
        assert "Test" in str_repr
        assert "Test Company" in str_repr
        assert "100,000 - 150,000 RUR" in str_repr
        assert "https://hh.ru/vacancy/123" in str_repr

    def test_repr_representation(self):
        """Тест представления для отладки."""
        vacancy = Vacancy(
            name="Test",
            url="https://hh.ru/vacancy/123",
            salary_from=100000,
            salary_to=150000,
        )

        repr_str = repr(vacancy)
        assert "Vacancy" in repr_str
        assert "Test" in repr_str
        assert "100000" in repr_str
        assert "150000" in repr_str

    def test_cast_to_object_list_with_invalid_data(self):
        """Тест преобразования списка с некорректными данными."""
        hh_data_list = [
            {
                "name": "Valid Vacancy",
                "alternate_url": "https://hh.ru/vacancy/1",
                "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
                "snippet": {
                    "requirement": "Test requirements",
                    "responsibility": "Test description",
                },
                "employer": {"name": "Test Company"},
            },
            {
                # Некорректные данные - отсутствует обязательное поле 'name'
                "alternate_url": "https://hh.ru/vacancy/2",
                "salary": {"from": 200000, "to": 250000, "currency": "RUR"},
                "snippet": {
                    "requirement": "Test requirements",
                    "responsibility": "Test description",
                },
                "employer": {"name": "Test Company"},
            },
        ]

        vacancies = Vacancy.cast_to_object_list(hh_data_list)

        # Должна остаться только одна валидная вакансия
        assert len(vacancies) == 1
        assert vacancies[0].name == "Valid Vacancy"

    def test_from_hh_data_with_missing_fields(self):
        """Тест создания вакансии из данных HeadHunter с отсутствующими полями."""
        hh_data = {
            "name": "Python Developer",
            "alternate_url": "https://hh.ru/vacancy/123",
            # Отсутствует salary
            "snippet": {
                "requirement": "Test requirements",
                "responsibility": "Test description",
            },
            "employer": {"name": "Test Company"},
        }

        vacancy = Vacancy.from_hh_data(hh_data)

        assert vacancy.name == "Python Developer"
        assert vacancy.url == "https://hh.ru/vacancy/123"
        assert vacancy.salary_from is None
        assert vacancy.salary_to is None
        assert vacancy.currency == "RUR"  # Значение по умолчанию
        assert vacancy.description == "Test description"
        assert vacancy.requirements == "Test requirements"
        assert vacancy.employer == "Test Company"

    def test_comparison_with_non_vacancy(self):
        """Тест сравнения с объектом, не являющимся вакансией."""
        vacancy = Vacancy(
            name="Test", url="https://hh.ru/vacancy/123", salary_from=100000
        )

        # Сравнение с не-Vacancy объектом должно возвращать NotImplemented
        assert vacancy.__lt__("not a vacancy") == NotImplemented
        assert vacancy.__gt__("not a vacancy") == NotImplemented
        assert vacancy.__le__("not a vacancy") == NotImplemented
        assert vacancy.__ge__("not a vacancy") == NotImplemented
        assert vacancy.__eq__("not a vacancy") == NotImplemented
        assert vacancy.__ne__("not a vacancy") == NotImplemented

    def test_validate_currency_empty_string(self):
        """Тест валидации валюты с пустой строкой."""
        vacancy = Vacancy(name="Test", url="https://hh.ru/vacancy/123", currency="")
        assert vacancy.currency == "RUR"  # Значение по умолчанию

    def test_validate_currency_whitespace(self):
        """Тест валидации валюты с пробелами."""
        vacancy = Vacancy(name="Test", url="https://hh.ru/vacancy/123", currency="   ")
        assert vacancy.currency == "RUR"  # Значение по умолчанию

    def test_validate_currency_non_string(self):
        """Тест валидации валюты с не-строковым значением."""
        vacancy = Vacancy(name="Test", url="https://hh.ru/vacancy/123", currency=123)
        assert vacancy.currency == "RUR"  # Значение по умолчанию

    def test_validate_text_non_string(self):
        """Тест валидации текстовых полей с не-строковыми значениями."""
        vacancy = Vacancy(
            name="Test",
            url="https://hh.ru/vacancy/123",
            description=123,
            requirements=456,
            employer=789,
        )
        assert vacancy.description == ""
        assert vacancy.requirements == ""
        assert vacancy.employer == ""

    def test_get_salary_info_no_salary(self):
        """Тест получения информации о зарплате без указания зарплаты."""
        vacancy = Vacancy(name="Test", url="https://hh.ru/vacancy/123")
        salary_info = vacancy._get_salary_info()
        assert salary_info == "Зарплата не указана"

    def test_get_salary_info_only_from(self):
        """Тест получения информации о зарплате только с минимальной зарплатой."""
        vacancy = Vacancy(
            name="Test", url="https://hh.ru/vacancy/123", salary_from=100000
        )
        salary_info = vacancy._get_salary_info()
        assert salary_info == "от 100,000 RUR"

    def test_get_salary_info_only_to(self):
        """Тест получения информации о зарплате только с максимальной зарплатой."""
        vacancy = Vacancy(
            name="Test", url="https://hh.ru/vacancy/123", salary_to=150000
        )
        salary_info = vacancy._get_salary_info()
        assert salary_info == "до 150,000 RUR"

    def test_get_salary_info_range(self):
        """Тест получения информации о зарплате с диапазоном."""
        vacancy = Vacancy(
            name="Test",
            url="https://hh.ru/vacancy/123",
            salary_from=100000,
            salary_to=150000,
        )
        salary_info = vacancy._get_salary_info()
        assert salary_info == "100,000 - 150,000 RUR"

    def test_comparison_methods_edge_cases(self):
        """Тест методов сравнения для граничных случаев."""
        vacancy1 = Vacancy(
            name="Test1", url="https://hh.ru/vacancy/1", salary_from=100000
        )
        vacancy2 = Vacancy(name="Test2", url="https://hh.ru/vacancy/2")  # Без зарплаты

        # Тест __gt__ с None зарплатой
        assert vacancy1 > vacancy2  # vacancy1 имеет зарплату, vacancy2 - нет

        # Тест __lt__ с None зарплатой
        assert vacancy2 < vacancy1  # vacancy2 без зарплаты меньше vacancy1 с зарплатой

        # Тест __gt__ когда обе вакансии без зарплаты
        vacancy3 = Vacancy(name="Test3", url="https://hh.ru/vacancy/3")
        assert not (vacancy2 > vacancy3)  # Обе без зарплаты, должно быть False

        # Тест __gt__ когда self_avg is None
        assert not (vacancy2 > vacancy1)  # vacancy2 без зарплаты, vacancy1 с зарплатой
