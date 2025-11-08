import json
from datetime import datetime
import os
from colorama import init, Fore, Style

init(autoreset=True)

class TaskManager:
    def __init__(self):
        self.tasks = []
        self.filename = 'tasks.json'
        self.load_tasks()
    
    def load_tasks(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    self.tasks = json.load(f)
            except json.JSONDecodeError:
                print(f"{Fore.RED}Error loading tasks file. Starting with empty task list.{Style.RESET_ALL}")
                self.tasks = []
    
    def save_tasks(self):
        with open(self.filename, 'w') as f:
            json.dump(self.tasks, f, indent=4)
    
    def add_task(self, title, description, due_date, priority):
        task = {
            'id': len(self.tasks) + 1,
            'title': title,
            'description': description,
            'due_date': due_date,
            'priority': priority,
            'status': 'pending',
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        self.tasks.append(task)
        self.save_tasks()
        print(f"{Fore.GREEN}Task added successfully!{Style.RESET_ALL}")
    
    def list_tasks(self, filter_status=None):
        if not self.tasks:
            print(f"{Fore.YELLOW}No tasks found.{Style.RESET_ALL}")
            return
        
        tasks_to_show = self.tasks
        if filter_status:
            tasks_to_show = [t for t in self.tasks if t['status'] == filter_status]
        
        print(f"\n{Fore.CYAN}=== Tasks ==={Style.RESET_ALL}")
        for task in tasks_to_show:
            status_color = Fore.RED if task['status'] == 'pending' else \
                          Fore.YELLOW if task['status'] == 'in-progress' else Fore.GREEN
            print(f"\nID: {task['id']}")
            print(f"Title: {Fore.BLUE}{task['title']}{Style.RESET_ALL}")
            print(f"Description: {task['description']}")
            print(f"Due Date: {task['due_date']}")
            print(f"Priority: {task['priority']}")
            print(f"Status: {status_color}{task['status']}{Style.RESET_ALL}")
            print(f"Created: {task['created_at']}")
            print("-" * 50)
    
    def update_task_status(self, task_id, new_status):
        for task in self.tasks:
            if task['id'] == task_id:
                task['status'] = new_status
                self.save_tasks()
                print(f"{Fore.GREEN}Task status updated successfully!{Style.RESET_ALL}")
                return
        print(f"{Fore.RED}Task not found!{Style.RESET_ALL}")

def test_application():
    # Create an instance of TaskManager
    tm = TaskManager()
    
    # Add a sample task
    print("\nAdding a sample task...")
    tm.add_task(
        "Complete Project Report",
        "Write and submit the quarterly project report",
        "2024-01-15",
        "high"
    )
    
    # List all tasks
    print("\nListing all tasks...")
    tm.list_tasks()
    
    # Update task status
    print("\nUpdating task status to in-progress...")
    tm.update_task_status(1, 'in-progress')
    
    # List in-progress tasks
    print("\nListing in-progress tasks...")
    tm.list_tasks('in-progress')

if __name__ == "__main__":
    test_application()