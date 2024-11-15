import threading
import random
import time


class Bank:
    def __init__(self):
        self.balance = 0
        self.lock = threading.Lock()

    def deposit(self):
        for _ in range(100):
            r = random.randint(50, 500)
            self.balance += r
            time.sleep(0.001)
            print(f"Пополнение: {r}. Баланс: {self.balance}")
            time.sleep(0.001)
            if self.balance >= 500 and self.lock.locked():
                self.lock.release()
                time.sleep(0.001)

    def take(self):
        for _ in range(100):
            r = random.randint(50, 500)
            print(f"Запрос на {r}")
            if self.balance >= r:
                self.balance -= r
                print(f"Снятие: {r}. Баланс: {self.balance}")
            else:
                print("Запрос отклонён, недостаточно средств")
                self.lock.acquire()


bk = Bank()

# Т.к. методы принимают self, в потоки нужно передать сам объект класса Bank
th1 = threading.Thread(target=Bank.deposit, args=(bk,))
th2 = threading.Thread(target=Bank.take, args=(bk,))

th1.start()
th2.start()
th1.join()
th2.join()

print(f'Итоговый баланс: {bk.balance}')
