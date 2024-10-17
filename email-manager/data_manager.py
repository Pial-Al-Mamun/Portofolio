import json
from dataclasses import dataclass
import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Path to the JSON file that stores employee data
EMPLOYEE_DATA_PATH = r"./employees.json"


@dataclass(repr=True)
class Employee:
    """Data class representing an employee."""
    name: str
    email: str
    department: str
    team: int | str = 1  # Default team is set to 1


class EmployeeDataManager:
    """Class to manage employee data using a JSON file."""

    def __init__(self) -> None:
        """Initialize the EmployeeDataManager and load existing employee data."""
        self.data: dict = self.load_employee_data()

    def load_employee_data(self) -> dict:
        """Read the employee data from the specified JSON file and return it as a dictionary."""
        try:
            with open(EMPLOYEE_DATA_PATH, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            with open(EMPLOYEE_DATA_PATH, "w") as file:
                json.dump({}, file)
            print("There was no employee file. A new file has been created.")

    def upload_json_data(self, data) -> None:
        """Write the provided data to the specified JSON file."""
        try:
            with open(EMPLOYEE_DATA_PATH, "w") as file:
                json.dump(data, file, indent=4)
        except Exception as e:
            print(f"Error writing to file: {e}")

    def add_department(self) -> None:
        """Add a new department to the employee data."""
        new_department_name = input(
            "What is the name of the new department (name + Department)? ")
        new_data = {new_department_name: []}

        self.data |= new_data
        self.upload_json_data(self.data)

    def add_employee(self) -> None:
        """Add a new employee to the specified department."""
        departments_names: list[str] = list(
            self.data.keys()  # Get list of department names
        )

        for index, department in enumerate(departments_names):
            print(index + 1, department)  # Display departments to user

        department_choice: int = int(
            input("Which department to add the new employee to ") - 1
        )
        employee_name: str = input("Enter the name of the employee: ")
        employee_email: str = input("Enter the email of the employee: ")
        employee_team: int = int(input("Enter the team of the employee: "))

        new_employee = Employee(
            name=employee_name,
            email=employee_email,
            department=departments_names[department_choice],
            team=employee_team
        )
        self.data[departments_names[department_choice]].append(
            new_employee.__dict__)  # Add new employee to the chosen department
        self.upload_json_data(self.data)  # Save updated data to JSON

    def get_all_employees(self) -> list[Employee]:
        """Return a list of all employees as Employee objects."""
        employee_list = []

        for department in self.data.keys():
            employees = self.data[department]

            for employee in employees:
                employee_list.append(
                    Employee(
                        name=employee["name"],
                        email=employee["email"],
                        department=department,
                        team=employee["team"],
                    )
                )

        return employee_list

    def get_department(self) -> list[Employee]:
        """Return a list of all employees in a chosen department."""
        employee_list: list[Employee] = []

        departments = list(self.data.keys())

        for index, department_name in enumerate(departments):
            print(f"{index + 1}. {department_name}")

        department_number = int(input("Choose a department: "))
        department = self.data.get(
            departments[department_number - 1]
        )  # Fetch chosen department

        for employee in department:
            employee_list.append(
                Employee(
                    name=employee["name"],
                    email=employee["email"],
                    department=departments[department_number - 1],
                    team=employee["team"],
                )
            )

        return employee_list

    def get_department_team(self) -> list[str]:
        """Return a list of all employees that are part of a team in a department as Employee objects."""

        department_team = list(
            set(employee.team for employee in self.get_department()  # Unique teams in the chosen department
                ))

        print("Available teams:")
        for index, team in enumerate(department_team, start=1):
            print(f"Team {index}: {team}")

        team_to_send = int(input("Enter the team number: "))

        return [
            employee.email
            for employee in self.get_department()
            if employee.team == team_to_send
        ]
