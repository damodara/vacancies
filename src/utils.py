from typing import List

from .vacancy import Vacancy


def filter_vacancies(
    vacancies: List[Vacancy], filter_words: List[str]
) -> List[Vacancy]:
    """
    Фильтровать вакансии по ключевым словам.

    Args:
        vacancies (List[Vacancy]): Список вакансий для фильтрации
        filter_words (List[str]): Список ключевых слов для поиска

    Returns:
        List[Vacancy]: Отфильтрованный список вакансий
    """
    if not filter_words:
        return vacancies

    filtered_vacancies = []

    for vacancy in vacancies:
        # Проверяем наличие ключевых слов в названии, описании или требованиях
        text_to_search = (
            f"{vacancy.name} {vacancy.description} {vacancy.requirements}".lower()
        )

        # Проверяем, что хотя бы одно ключевое слово присутствует
        if any(word.lower() in text_to_search for word in filter_words):
            filtered_vacancies.append(vacancy)

    return filtered_vacancies


def get_vacancies_by_salary(
    vacancies: List[Vacancy], salary_range: str
) -> List[Vacancy]:
    """
    Фильтровать вакансии по диапазону зарплат.

    Args:
        vacancies (List[Vacancy]): Список вакансий для фильтрации
        salary_range (str): Диапазон зарплат в формате "min-max" или "min" или "max"

    Returns:
        List[Vacancy]: Отфильтрованный список вакансий
    """
    if not salary_range.strip():
        return vacancies

    try:
        # Парсим диапазон зарплат
        if "-" in salary_range:
            min_salary, max_salary = map(int, salary_range.split("-"))
        else:
            min_salary = int(salary_range)
            max_salary = None
    except ValueError:
        return vacancies

    filtered_vacancies = []

    for vacancy in vacancies:
        vacancy_avg = vacancy.average_salary

        if vacancy_avg is None:
            continue

        # Проверяем соответствие диапазону
        if max_salary is not None:
            if min_salary <= vacancy_avg <= max_salary:
                filtered_vacancies.append(vacancy)
        else:
            if vacancy_avg >= min_salary:
                filtered_vacancies.append(vacancy)

    return filtered_vacancies


def sort_vacancies(vacancies: List[Vacancy], reverse: bool = True) -> List[Vacancy]:
    """
    Отсортировать вакансии по зарплате.

    Args:
        vacancies (List[Vacancy]): Список вакансий для сортировки
        reverse (bool): Если True, сортировка по убыванию, иначе по возрастанию

    Returns:
        List[Vacancy]: Отсортированный список вакансий
    """
    return sorted(vacancies, reverse=reverse)


def get_top_vacancies(vacancies: List[Vacancy], top_n: int) -> List[Vacancy]:
    """
    Получить топ N вакансий по зарплате.

    Args:
        vacancies (List[Vacancy]): Список вакансий
        top_n (int): Количество вакансий для возврата

    Returns:
        List[Vacancy]: Топ N вакансий
    """
    if top_n <= 0:
        return []

    sorted_vacancies = sort_vacancies(vacancies)
    return sorted_vacancies[:top_n]


def print_vacancies(vacancies: List[Vacancy]) -> None:
    """
    Вывести вакансии в читаемом формате.

    Args:
        vacancies (List[Vacancy]): Список вакансий для вывода
    """
    if not vacancies:
        print("Вакансии не найдены.")
        return

    print(f"\nНайдено вакансий: {len(vacancies)}")
    print("=" * 80)

    for i, vacancy in enumerate(vacancies, 1):
        print(f"\n{i}. {vacancy.name}")
        print(f"   Работодатель: {vacancy.employer}")
        print(f"   Зарплата: {vacancy._get_salary_info()}")

        if vacancy.description:
            description = (
                vacancy.description[:200] + "..."
                if len(vacancy.description) > 200
                else vacancy.description
            )
            print(f"   Описание: {description}")

        if vacancy.requirements:
            requirements = (
                vacancy.requirements[:200] + "..."
                if len(vacancy.requirements) > 200
                else vacancy.requirements
            )
            print(f"   Требования: {requirements}")

        print(f"   Ссылка: {vacancy.url}")
        print("-" * 80)


