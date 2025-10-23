from .api_connector import HeadHunterAPI
from .file_saver import CSVSaver, JSONSaver
from .utils import (
    get_top_vacancies,
    get_vacancies_by_keyword,
    get_vacancies_by_salary,
    print_statistics,
    print_vacancies,
    remove_duplicates,
)
from .vacancy import Vacancy


def user_interaction():
    """
    Функция для взаимодействия с пользователем через консоль.
    Предоставляет интерфейс для поиска, фильтрации и работы с вакансиями.
    """
    print("=" * 60)
    print("ПРОГРАММА ДЛЯ РАБОТЫ С ВАКАНСИЯМИ")
    print("=" * 60)

    # Инициализация компонентов
    hh_api = HeadHunterAPI()
    json_saver = JSONSaver()
    csv_saver = CSVSaver()

    while True:
        print("\nВыберите действие:")
        print("1. Поиск вакансий на HeadHunter")
        print("2. Показать топ N вакансий по зарплате")
        print("3. Фильтр вакансий по ключевому слову")
        print("4. Фильтр вакансий по диапазону зарплат")
        print("5. Показать все сохраненные вакансии")
        print("6. Показать статистику по вакансиям")
        print("7. Очистить все сохраненные вакансии")
        print("8. Экспорт в CSV")
        print("0. Выход")

        choice = input("\nВведите номер действия: ").strip()

        if choice == "0":
            print("До свидания!")
            break

        elif choice == "1":
            _search_vacancies(hh_api, json_saver)

        elif choice == "2":
            _show_top_vacancies(json_saver)

        elif choice == "3":
            _filter_by_keyword(json_saver)

        elif choice == "4":
            _filter_by_salary(json_saver)

        elif choice == "5":
            _show_all_vacancies(json_saver)

        elif choice == "6":
            _show_statistics(json_saver)

        elif choice == "7":
            _clear_vacancies(json_saver)

        elif choice == "8":
            _export_to_csv(json_saver, csv_saver)

        else:
            print("Неверный выбор. Попробуйте снова.")


def _search_vacancies(hh_api: HeadHunterAPI, json_saver: JSONSaver) -> None:
    """
    Поиск вакансий на HeadHunter.

    Args:
        hh_api (HeadHunterAPI): API для работы с HeadHunter
        json_saver (JSONSaver): Сохранитель в JSON
    """
    search_query = input("Введите поисковый запрос: ").strip()

    if not search_query:
        print("Поисковый запрос не может быть пустым.")
        return

    try:
        print(f"\nПоиск вакансий по запросу: '{search_query}'...")
        hh_vacancies = hh_api.get_vacancies(search_query)

        if not hh_vacancies:
            print("Вакансии не найдены.")
            return

        print(f"Найдено {len(hh_vacancies)} вакансий.")

        # Преобразуем в объекты Vacancy
        vacancies_list = Vacancy.cast_to_object_list(hh_vacancies)

        # Удаляем дубликаты
        vacancies_list = remove_duplicates(vacancies_list)

        print(f"После удаления дубликатов: {len(vacancies_list)} вакансий.")

        # Сохраняем в JSON
        for vacancy in vacancies_list:
            json_saver.add_vacancy(vacancy)

        print(f"Вакансии сохранены в файл {json_saver.filename}")

        # Показываем первые 5 вакансий
        print("\nПервые 5 найденных вакансий:")
        print_vacancies(vacancies_list[:5])

    except Exception as e:
        print(f"Ошибка при поиске вакансий: {e}")


def _show_top_vacancies(json_saver: JSONSaver) -> None:
    """
    Показать топ N вакансий по зарплате.

    Args:
        json_saver (JSONSaver): Сохранитель в JSON
    """
    try:
        top_n = int(input("Введите количество вакансий для вывода в топ N: "))

        if top_n <= 0:
            print("Количество должно быть положительным числом.")
            return

        # Получаем все вакансии
        vacancies_data = json_saver.get_vacancies()
        vacancies = [Vacancy.from_dict(v) for v in vacancies_data]

        if not vacancies:
            print("Нет сохраненных вакансий.")
            return

        # Получаем топ N вакансий
        top_vacancies = get_top_vacancies(vacancies, top_n)

        print(f"\nТоп {len(top_vacancies)} вакансий по зарплате:")
        print_vacancies(top_vacancies)

    except ValueError:
        print("Введите корректное число.")
    except Exception as e:
        print(f"Ошибка: {e}")


