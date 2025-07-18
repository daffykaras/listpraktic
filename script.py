import json
import os

DATA_FILE = "tasks.json"

def load_tasks():
    """Загружает список задач из файла."""
    if os.path.exists(DATA_FILE): # Используем os.path.exists вместо os.path.isfile
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
        except json.JSONDecodeError:
            print(f"[{DATA_FILE}] повреждён или пуст. Создаётся новый список.")
            return []
        except IOError as e:
            print(f"Ошибка при чтении файла [{DATA_FILE}]: {e}")
            return []
    return [] # Возвращаем пустой список, если файл не существует

def save_tasks(task_list):
    """Сохраняет текущие задачи в файл."""
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(task_list, file, ensure_ascii=False, indent=2)
    except IOError as e:
        print(f"Ошибка при записи в файл [{DATA_FILE}]: {e}")

def display_menu():
    print("\n=== Меню ToDoList ===")
    print("1. Добавить новую задачу")
    print("2. Показать все задачи")
    print("3. Изменить статус задачи (выполнена/не выполнена)")
    print("4. Удалить задачу")
    print("5. Очистить весь список задач")
    print("6. Выйти и сохранить")

def create_task(task_list):
    description = input("Введите описание новой задачи: ").strip()
    if description:
        task_list.append({"task": description, "done": False})
        print(f"Задача '{description}' добавлена.")
    else:
        print("Описание задачи не может быть пустым.")

def display_tasks(task_list):
    if not task_list:
        print("Список задач пуст.")
        return

    # Разделяем задачи на выполненные и невыполненные для лучшей читаемости
    pending_tasks = [task for task in task_list if not task["done"]]
    completed_tasks = [task for task in task_list if task["done"]]

    print("\n--- Невыполненные задачи ---")
    if not pending_tasks:
        print("Нет невыполненных задач.")
    for idx, task in enumerate(pending_tasks, start=1):
        original_idx = task_list.index(task) + 1 # Находим оригинальный индекс
        print(f"{original_idx}. [ ] {task['task']}")

    print("\n--- Выполненные задачи ---")
    if not completed_tasks:
        print("Нет выполненных задач.")
    for idx, task in enumerate(completed_tasks, start=1):
        original_idx = task_list.index(task) + 1 # Находим оригинальный индекс
        print(f"{original_idx}. [x] {task['task']}")


def toggle_task_status(task_list):
    if not task_list:
        print("Список задач пуст.")
        return

    display_tasks(task_list)
    numbers_input = input("Введите номера задач для изменения статуса (через запятую): ")
    if not numbers_input:
        print("Не введены номера задач.")
        return

    try:
        # Преобразуем ввод в список уникальных чисел
        indexes_to_toggle = set()
        for n_str in numbers_input.split(','):
            num = int(n_str.strip())
            if 1 <= num <= len(task_list):
                indexes_to_toggle.add(num - 1)
            else:
                print(f"Внимание: Задача с номером {num} не найдена.")

        if not indexes_to_toggle:
            print("Не выбраны существующие задачи для изменения статуса.")
            return

        changed_count = 0
        for i in indexes_to_toggle:
            task_list[i]["done"] = not task_list[i]["done"] # Переключаем статус
            status = "выполнена" if task_list[i]["done"] else "не выполнена"
            print(f"Задача '{task_list[i]['task']}' теперь: {status}")
            changed_count += 1

        if changed_count > 0:
            print(f"{changed_count} задач(а/и) изменены.")
        else:
            print("Статус задач не изменен.")

    except ValueError:
        print("Неверный формат ввода. Введите числа, разделенные запятыми.")

def remove_task(task_list):
    if not task_list:
        print("Нет задач для удаления.")
        return

    display_tasks(task_list)
    try:
        num = int(input("Введите номер задачи для удаления: "))
        if 1 <= num <= len(task_list):
            confirm = input(f"Вы уверены, что хотите удалить задачу '{task_list[num - 1]['task']}'? (да/нет): ").strip().lower()
            if confirm == 'да':
                deleted = task_list.pop(num - 1)
                print(f"Задача '{deleted['task']}' удалена.")
            else:
                print("Удаление отменено.")
        else:
            print("Неверный номер задачи. Укажите существующий номер.")
    except ValueError:
        print("Неверный формат ввода. Введите корректное число.")

def clear_tasks(task_list):
    if not task_list:
        print("Список задач уже пуст.")
        return
    confirm = input("Вы уверены, что хотите удалить ВСЕ задачи? Это действие необратимо! (да/нет): ").strip().lower()
    if confirm == 'да':
        task_list.clear()
        print("Все задачи удалены.")
    else:
        print("Очистка отменена.")

def run():
    task_list = load_tasks()
    print("Добро пожаловать в ToDoList!")
    try:
        while True:
            display_menu()
            action = input("Выберите действие (1-6): ").strip()
            if action == "1":
                create_task(task_list)
            elif action == "2":
                display_tasks(task_list)
            elif action == "3":
                toggle_task_status(task_list)
            elif action == "4":
                remove_task(task_list)
            elif action == "5":
                clear_tasks(task_list)
            elif action == "6":
                save_tasks(task_list)
                print("Список задач сохранён. До свидания!")
                break
            else:
                print("Неверный выбор. Пожалуйста, введите число от 1 до 6.")
    except KeyboardInterrupt:
        print("\nПрограмма прервана пользователем.")
        save_tasks(task_list) # Сохраняем задачи перед аварийным выходом
        print("Изменения сохранены.")

if __name__ == "__main__": # Исправлено: if name == "main": -> if __name__ == "__main__":
    run()
