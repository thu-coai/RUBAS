from BaseEnv import BaseEnv

class Todoist(BaseEnv):
    def __init__(self, *, parameters=None):
        super().__init__()
        self.parameters = parameters if parameters is not None else {}
        self.tasks = self.parameters.get("tasks", [])
        self.reminders = self.parameters.get("reminders", [])
        self.shared_tasks = self.parameters.get("shared_tasks", [])

        self._task_id_counter = 1

    def create_task(self, *, task_name, due_date=None, priority=None):
        if not isinstance(task_name, str) or not task_name:
            return {"success": False, "message": "Invalid or missing task_name."}
        if priority is not None and (priority < 1 or priority > 4):
            return {"success": False, "message": "Priority must be between 1 and 4."}
        task_id = str(self._task_id_counter)
        self._task_id_counter += 1
        task = {
            "id": task_id,
            "name": task_name,
            "due_date": due_date,
            "priority": priority,
            "status": "in progress"
        }
        self.tasks.append(task)
        return {"success": True, "data": {"task_id": task_id}}

    def update_task(self, *, task_id, task_name=None, due_date=None, priority=None, status=None):
        for task in self.tasks:
            if task.get("id") == task_id:
                if task_name is not None:
                    task["name"] = task_name
                if due_date is not None:
                    task["due_date"] = due_date
                if priority is not None:
                    if priority < 1 or priority > 4:
                        return {"success": False, "message": "Priority must be between 1 and 4."}
                    task["priority"] = priority
                if status is not None:
                    if status not in ["in progress", "completed"]:
                        return {"success": False, "message": "Status must be 'in progress' or 'completed'."}
                    task["status"] = status
                return {"success": True, "data": {"task": task}}
        return {"success": False, "message": "Task not found."}

    def delete_task(self, *, task_id):
        for task in self.tasks:
            if task.get("id") == task_id:
                self.tasks.remove(task)
                return {"success": True, "message": "Task deleted."}
        return {"success": False, "message": "Task not found."}

    def search_tasks(self, *, keywords=None, due_date=None, priority=None, status=None, max_results=None):
        results = []
        for task in self.tasks:
            match = True
            if keywords is not None:
                if keywords.lower() not in task.get("name", "").lower():
                    match = False
            if due_date is not None:
                if task.get("due_date") != due_date:
                    match = False
            if priority is not None:
                if task.get("priority") != priority:
                    match = False
            if status is not None:
                if task.get("status") != status:
                    match = False
            if match:
                results.append(task)
        if max_results is None:
            max_results = 10
        results = results[:max_results]
        return {"success": True, "data": {"tasks": results}}

    def set_reminder(self, *, task_id, reminder_time):
        for task in self.tasks:
            if task.get("id") == task_id:
                reminder = {
                    "task_id": task_id,
                    "reminder_time": reminder_time
                }
                self.reminders.append(reminder)
                return {"success": True, "message": "Reminder set."}
        return {"success": False, "message": "Task not found."}

    def share_task(self, *, task_id, user_email):
        for task in self.tasks:
            if task.get("id") == task_id:
                share_info = {
                    "task_id": task_id,
                    "user_email": user_email
                }
                self.shared_tasks.append(share_info)
                return {"success": True, "message": f"Task shared with {user_email}."}
        return {"success": False, "message": "Task not found."}