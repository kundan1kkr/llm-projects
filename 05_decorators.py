class MathUtils:
    pi = 3.14159

    def __init__(self, value):
        self.value = value

    def double(self):
        return self.value * 2

    @staticmethod
    def add(a, b):
        return a + b

    @classmethod
    def get_pi(cls):
        return cls.pi

    @classmethod
    def from_string(cls, s):
        return cls(int(s))


m = MathUtils(10)
print(m.double())
print(MathUtils.add(3, 4))
print(MathUtils.get_pi())
m2 = MathUtils.from_string("42")
print(m2.value)