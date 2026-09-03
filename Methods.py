class Student:
    std_count=0
    def __init__(self):
        self.name = input("Enter student's name: ")
        self.age = int(input("Enter student's age: "))
        self.grade = float(input("Enter student's grade: "))
        Student.std_count += 1
        print("Student created successfully!")
    #getter methods
    def get_grade(self):
        return self.grade
    def get_name(self):
        return self.name
    def get_age(self):
        return self.age
    #setter methods
    def set_grade(self, grade):
        self.grade = grade
    def set_name(self, name):
        self.name = name
    def set_age(self, age):
        self.age = age
    #method to display student information
    def info(self):
        return f"Name: {self.name}\nAge: {self.age}\nGrade: {self.grade}"


s1 = Student()
s2 = Student()
print("Total number of students:", Student.std_count)
print(s1.info())
print(s2.info())
