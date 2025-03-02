#!/usr/bin/env python3
# refined_treehouse_tasks.py

import json
import os
from datetime import datetime

DATA_FILE = "tasks.json"

def load_tasks():
    """
    Load tasks from a JSON file if it exists, otherwise return an empty list.
    Each task is a dictionary with:
        {
            "description": str,
            "priority": int (1=High, 5=Low),
            "due_date": str (YYYY-MM-DD or free-form),
            "completed": bool
        }
    """
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    """
    Save tasks to a JSON file (tasks.json by default).
    """
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

def add_task(tasks):
    """
    Add a new task to the list.
    Prompts for description, priority, and due date.
    """
    print("\n-- Add a New Task --")
    description = input("Task description: ").strip()
    if not description:
        print("Task description cannot be empty.")
        return tasks

    # Priority
    while True:
        priority_input = input("Priority (1=High, 5=Low): ").strip()
        if priority_input.isdigit():
            priority_value = int(priority_input)
            if 1 <= priority_value <= 5:
                break
        print("Invalid priority. Please enter a number between 1 and 5.")

    # Due Date (optional format enforcement; here we just store what the user enters)
    due_date = input("Due date (YYYY-MM-DD or leave blank): ").strip()
    if due_date == "":
        due_date = "No due date"

    new_task = {
        "description": description,
        "priority": priority_value,
        "due_date": due_date,
        "completed": False
    }
    tasks.append(new_task)
    print(f"Task '{description}' added successfully.")
    return tasks

def view_tasks(tasks):
    """
    Display all tasks with their status, priority, and due date.
    """
    print("\n-- View Tasks --")
    if not tasks:
        print("No tasks yet! Add one using the 'Add Task' option.")
        return

    for i, task in enumerate(tasks, start=1):
        status = "✓" if task["completed"] else "✗"
        print(f"{i}. [{status}] {task['description']} | Priority: {task['priority']} | Due: {task['due_date']}")
    print()  # Extra newline for spacing

def complete_task(tasks):
    """
    Mark a task as completed.
    """
    print("\n-- Complete a Task --")
    if not tasks:
        print("No tasks available to complete.")
        return tasks

    view_tasks(tasks)  # Show tasks for reference

    try:
        choice = int(input("Enter the task number to mark as completed (0 to cancel): "))
        if choice == 0:
            print("Operation cancelled.")
            return tasks
        if 1 <= choice <= len(tasks):
            tasks[choice - 1]["completed"] = True
            print(f"Task '{tasks[choice - 1]['description']}' marked completed!")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter a valid number.")

    return tasks

def remove_task(tasks):
    """
    Remove a task from the list entirely.
    """
    print("\n-- Remove a Task --")
    if not tasks:
        print("No tasks to remove.")
        return tasks

    view_tasks(tasks)

    try:
        choice = int(input("Enter the task number to remove (0 to cancel): "))
        if choice == 0:
            print("Operation cancelled.")
            return tasks
        if 1 <= choice <= len(tasks):
            removed_task = tasks.pop(choice - 1)
            print(f"Task '{removed_task['description']}' removed.")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter a valid number.")

    return tasks

def edit_task(tasks):
    """
    Edit an existing task's fields (description, priority, or due date).
    """
    print("\n-- Edit a Task --")
    if not tasks:
        print("No tasks to edit.")
        return tasks

    view_tasks(tasks)

    try:
        choice = int(input("Enter the task number to edit (0 to cancel): "))
        if choice == 0:
            print("Operation cancelled.")
            return tasks
        if 1 <= choice <= len(tasks):
            task = tasks[choice - 1]
            print(f"Editing Task #{choice}: '{task['description']}'")

            # Edit Description
            new_description = input("New description (leave blank to keep current): ").strip()
            if new_description:
                task["description"] = new_description

            # Edit Priority
            new_priority_str = input("New priority (1=High, 5=Low) [leave blank to keep current]: ").strip()
            if new_priority_str:
                if new_priority_str.isdigit():
                    new_priority = int(new_priority_str)
                    if 1 <= new_priority <= 5:
                        task["priority"] = new_priority
                    else:
                        print("Invalid priority. Keeping old value.")
                else:
                    print("Invalid priority input. Keeping old value.")

            # Edit Due Date
            new_due_date = input("New due date (YYYY-MM-DD or blank) [leave blank to keep current]: ").strip()
            if new_due_date:
                task["due_date"] = new_due_date

            print("Task updated successfully.")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter a valid number.")

    return tasks

