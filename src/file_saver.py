import csv
import json
import os
from abc import ABC, abstractmethod
from typing import Any, Dict, List

# Пути по умолчанию для хранения данных
DEFAULT_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
DEFAULT_JSON_FILE = os.path.join(DEFAULT_DATA_DIR, "vacancies.json")
DEFAULT_CSV_FILE = os.path.join(DEFAULT_DATA_DIR, "vacancies.csv")


class FileSaver(ABC):
    """
    Абстрактный класс для работы с файлами.
    Определяет интерфейс для сохранения, загрузки и удаления данных о вакансиях.
    """

    def __init__(self, filename: str = "vacancies"):
        """
        Инициализация базового класса.

        Args:
            filename (str): Имя файла для сохранения данных
        """
        self._filename = filename

    @property
    def filename(self) -> str:
        """Получить имя файла."""
        return self._filename

    @filename.setter
    def filename(self, value: str) -> None:
        """Установить имя файла."""
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Имя файла не может быть пустым")
        self._filename = value.strip()

    @abstractmethod
    def add_vacancy(self, vacancy) -> None:
        """
        Добавить вакансию в файл.

        Args:
            vacancy (Vacancy): Объект вакансии для добавления
        """
        pass

    @abstractmethod
    def get_vacancies(self, **criteria) -> List[Dict[str, Any]]:
        """
        Получить вакансии из файла по указанным критериям.

        Args:
            **criteria: Критерии для фильтрации вакансий

        Returns:
            List[Dict[str, Any]]: Список вакансий в формате словарей
        """
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy) -> None:
        """
        Удалить вакансию из файла.

        Args:
            vacancy (Vacancy): Объект вакансии для удаления
        """
        pass

    @abstractmethod
    def clear_all(self) -> None:
        """Очистить все данные из файла."""
        pass


