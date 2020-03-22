import sqlite3
from pandas import DataFrame

isRunning = 1 # Running variable for main loop

conn = sqlite3.connect('C:/Users/grant/Documents/Spring 2020/Database/StudentDB') # Connect to DB
c = conn.cursor() # Cursor instance

def displayTable(all_rows): # Use pandas to organize & display data
    df = DataFrame(all_rows, columns=['StudentID', 'FirstName', 'LastName', 'GPA',
                                      'Major', 'FacultyAdvisor', 'isDeleted'])
    df = df.drop(['isDeleted'], axis=1)  # Remove the isDeleted column for display
    if df.empty:  # Empty dataframe = no results for selection
        print('No results.\n')
    else:  # Otherwise print results
        print('\n', df, '\n')
def displayStudents():
    c.execute('SELECT * FROM Student WHERE isDeleted = 0')
    all_rows = c.fetchall()
    displayTable(all_rows)
def createNewStudent():
    # ALL attributes required when creating a new student
    # isDeleted = 0, user can delete later
    # Validate user input appropriately
    try:
        print('\nPlease input:')
        studentId = int(input('Student ID as int : '))
        c.execute("SELECT 1 FROM Student WHERE StudentId = ?", (studentId,)) # Make sure student doesn't exist
        doesExist = c.fetchone()
        if not doesExist: # Take in new student info
            firstName = input('First name: ')
            lastName = input('Last name: ')
            gpa = float(input('GPA as float: '))
            major = input('Major: ')
            facultyAdvisor = input('Faculty advisor: ')
            isDeleted = 0
            c.execute("INSERT INTO Student(StudentID, FirstName, LastName, GPA, Major, FacultyAdvisor, isDeleted)"
                      "VALUES (?,?,?,?,?,?,?)", (studentId, firstName, lastName, gpa, major, facultyAdvisor, isDeleted,))
            conn.commit()
            print('Student ', studentId, ' created.\n')
        else:
            print('Student with that ID already exists/ID was previously assigned. Please try again.\n')
    except sqlite3.IntegrityError:
        print('Integrity error. Check for primary key conflict.\n')
    except ValueError:
        print('Error, please check your input type.\n')
    except Exception:
        print("Error. Please try again.\n")
def updateStudent():
    # ONLY major and advisor can be updated
    # Construct proper UPDATE to not update EVERY record in the DB
    # Validate user input appropriately
    # Select student based on StudentId
    try:
        # Major/advisor updates set to empty to give user option to update one or both fields
        majorUpdate = ''
        advisorUpdate = ''
        updateId = int(input('\nPlease input student ID to select student to update: '))

        # Check if the student exists, if not then alert user
        c.execute("SELECT 1 FROM Student WHERE StudentId = ? AND isDeleted = 0", (updateId,))
        doesExist = c.fetchone()
        if doesExist:
            option1 = input('Update major? Y/N: ')
            if option1.lower() == 'y': # Take in updated major info
                majorUpdate = input('Input update: ')
            option2 = input('Update advisor? Y/N: ')
            if option2.lower() == 'y': # Take in updated advisor info
                advisorUpdate = input('Input update: ')

            # All the possibilities to update major/advisor
            if not majorUpdate and not advisorUpdate: # No updates to major/advisor
                print('No updates to make.\n')
            elif not majorUpdate: # Update to only advisor
                c.execute("UPDATE Student SET FacultyAdvisor = ? WHERE StudentId = ?",
                          (advisorUpdate, updateId,))
                conn.commit()
                print('Advisor updated to ', advisorUpdate, '.\n')
            elif not advisorUpdate: # Update to only major
                c.execute("UPDATE Student SET Major = ? WHERE StudentId = ?",
                          (majorUpdate, updateId,))
                conn.commit()
                print('Major updated to ', majorUpdate, '.\n')
            else: # Updates to both major/advisor
                c.execute("UPDATE Student SET Major = ? WHERE StudentId = ?",
                          (majorUpdate, updateId,))
                c.execute("UPDATE Student SET FacultyAdvisor = ? WHERE StudentId = ?",
                          (advisorUpdate, updateId,))
                conn.commit()
                print('Major updated to ', majorUpdate, ' and advisor updated to ', advisorUpdate, '.\n')
        else:
            print("Student with that ID does not exist. Please try again.\n")
    except ValueError:
        print('Error, please check your input type.\n')
    except Exception: # Handle exceptions
        print("Error occurred. Please check your inputs/query and try again.\n")
