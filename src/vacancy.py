from typing import Any, Dict, List, Optional


class Vacancy:
    """
    Класс для работы с вакансиями.
    Поддерживает методы сравнения по зарплате и валидацию данных.
    """

    __slots__ = [
        "_name",
        "_url",
        "_salary_from",
        "_salary_to",
        "_currency",
        "_description",
        "_requirements",
        "_employer",
    ]

    def __init__(
        self,
        name: str,
        url: str,
        salary_from: Optional[int] = None,
        salary_to: Optional[int] = None,
        currency: str = "RUR",
        description: str = "",
        requirements: str = "",
        employer: str = "",
    ):
        """
        Инициализация объекта вакансии.

        Args:
            name (str): Название вакансии
            url (str): Ссылка на вакансию
            salary_from (Optional[int]): Минимальная зарплата
            salary_to (Optional[int]): Максимальная зарплата
            currency (str): Валюта зарплаты
            description (str): Описание вакансии
            requirements (str): Требования к кандидату
            employer (str): Название работодателя
        """
        self._name = self._validate_name(name)
        self._url = self._validate_url(url)
        self._salary_from = self._validate_salary(salary_from)
        self._salary_to = self._validate_salary(salary_to)
        self._currency = self._validate_currency(currency)
        self._description = self._validate_text(description)
        self._requirements = self._validate_text(requirements)
        self._employer = self._validate_text(employer)

    @property
    def name(self) -> str:
        """Получить название вакансии."""
        return self._name

    @property
    def url(self) -> str:
        """Получить ссылку на вакансию."""
        return self._url

    @property
    def salary_from(self) -> Optional[int]:
        """Получить минимальную зарплату."""
        return self._salary_from

    @property
    def salary_to(self) -> Optional[int]:
        """Получить максимальную зарплату."""
        return self._salary_to

    @property
    def currency(self) -> str:
        """Получить валюту зарплаты."""
        return self._currency

    @property
    def description(self) -> str:
        """Получить описание вакансии."""
        return self._description

    @property
    def requirements(self) -> str:
        """Получить требования к кандидату."""
        return self._requirements

    @property
    def employer(self) -> str:
        """Получить название работодателя."""
        return self._employer

    @property
    def average_salary(self) -> Optional[int]:
        """
        Получить среднюю зарплату.

        Returns:
            Optional[int]: Средняя зарплата или None если зарплата не указана
        """
        if self._salary_from is not None and self._salary_to is not None:
            return (self._salary_from + self._salary_to) // 2
        elif self._salary_from is not None:
            return self._salary_from
        elif self._salary_to is not None:
            return self._salary_to
        return None

    def _validate_name(self, name: str) -> str:
        """
        Приватный метод валидации названия вакансии.

        Args:
            name (str): Название вакансии

        Returns:
            str: Валидное название вакансии

        Raises:
            ValueError: Если название пустое или содержит только пробелы
        """
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Название вакансии не может быть пустым")
        return name.strip()

    def _validate_url(self, url: str) -> str:
        """
        Приватный метод валидации URL вакансии.

        Args:
            url (str): URL вакансии

        Returns:
            str: Валидный URL

        Raises:
            ValueError: Если URL пустой или не содержит http/https
        """
        if not isinstance(url, str) or not url.strip():
            raise ValueError("URL вакансии не может быть пустым")

        url = url.strip()
        if not url.startswith(("http://", "https://")):
            raise ValueError("URL должен начинаться с http:// или https://")

        return url

    def _validate_salary(self, salary: Optional[int]) -> Optional[int]:
        """
        Приватный метод валидации зарплаты.

        Args:
            salary (Optional[int]): Зарплата

        Returns:
            Optional[int]: Валидная зарплата или None
        """
        if salary is None:
            return None

        if not isinstance(salary, int):
            try:
                salary = int(salary)
            except (ValueError, TypeError):
                return None

        if salary < 0:
            return None

        return salary

    def _validate_currency(self, currency: str) -> str:
        """
        Приватный метод валидации валюты.

        Args:
            currency (str): Валюта

        Returns:
            str: Валидная валюта
        """
        if not isinstance(currency, str) or not currency.strip():
            return "RUR"

        return currency.strip().upper()

    def _validate_text(self, text: str) -> str:
        """
        Приватный метод валидации текстовых полей.

        Args:
            text (str): Текстовое поле

        Returns:
            str: Валидный текст
        """
        if not isinstance(text, str):
            return ""

        return text.strip()

    def __str__(self) -> str:
        """
        Строковое представление вакансии.

        Returns:
            str: Строковое представление вакансии
        """
        salary_info = self._get_salary_info()
        return (
            f"Вакансия: {self._name}\n"
            f"Работодатель: {self._employer}\n"
            f"Зарплата: {salary_info}\n"
            f"Описание: {self._description[:100]}...\n"
            f"Ссылка: {self._url}"
        )

    def __repr__(self) -> str:
        """
        Представление вакансии для отладки.

        Returns:
            str: Представление вакансии
        """
        return f"Vacancy(name='{self._name}', url='{self._url}', salary_from={self._salary_from}, salary_to={self._salary_to})"

    def _get_salary_info(self) -> str:
        """
        Получить информацию о зарплате в читаемом формате.

        Returns:
            str: Информация о зарплате
        """
        if self._salary_from is None and self._salary_to is None:
            return "Зарплата не указана"

        if self._salary_from is not None and self._salary_to is not None:
            return f"{self._salary_from:,} - {self._salary_to:,} {self._currency}"
        elif self._salary_from is not None:
            return f"от {self._salary_from:,} {self._currency}"
        else:
            return f"до {self._salary_to:,} {self._currency}"

    # Методы сравнения по зарплате
    def __lt__(self, other: "Vacancy") -> bool:
        """Меньше по средней зарплате."""
        if not isinstance(other, Vacancy):
            return NotImplemented

        self_avg = self.average_salary
        other_avg = other.average_salary

        if self_avg is None and other_avg is None:
            return False
        if self_avg is None:
            return True
        if other_avg is None:
            return False

        return self_avg < other_avg

    def __le__(self, other: "Vacancy") -> bool:
        """Меньше или равно по средней зарплате."""
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self < other or self == other

    def __gt__(self, other: "Vacancy") -> bool:
        """Больше по средней зарплате."""
        if not isinstance(other, Vacancy):
            return NotImplemented

        self_avg = self.average_salary
        other_avg = other.average_salary

        if self_avg is None and other_avg is None:
            return False
        if self_avg is None:
            return False
        if other_avg is None:
            return True

        return self_avg > other_avg

    def __ge__(self, other: "Vacancy") -> bool:
        """Больше или равно по средней зарплате."""
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self > other or self == other

    def __eq__(self, other: "Vacancy") -> bool:
        """Равны по средней зарплате."""
        if not isinstance(other, Vacancy):
            return NotImplemented

        return self.average_salary == other.average_salary

    def __ne__(self, other: "Vacancy") -> bool:
        """Не равны по средней зарплате."""
        if not isinstance(other, Vacancy):
            return NotImplemented
        return not self == other

    def to_dict(self) -> Dict[str, Any]:
        """
        Преобразовать вакансию в словарь.

        Returns:
            Dict[str, Any]: Словарь с данными вакансии
        """
        return {
            "name": self._name,
            "url": self._url,
            "salary_from": self._salary_from,
            "salary_to": self._salary_to,
            "currency": self._currency,
            "description": self._description,
            "requirements": self._requirements,
            "employer": self._employer,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Vacancy":
        """
        Создать вакансию из словаря.

        Args:
            data (Dict[str, Any]): Словарь с данными вакансии

        Returns:
            Vacancy: Объект вакансии
        """
        return cls(
            name=data.get("name", ""),
            url=data.get("url", ""),
            salary_from=data.get("salary_from"),
            salary_to=data.get("salary_to"),
            currency=data.get("currency", "RUR"),
            description=data.get("description", ""),
            requirements=data.get("requirements", ""),
            employer=data.get("employer", ""),
        )

    @classmethod
    def from_hh_data(cls, hh_data: Dict[str, Any]) -> "Vacancy":
        """
        Создать вакансию из данных HeadHunter API.

        Args:
            hh_data (Dict[str, Any]): Данные вакансии из HeadHunter API

        Returns:
            Vacancy: Объект вакансии
        """
        salary_data = hh_data.get("salary")
        salary_from = salary_data.get("from") if salary_data else None
        salary_to = salary_data.get("to") if salary_data else None
        currency = salary_data.get("currency", "RUR") if salary_data else "RUR"

        snippet = hh_data.get("snippet", {})
        description = snippet.get("responsibility", "")
        requirements = snippet.get("requirement", "")

        employer_data = hh_data.get("employer", {})
        employer = employer_data.get("name", "")

        return cls(
            name=hh_data.get("name", ""),
            url=hh_data.get("alternate_url", ""),
            salary_from=salary_from,
            salary_to=salary_to,
            currency=currency,
            description=description,
            requirements=requirements,
            employer=employer,
        )

    @classmethod
    def cast_to_object_list(
        cls, vacancies_data: List[Dict[str, Any]]
    ) -> List["Vacancy"]:
        """
        Преобразовать список словарей с данными вакансий в список объектов Vacancy.

        Args:
            vacancies_data (List[Dict[str, Any]]): Список словарей с данными вакансий

        Returns:
            List[Vacancy]: Список объектов Vacancy
        """
        vacancies = []
        for vacancy_data in vacancies_data:
            try:
                vacancy = cls.from_hh_data(vacancy_data)
                vacancies.append(vacancy)
            except (ValueError, KeyError) as e:
                # Пропускаем некорректные данные
                continue

        return vacancies
