#!/usr/bin/python3
'''
This module defines a script to fetch and export user tasks from a REST API to a CSV file.
'''

import requests
import csv
import sys

BASE_URL = 'https://jsonplaceholder.typicode.com'


def get_user_info(id):
    '''
    Fetch user information by ID from the REST API.

    Args:
        id (int): The ID of the user.

    Returns:
        dict: User information in dictionary format.
    '''
    response = requests.get(f'{BASE_URL}/users/{id}')
    response.raise_for_status()
    return response.json()


def get_user_todos(id):
    '''
    Fetch TODOs for a given user ID from the REST API.

    Args:
        id (int): The ID of the user.

    Returns:
        list: A list of TODO items.
    '''
    response = requests.get(f'{BASE_URL}/todos', params={'userId': id})
    response.raise_for_status()
    return response.json()


def export_user_tasks_to_csv(user_id, username, tasks):
    '''
    Export user tasks to a CSV file.

    Args:
        user_id (int): The ID of the user.
        username (str): The username of the user.
        tasks (list): A list of user tasks.

    Returns:
        None
    '''
    file_name = f'{user_id}.csv'

    with open(file_name, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["USER_ID", "USERNAME", "TASK_COMPLETED_STATUS", "TASK_TITLE"])

        for task in tasks:
            csv_writer.writerow([user_id, username, task["completed"], task["title"]])

    print(f'Tasks for User {user_id} exported to {file_name}')


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <employee_id>")
        sys.exit(1)

    try:
        employee_id = int(sys.argv[1])
        user_info = get_user_info(employee_id)
        user_username = user_info.get('username')
        user_tasks = get_user_todos(employee_id)
        export_user_tasks_to_csv(employee_id, user_username, user_tasks)
    except ValueError:
        print("Error: Employee ID must be an integer.")
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