def deleteStudent():
    # Delete by StudentId
    # Soft delete, set isDeleted to 1
    # Validate user input appropriately
    # Secondary prompt to confirm the soft delete

    try: # Prompt for student id input
        studentId = int(input('\nPlease input student ID to delete student: '))
        c.execute("SELECT 1 FROM Student WHERE StudentId = ? AND isDeleted = 0", (studentId,))
        doesExist = c.fetchone()
        if doesExist: # Double check
            doDelete = input('Are you sure? Y/N: ')
            if doDelete.lower() == 'y': # Set isDeleted = 1
                c.execute("UPDATE Student SET isDeleted = 1 WHERE StudentId = ?",
                          (studentId,))
                conn.commit()
                print('Student ', studentId, ' deleted.\n')
            else:
                print('Nothing deleted then.\n')
        else:
            print("Student with that ID does not exist. Please try again.\n")
    except ValueError:
        print('Please input an int for the student ID.\n')
    except Exception:
        print('Error.\n')
def searchDisplayQuery(searchInput):
    try:
        if searchInput == 1:  # Search & display by major
            majorSearch = input('Please input Major to search by: ')
            c.execute("SELECT * FROM Student WHERE Major = ? AND isDeleted = 0", (majorSearch,))
            all_rows = c.fetchall()
            if all_rows:
                displayTable(all_rows)
            else:
                print('No students to display.\n')
        elif searchInput == 2:  # Search and display by exact GPA
            gpaSearch = float(input('Please input GPA to search by: '))
            c.execute("SELECT * FROM Student WHERE GPA = ? AND isDeleted = 0", (gpaSearch,))
            all_rows = c.fetchall()
            if all_rows:
                displayTable(all_rows)
            else:
                print('No students to display.\n')
        elif searchInput == 3:  # Search and display by Advisor
            advisorSearch = input('Please input Advisor to search by: ')
            c.execute("SELECT * FROM Student WHERE FacultyAdvisor = ? AND isDeleted = 0", (advisorSearch,))
            all_rows = c.fetchall()
            if all_rows:
                displayTable(all_rows)
            else:
                print('No students to display.\n')
        else:
            print('Not a valid selection. Please try again.\n')
    except Exception:
        print('Error. Please try again.\n')
def searchDisplayStudent():
    # User should be able to query by the 3 fields
    # Search by Major, GPA, Advisor
    # Display by Major, GPA, Advisor
    # Validate user input appropriately
    # Exact value for GPA
    try:
        print('\nSearch and display students by:')
        searchInput = int(input('(1) Major, (2) GPA, (3) Advisor. Input as int: '))
        searchDisplayQuery(searchInput)
    except ValueError:
        print('Please input a valid int.\n')
    except Exception:
        print('Error. Please try again.\n')

# Main loop
while(isRunning): # Set isRunning to 0 to end app
    userSelect = 0 # Reset user selection if invalid input
    print('Please select one of 6 options to execute: ')
    print('1. Display ALL students and their attributes\n'
          '2. Create a new student\n'
          '3. Update major and advisor for a student\n'
          '4. Delete student by StudentID\n'
          '5. Search/display students by Major, GPA and Advisor\n'
          '6. Exit application')
    try: # Catch invalid input
        userSelect = int(input('Make your selection as an integer: '))
    except ValueError:
        print('\nPlease input an integer selection.')

    if userSelect == 1: # Display all students
        displayStudents()
    elif userSelect == 2: # Create new student
        createNewStudent()
    elif userSelect == 3: # Update major/advisor
        updateStudent()
    elif userSelect == 4: # Delete by StudentID
        deleteStudent()
    elif userSelect == 5: # Search/display student
        searchDisplayStudent()
    elif userSelect == 6: # Exit
        print('Bye!')
        isRunning = 0
    else:
        print('Invalid input. Please try again.\n')