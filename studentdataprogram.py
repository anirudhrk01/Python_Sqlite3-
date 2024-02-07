from contextlib import closing
import sqlite3

with closing(sqlite3.connect("student_data.db" ))as connection:
   cursor=connection.cursor()

    #table creation

   cursor.execute('''
                  CREATE TABLE IF NOT EXISTS students(
                      student_id INTEGER PRIMARY KEY,
                      name TEXT NOT NULL,
                      batch INTEGER,
                      age INTEGER NOT NULL
                  )
              ''')

   cursor.execute('''
           CREATE TABLE IF NOT EXISTS subjects(
                  subject_id INTEGER PRIMARY KEY,
                  subject_name TEXT NOT NULL
                 )
              ''')

   cursor.execute('''
           CREATE TABLE IF NOT EXISTS results(
                  results_id INTEGER PRIMARY KEY,
                  student_id INTEGER,
                  subject_id INTEGER,
                  marks INTEGER,

                  FOREIGN KEY(student_id) REFERENCES students(student_id),
                  FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
           )
   ''')

   connection.commit()


   def add_student(name, batch, age):
       try:
           batch = int(batch)
           age = int(age)
       except ValueError:
           print("Invalid input for batch or age. Please enter numeric values.")
           return

       cursor.execute('''
           INSERT INTO students(name, batch, age) VALUES(?,?,?) ''', 
           (name, batch, age))
       connection.commit()
       print("Student added.")



   def add_subject(subject_name):
       cursor.execute("INSERT INTO subjects(subject_name) VALUES(?)",(subject_name,))
       connection.commit()
       print("subject added")


   def add_marks(student_id, subject_id, marks):
       cursor.execute("INSERT INTO results(student_id,subject_id,marks) VALUES(?,?,?)",(student_id, subject_id, marks))
       connection.commit()
       print("marks added ")

   def display_student_marks(student_id):
       cursor.execute('''
                   SELECT subjects.subject_name,results.marks
                      FROM results
                      JOIN subjects ON results.subject_id=subjects.subject_id
                      WHERE results.student_id=?
                   ''',(student_id,))
       marks= cursor.fetchall()
       print("Student Marks")
       for i in marks:
           print(f"{i[0]}:{i[1]}")

   def display_subject_toppers(subject_id):
       cursor.execute('''
               SELECT students.name,results.marks
               FROM results 
               JOIN students ON 
              results.student_id=students.student_id 
              WHERE results.subject_id=?
              ORDER BY results.marks DESC LIMIT 1                                    
       ''',(subject_id,))
       topper=cursor.fetchone()
       print(f"Topper in the subject :")
       if topper:
           print(f"{topper[0]} - Marks: {topper[1]}")
       else:
           print("No data available.")

   def display_subject_average(subject_id):
       cursor.execute('''
                   SELECT AVG(marks)
                      FROM results
                      WHERE subject_id=?

           ''',(subject_id,))
       avg=cursor.fetchone()[0]
       print(f"average marks in subject is :{avg}")

   def display_top_5():
       cursor.execute('''
               SELECT students.name,subjects.subject_name,results.marks
               FROM results
               JOIN students ON results.student_id = students.student_id
               JOIN subjects ON results.subject_id= subjects.subject_id
               ORDER BY results.marks DESC
               LIMIT 5                     

       ''')
       top_5= cursor.fetchall()
       print("Top 5 marks:")
       for rank,entry in enumerate(top_5, start=1):
           print(f"{rank}. {entry[0]} --{entry[1]}: {entry[2]} ")

   while True:
       print("\n Options")
       print("1. Add Student")
       print("2. Add Subject")
       print("3. Add Marks")
       print("4. Display Student Marks")
       print("5. Display Subject Toppers")
       print("6. Display Subject Average")
       print("7. Display Top  marks")
       print("q. Quit ")

       choice=input("Enter your choice :")

       if choice=='q':
           break
       elif choice=="1":
           name=input("Enter Student name :")
           batch=input("Enter the batch :")
           age=input("Enter the age")
           add_student(name,batch,age)    

       elif choice=="2":
           subject_name=input("Enter the Sunject name") 
           add_subject(subject_name)

       elif choice=="3":
           student_id=int(input("Enter student id"))
           subject_id=int(input("Enter the subject id :"))
           marks=int(input("Enter marks:"))
           add_marks(student_id, subject_id, marks)

       elif choice=="4":
           student_id=int(input("Enter Student ID :"))
           display_student_marks(student_id)    
       
       elif choice=="5":
           subject_id=int(input("Enter stubject id :"))
           display_subject_toppers(subject_id)   
       
       elif choice=="6":
           subject_id=int(input("Enter Subject ID :"))
           display_subject_average(subject_id)

       elif  choice=="7":
           display_top_5()
       else:
           print("Ivalid choice")    







