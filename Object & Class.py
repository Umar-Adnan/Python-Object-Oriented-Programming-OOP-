class Student:
    def __init__(self):  #default constructor
        self.name = ""  #instance variable
        self.age = 0    #instance variable
        print("Student object created")  #message to indicate that the object has been created

    def display(self):  #method to display the values of the instance variables
        print("Name: ", self.name)  #printing the value of the instance variable 'name'
        print("Age: ", self.age)    #printing the value of the instance variable 'age'

s1=Student() # This line creates an instance of the Student class
s1.name=input("Enter the name of the student: ")  #Assigning value to the instance variable 'name' of the object 's1'
s1.age=int(input("Enter the age of the student: "))  #Assigning value to the instance variable 'age' of the object 's1'

#Printing the values of the instance variables 'name' and 'age' of the object 's1'
s1.display()  # This line calls the display method of the Student class to print the name and age of the student object 's1'
s1.initialize(input("Enter the name of the student: "), int(input("Enter the age of the student: ")))  # This line calls the initialize method of the Student class to set the name and age of the student object 's1'
s1.display()