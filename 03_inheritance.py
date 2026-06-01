class Animal:
    def __init__(self, name):
        self.name = name

    def eat(self):
        print(f"{self.name} is eating.")

    def sleep(self):
        print(f"{self.name} is sleeping.")


class Dog(Animal):
    def eat(self):
        print(f"{self.name} is gobbling food fast.")


class Cat(Animal):
    def meow(self):
        print(f"{self.name} says Meow!")


buddy = Dog("Buddy")
buddy.eat()
