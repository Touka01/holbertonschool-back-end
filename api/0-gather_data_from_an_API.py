import requests
import sys

def fetch_employee_todo_progress(employee_id):
    base_url = 'https://jsonplaceholder.typicode.com'
    user_url = f'{base_url}/users/{employee_id}'
    todos_url = f'{base_url}/todos?userId={employee_id}'

    try:
        user_response = requests.get(user_url)
        user_data = user_response.json()
        if user_response.status_code != 200:
            print(f"Error: Unable to fetch user data for employee {employee_id}")
            return

        todos_response = requests.get(todos_url)
        todos_data = todos_response.json()
        if todos_response.status_code != 200:
            print(f"Error: Unable to fetch TODO list for employee {employee_id}")
            return

        # Count completed tasks
        completed_tasks = [task for task in todos_data if task['completed']]
        num_completed_tasks = len(completed_tasks)
        total_num_tasks = len(todos_data)

        # Display employee information and progress
        print(f"Employee {user_data['name']} is done with tasks "
              f"({num_completed_tasks}/{total_num_tasks}):")

        # Display titles of completed tasks
        for task in completed_tasks:
            print(f"\t{task['title']}")

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <employee_id>")
        sys.exit(1)

    try:
        employee_id = int(sys.argv[1])
        fetch_employee_todo_progress(employee_id)
    except ValueError:
        print("Error: Employee ID must be an integer.")
