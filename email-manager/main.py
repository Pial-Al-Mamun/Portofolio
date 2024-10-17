from data_manager import EmployeeDataManager
from email_sender import EmployeeEmailSender
from os import system


def main():
    while True:
        print("Choose an option:")
        print("1. Add a new department")
        print("2. Add a new employee")
        print("3. Send email to all employees")
        print("4. Send email to all employees in a department")
        print("5. Send email to a specific team")
        print("0. Exit")
        choice = int(input("Enter your choice: "))
        system("cls || clear")

        match choice:
            case 1:
                EmployeeDataManager().add_department()
            case 2:
                EmployeeDataManager().add_employee()
            case 3:
                employees = EmployeeDataManager().get_all_employees()
                sender = EmployeeEmailSender("This is a test email.")
                sender.send_email(employees)
            case 4:
                employees = EmployeeDataManager().get_department()
                sender = EmployeeEmailSender("This is a test email.")
                sender.send_email(employees)
            case 5:
                employees = EmployeeDataManager().get_department_team()
                sender = EmployeeEmailSender("This is a test email.")
                sender.send_email(employees)
            case 0:
                print("Exiting...")
                break
            case _:
                system("cls || clear")
                print("Invalid choice.")


if __name__ == "__main__":
    main()
