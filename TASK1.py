def display_tasks(tasks):
    """Displays the current list of tasks."""
    if not tasks:
        print("Your To-Do list is empty.")
    else:
        print("Your To-Do List:")
        for i, task in enumerate(tasks):
            status = "✓" if task["completed"] else " "
            print(f"{i + 1}. [{status}] {task['description']}")

def add_task(tasks, description):
    """Adds a new task to the list."""
    tasks.append({"description": description, "completed": False})
    print(f"Task '{description}' added.")

def mark_completed(tasks, task_index):
    """Marks a task as completed."""
    if 0 <= task_index < len(tasks):
        tasks[task_index]["completed"] = True
        print(f"Task '{tasks[task_index]['description']}' marked as completed.")
    else:
        print("Invalid task number.")

def delete_task(tasks, task_index):
    """Deletes a task from the list."""
    if 0 <= task_index < len(tasks):
        deleted_task = tasks.pop(task_index)
        print(f"Task '{deleted_task['description']}' deleted.")
    else:
        print("Invalid task number.")

def main():
    tasks = []
    while True:
        print("\n--- To-Do List Application ---")
        print("1. View tasks")
        print("2. Add task")
        print("3. Mark task as completed")
        print("4. Delete task")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            display_tasks(tasks)
        elif choice == '2':
            description = input("Enter task description: ")
            add_task(tasks, description)
        elif choice == '3':
            try:
                task_num = int(input("Enter task number to mark as completed: ")) - 1
                mark_completed(tasks, task_num)
            except ValueError:
                print("Invalid input. Please enter a number.")
        elif choice == '4':
            try:
                task_num = int(input("Enter task number to delete: ")) - 1
                delete_task(tasks, task_num)
            except ValueError:
                print("Invalid input. Please enter a number.")
        elif choice == '5':
            print("Exiting To-Do List application. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if '_name_' == '_main_':
    main()