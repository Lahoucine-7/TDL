# models/subtask.py

class Subtask:
    def __init__(self, task_key, title, description=None, key=None, done=False):
        self.key = key
        self.task_key = task_key
        self.title = title
        self.description = description
        self.done = done

    def __str__(self):
        return f"Subtask(key={self.key}, task_key={self.task_key}, title={self.title})"

    def to_dict(self):
        return {
            "key": self.key,
            "task_key": self.task_key,
            "title": self.title,
            "description": self.description,
            "done": self.done
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            task_key=data.get("task_key"),
            title=data.get("title"),
            description=data.get("description"),
            key=data.get("key"),
            done=data.get("done", False)
        )
