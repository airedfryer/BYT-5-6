from abc import ABC, abstractmethod
import time


class Mediator(ABC):
    @abstractmethod
    def send_message(self, message, sender):
        pass


class Colleague(ABC):
    def __init__(self, mediator, name):
        self.mediator = mediator
        self.name = name

    @abstractmethod
    def send(self, message):
        pass

    @abstractmethod
    def receive(self, message):
        pass


class ConcreteMediator(Mediator):
    def __init__(self):
        self.user1 = None
        self.user2 = None

    def set_user1(self, user):
        self.user1 = user

    def set_user2(self, user):
        self.user2 = user

    def send_message(self, message, sender):
        time.sleep(1)
        if sender == self.user1:
            self.user2.receive(message)
            print("\n")
        elif sender == self.user2:
            self.user1.receive(message)


class User(Colleague):
    def send(self, message):
        print(f"{self.name} sends:", message)
        self.mediator.send_message(message, self)

    def receive(self, message):
        print(f"{self.name} receives:", message)


mediator = ConcreteMediator()

andrew = User(mediator, "Andy")
barbara = User(mediator, "Barbara")
christine = User(mediator, "Christine")

mediator.set_user1(andrew)
mediator.set_user2(barbara)

andrew.send("Hello, Barbara!")
time.sleep(1)
barbara.send("Hi, Andy!")

time.sleep(2)

mediator.set_user1(andrew)
mediator.set_user2(christine)

andrew.send("Hello, Christine!")
time.sleep(1)
christine.send("Good morning, Andrew.")

time.sleep(2)

mediator.set_user1(barbara)
mediator.set_user2(christine)

barbara.send("Hi, Chris!")
time.sleep(1)
christine.send("Good morning, Barbara.")
