def add_task(tasks, task):
    """Add a new task to the list"""
    tasks.append({"task": task, "completed": False})
    print(f"Task '{task}' added successfully!")

def view_tasks(tasks):
    """Display all tasks with their completion status"""
    if not tasks:
        print("No tasks in the list!")
        return
    
    print("\nYour To-Do List:")
    print("-" * 30)
    for index, task in enumerate(tasks, 1):
        status = "✓" if task["completed"] else " "
        print(f"{index}. [{status}] {task['task']}")
    print("-" * 30)

def remove_task(tasks, task_index):
    """Remove a task from the list"""
    if 1 <= task_index <= len(tasks):
        removed_task = tasks.pop(task_index - 1)
        print(f"Task '{removed_task['task']}' removed successfully!")
    else:
        print("Invalid task number!")

def toggle_task(tasks, task_index):
    """Toggle the completion status of a task"""
    if 1 <= task_index <= len(tasks):
        tasks[task_index - 1]["completed"] = not tasks[task_index - 1]["completed"]
        status = "completed" if tasks[task_index - 1]["completed"] else "uncompleted"
        print(f"Task '{tasks[task_index - 1]['task']}' marked as {status}!")
    else:
        print("Invalid task number!")

def main():
    tasks = []
    
    while True:
        print("\n=== To-Do List Manager ===")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Remove Task")
        print("4. Toggle Task Completion")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ")
        
        if choice == "1":
            task = input("Enter the task: ")
            add_task(tasks, task)
        
        elif choice == "2":
            view_tasks(tasks)
        
        elif choice == "3":
            view_tasks(tasks)
            if tasks:
                task_num = int(input("Enter task number to remove: "))
                remove_task(tasks, task_num)
        
        elif choice == "4":
            view_tasks(tasks)
            if tasks:
                task_num = int(input("Enter task number to toggle: "))
                toggle_task(tasks, task_num)
        
        elif choice == "5":
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main() 