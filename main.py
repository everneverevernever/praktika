class Task:
    def __init__(self, task_id, task_name='', responsible='', status=0, report='', subtasks_count=0, deadline='', start_time='', completion_time=''):
        self.id = task_id
        self.task_name = task_name
        self.responsible = responsible
        self.status = int(status)
        self.report = report
        self.subtasks_count = int(subtasks_count)
        self.deadline = deadline
        self.start_time = start_time
        self.completion_time = completion_time

    def to_dict(self):
        return {
            'id': self.id,
            'Наименование_задачи': self.task_name,
            'Сотрудник': self.responsible,
            'Статус': self.status,
            'Отчетность': self.report,
            'Количество_подзадач': self.subtasks_count,
            'Срок': self.deadline,
            'Время_начала_задачи': self.start_time,
            'Время_выполнения': self.completion_time
        }

class Subtask:
    def __init__(self, task_id, subtask_count=0, subtask_name='', completion_time=''):
        self.task_id = task_id
        self.subtask_count = int(subtask_count)
        self.subtask_name = subtask_name
        self.completion_time = completion_time

    def to_dict(self):
        return {
            'id_задачи': self.task_id,
            'Количество_подзадач': self.subtask_count,
            'Наименование_подзадачи': self.subtask_name,
            'Время_выполнения': self.completion_time
        }


class TaskManager:
    def __init__(self):
        self.tasks_file_path = 'Задачи.txt'
        self.subtasks_file_path = 'Подзадачи.txt'
        self.last_id = 0
        self.tasks = self.load_tasks_from_file()
        self.subtasks = self.load_subtasks_from_file()

    def load_tasks_from_file(self):
        tasks = []
        with open(self.tasks_file_path, 'r', encoding='utf-8') as file:
            for line in file:
                task_data = line.strip().split(';')
                task = Task(*task_data)
                tasks.append(task.to_dict())
            return tasks

    def load_subtasks_from_file(self):
        subtasks = []
        with open(self.subtasks_file_path, 'r', encoding='utf-8') as file:
            for line in file:
                subtask_data = line.strip().split(';')
                subtask = Subtask(*subtask_data)
                subtasks.append(subtask.to_dict())
            return subtasks

    def save_tasks_to_file(self):
        with open(self.tasks_file_path, 'w', encoding='utf-8') as file:
            for task in self.tasks:
                data = []
                for key in task:
                    data.append(str(task[key]))
                file.write(';'.join(data) + '\n')

    def save_subtasks_to_file(self):
        with open(self.subtasks_file_path, 'w', encoding='utf-8') as file:
            for subtask in self.subtasks:
                data = []
                for key in subtask:
                    data.append(str(subtask[key]))
                file.write(';'.join(data) + '\n')

    def generate_id(self):
        #генерация уникального ID для новой задачи
        self.last_id += 1
        return str(self.last_id)

    def show_tasks_menu(self):
        #отображение меню задач
        while True:
            print("\n=== Задачи ===")
            print("1. Добавить задачу")
            print("2. Назад")

            choice = input("Выберите действие: ")
            if choice == '1':
                self.add_task()
            elif choice == '2':
                break
            else:
                print("Некорректный выбор. Пожалуйста, повторите.")

    def add_task(self):
        #добавление новой задачи с вводом пользователем
        task_name = input("Введите наименование задачи: ")
        responsible = input("Введите сотрудника, ответственного за задачу: ")
        status = int(input("Введите статус задачи в процентах: "))
        report = input("Введите отчетность по задаче: ")
        subtasks_count = int(input("Введите количество подзадач задачи: "))
        data_srok = int(input("Введите срок выполнения задачи (в Днях, число): "))
        start_time = input("Введите время начала задачи (формат: ГГГГ-ММ-ДД): ")
        completion_time = input("Введите время выполнения задачи (формат: ГГГГ-ММ-ДД): ")

        new_task = {
            'id': self.generate_id(),
            'Наименование_задачи': task_name,
            'Сотрудник': responsible,
            'Статус': status,
            'Отчетность': report,
            'Количество_подзадач': subtasks_count,
            'Срок': data_srok,
            'Время_начала_задачи': start_time,
            'Время_выполнения': completion_time
        }

        self.tasks.append(new_task)
        self.save_tasks_to_file()
        self.add_subtasks(new_task)
        print("Задача добавлена успешно.")

    def add_subtasks(self, task):
        #добавление подзадач для задачи с вводом пользователем
        subtasks_list = []
        for i in range(task['Количество_подзадач']):
            subtask_name = input(f"Введите наименование подзадачи {i + 1}: ")
            completion_time = input(f"Введите время выполнения подзадачи {i + 1}: ")
            subtasks_list.append({
                'id_задачи': task['id'],
                'Количество_подзадач': i + 1,
                'Наименование_подзадачи': subtask_name,
                'Время_выполнения': completion_time
            })
        self.subtasks.extend(subtasks_list)
        self.save_subtasks_to_file()

    def show_main_menu(self):
        #отображение главного меню
        while True:
            print("\n=== Главное меню ===")
            print("1. Задачи")
            print("2. Подзадачи")
            print("3. Сделать отчет")
            print("4. Выход")

            choice = input("Выберите действие: ")
            if choice == '1':
                self.show_tasks_menu()
            elif choice == '2':
                self.show_subtasks_menu()
            elif choice == '3':
                self.generate_report()
            elif choice == '4':
                break
            else:
                print("Некорректный выбор. Пожалуйста, повторите.")

    def show_subtasks_menu(self):
        # Отображение меню подзадач
        while True:
            print("\n=== Подзадачи ===")
            print("1. Добавить подзадачу к задаче")
            print("2. Назад")

            choice = input("Выберите действие: ")
            if choice == '1':
                self.add_subtask()
            elif choice == '2':
                break
            else:
                print("Некорректный выбор. Пожалуйста, повторите.")

    def add_subtask(self):
        #добавление подзадачи к задаче с вводом ID задачи пользователем
        task_id = input("Введите ID задачи, к которой добавить подзадачу: ")
        task = next((t for t in self.tasks if t['id'] == task_id), None)

        if task:
            self.add_subtasks(task)
            print("Подзадачи добавлены успешно.")
        else:
            print("Задача с указанным ID не найдена.")

    def generate_report(self):
        #генерация отчета по выполненным задачам и сохранение в файл
        completed_tasks = [task for task in self.tasks if task['Статус'] == 100]

        with open('Отчет.txt', 'w', encoding='utf-8') as report_file:
            report_file.write("Наименование задачи,Сотрудник,Статус,Время выполения задачи\n")
            for task in completed_tasks:
                status = 'Выполнено' if task['Статус'] == 100 else 'Не выполнено'
                report_file.write(
                    f"{task['Наименование_задачи']},{task['Сотрудник']},{status},{task['Время_выполнения']}\n"
                )

if __name__ == "__main__":
    task_manager = TaskManager()
    task_manager.show_main_menu()
