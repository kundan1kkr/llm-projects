class Book:
    def __init__(self, title, pages):
        self.title = title
        self.pages = pages

    def __str__(self):
        return f"{self.title} ({self.pages} pages)"

    def __repr__(self):
        return f"Book(title='{self.title}', pages={self.pages})"

    def __len__(self):
        return self.pages

    def __eq__(self, other):
        return self.title == other.title

    def __add__(self, other):
        return Book(f"{self.title} & {other.title}", self.pages + other.pages)


b1 = Book("Atomic Habits", 320)
b2 = Book("Deep Work", 280)

print(b1)
print(repr(b1))
print(len(b1))
print(b1 == b2)
combined = b1 + b2
print(combined)
