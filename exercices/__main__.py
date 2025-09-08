"""Point d'entrée pour le programme exercices."""

from . import (
    anglais_hello_world,
    hist_test,
    math_tables_multiplication,
    physique_changements_etats,
)

EXERCICES = [
    ("anglais_hello_world", anglais_hello_world.main),
    ("hist_test", hist_test.main),
    ("physique_changements_etats", physique_changements_etats.main),
    ("math_tables_multiplication", math_tables_multiplication.main),
]


def main():
    """Affiche un menu et lance l'exercice choisi."""
    while True:
        print("Choisissez un exercice :")
        for index, (name, _) in enumerate(EXERCICES, start=1):
            print(f"{index}. {name}")
        print("0. Quitter")
        choice = input("Votre choix : ")
        if choice == "0":
            break
        try:
            index = int(choice) - 1
            _, func = EXERCICES[index]
        except (ValueError, IndexError):
            print("Choix invalide")
            continue
        func()


if __name__ == "__main__":
    main()
