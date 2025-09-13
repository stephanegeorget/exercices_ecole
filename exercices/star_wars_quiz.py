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
        "context": (
            "Au début de 'La Menace fantôme', Qui-Gon Jinn accompagne Obi-Wan pour négocier avec la "
            "Fédération du Commerce. Leur vaisseau est rapidement attaqué, ce qui les pousse à fuir "
            "vers Naboo."
        ),
    },
    {
        "question": "2. Quelle race est Jar Jar Binks ?",
        "options": ["Gungan", "Twi'lek", "Ewok"],
        "answer": 0,
        "context": (
            "Jar Jar Binks est un Gungan, un peuple amphibie vivant dans les lacs de Naboo. Il "
            "rencontre les Jedi après avoir été banni de sa cité sous-marine."
        ),
    },
    {
        "question": "3. Dans l’épisode I, sur quelle planète se déroule la course de podracers ?",
        "options": ["Tatooine", "Naboo", "Coruscant"],
        "answer": 0,
        "context": (
            "La course de podracers se déroule sur Tatooine, une planète désertique contrôlée par les "
            "Hutt. Anakin y gagne sa liberté en remportant la course grâce à ses talents de pilote."
        ),
    },
    {
        "question": "4. Qui construit C-3PO à partir de pièces récupérées ?",
        "options": ["Anakin Skywalker", "Watto", "Shmi Skywalker"],
        "answer": 0,
        "context": (
            "Sur Tatooine, le jeune Anakin assemble C-3PO pour aider sa mère dans les tâches "
            "domestiques. Ce droïde deviendra plus tard un compagnon fidèle de la Rébellion."
        ),
    },
    {
        "question": "5. Comment s’appelle la reine de Naboo dans l’épisode I ?",
        "options": ["Padmé Amidala", "Jamillia", "Breha Organa"],
        "answer": 0,
        "context": (
            "Padmé Amidala est la jeune souveraine de Naboo durant la crise du blocus. Elle se fait "
            "souvent passer pour une servante afin de protéger son identité lors de ses missions."
        ),
    },
    {
        "question": "6. Quel est le nom du seigneur Sith qui affronte Qui-Gon et Obi-Wan à la fin de l’épisode I ?",
        "options": ["Dark Maul", "Dark Tyrannus", "Dark Sidious"],
        "answer": 0,
        "context": (
            "Dark Maul est l'apprenti de Dark Sidious armé d'un double sabre laser. Son duel avec les "
            "deux Jedi se conclut par la mort de Qui-Gon."
        ),
    },
    {
        "question": "7. Dans l’épisode II, sur quelle planète se trouve l’usine de droïdes séparatistes ?",
        "options": ["Geonosis", "Kamino", "Mustafar"],
        "answer": 0,
        "context": (
            "Les usines secrètes de droïdes sont établies sur Geonosis, une planète rocheuse et "
            "inhospitalière. C'est là que la République découvre l'ampleur de la menace séparatiste."
        ),
    },
    {
        "question": "8. Qui commande l’Armée des Clones dans l’épisode II ?",
        "options": ["Maître Yoda", "Mace Windu", "Bail Organa"],
        "answer": 0,
        "context": (
            "Lorsque l'armée des clones intervient sur Geonosis, c'est Yoda qui en prend la "
            "tête. Cette première bataille marque le début de la Guerre des Clones."
        ),
    },
    {
        "question": "9. Quel est le nom du chasseur de primes qui sert de modèle aux clones ?",
        "options": ["Jango Fett", "Boba Fett", "Cad Bane"],
        "answer": 0,
        "context": (
            "Le code génétique de Jango Fett est utilisé pour produire les soldats clones sur "
            "Kamino. En échange, il reçoit un clone non modifié qu'il élève comme son fils Boba."
        ),
    },
    {
        "question": "10. Quel Jedi est chargé de la protection de Padmé Amidala au début de l’épisode II ?",
        "options": ["Obi-Wan Kenobi", "Mace Windu", "Kit Fisto"],
        "answer": 0,
        "context": (
            "Après les tentatives d'assassinat, Obi-Wan est chargé de protéger la sénatrice. Il "
            "confie ensuite cette mission à Anakin tandis qu'il enquête sur les conspirateurs."
        ),
    },
    {
        "question": "11. Dans l’épisode II, qui organise l’arène de Geonosis ?",
        "options": ["Poggle le Bref", "Wat Tambor", "Nute Gunray"],
        "answer": 0,
        "context": (
            "Poggle le Bref, dirigeant géonosien, orchestre l'exécution de Padmé, Anakin et "
            "Obi-Wan dans l'arène. Son peuple s'est rallié à la Confédération séparatiste."
        ),
    },
    {
        "question": "12. Quel membre du Conseil Jedi découvre l’armée de clones sur Kamino ?",
        "options": ["Obi-Wan Kenobi", "Mace Windu", "Ki-Adi-Mundi"],
        "answer": 0,
        "context": (
            "En suivant la piste d'un chasseur de primes, Obi-Wan se rend sur la planète océanique "
            "Kamino. Il y découvre une vaste armée de clones commandée pour la République."
        ),
    },
    {
        "question": "13. Qui est le chef de la Confédération des Systèmes Indépendants dans l’épisode II ?",
        "options": ["Comte Dooku", "Général Grievous", "Dark Sidious"],
        "answer": 0,
        "context": (
            "Ancien Jedi, le Comte Dooku dirige la Confédération des Systèmes Indépendants contre la "
            "République. Il agit en secret comme apprenti de Dark Sidious."
        ),
    },
    {
        "question": "14. Dans l’épisode III, sur quelle planète se déroule la première bataille où Anakin sauve Palpatine ?",
        "options": ["Coruscant", "Kashyyyk", "Mustafar"],
        "answer": 0,
        "context": (
            "L'épisode III s'ouvre sur une grande bataille au-dessus de Coruscant où le Chancelier "
            "est retenu prisonnier. Anakin y sauve Palpatine après avoir vaincu le Comte Dooku."
        ),
    },
    {
        "question": "15. Comment s’appelle le général droïde que l’on voit dans l’épisode III ?",
        "options": ["Général Grievous", "Commandant Cody", "IG-88"],
        "answer": 0,
        "context": (
            "Général Grievous est un cyborg redoutable qui dirige l'armée droïde. Il collectionne les "
            "sabres laser des Jedi qu'il a vaincus."
        ),
    },
    {
        "question": "16. Qui ordonne l’Ordre 66 ?",
        "options": ["Palpatine", "Yoda", "Bail Organa"],
        "answer": 0,
        "context": (
            "Palpatine active l'Ordre 66, une directive secrète implantée dans les clones. Ce signal "
            "provoque l'exécution de la plupart des Jedi à travers la galaxie."
        ),
    },
    {
        "question": "17. Sur quelle planète Obi-Wan affronte-t-il Anakin à la fin de l’épisode III ?",
        "options": ["Mustafar", "Geonosis", "Utapau"],
        "answer": 0,
        "context": (
            "Mustafar est un monde volcanique où Anakin, devenu Vador, élimine les chefs séparatistes. "
            "Le duel final contre Obi-Wan s'y termine par sa terrible défaite."
        ),
    },
    {
        "question": "18. Quel maître Jedi est tué par Anakin dans le Temple Jedi lors de la purge ?",
        "options": ["Maître Cin Drallig", "Shaak Ti", "Depa Billaba"],
        "answer": 0,
        "context": (
            "Cin Drallig est le maître d'armes du Temple chargé de former les Padawans. Malgré son "
            "expérience, il est abattu par Anakin durant l'assaut."
        ),
    },
    {
        "question": "19. Dans l’épisode III, quelle est la cause officielle de la mort de Padmé ?",
        "options": ["Elle perd sa volonté de vivre", "Complications médicales", "Assassinée par Anakin"],
        "answer": 0,
        "context": (
            "Après avoir donné naissance aux jumeaux, Padmé succombe officiellement au chagrin. Les "
            "médecins ne trouvent aucune blessure physique expliquant sa mort."
        ),
    },
    {
        "question": "20. Dans l’épisode III, qui conduit les bébés jumeaux vers leur famille adoptive sur Tatooine ?",
        "options": ["Obi-Wan Kenobi", "Bail Organa", "Yoda"],
        "answer": 0,
        "context": (
            "Après la chute de la République, Obi-Wan emmène Luke jusqu'à la ferme des Lars sur "
            "Tatooine. Il choisit ensuite l'exil pour veiller discrètement sur l'enfant."
        ),
    },
    {
        "question": "21. Au début de l’épisode IV, quelle princesse transporte les plans de l’Étoile de la Mort ?",
        "options": ["Leia Organa", "Padmé Amidala", "Ahsoka Tano"],
        "answer": 0,
        "context": (
            "La princesse Leia tente de livrer les plans de l'Étoile de la Mort à l'Alliance Rebelle. "
            "Avant d'être capturée, elle cache les données dans la mémoire de R2-D2."
        ),
    },
    {
        "question": "22. Comment s’appelle le vaisseau de Dark Vador dans l’épisode IV ?",
        "options": ["Le Destroyer stellaire Devastator", "L'Executor", "Le Finalizer"],
        "answer": 0,
        "context": (
            "Le Devastator est le destroyer stellaire qui capture le Tantive IV au début du film. Il "
            "représente la puissance écrasante de la flotte impériale."
        ),
    },
    {
        "question": "23. Qui trouve R2-D2 et C-3PO sur Tatooine dans l’épisode IV ?",
        "options": ["Luke Skywalker", "Han Solo", "Biggs Darklighter"],
        "answer": 0,
        "context": (
            "Les droïdes sont achetés par l'oncle Owen auprès des Jawas, et Luke les découvre à la "
            "ferme. Le message de Leia enregistré dans R2-D2 l'entraîne dans l'aventure."
        ),
    },
    {
        "question": "24. Quel est le nom du mentor de Luke Skywalker dans l’épisode IV ?",
        "options": ["Obi-Wan Kenobi", "Qui-Gon Jinn", "Mon Mothma"],
        "answer": 0,
        "context": (
            "Obi-Wan, vivant sous le nom de Ben, initie Luke à la Force et au sabre laser. Il "
            "l'accompagne jusqu'à l'Étoile de la Mort avant de se sacrifier face à Vador."
        ),
    },
    {
        "question": "25. Comment s’appelle la planète désertique où grandit Luke dans l’épisode IV ?",
        "options": ["Tatooine", "Jakku", "Geonosis"],
        "answer": 0,
        "context": (
            "Tatooine est une planète aride peuplée de fermiers d'humidité et de contrebandiers. "
            "C'est le monde natal d'Anakin et le lieu où Luke passe son enfance."
        ),
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
        print(item["context"])
        print()

    total = len(QUESTIONS)
    print(f"Score final : {score}/{total}")
    log_result("star_wars_quiz", score / total * 100)


if __name__ == "__main__":  # pragma: no cover - module executable
    main()

