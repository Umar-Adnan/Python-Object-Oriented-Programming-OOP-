# In this code, we define a class named 'Student' that has a constructor method '__init__'.
# The constructor is called when an object of the class is created.
# It initializes the instance variables 'name' and 'age' by taking input from the user.
# After initializing the variables, it prints a message indicating that the Student object
# has been created along with the name and age of the student.
class Student:
    def __init__(self):
        self.name=input("Enter you name: ")
        self.age =int(input("Enter your age: "))
        print(f"\tStudent object s1 with name: {self.name}\n\tand age: {self.age} is created")  #message to indicate that the object has been created

s1=Student() # This line creates an instance of the Student class
s2=Student() # This line creates another instance of the Student class