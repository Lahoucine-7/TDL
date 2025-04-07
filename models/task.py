# models/task.py

class Task:
    def __init__(self, title, description=None, date=None, time=None, duration=None, key=None, done=False):
        self.key = key
        self.title = title
        self.description = description
        self.date = date
        self.time = time 
        self.duration = duration 
        self.done = done
        self.subtasks = []  # List to store associated subtasks

    def __str__(self):
        # Simulate strikethrough if task is done (for a more advanced UI, consider using images or custom drawing)
        if self.done:
            return f"~~Task(key={self.key}, title={self.title})~~"
        return f"Task(key={self.key}, title={self.title})"

    def to_dict(self):
        return {
            "key": self.key,
            "title": self.title,
            "description": self.description,
            "date": self.date,
            "time": self.time,
            "duration": self.duration,
            "subtasks": [subtask.to_dict() for subtask in self.subtasks],
            "done": self.done
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            title=data.get("title"),
            description=data.get("description"),
            date=data.get("date"),
            time=data.get("time"),
            duration=data.get("duration"),
            key=data.get("key"),
            done=data.get("done", False)
        )

    def add_subtask(self, subtask):
        self.subtasks.append(subtask)
