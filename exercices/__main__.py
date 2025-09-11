"""Point d'entrée pour le programme exercices."""

import os
import sys
import subprocess
from pathlib import Path

from . import (
    anglais_hello_world,
    hist_test,
    physique_changements_etats,
    physique_proprietes_eau_liquide,
    math_tables_multiplication,
    geometrie_notation,
)

# Les modules d'exercices sont listés ici pour apparaître dans le menu.
# Chaque module définit sa propre chaîne ``DISPLAY_NAME`` utilisée pour
# afficher un intitulé lisible par un humain.
EXERCICES = [
    anglais_hello_world,
    hist_test,
    physique_changements_etats,
    physique_proprietes_eau_liquide,
    math_tables_multiplication,
    geometrie_notation,
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
        for index, module in enumerate(EXERCICES, start=1):
            print(f"{index}. {module.DISPLAY_NAME}")
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
            module = EXERCICES[index]
        except (ValueError, IndexError):
            print("Choix invalide")
            continue
        module.main()


if __name__ == "__main__":
    main()
