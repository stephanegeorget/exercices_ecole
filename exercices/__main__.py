"""Point d'entrée pour le programme exercices."""

import os
import sys
import subprocess
from pathlib import Path

from . import (
    anglais_hello_world,
    hist_test,
    math_tables_multiplication,
    physique_changements_etats,
    geometrie_notation,
)

EXERCICES = [
    ("anglais_hello_world", anglais_hello_world.main),
    ("hist_test", hist_test.main),
    ("physique_changements_etats", physique_changements_etats.main),
    ("math_tables_multiplication", math_tables_multiplication.main),
    ("geometrie_notation", geometrie_notation.main),
]


def update_and_restart():
    """Met à jour le dépôt via git pull puis redémarre le programme."""
    repo_dir = Path(__file__).resolve().parent.parent
    subprocess.run(["git", "pull"], cwd=repo_dir, check=False)
    os.execv(sys.executable, [sys.executable] + sys.argv)


def main():
    """Affiche un menu et lance l'exercice choisi."""
    while True:
        print("Choisissez un exercice :")
        for index, (name, _) in enumerate(EXERCICES, start=1):
            print(f"{index}. {name}")
        print(f"{len(EXERCICES) + 1}. Mettre à jour le logiciel")
        print("0. Quitter")
        choice = input("Votre choix : ")
        if choice == "0":
            break
        if choice == str(len(EXERCICES) + 1):
            update_and_restart()
            return
        try:
            index = int(choice) - 1
            _, func = EXERCICES[index]
        except (ValueError, IndexError):
            print("Choix invalide")
            continue
        func()


if __name__ == "__main__":
    main()