def get_vacancies_by_keyword(vacancies: List[Vacancy], keyword: str) -> List[Vacancy]:
    """
    Получить вакансии с ключевым словом в описании.

    Args:
        vacancies (List[Vacancy]): Список вакансий для поиска
        keyword (str): Ключевое слово для поиска

    Returns:
        List[Vacancy]: Список вакансий, содержащих ключевое слово
    """
    if not keyword.strip():
        return vacancies

    keyword = keyword.lower()
    filtered_vacancies = []

    for vacancy in vacancies:
        # Ищем ключевое слово в названии, описании и требованиях
        search_text = (
            f"{vacancy.name} {vacancy.description} {vacancy.requirements}".lower()
        )

        if keyword in search_text:
            filtered_vacancies.append(vacancy)

    return filtered_vacancies


def remove_duplicates(vacancies: List[Vacancy]) -> List[Vacancy]:
    """
    Удалить дубликаты вакансий по URL.

    Args:
        vacancies (List[Vacancy]): Список вакансий

    Returns:
        List[Vacancy]: Список вакансий без дубликатов
    """
    seen_urls = set()
    unique_vacancies = []

    for vacancy in vacancies:
        if vacancy.url not in seen_urls:
            seen_urls.add(vacancy.url)
            unique_vacancies.append(vacancy)

    return unique_vacancies


def get_statistics(vacancies: List[Vacancy]) -> dict:
    """
    Получить статистику по вакансиям.

    Args:
        vacancies (List[Vacancy]): Список вакансий

    Returns:
        dict: Словарь со статистикой
    """
    if not vacancies:
        return {
            "total_count": 0,
            "with_salary": 0,
            "without_salary": 0,
            "avg_salary": 0,
            "min_salary": 0,
            "max_salary": 0,
            "employers": {},
        }

    salaries = []
    employers = {}

    for vacancy in vacancies:
        # Статистика по зарплатам
        avg_salary = vacancy.average_salary
        if avg_salary is not None:
            salaries.append(avg_salary)

        # Статистика по работодателям
        employer = vacancy.employer
        if employer:
            employers[employer] = employers.get(employer, 0) + 1

    with_salary = len(salaries)
    without_salary = len(vacancies) - with_salary

    return {
        "total_count": len(vacancies),
        "with_salary": with_salary,
        "without_salary": without_salary,
        "avg_salary": sum(salaries) // len(salaries) if salaries else 0,
        "min_salary": min(salaries) if salaries else 0,
        "max_salary": max(salaries) if salaries else 0,
        "employers": employers,
    }


def print_statistics(vacancies: List[Vacancy]) -> None:
    """
    Вывести статистику по вакансиям.

    Args:
        vacancies (List[Vacancy]): Список вакансий
    """
    stats = get_statistics(vacancies)

    print("\n" + "=" * 50)
    print("СТАТИСТИКА ПО ВАКАНСИЯМ")
    print("=" * 50)
    print(f"Всего вакансий: {stats['total_count']}")
    print(f"С указанной зарплатой: {stats['with_salary']}")
    print(f"Без указания зарплаты: {stats['without_salary']}")

    if stats["with_salary"] > 0:
        print(f"Средняя зарплата: {stats['avg_salary']:,} руб.")
        print(f"Минимальная зарплата: {stats['min_salary']:,} руб.")
        print(f"Максимальная зарплата: {stats['max_salary']:,} руб.")

    if stats["employers"]:
        print(f"\nТоп-5 работодателей:")
        sorted_employers = sorted(
            stats["employers"].items(), key=lambda x: x[1], reverse=True
        )
        for i, (employer, count) in enumerate(sorted_employers[:5], 1):
            print(f"{i}. {employer}: {count} вакансий")

    print("=" * 50)
