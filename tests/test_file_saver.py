import csv
import json
import os
import tempfile

import pytest

from src.file_saver import CSVSaver, FileSaver, JSONSaver
from src.vacancy import Vacancy


class TestFileSaver:
    """Тесты для абстрактного класса FileSaver."""

    def test_init(self):
        """Тест инициализации базового класса."""

        # Создаем конкретную реализацию для тестирования
        class ConcreteSaver(FileSaver):
            def add_vacancy(self, vacancy):
                pass

            def get_vacancies(self, **criteria):
                return []

            def delete_vacancy(self, vacancy):
                pass

            def clear_all(self):
                pass

        saver = ConcreteSaver("test.txt")
        assert saver.filename == "test.txt"

    def test_filename_property(self):
        """Тест свойства filename."""

        # Создаем конкретную реализацию для тестирования
        class ConcreteSaver(FileSaver):
            def add_vacancy(self, vacancy):
                pass

            def get_vacancies(self, **criteria):
                return []

            def delete_vacancy(self, vacancy):
                pass

            def clear_all(self):
                pass

        saver = ConcreteSaver()

        saver.filename = "new_file.txt"
        assert saver.filename == "new_file.txt"

        with pytest.raises(ValueError):
            saver.filename = ""

        with pytest.raises(ValueError):
            saver.filename = "   "


