"""Point d'entrée pour le programme exercices."""

from . import anglais_hello_world, hist_test, math_addition, physique_changements_etats

EXERCICES = [
    ("anglais_hello_world", anglais_hello_world.main),
    ("math_addition", math_addition.main),
    ("hist_test", hist_test.main),
    ("physique_changements_etats", physique_changements_etats.main),
]


def main():
    """Affiche un menu et lance l'exercice choisi."""
    print("Choisissez un exercice :")
    for index, (name, _) in enumerate(EXERCICES, start=1):
        print(f"{index}. {name}")
    choice = input("Votre choix : ")
    try:
        index = int(choice) - 1
        _, func = EXERCICES[index]
    except (ValueError, IndexError):
        print("Choix invalide")
        return
    func()


if __name__ == "__main__":
    main()
