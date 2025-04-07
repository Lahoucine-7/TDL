class Subtask:
    def __init__(self, task_key, titre, description=None, key=None):
        self.key = key
        self.task_key = task_key
        self.titre = titre
        self.description = description

    def __str__(self):
        return f"Subtask(key={self.key}, task_id={self.task_key}, titre={self.titre})"

    def to_dict(self):
        return {
            "key": self.key,
            "task_key": self.task_key,
            "titre": self.titre,
            "description": self.description,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            task_key=data.get("task_key"),
            titre=data.get("titre"),
            description=data.get("description"),
            key=data.get("key")
        )