class JSONSaver(FileSaver):
    """
    Класс для работы с JSON-файлами.
    Наследуется от абстрактного класса FileSaver.
    """

    def __init__(self, filename: str = DEFAULT_JSON_FILE):
        """
        Инициализация класса для работы с JSON-файлами.

        Args:
            filename (str): Имя JSON-файла для сохранения данных (по умолчанию data/vacancies.json)
        """
        super().__init__(filename)
        # Создаем директорию data если она не существует
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)
        self._ensure_file_exists()

    def _ensure_file_exists(self) -> None:
        """Приватный метод для создания файла если он не существует."""
        if not os.path.exists(self._filename):
            with open(self._filename, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=2)

    def _load_vacancies(self) -> List[Dict[str, Any]]:
        """
        Приватный метод для загрузки вакансий из JSON-файла.

        Returns:
            List[Dict[str, Any]]: Список вакансий
        """
        try:
            with open(self._filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _save_vacancies(self, vacancies: List[Dict[str, Any]]) -> None:
        """
        Приватный метод для сохранения вакансий в JSON-файл.

        Args:
            vacancies (List[Dict[str, Any]]): Список вакансий для сохранения
        """
        with open(self._filename, "w", encoding="utf-8") as f:
            json.dump(vacancies, f, ensure_ascii=False, indent=2)

    def add_vacancy(self, vacancy) -> None:
        """
        Добавить вакансию в JSON-файл.
        Не добавляет дубликаты вакансий.

        Args:
            vacancy (Vacancy): Объект вакансии для добавления
        """
        vacancies = self._load_vacancies()
        vacancy_dict = vacancy.to_dict()

        # Проверяем на дубликаты по URL
        if not any(v.get("url") == vacancy_dict["url"] for v in vacancies):
            vacancies.append(vacancy_dict)
            self._save_vacancies(vacancies)

    def get_vacancies(self, **criteria) -> List[Dict[str, Any]]:
        """
        Получить вакансии из JSON-файла по указанным критериям.

        Args:
            **criteria: Критерии для фильтрации вакансий
                - keyword: ключевое слово для поиска в названии и описании
                - salary_from: минимальная зарплата
                - salary_to: максимальная зарплата
                - employer: название работодателя

        Returns:
            List[Dict[str, Any]]: Отфильтрованный список вакансий
        """
        vacancies = self._load_vacancies()

        if not criteria:
            return vacancies

        filtered_vacancies = []

        for vacancy in vacancies:
            # Фильтр по ключевому слову
            if "keyword" in criteria:
                keyword = criteria["keyword"].lower()
                if not (
                    keyword in vacancy.get("name", "").lower()
                    or keyword in vacancy.get("description", "").lower()
                    or keyword in vacancy.get("requirements", "").lower()
                ):
                    continue

            # Фильтр по минимальной зарплате
            if "salary_from" in criteria:
                vacancy_salary_from = vacancy.get("salary_from")
                if (
                    vacancy_salary_from is None
                    or vacancy_salary_from < criteria["salary_from"]
                ):
                    continue

            # Фильтр по максимальной зарплате
            if "salary_to" in criteria:
                vacancy_salary_to = vacancy.get("salary_to")
                if (
                    vacancy_salary_to is None
                    or vacancy_salary_to > criteria["salary_to"]
                ):
                    continue

            # Фильтр по работодателю
            if "employer" in criteria:
                employer = criteria["employer"].lower()
                if employer not in vacancy.get("employer", "").lower():
                    continue

            filtered_vacancies.append(vacancy)

        return filtered_vacancies

    def delete_vacancy(self, vacancy) -> None:
        """
        Удалить вакансию из JSON-файла.

        Args:
            vacancy (Vacancy): Объект вакансии для удаления
        """
        vacancies = self._load_vacancies()
        vacancy_url = vacancy.url

        # Удаляем вакансию по URL
        vacancies = [v for v in vacancies if v.get("url") != vacancy_url]
        self._save_vacancies(vacancies)

    def clear_all(self) -> None:
        """Очистить все данные из JSON-файла."""
        self._save_vacancies([])


class CSVSaver(FileSaver):
    """
    Класс для работы с CSV-файлами.
    Наследуется от абстрактного класса FileSaver.
    """

    def __init__(self, filename: str = DEFAULT_CSV_FILE):
        """
        Инициализация класса для работы с CSV-файлами.

        Args:
            filename (str): Имя CSV-файла для сохранения данных (по умолчанию data/vacancies.csv)
        """
        super().__init__(filename)
        # Создаем директорию data если она не существует
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)
        self._ensure_file_exists()

    def _ensure_file_exists(self) -> None:
        """Приватный метод для создания файла если он не существует."""
        if not os.path.exists(self._filename):
            with open(self._filename, "w", encoding="utf-8", newline="") as f:
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

    def _load_vacancies(self) -> List[Dict[str, Any]]:
        """
        Приватный метод для загрузки вакансий из CSV-файла.

        Returns:
            List[Dict[str, Any]]: Список вакансий
        """
        vacancies = []
        try:
            with open(self._filename, "r", encoding="utf-8", newline="") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Преобразуем строковые значения в нужные типы
                    if row.get("salary_from"):
                        try:
                            row["salary_from"] = int(row["salary_from"])
                        except ValueError:
                            row["salary_from"] = None
                    else:
                        row["salary_from"] = None

                    if row.get("salary_to"):
                        try:
                            row["salary_to"] = int(row["salary_to"])
                        except ValueError:
                            row["salary_to"] = None
                    else:
                        row["salary_to"] = None

                    vacancies.append(row)
        except FileNotFoundError:
            pass

        return vacancies

    def _save_vacancies(self, vacancies: List[Dict[str, Any]]) -> None:
        """
        Приватный метод для сохранения вакансий в CSV-файл.

        Args:
            vacancies (List[Dict[str, Any]]): Список вакансий для сохранения
        """
        with open(self._filename, "w", encoding="utf-8", newline="") as f:
            if vacancies:
                fieldnames = vacancies[0].keys()
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(vacancies)
            else:
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

    def add_vacancy(self, vacancy) -> None:
        """
        Добавить вакансию в CSV-файл.
        Не добавляет дубликаты вакансий.

        Args:
            vacancy (Vacancy): Объект вакансии для добавления
        """
        vacancies = self._load_vacancies()
        vacancy_dict = vacancy.to_dict()

        # Проверяем на дубликаты по URL
        if not any(v.get("url") == vacancy_dict["url"] for v in vacancies):
            vacancies.append(vacancy_dict)
            self._save_vacancies(vacancies)

    def get_vacancies(self, **criteria) -> List[Dict[str, Any]]:
        """
        Получить вакансии из CSV-файла по указанным критериям.

        Args:
            **criteria: Критерии для фильтрации вакансий

        Returns:
            List[Dict[str, Any]]: Отфильтрованный список вакансий
        """
        vacancies = self._load_vacancies()

        if not criteria:
            return vacancies

        filtered_vacancies = []

        for vacancy in vacancies:
            # Фильтр по ключевому слову
            if "keyword" in criteria:
                keyword = criteria["keyword"].lower()
                if not (
                    keyword in vacancy.get("name", "").lower()
                    or keyword in vacancy.get("description", "").lower()
                    or keyword in vacancy.get("requirements", "").lower()
                ):
                    continue

            # Фильтр по минимальной зарплате
            if "salary_from" in criteria:
                vacancy_salary_from = vacancy.get("salary_from")
                if (
                    vacancy_salary_from is None
                    or vacancy_salary_from < criteria["salary_from"]
                ):
                    continue

            # Фильтр по максимальной зарплате
            if "salary_to" in criteria:
                vacancy_salary_to = vacancy.get("salary_to")
                if (
                    vacancy_salary_to is None
                    or vacancy_salary_to > criteria["salary_to"]
                ):
                    continue

            # Фильтр по работодателю
            if "employer" in criteria:
                employer = criteria["employer"].lower()
                if employer not in vacancy.get("employer", "").lower():
                    continue

            filtered_vacancies.append(vacancy)

        return filtered_vacancies

    def delete_vacancy(self, vacancy) -> None:
        """
        Удалить вакансию из CSV-файла.

        Args:
            vacancy (Vacancy): Объект вакансии для удаления
        """
        vacancies = self._load_vacancies()
        vacancy_url = vacancy.url

        # Удаляем вакансию по URL
        vacancies = [v for v in vacancies if v.get("url") != vacancy_url]
        self._save_vacancies(vacancies)

    def clear_all(self) -> None:
        """Очистить все данные из CSV-файла."""
        self._save_vacancies([])