class TestJSONSaver:
    """Тесты для класса JSONSaver."""

    def test_init(self):
        """Тест инициализации JSONSaver."""
        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "test.json")
            saver = JSONSaver(filename)
            assert saver.filename == filename
            assert os.path.exists(filename)

    def test_add_vacancy(self):
        """Тест добавления вакансии."""
        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "test.json")
            saver = JSONSaver(filename)

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

            saver.add_vacancy(vacancy)

            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)

            assert len(data) == 1
            assert data[0]["name"] == "Test"
            assert data[0]["url"] == "https://hh.ru/vacancy/123"

    def test_add_duplicate_vacancy(self):
        """Тест добавления дубликата вакансии."""
        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "test.json")
            saver = JSONSaver(filename)

            vacancy = Vacancy(
                name="Test",
                url="https://hh.ru/vacancy/123",
                salary_from=100000,
                salary_to=150000,
            )

            saver.add_vacancy(vacancy)
            saver.add_vacancy(vacancy)  # Дубликат

            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)

            assert len(data) == 1  # Дубликат не должен добавиться

    def test_get_vacancies_no_criteria(self):
        """Тест получения всех вакансий без критериев."""
        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "test.json")
            saver = JSONSaver(filename)

            vacancy1 = Vacancy(
                name="Test1", url="https://hh.ru/vacancy/1", salary_from=100000
            )
            vacancy2 = Vacancy(
                name="Test2", url="https://hh.ru/vacancy/2", salary_from=200000
            )

            saver.add_vacancy(vacancy1)
            saver.add_vacancy(vacancy2)

            vacancies = saver.get_vacancies()
            assert len(vacancies) == 2

    def test_get_vacancies_with_keyword(self):
        """Тест получения вакансий по ключевому слову."""
        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "test.json")
            saver = JSONSaver(filename)

            vacancy1 = Vacancy(
                name="Python Developer",
                url="https://hh.ru/vacancy/1",
                description="Python job",
            )
            vacancy2 = Vacancy(
                name="Java Developer",
                url="https://hh.ru/vacancy/2",
                description="Java job",
            )

            saver.add_vacancy(vacancy1)
            saver.add_vacancy(vacancy2)

            vacancies = saver.get_vacancies(keyword="Python")
            assert len(vacancies) == 1
            assert vacancies[0]["name"] == "Python Developer"

    def test_get_vacancies_with_salary_range(self):
        """Тест получения вакансий по диапазону зарплат."""
        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "test.json")
            saver = JSONSaver(filename)

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

            saver.add_vacancy(vacancy1)
            saver.add_vacancy(vacancy2)

            # Тестируем фильтрацию по минимальной зарплате (salary_from вакансии >= критерий)
            vacancies = saver.get_vacancies(salary_from=120000)
            assert len(vacancies) == 1
            assert vacancies[0]["name"] == "Test2"  # Test2 имеет salary_from=200000

            # Тестируем фильтрацию по максимальной зарплате (salary_to вакансии <= критерий)
            vacancies = saver.get_vacancies(salary_to=180000)
            assert len(vacancies) == 1
            assert vacancies[0]["name"] == "Test1"  # Test1 имеет salary_to=150000

    def test_delete_vacancy(self):
        """Тест удаления вакансии."""
        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "test.json")
            saver = JSONSaver(filename)

            vacancy1 = Vacancy(name="Test1", url="https://hh.ru/vacancy/1")
            vacancy2 = Vacancy(name="Test2", url="https://hh.ru/vacancy/2")

            saver.add_vacancy(vacancy1)
            saver.add_vacancy(vacancy2)

            saver.delete_vacancy(vacancy1)

            vacancies = saver.get_vacancies()
            assert len(vacancies) == 1
            assert vacancies[0]["name"] == "Test2"

    def test_clear_all(self):
        """Тест очистки всех данных."""
        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "test.json")
            saver = JSONSaver(filename)

            vacancy = Vacancy(name="Test", url="https://hh.ru/vacancy/123")
            saver.add_vacancy(vacancy)

            saver.clear_all()

            vacancies = saver.get_vacancies()
            assert len(vacancies) == 0

    def test_csv_saver_load_vacancies_file_not_found(self):
        """Тест загрузки вакансий из несуществующего CSV файла."""
        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "nonexistent.csv")
            saver = CSVSaver(filename)

            # Файл не существует, должен вернуть пустой список
            vacancies = saver._load_vacancies()
            assert vacancies == []

    def test_csv_saver_load_vacancies_empty_file(self):
        """Тест загрузки вакансий из пустого CSV файла."""
        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "empty.csv")

            # Создаем пустой файл
            with open(filename, "w", encoding="utf-8") as f:
                pass

            saver = CSVSaver(filename)

            # Пустой файл должен вернуть пустой список
            vacancies = saver._load_vacancies()
            assert vacancies == []

    def test_csv_saver_get_vacancies_with_employer_filter(self):
        """Тест фильтрации по работодателю в CSVSaver."""
        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "test.csv")
            saver = CSVSaver(filename)

            vacancy1 = Vacancy(
                name="Test1", url="https://hh.ru/vacancy/1", employer="Company1"
            )
            vacancy2 = Vacancy(
                name="Test2", url="https://hh.ru/vacancy/2", employer="Company2"
            )

            saver.add_vacancy(vacancy1)
            saver.add_vacancy(vacancy2)

            # Фильтрация по работодателю
            vacancies = saver.get_vacancies(employer="Company1")
            assert len(vacancies) == 1
            assert vacancies[0]["name"] == "Test1"

    def test_csv_saver_save_vacancies_empty_list(self):
        """Тест сохранения пустого списка вакансий в CSV."""
        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "test.csv")
            saver = CSVSaver(filename)

            # Сохраняем пустой список
            saver._save_vacancies([])

            # Проверяем, что файл создан с заголовками
            with open(filename, "r", encoding="utf-8", newline="") as f:
                content = f.read()
                assert "name" in content
                assert "url" in content

    def test_csv_saver_load_vacancies_with_invalid_salary(self):
        """Тест загрузки CSV с невалидными данными зарплаты."""
        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "test.csv")

            # Создаем CSV файл с невалидными данными зарплаты
            with open(filename, "w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(
                    [
                        "name",
                        "url",
                        "salary_from",
                        "salary_to",
                        "currency",
                        "description",
                        "requirements",
                        "employer",
                    ]
                )
                writer.writerow(
                    [
                        "Test",
                        "https://hh.ru/vacancy/1",
                        "invalid",
                        "also_invalid",
                        "RUR",
                        "desc",
                        "req",
                        "emp",
                    ]
                )

            saver = CSVSaver(filename)
            vacancies = saver._load_vacancies()

            # Невалидные данные должны быть преобразованы в None
            assert len(vacancies) == 1
            assert vacancies[0]["salary_from"] is None
            assert vacancies[0]["salary_to"] is None

    def test_csv_saver_load_vacancies_file_not_found_error(self):
        """Тест обработки FileNotFoundError в CSVSaver."""
        import os
        import tempfile

        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "nonexistent.csv")

            # Удаляем файл если он существует
            if os.path.exists(filename):
                os.remove(filename)

            saver = CSVSaver(filename)

            # Должен вернуть пустой список при FileNotFoundError
            vacancies = saver._load_vacancies()
            assert vacancies == []

    def test_json_saver_get_vacancies_with_multiple_filters(self):
        """Тест фильтрации по нескольким критериям в JSONSaver."""
        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "test.json")
            saver = JSONSaver(filename)

            vacancy1 = Vacancy(
                name="Python Developer",
                url="https://hh.ru/vacancy/1",
                salary_from=100000,
                salary_to=150000,
                employer="Company1",
            )
            vacancy2 = Vacancy(
                name="Java Developer",
                url="https://hh.ru/vacancy/2",
                salary_from=200000,
                salary_to=250000,
                employer="Company2",
            )

            saver.add_vacancy(vacancy1)
            saver.add_vacancy(vacancy2)

            # Фильтрация по нескольким критериям (используем keyword вместо name)
            vacancies = saver.get_vacancies(keyword="Python", salary_from=50000)
            assert len(vacancies) == 1
            assert vacancies[0]["name"] == "Python Developer"

    def test_csv_saver_get_vacancies_with_multiple_filters(self):
        """Тест фильтрации по нескольким критериям в CSVSaver."""
        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "test.csv")
            saver = CSVSaver(filename)

            vacancy1 = Vacancy(
                name="Python Developer",
                url="https://hh.ru/vacancy/1",
                salary_from=100000,
                salary_to=150000,
                employer="Company1",
            )
            vacancy2 = Vacancy(
                name="Java Developer",
                url="https://hh.ru/vacancy/2",
                salary_from=200000,
                salary_to=250000,
                employer="Company2",
            )

            saver.add_vacancy(vacancy1)
            saver.add_vacancy(vacancy2)

            # Фильтрация по нескольким критериям (используем keyword вместо name)
            vacancies = saver.get_vacancies(keyword="Python", salary_from=50000)
            assert len(vacancies) == 1
            assert vacancies[0]["name"] == "Python Developer"

    def test_json_saver_save_vacancies_empty_list(self):
        """Тест сохранения пустого списка вакансий в JSON."""
        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "test.json")
            saver = JSONSaver(filename)

            # Сохраняем пустой список
            saver._save_vacancies([])

            # Проверяем, что файл содержит пустой массив
            with open(filename, "r", encoding="utf-8") as f:
                content = f.read()
                assert content.strip() == "[]"

    def test_json_saver_get_vacancies_with_salary_from_filter(self):
        """Тест фильтрации по минимальной зарплате в JSONSaver."""
        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "test.json")
            saver = JSONSaver(filename)

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

            saver.add_vacancy(vacancy1)
            saver.add_vacancy(vacancy2)

            # Фильтрация по минимальной зарплате
            vacancies = saver.get_vacancies(salary_from=120000)
            assert len(vacancies) == 1
            assert vacancies[0]["name"] == "Test2"

    def test_json_saver_get_vacancies_with_salary_to_filter(self):
        """Тест фильтрации по максимальной зарплате в JSONSaver."""
        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "test.json")
            saver = JSONSaver(filename)

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

            saver.add_vacancy(vacancy1)
            saver.add_vacancy(vacancy2)

            # Фильтрация по максимальной зарплате
            vacancies = saver.get_vacancies(salary_to=180000)
            assert len(vacancies) == 1
            assert vacancies[0]["name"] == "Test1"

    def test_json_saver_load_vacancies_file_not_found(self):
        """Тест загрузки вакансий из несуществующего файла."""
        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "nonexistent.json")
            saver = JSONSaver(filename)

            # Файл не существует, должен вернуть пустой список
            vacancies = saver._load_vacancies()
            assert vacancies == []

    def test_json_saver_load_vacancies_invalid_json(self):
        """Тест загрузки вакансий из файла с невалидным JSON."""
        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "invalid.json")

            # Создаем файл с невалидным JSON
            with open(filename, "w", encoding="utf-8") as f:
                f.write("invalid json content")

            saver = JSONSaver(filename)

            # Невалидный JSON должен вернуть пустой список
            vacancies = saver._load_vacancies()
            assert vacancies == []

    def test_json_saver_get_vacancies_with_employer_filter(self):
        """Тест фильтрации по работодателю в JSONSaver."""
        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "test.json")
            saver = JSONSaver(filename)

            vacancy1 = Vacancy(
                name="Test1", url="https://hh.ru/vacancy/1", employer="Company1"
            )
            vacancy2 = Vacancy(
                name="Test2", url="https://hh.ru/vacancy/2", employer="Company2"
            )

            saver.add_vacancy(vacancy1)
            saver.add_vacancy(vacancy2)

            # Фильтрация по работодателю
            vacancies = saver.get_vacancies(employer="Company1")
            assert len(vacancies) == 1
            assert vacancies[0]["name"] == "Test1"

    def test_csv_saver_save_vacancies_empty_list(self):
        """Тест сохранения пустого списка вакансий в CSV."""
        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "test.csv")
            saver = CSVSaver(filename)

            # Сохраняем пустой список
            saver._save_vacancies([])

            # Проверяем, что файл создан с заголовками
            with open(filename, "r", encoding="utf-8", newline="") as f:
                content = f.read()
                assert "name" in content
                assert "url" in content

    def test_csv_saver_load_vacancies_with_invalid_salary(self):
        """Тест загрузки CSV с невалидными данными зарплаты."""
        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "test.csv")

            # Создаем CSV файл с невалидными данными зарплаты
            with open(filename, "w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(
                    [
                        "name",
                        "url",
                        "salary_from",
                        "salary_to",
                        "currency",
                        "description",
                        "requirements",
                        "employer",
                    ]
                )
                writer.writerow(
                    [
                        "Test",
                        "https://hh.ru/vacancy/1",
                        "invalid",
                        "also_invalid",
                        "RUR",
                        "desc",
                        "req",
                        "emp",
                    ]
                )

            saver = CSVSaver(filename)
            vacancies = saver._load_vacancies()

            # Невалидные данные должны быть преобразованы в None
            assert len(vacancies) == 1
            assert vacancies[0]["salary_from"] is None
            assert vacancies[0]["salary_to"] is None

    def test_csv_saver_load_vacancies_file_not_found_error(self):
        """Тест обработки FileNotFoundError в CSVSaver."""
        import os
        import tempfile

        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "nonexistent.csv")

            # Удаляем файл если он существует
            if os.path.exists(filename):
                os.remove(filename)

            saver = CSVSaver(filename)

            # Должен вернуть пустой список при FileNotFoundError
            vacancies = saver._load_vacancies()
            assert vacancies == []

    def test_json_saver_get_vacancies_with_multiple_filters(self):
        """Тест фильтрации по нескольким критериям в JSONSaver."""
        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "test.json")
            saver = JSONSaver(filename)

            vacancy1 = Vacancy(
                name="Python Developer",
                url="https://hh.ru/vacancy/1",
                salary_from=100000,
                salary_to=150000,
                employer="Company1",
            )
            vacancy2 = Vacancy(
                name="Java Developer",
                url="https://hh.ru/vacancy/2",
                salary_from=200000,
                salary_to=250000,
                employer="Company2",
            )

            saver.add_vacancy(vacancy1)
            saver.add_vacancy(vacancy2)

            # Фильтрация по нескольким критериям (используем keyword вместо name)
            vacancies = saver.get_vacancies(keyword="Python", salary_from=50000)
            assert len(vacancies) == 1
            assert vacancies[0]["name"] == "Python Developer"

    def test_csv_saver_get_vacancies_with_multiple_filters(self):
        """Тест фильтрации по нескольким критериям в CSVSaver."""
        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "test.csv")
            saver = CSVSaver(filename)

            vacancy1 = Vacancy(
                name="Python Developer",
                url="https://hh.ru/vacancy/1",
                salary_from=100000,
                salary_to=150000,
                employer="Company1",
            )
            vacancy2 = Vacancy(
                name="Java Developer",
                url="https://hh.ru/vacancy/2",
                salary_from=200000,
                salary_to=250000,
                employer="Company2",
            )

            saver.add_vacancy(vacancy1)
            saver.add_vacancy(vacancy2)

            # Фильтрация по нескольким критериям (используем keyword вместо name)
            vacancies = saver.get_vacancies(keyword="Python", salary_from=50000)
            assert len(vacancies) == 1
            assert vacancies[0]["name"] == "Python Developer"

    def test_json_saver_save_vacancies_empty_list(self):
        """Тест сохранения пустого списка вакансий в JSON."""
        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "test.json")
            saver = JSONSaver(filename)

            # Сохраняем пустой список
            saver._save_vacancies([])

            # Проверяем, что файл содержит пустой массив
            with open(filename, "r", encoding="utf-8") as f:
                content = f.read()
                assert content.strip() == "[]"

    def test_json_saver_get_vacancies_with_salary_from_filter(self):
        """Тест фильтрации по минимальной зарплате в JSONSaver."""
        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "test.json")
            saver = JSONSaver(filename)

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

            saver.add_vacancy(vacancy1)
            saver.add_vacancy(vacancy2)

            # Фильтрация по минимальной зарплате
            vacancies = saver.get_vacancies(salary_from=120000)
            assert len(vacancies) == 1
            assert vacancies[0]["name"] == "Test2"

    def test_json_saver_get_vacancies_with_salary_to_filter(self):
        """Тест фильтрации по максимальной зарплате в JSONSaver."""
        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "test.json")
            saver = JSONSaver(filename)

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

            saver.add_vacancy(vacancy1)
            saver.add_vacancy(vacancy2)

            # Фильтрация по максимальной зарплате
            vacancies = saver.get_vacancies(salary_to=180000)
            assert len(vacancies) == 1
            assert vacancies[0]["name"] == "Test1"


