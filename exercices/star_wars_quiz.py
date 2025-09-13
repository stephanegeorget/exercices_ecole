from __future__ import annotations

"""Quiz sur Star Wars épisodes I à III et début IV."""

# Nom lisible de l'exercice pour le menu principal
DISPLAY_NAME = "Culture : Star Wars I-III + IV (début)"

from .logger import log_result


QUESTIONS = [
    {
        "question": "1. Qui accompagne Obi-Wan Kenobi pour la mission de négociation au début de l’épisode I ?",
        "options": ["Qui-Gon Jinn", "Mace Windu", "Yoda"],
        "answer": 0,
    },
    {
        "question": "2. Quelle race est Jar Jar Binks ?",
        "options": ["Gungan", "Twi'lek", "Ewok"],
        "answer": 0,
    },
    {
        "question": "3. Dans l’épisode I, sur quelle planète se déroule la course de podracers ?",
        "options": ["Tatooine", "Naboo", "Coruscant"],
        "answer": 0,
    },
    {
        "question": "4. Qui construit C-3PO à partir de pièces récupérées ?",
        "options": ["Anakin Skywalker", "Watto", "Shmi Skywalker"],
        "answer": 0,
    },
    {
        "question": "5. Comment s’appelle la reine de Naboo dans l’épisode I ?",
        "options": ["Padmé Amidala", "Jamillia", "Breha Organa"],
        "answer": 0,
    },
    {
        "question": "6. Quel est le nom du seigneur Sith qui affronte Qui-Gon et Obi-Wan à la fin de l’épisode I ?",
        "options": ["Dark Maul", "Dark Tyrannus", "Dark Sidious"],
        "answer": 0,
    },
    {
        "question": "7. Dans l’épisode II, sur quelle planète se trouve l’usine de droïdes séparatistes ?",
        "options": ["Geonosis", "Kamino", "Mustafar"],
        "answer": 0,
    },
    {
        "question": "8. Qui commande l’Armée des Clones dans l’épisode II ?",
        "options": ["Maître Yoda", "Mace Windu", "Bail Organa"],
        "answer": 0,
    },
    {
        "question": "9. Quel est le nom du chasseur de primes qui sert de modèle aux clones ?",
        "options": ["Jango Fett", "Boba Fett", "Cad Bane"],
        "answer": 0,
    },
    {
        "question": "10. Quel Jedi est chargé de la protection de Padmé Amidala au début de l’épisode II ?",
        "options": ["Obi-Wan Kenobi", "Mace Windu", "Kit Fisto"],
        "answer": 0,
    },
    {
        "question": "11. Dans l’épisode II, qui organise l’arène de Geonosis ?",
        "options": ["Poggle le Bref", "Wat Tambor", "Nute Gunray"],
        "answer": 0,
    },
    {
        "question": "12. Quel membre du Conseil Jedi découvre l’armée de clones sur Kamino ?",
        "options": ["Obi-Wan Kenobi", "Mace Windu", "Ki-Adi-Mundi"],
        "answer": 0,
    },
    {
        "question": "13. Qui est le chef de la Confédération des Systèmes Indépendants dans l’épisode II ?",
        "options": ["Comte Dooku", "Général Grievous", "Dark Sidious"],
        "answer": 0,
    },
    {
        "question": "14. Dans l’épisode III, sur quelle planète se déroule la première bataille où Anakin sauve Palpatine ?",
        "options": ["Coruscant", "Kashyyyk", "Mustafar"],
        "answer": 0,
    },
    {
        "question": "15. Comment s’appelle le général droïde que l’on voit dans l’épisode III ?",
        "options": ["Général Grievous", "Commandant Cody", "IG-88"],
        "answer": 0,
    },
    {
        "question": "16. Qui ordonne l’Ordre 66 ?",
        "options": ["Palpatine", "Yoda", "Bail Organa"],
        "answer": 0,
    },
    {
        "question": "17. Sur quelle planète Obi-Wan affronte-t-il Anakin à la fin de l’épisode III ?",
        "options": ["Mustafar", "Geonosis", "Utapau"],
        "answer": 0,
    },
    {
        "question": "18. Quel maître Jedi est tué par Anakin dans le Temple Jedi lors de la purge ?",
        "options": ["Maître Cin Drallig", "Shaak Ti", "Depa Billaba"],
        "answer": 0,
    },
    {
        "question": "19. Dans l’épisode III, quelle est la cause officielle de la mort de Padmé ?",
        "options": ["Elle perd sa volonté de vivre", "Complications médicales", "Assassinée par Anakin"],
        "answer": 0,
    },
    {
        "question": "20. Dans l’épisode III, qui conduit les bébés jumeaux vers leur famille adoptive sur Tatooine ?",
        "options": ["Obi-Wan Kenobi", "Bail Organa", "Yoda"],
        "answer": 0,
    },
    {
        "question": "21. Au début de l’épisode IV, quelle princesse transporte les plans de l’Étoile de la Mort ?",
        "options": ["Leia Organa", "Padmé Amidala", "Ahsoka Tano"],
        "answer": 0,
    },
    {
        "question": "22. Comment s’appelle le vaisseau de Dark Vador dans l’épisode IV ?",
        "options": ["Le Destroyer stellaire Devastator", "L'Executor", "Le Finalizer"],
        "answer": 0,
    },
    {
        "question": "23. Qui trouve R2-D2 et C-3PO sur Tatooine dans l’épisode IV ?",
        "options": ["Luke Skywalker", "Han Solo", "Biggs Darklighter"],
        "answer": 0,
    },
    {
        "question": "24. Quel est le nom du mentor de Luke Skywalker dans l’épisode IV ?",
        "options": ["Obi-Wan Kenobi", "Qui-Gon Jinn", "Mon Mothma"],
        "answer": 0,
    },
    {
        "question": "25. Comment s’appelle la planète désertique où grandit Luke dans l’épisode IV ?",
        "options": ["Tatooine", "Jakku", "Geonosis"],
        "answer": 0,
    },
]


def main() -> None:
    """Lance le quiz Star Wars."""

    score = 0
    for item in QUESTIONS:
        print(item["question"])
        for idx, option in enumerate(item["options"], start=1):
            print(f"{idx}. {option}")
        choice = input("Votre réponse (1-3) : ").strip()
        try:
            answer = int(choice) - 1
        except ValueError:
            answer = -1
        if answer == item["answer"]:
            print("✅ Correct !")
            score += 1
        else:
            print(f"❌ Mauvaise réponse : {item['options'][item['answer']]}")
        print()

    total = len(QUESTIONS)
    print(f"Score final : {score}/{total}")
    log_result("star_wars_quiz", score / total * 100)


if __name__ == "__main__":  # pragma: no cover - module executable
    main()

