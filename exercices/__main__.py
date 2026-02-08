"""Point d'entrée pour le programme exercices."""

import os
import sys
import subprocess
from pathlib import Path

from . import (
    anglais_alphabet_couleurs,
    anglais_big_test_inside_out,
    anglais_hello_world,
    anglais_jours_semaine,
    anglais_pets_animals,
    anglais_spelling_bee_contest,
    francais_cloze_dictations,
    francais_grilles_mystere,
    francais_homophones_a_as_a_on_ont,
    francais_present_indicatif,
    francais_present_imperatif,
    francais_imparfait_indicatif,
    francais_imparfait_passe_simple,
    francais_passe_compose_terminaisons,
    francais_passe_simple_terminaisons,
    geometrie_appartenance,
    geometrie_cercles_disques,
    geometrie_notation,
    hist_test,
    histoire_prehistoire_neolithique,
    histoire_premiers_etats_premieres_ecritures,
    math_comparaison_encadrement_decimaux,
    math_nombres_entiers_et_decimaux,
    math_nombres_decimaux,
    math_tables_multiplication,
    musique_cest_quoi,
    musique_notes_portee,
    physique_changements_etats,
    physique_proprietes_eau_liquide,
    sciences_vivant_non_vivant,
    star_wars_quiz,
)

# Les modules d'exercices sont listés ici pour apparaître dans le menu.
# Chaque module définit sa propre chaîne ``DISPLAY_NAME`` utilisée pour
# afficher un intitulé lisible par un humain.
CATEGORIES = [
    (
        "Anglais",
        [
            anglais_hello_world,
            anglais_jours_semaine,
            anglais_alphabet_couleurs,
            anglais_spelling_bee_contest,
            anglais_pets_animals,
            anglais_big_test_inside_out,
        ],
    ),
    (
        "Français",
        [
            francais_cloze_dictations,
            francais_imparfait_indicatif,
            francais_imparfait_passe_simple,
            francais_present_indicatif,
            francais_present_imperatif,
            francais_passe_compose_terminaisons,
            francais_passe_simple_terminaisons,
            francais_grilles_mystere,
            francais_homophones_a_as_a_on_ont,
        ],
    ),
    (
        "Mathématiques",
        [
            math_tables_multiplication,
            math_nombres_decimaux,
            math_comparaison_encadrement_decimaux,
            math_nombres_entiers_et_decimaux,
            geometrie_appartenance,
            geometrie_cercles_disques,
            geometrie_notation,
        ],
    ),
    (
        "Sciences",
        [
            physique_changements_etats,
            physique_proprietes_eau_liquide,
            sciences_vivant_non_vivant,
        ],
    ),
    (
        "Musique",
        [
            musique_notes_portee,
            musique_cest_quoi,
        ],
    ),
    (
        "Histoire",
        [
            hist_test,
            histoire_prehistoire_neolithique,
            histoire_premiers_etats_premieres_ecritures,
        ],
    ),
    (
        "Autres",
        [
            star_wars_quiz,
        ],
    ),
]

def update_and_restart():
    """Met à jour le dépôt et ses dépendances, puis redémarre le programme."""
    repo_dir = Path(__file__).resolve().parent.parent
    subprocess.run(["git", "pull"], cwd=repo_dir, check=False)

    requirements_file = repo_dir / "requirements.txt"
    if requirements_file.exists():
        subprocess.run(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "--upgrade",
                "-r",
                str(requirements_file),
            ],
            check=False,
        )

    os.execv(sys.executable, [sys.executable] + sys.argv)


def _display_category_menu():
    """Affiche le menu des catégories et renvoie le choix de l'utilisateur."""

    print("Choisissez une catégorie :")
    for index, (category_name, _) in enumerate(CATEGORIES, start=1):
        print(f"{index}. {category_name}")

    update_index = len(CATEGORIES) + 1
    print(f"{update_index}. Mettre à jour le logiciel")
    print("0. Quitter")
    return input("Votre choix : ")


def _display_exercise_menu(category_name, modules):
    """Affiche un sous-menu pour la catégorie ``category_name``."""

    print(f"\n=== {category_name} ===")
    for index, module in enumerate(modules, start=1):
        print(f"{index}. {module.DISPLAY_NAME}")
    print("0. Retour")
    return input("Votre choix : ")


def main():
    """Affiche un menu à deux niveaux et lance l'exercice choisi."""

    while True:
        choice = _display_category_menu()
        if choice == "0":
            break

        update_index = len(CATEGORIES) + 1
        if choice == str(update_index):
            update_and_restart()
            return

        try:
            category_index = int(choice) - 1
            category_name, modules = CATEGORIES[category_index]
        except (ValueError, IndexError):
            print("Choix invalide\n")
            continue

        while True:
            sub_choice = _display_exercise_menu(category_name, modules)
            if sub_choice == "0":
                print()
                break

            try:
                module_index = int(sub_choice) - 1
                module = modules[module_index]
            except (ValueError, IndexError):
                print("Choix invalide\n")
                continue

            print()
            module.main()
            print()


if __name__ == "__main__":
    main()