class TestCSVSaver:
    """Тесты для класса CSVSaver."""

    def test_init(self):
        """Тест инициализации CSVSaver."""
        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "test.csv")
            saver = CSVSaver(filename)
            assert saver.filename == filename
            assert os.path.exists(filename)

    def test_add_vacancy(self):
        """Тест добавления вакансии в CSV."""
        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "test.csv")
            saver = CSVSaver(filename)

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

            saver.add_vacancy(vacancy)

            with open(filename, "r", encoding="utf-8", newline="") as f:
                reader = csv.DictReader(f)
                data = list(reader)

            assert len(data) == 1
            assert data[0]["name"] == "Test"
            assert data[0]["url"] == "https://hh.ru/vacancy/123"

    def test_get_vacancies(self):
        """Тест получения вакансий из CSV."""
        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "test.csv")
            saver = CSVSaver(filename)

            vacancy1 = Vacancy(
                name="Test1", url="https://hh.ru/vacancy/1", salary_from=100000
            )
            vacancy2 = Vacancy(
                name="Test2", url="https://hh.ru/vacancy/2", salary_from=200000
            )

            saver.add_vacancy(vacancy1)
            saver.add_vacancy(vacancy2)

            vacancies = saver.get_vacancies()
            assert len(vacancies) == 2

    def test_delete_vacancy(self):
        """Тест удаления вакансии из CSV."""
        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "test.csv")
            saver = CSVSaver(filename)

            vacancy1 = Vacancy(name="Test1", url="https://hh.ru/vacancy/1")
            vacancy2 = Vacancy(name="Test2", url="https://hh.ru/vacancy/2")

            saver.add_vacancy(vacancy1)
            saver.add_vacancy(vacancy2)

            saver.delete_vacancy(vacancy1)

            vacancies = saver.get_vacancies()
            assert len(vacancies) == 1
            assert vacancies[0]["name"] == "Test2"

    def test_clear_all(self):
        """Тест очистки всех данных в CSV."""
        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "test.csv")
            saver = CSVSaver(filename)

            vacancy = Vacancy(name="Test", url="https://hh.ru/vacancy/123")
            saver.add_vacancy(vacancy)

            saver.clear_all()

            vacancies = saver.get_vacancies()
            assert len(vacancies) == 0

    def test_csv_saver_load_vacancies_file_not_found(self):
        """Тест загрузки вакансий из несуществующего CSV файла."""
        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "nonexistent.csv")
            saver = CSVSaver(filename)

            # Файл не существует, должен вернуть пустой список
            vacancies = saver._load_vacancies()
            assert vacancies == []

    def test_csv_saver_load_vacancies_empty_file(self):
        """Тест загрузки вакансий из пустого CSV файла."""
        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "empty.csv")

            # Создаем пустой файл
            with open(filename, "w", encoding="utf-8") as f:
                pass

            saver = CSVSaver(filename)

            # Пустой файл должен вернуть пустой список
            vacancies = saver._load_vacancies()
            assert vacancies == []

    def test_csv_saver_get_vacancies_with_employer_filter(self):
        """Тест фильтрации по работодателю в CSVSaver."""
        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "test.csv")
            saver = CSVSaver(filename)

            vacancy1 = Vacancy(
                name="Test1", url="https://hh.ru/vacancy/1", employer="Company1"
            )
            vacancy2 = Vacancy(
                name="Test2", url="https://hh.ru/vacancy/2", employer="Company2"
            )

            saver.add_vacancy(vacancy1)
            saver.add_vacancy(vacancy2)

            # Фильтрация по работодателю
            vacancies = saver.get_vacancies(employer="Company1")
            assert len(vacancies) == 1
            assert vacancies[0]["name"] == "Test1"

    def test_csv_saver_save_vacancies_empty_list(self):
        """Тест сохранения пустого списка вакансий в CSV."""
        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "test.csv")
            saver = CSVSaver(filename)

            # Сохраняем пустой список
            saver._save_vacancies([])

            # Проверяем, что файл создан с заголовками
            with open(filename, "r", encoding="utf-8", newline="") as f:
                content = f.read()
                assert "name" in content
                assert "url" in content

    def test_csv_saver_load_vacancies_with_invalid_salary(self):
        """Тест загрузки CSV с невалидными данными зарплаты."""
        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "test.csv")

            # Создаем CSV файл с невалидными данными зарплаты
            with open(filename, "w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(
                    [
                        "name",
                        "url",
                        "salary_from",
                        "salary_to",
                        "currency",
                        "description",
                        "requirements",
                        "employer",
                    ]
                )
                writer.writerow(
                    [
                        "Test",
                        "https://hh.ru/vacancy/1",
                        "invalid",
                        "also_invalid",
                        "RUR",
                        "desc",
                        "req",
                        "emp",
                    ]
                )

            saver = CSVSaver(filename)
            vacancies = saver._load_vacancies()

            # Невалидные данные должны быть преобразованы в None
            assert len(vacancies) == 1
            assert vacancies[0]["salary_from"] is None
            assert vacancies[0]["salary_to"] is None

    def test_csv_saver_load_vacancies_file_not_found_error(self):
        """Тест обработки FileNotFoundError в CSVSaver."""
        import os
        import tempfile

        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "nonexistent.csv")

            # Удаляем файл если он существует
            if os.path.exists(filename):
                os.remove(filename)

            saver = CSVSaver(filename)

            # Должен вернуть пустой список при FileNotFoundError
            vacancies = saver._load_vacancies()
            assert vacancies == []

    def test_json_saver_get_vacancies_with_multiple_filters(self):
        """Тест фильтрации по нескольким критериям в JSONSaver."""
        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "test.json")
            saver = JSONSaver(filename)

            vacancy1 = Vacancy(
                name="Python Developer",
                url="https://hh.ru/vacancy/1",
                salary_from=100000,
                salary_to=150000,
                employer="Company1",
            )
            vacancy2 = Vacancy(
                name="Java Developer",
                url="https://hh.ru/vacancy/2",
                salary_from=200000,
                salary_to=250000,
                employer="Company2",
            )

            saver.add_vacancy(vacancy1)
            saver.add_vacancy(vacancy2)

            # Фильтрация по нескольким критериям (используем keyword вместо name)
            vacancies = saver.get_vacancies(keyword="Python", salary_from=50000)
            assert len(vacancies) == 1
            assert vacancies[0]["name"] == "Python Developer"

    def test_csv_saver_get_vacancies_with_multiple_filters(self):
        """Тест фильтрации по нескольким критериям в CSVSaver."""
        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "test.csv")
            saver = CSVSaver(filename)

            vacancy1 = Vacancy(
                name="Python Developer",
                url="https://hh.ru/vacancy/1",
                salary_from=100000,
                salary_to=150000,
                employer="Company1",
            )
            vacancy2 = Vacancy(
                name="Java Developer",
                url="https://hh.ru/vacancy/2",
                salary_from=200000,
                salary_to=250000,
                employer="Company2",
            )

            saver.add_vacancy(vacancy1)
            saver.add_vacancy(vacancy2)

            # Фильтрация по нескольким критериям (используем keyword вместо name)
            vacancies = saver.get_vacancies(keyword="Python", salary_from=50000)
            assert len(vacancies) == 1
            assert vacancies[0]["name"] == "Python Developer"

    def test_json_saver_save_vacancies_empty_list(self):
        """Тест сохранения пустого списка вакансий в JSON."""
        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "test.json")
            saver = JSONSaver(filename)

            # Сохраняем пустой список
            saver._save_vacancies([])

            # Проверяем, что файл содержит пустой массив
            with open(filename, "r", encoding="utf-8") as f:
                content = f.read()
                assert content.strip() == "[]"

    def test_json_saver_get_vacancies_with_salary_from_filter(self):
        """Тест фильтрации по минимальной зарплате в JSONSaver."""
        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "test.json")
            saver = JSONSaver(filename)

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

            saver.add_vacancy(vacancy1)
            saver.add_vacancy(vacancy2)

            # Фильтрация по минимальной зарплате
            vacancies = saver.get_vacancies(salary_from=120000)
            assert len(vacancies) == 1
            assert vacancies[0]["name"] == "Test2"

    def test_json_saver_get_vacancies_with_salary_to_filter(self):
        """Тест фильтрации по максимальной зарплате в JSONSaver."""
        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "test.json")
            saver = JSONSaver(filename)

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

            saver.add_vacancy(vacancy1)
            saver.add_vacancy(vacancy2)

            # Фильтрация по максимальной зарплате
            vacancies = saver.get_vacancies(salary_to=180000)
            assert len(vacancies) == 1
            assert vacancies[0]["name"] == "Test1"
