class Dog:
    def __init__(self, name, breed, age):
        self.name = name
        self.breed = breed
        self.age = age

    def bark(self):
        print(f"{self.name} says: Woof!")


buddy = Dog("Buddy", "Labrador", 3)
rocky = Dog("Rocky", "Beagle", 5)

print(buddy.name)
buddy.bark()
rocky.bark()
