class Student : 
    school = "ABC School" # This is a class variable

    def __init__(self, name, age):
        self.name = name
        self.age = age

# Below given method is a static method as it does not have access to the instance (self) or class (cls) variables.
# It can be called using the class name without creating an instance of the class.
    @staticmethod # This is a decorator that defines a static method.
    def get_school():
        return Student.school

# Calling the static method using the class name
print(Student.get_school())  # Output: ABC School
