class Student:
    name = ""  #class variable
    age = None       #class variable
    def initialize(n, a):  #constructor
        name = n  #instance variable
        age = a    #instance variable


s1=Student() # This line creates an instance of the Student class with the name "John" and age 20
s1.name=input("Enter the name of the student: ")  #Assigning value to the instance variable 'name' of the object 's1'
s1.age=int(input("Enter the age of the student: "))  #Assigning value to the instance variable 'age' of the object 's1'


#Printing the values of the instance variables 'name' and 'age' of the object 's1'
print(s1.name)
print(s1.age)