def _filter_by_keyword(json_saver: JSONSaver) -> None:
    """
    Фильтр вакансий по ключевому слову.

    Args:
        json_saver (JSONSaver): Сохранитель в JSON
    """
    keyword = input("Введите ключевое слово для фильтрации: ").strip()

    if not keyword:
        print("Ключевое слово не может быть пустым.")
        return

    try:
        # Получаем все вакансии
        vacancies_data = json_saver.get_vacancies()
        vacancies = [Vacancy.from_dict(v) for v in vacancies_data]

        if not vacancies:
            print("Нет сохраненных вакансий.")
            return

        # Фильтруем по ключевому слову
        filtered_vacancies = get_vacancies_by_keyword(vacancies, keyword)

        if not filtered_vacancies:
            print(f"Вакансии с ключевым словом '{keyword}' не найдены.")
            return

        print(
            f"\nНайдено {len(filtered_vacancies)} вакансий с ключевым словом '{keyword}':"
        )
        print_vacancies(filtered_vacancies)

    except Exception as e:
        print(f"Ошибка: {e}")


def _filter_by_salary(json_saver: JSONSaver) -> None:
    """
    Фильтр вакансий по диапазону зарплат.

    Args:
        json_saver (JSONSaver): Сохранитель в JSON
    """
    salary_range = input(
        "Введите диапазон зарплат (например: 100000-200000 или 100000): "
    ).strip()

    if not salary_range:
        print("Диапазон зарплат не может быть пустым.")
        return

    try:
        # Получаем все вакансии
        vacancies_data = json_saver.get_vacancies()
        vacancies = [Vacancy.from_dict(v) for v in vacancies_data]

        if not vacancies:
            print("Нет сохраненных вакансий.")
            return

        # Фильтруем по зарплате
        filtered_vacancies = get_vacancies_by_salary(vacancies, salary_range)

        if not filtered_vacancies:
            print(f"Вакансии с зарплатой в диапазоне '{salary_range}' не найдены.")
            return

        print(
            f"\nНайдено {len(filtered_vacancies)} вакансий с зарплатой в диапазоне '{salary_range}':"
        )
        print_vacancies(filtered_vacancies)

    except Exception as e:
        print(f"Ошибка: {e}")


def _show_all_vacancies(json_saver: JSONSaver) -> None:
    """
    Показать все сохраненные вакансии.

    Args:
        json_saver (JSONSaver): Сохранитель в JSON
    """
    try:
        vacancies_data = json_saver.get_vacancies()
        vacancies = [Vacancy.from_dict(v) for v in vacancies_data]

        if not vacancies:
            print("Нет сохраненных вакансий.")
            return

        print(f"\nВсе сохраненные вакансии ({len(vacancies)} шт.):")
        print_vacancies(vacancies)

    except Exception as e:
        print(f"Ошибка: {e}")


def _show_statistics(json_saver: JSONSaver) -> None:
    """
    Показать статистику по вакансиям.

    Args:
        json_saver (JSONSaver): Сохранитель в JSON
    """
    try:
        vacancies_data = json_saver.get_vacancies()
        vacancies = [Vacancy.from_dict(v) for v in vacancies_data]

        if not vacancies:
            print("Нет сохраненных вакансий.")
            return

        print_statistics(vacancies)

    except Exception as e:
        print(f"Ошибка: {e}")


def _clear_vacancies(json_saver: JSONSaver) -> None:
    """
    Очистить все сохраненные вакансии.

    Args:
        json_saver (JSONSaver): Сохранитель в JSON
    """
    confirm = (
        input("Вы уверены, что хотите удалить все вакансии? (да/нет): ").strip().lower()
    )

    if confirm in ["да", "yes", "y"]:
        try:
            json_saver.clear_all()
            print("Все вакансии удалены.")
        except Exception as e:
            print(f"Ошибка при удалении: {e}")
    else:
        print("Операция отменена.")


def _export_to_csv(json_saver: JSONSaver, csv_saver: CSVSaver) -> None:
    """
    Экспорт вакансий в CSV файл.

    Args:
        json_saver (JSONSaver): Сохранитель в JSON
        csv_saver (CSVSaver): Сохранитель в CSV
    """
    try:
        vacancies_data = json_saver.get_vacancies()

        if not vacancies_data:
            print("Нет сохраненных вакансий для экспорта.")
            return

        # Очищаем CSV файл и добавляем все вакансии
        csv_saver.clear_all()
        for vacancy_data in vacancies_data:
            vacancy = Vacancy.from_dict(vacancy_data)
            csv_saver.add_vacancy(vacancy)

        print(f"Вакансии экспортированы в файл {csv_saver.filename}")

    except Exception as e:
        print(f"Ошибка при экспорте: {e}")