def sort_tasks(tasks):
    """
    Sort tasks by priority or due date.
    """
    print("\n-- Sort Tasks --")
    if not tasks:
        print("No tasks to sort.")
        return tasks

    print("1. Sort by Priority (ascending: 1=High, 5=Low)")
    print("2. Sort by Due Date (ascending)")
    print("3. Cancel")
    choice = input("Select an option: ").strip()

    if choice == "1":
        tasks.sort(key=lambda t: t["priority"])
        print("Tasks sorted by priority.")
    elif choice == "2":
        # We'll try to parse due_date as YYYY-MM-DD; if it fails, we treat it as '9999-12-31' (far future)
        def parse_date(d):
            try:
                return datetime.strptime(d, "%Y-%m-%d")
            except ValueError:
                # If the date is "No due date" or an invalid format, sort it last
                return datetime(9999, 12, 31)

        tasks.sort(key=lambda t: parse_date(t["due_date"]))
        print("Tasks sorted by due date.")
    else:
        print("Sorting cancelled.")

    return tasks

def get_treehouse_level(tasks):
    """
    Return the treehouse level based on how many tasks are completed.
    We'll use the following thresholds:
        Level 0: 0 tasks completed
        Level 1: 1-4
        Level 2: 5-9
        Level 3: 10-14
        Level 4: 15-19
        Level 5: >= 20
    """
    completed_count = sum(1 for t in tasks if t["completed"])
    if completed_count >= 20:
        return 5
    elif completed_count >= 15:
        return 4
    elif completed_count >= 10:
        return 3
    elif completed_count >= 5:
        return 2
    elif completed_count >= 1:
        return 1
    else:
        return 0

def show_treehouse(tasks):
    """
    Display ASCII art representing the treehouse progress based on completed tasks.
    """
    level = get_treehouse_level(tasks)

    print("\n=== Your Treehouse ===")
    if level == 0:
        print("  (No tasks completed yet!)")
        print("        🌱 A tiny seedling sits alone...\n")
        return

    # LEVEL 1
    if level >= 1:
        print("          🌳")
        print("         🌳🌳")
        print("          🌳      A small platform is starting to form!")
        print("          ||")
        print("          ||")
        print("          ||")

    # LEVEL 2
    if level >= 2:
        print("        _______")
        print("       /       \\   The platform is now sturdy!")
        print("       |_______|")

    # LEVEL 3
    if level >= 3:
        print("         /||\\       A ladder, walls, and railings added!")
        print("        / || \\")
        print("       /  ||  \\")

    # LEVEL 4
    if level >= 4:
        print("       [__||__]      A cozy rooftop and some decorations!")
        print("          ||")
        print("          ||")

    # LEVEL 5
    if level == 5:
        print("      ~~~~~~~~~~     Lights, furniture, and a hanging swing!")
        print("      ~  BONUS ~     It's a dream come true!")
        print("      ~~~~~~~~~~")

    print()  # Blank line

def main():
    tasks = load_tasks()

    while True:
        print("========== Treehouse Tasks ==========")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Complete Task")
        print("4. Remove Task")
        print("5. Edit Task")
        print("6. Sort Tasks")
        print("7. Show My Treehouse")
        print("8. Exit")

        choice = input("Select an option: ").strip()

        if choice == "1":
            tasks = add_task(tasks)
            save_tasks(tasks)
        elif choice == "2":
            view_tasks(tasks)
        elif choice == "3":
            tasks = complete_task(tasks)
            save_tasks(tasks)
        elif choice == "4":
            tasks = remove_task(tasks)
            save_tasks(tasks)
        elif choice == "5":
            tasks = edit_task(tasks)
            save_tasks(tasks)
        elif choice == "6":
            tasks = sort_tasks(tasks)
            save_tasks(tasks)
        elif choice == "7":
            show_treehouse(tasks)
        elif choice == "8":
            print("Exiting... Thank you for using Treehouse Tasks!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()