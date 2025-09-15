"""Leçon et quiz pour classer les éléments en vivant, naturel non vivant ou fabriqué."""

# Nom lisible de l'exercice pour le menu principal
DISPLAY_NAME = "Sciences : Vivant, naturel ou fabriqué"

import random

from .utils import show_lesson
from .logger import log_result

GREEN = "\033[92m"
RED = "\033[91m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"


def main() -> None:
    """Présente la leçon puis un quiz corrigé."""

    lesson = f"""
{CYAN}{BOLD}🔎 Observer et classer les objets de la cour 🔎{RESET}

Objectif :
- distinguer ce qui est {BOLD}vivant{RESET} ;
- ce qui est {BOLD}naturel mais non vivant{RESET} ;
- ce qui est {BOLD}fabriqué par l'humain{RESET}.

{BOLD}1. Ce qui est vivant{RESET}
Un être vivant naît, grandit, se nourrit, respire et se reproduit.
Exemples : arbres, oiseaux, chats, humains, champignons.

{BOLD}2. Ce qui est naturel non vivant{RESET}
Ces éléments viennent de la nature mais ne sont pas vivants.
Exemples : roches, eau, sable, branche morte.

{BOLD}3. Ce qui est fabriqué par l'humain{RESET}
Ce sont des objets créés par les humains.
Exemples : bancs, voitures, vélos, fontaines, bâtiments.

{BOLD}Activité :{RESET}
Observe la cour, fais une liste des éléments et classe-les dans la bonne catégorie.
"""
    show_lesson(lesson)

    items = [
        ("une fleur", "V"),
        ("une bouteille en plastique", "F"),
        ("le vent", "N"),
        ("un chien", "V"),
        ("un pont", "F"),
        ("un nuage", "N"),
        ("une lampe", "F"),
        ("une tomate", "V"),
        ("un jeu de balançoire", "F"),
        ("un champignon", "V"),
    ]

    categories = {
        "V": "vivant",
        "N": "naturel non vivant",
        "F": "fabriqué par l'humain",
    }

    quiz_items = items.copy()
    random.shuffle(quiz_items)

    print(f"{CYAN}{BOLD}✏️  Quiz : tape V, N ou F selon la catégorie !  ✏️{RESET}")
    score = 0
    answers: dict[str, str] = {}
    for element, expected in quiz_items:
        reply = input(f"{element} -> ").strip().upper()
        answers[element] = reply
        if reply == expected:
            print(f"{GREEN}Bien joué ! ✅{RESET}")
            score += 1
        else:
            print(f"{RED}Oups ! ❌{RESET}")

    total = len(items)
    print(f"\n{BOLD}Corrections :{RESET}")
    for element, expected in items:
        label = categories[expected]
        print(f"{element} → {label}")

    print(f"\n{BOLD}Score final : {score}/{total}{RESET}")
    if score == total:
        print(f"{GREEN}Excellent ! Tu es un as du classement ! 🥳{RESET}")
    elif score >= total / 2:
        print(f"{CYAN}Bravo ! Continue à observer autour de toi. 👍{RESET}")
    else:
        print(f"{RED}Relis la leçon et réessaie ! 💪{RESET}")
    log_result("sciences_vivant_non_vivant", score / total * 100)


if __name__ == "__main__":
    main()
