# models/task.py

class Task:
    def __init__(self, titre, description=None, date=None, heure=None, duree=None, key=None, done=False):
        self.key = key
        self.titre = titre
        self.description = description
        self.date = date
        self.heure = heure
        self.duree = duree
        self.done = done
        self.subtasks = []  # Liste pour stocker les sous-tâches associées

    def __str__(self):
        if self.done:
            return f"~~Task(key={self.key}, titre={self.titre})~~"
        return f"Task(key={self.key}, titre={self.titre})"

    def to_dict(self):
        return {
            "key": self.key,
            "titre": self.titre,
            "description": self.description,
            "date": self.date,
            "heure": self.heure,
            "duree": self.duree,
            "subtasks": [subtask.to_dict() for subtask in self.subtasks]
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            titre=data.get("titre"),
            description=data.get("description"),
            date=data.get("date"),
            heure=data.get("heure"),
            duree=data.get("duree"),
            key=data.get("key")
        )
    
    def add_subtask(self, subtask):
        self.subtasks.append(subtask)
