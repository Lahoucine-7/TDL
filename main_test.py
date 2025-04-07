# main_test_controller.py

from controllers.task_controller import (
    ajouter_tache, modifier_tache, supprimer_tache, lister_taches,
    ajouter_subtask, modifier_subtask, supprimer_subtask
)
from models.task import Task
from models.subtask import Subtask

def main():
    # 1. Création d'une nouvelle tâche
    print("=== Création d'une nouvelle tâche ===")
    task = Task(
        titre="Tâche de test",
        description="Test de création de tâche",
        date="2025-04-07",
        heure="10:00",
        duree=45,
        key=None  # La clé sera assignée par la BDD
    )
    task_key = ajouter_tache(task)
    task.key = task_key
    print(f"Tâche créée avec key: {task_key}")

    # 2. Ajout d'une sous-tâche pour cette tâche
    print("\n=== Ajout d'une sous-tâche ===")
    subtask = Subtask(
        task_key=task.key,
        titre="Sous-tâche 1",
        description="Première sous-tâche",
        key=None
    )
    subtask_key = ajouter_subtask(subtask)
    subtask.key = subtask_key
    print(f"Sous-tâche créée avec key: {subtask_key}")

    # 3. Affichage des tâches et de leurs sous-tâches
    print("\n=== Liste des tâches et leurs sous-tâches ===")
    tasks = lister_taches()
    for t in tasks:
        print(t)
        print("  Sous-tâches:")
        for st in t.subtasks:
            print("   ", st)
    
    # 4. Modification de la tâche
    print("\n=== Modification de la tâche ===")
    task.titre = "Tâche modifiée"
    task.description = "Description mise à jour"
    modifier_tache(task)
    print("Tâche modifiée.")

    # 5. Modification de la sous-tâche
    print("\n=== Modification de la sous-tâche ===")
    subtask.titre = "Sous-tâche modifiée"
    subtask.description = "Description mise à jour"
    modifier_subtask(subtask)
    print("Sous-tâche modifiée.")

    # # 6. Nouvelle liste après modifications
    # print("\n=== Nouvelle liste des tâches et leurs sous-tâches ===")
    # tasks = lister_taches()
    # for t in tasks:
    #     print(t)
    #     print("  Sous-tâches:")
    #     for st in t.subtasks:
    #         print("   ", st)

    # # 7. Suppression de la sous-tâche
    # print("\n=== Suppression de la sous-tâche ===")
    # supprimer_subtask(subtask.key)
    # print("Sous-tâche supprimée.")

    # # 8. Liste après suppression de la sous-tâche
    # print("\n=88== Liste des tâches après suppression de la sous-tâche ===")
    # tasks = lister_taches()
    # for t in tasks:
    #     print(t)
    #     print("  Sous-tâches:")
    #     for st in t.subtasks:
    #         print("   ", st)

    # # 9. Suppression de la tâche
    # print("\n=== Suppression de la tâche ===")
    # supprimer_tache(task.key)
    # print("Tâche supprimée.")

    # # 10. Liste finale
    # print("\n=== Liste finale des tâches ===")
    # tasks = lister_taches()
    # if not tasks:
    #     print("Aucune tâche trouvée.")
    # else:
    #     for t in tasks:
    #         print(t)

if __name__ == "__main__":
    main()
