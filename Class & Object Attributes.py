class Student:
    college_name = "Punjab Group of Colleges" #Class Attribute, common for all objects
    def __init__(self, n, a, m):
        self.name = n  #Object Attributes, unique for all objects, specified by the keyword self
        self.age = a   #Object Attributes, unique for all objects, specified by the keyword self
        self.marks = m #Object Attributes, unique for all objects, specified by the keyword self

s1 = Student("Ali", 20, 85)
s2 = Student("Ahmed", 21, 90)

print(f"{s1.name} is {s1.age} years old and scored {s1.marks} marks in the exam. He studies at {s1.college_name}.")
print(f"{s2.name} is {s2.age} years old and scored {s2.marks} marks in the exam. He studies at {s2.college_name}.")