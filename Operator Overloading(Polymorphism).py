class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add_simple(self, other):
        new_x = self.x + other.x
        new_y = self.y + other.y
        return Vector(new_x, new_y)
    #Below are the operator overloading methods for addition, subtraction, multiplication, and division.
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar):
        return Vector(self.x / scalar, self.y / scalar)

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

    def give(self):
        return self.__repr__()

# Example usage:
v1 = Vector(2, 3)
v2 = Vector(4, 7)
v7 = v1.add_simple(v2) # Vector addition through simple add function
v3 = v1 + v2  # Vector addition through dunder function
v4 = v2 - v1  # Vector subtraction
v5 = v1 * 2   # Scalar multiplication
v6 = v2 / 2   # Scalar division

print(v7)  # Output: Vector(6, 11)
print(v3)  # Output: Vector(6, 11)
print(v4)  # Output: Vector(2, 5)
print(v5)  # Output: Vector(4, 6)
print(v6)  # Output: Vector(2.0, 4.0)
