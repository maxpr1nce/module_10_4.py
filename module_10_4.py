import threading
import random
import time
from queue import Queue

class Table:
    def __init__(self, number):
        self.number = number
        self.guest = None  # Гость сидит за столом, по умолчанию None

class Guest(threading.Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        wait_time = random.randint(3, 10)
        time.sleep(wait_time)  # Имитация времени на приём пищи

class Cafe:
    def __init__(self, *tables):
        self.queue = Queue()  # Очередь для гостей
        self.tables = tables   # Список столов

    def guest_arrival(self, *guests):
        for guest in guests:
            free_table = self.find_free_table()
            if free_table:  # Если есть свободный стол
                free_table.guest = guest
                guest.start()  # Запуск потока
                print(f"{guest.name} сел(-а) за стол номер {free_table.number}")
            else:  # Если свободных столов нет, добавляем в очередь
                self.queue.put(guest)
                print(f"{guest.name} в очереди")

    def find_free_table(self):
        for table in self.tables:
            if table.guest is None:  # Проверка, свободен ли стол
                return table
        return None

    def discuss_guests(self):
        while not self.queue.empty() or any(table.guest is not None for table in self.tables):
            for table in self.tables:
                if table.guest is not None:
                    if not table.guest.is_alive():  # Если гость закончил приём пищи
                        print(f"{table.guest.name} покушал(-а) и ушёл(ушла)")
                        print(f"Стол номер {table.number} свободен")
                        table.guest = None  # Освобождаем стол
                        if not self.queue.empty():  # Если в очереди гости
                            next_guest = self.queue.get()  # Берём гостя из очереди
                            table.guest = next_guest
                            next_guest.start()  # Запуск потока
                            print(f"{next_guest.name} вышел(-ла) из очереди и сел(-а) за стол номер {table.number}")

# Пример использования классов

# Создание столов
tables = [Table(number) for number in range(1, 6)]

# Имена гостей
guests_names = [
    'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
    'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
]

# Создание гостей
guests = [Guest(name) for name in guests_names]

# Заполнение кафе столами
cafe = Cafe(*tables)

# Приём гостей
cafe.guest_arrival(*guests)

# Обслуживание гостей
cafe.discuss_guests()