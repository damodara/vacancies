import os
import sys

# Добавляем путь к модулям в sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from src.user_interface import user_interaction


def main():
    """
    Главная функция программы.
    Запускает интерфейс взаимодействия с пользователем.
    """
    try:
        user_interaction()
    except KeyboardInterrupt:
        print("\n\nПрограмма прервана пользователем.")
    except Exception as e:
        print(f"\nПроизошла ошибка: {e}")
        print("Программа завершена.")


if __name__ == "__main__":
    main()
