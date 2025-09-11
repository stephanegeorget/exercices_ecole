"""Leçon et quiz sur les jours de la semaine en anglais et leur origine."""

# Nom lisible de l'exercice pour le menu principal
DISPLAY_NAME = "Anglais : Jours de la semaine"

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
{CYAN}{BOLD}📚  Days of the Week Origins - Origines des jours  📚{RESET}

Chaque jour anglais vient d'un astre ou d'un dieu :
{BOLD}Monday{RESET} 🌙 → {BOLD}Moon day{RESET} (jour de la Lune)
{BOLD}Tuesday{RESET} ⚔️ → {BOLD}Tiw's day{RESET} (dieu germanique de la guerre)
{BOLD}Wednesday{RESET} 🧙 → {BOLD}Woden's day{RESET} (Odin, dieu de la sagesse)
{BOLD}Thursday{RESET} 🔨 → {BOLD}Thor's day{RESET} (dieu du tonnerre)
{BOLD}Friday{RESET} 💖 → {BOLD}Freya's day{RESET} (déesse de l'amour)
{BOLD}Saturday{RESET} 🪐 → {BOLD}Saturn day{RESET} (dieu romain)
{BOLD}Sunday{RESET} ☀️ → {BOLD}Sun day{RESET} (jour du Soleil)

✨ {BOLD}Astuce mémotechnique{RESET} :
Premières lettres → {BOLD}M T W T F S S{RESET}
"{BOLD}Ma Tête Veut Toujours Faire Simple Souvent{RESET}"
"""
    show_lesson(lesson)

    days = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]

    origins = {
        "Monday": ("Moon", "linked with the Moon"),
        "Tuesday": ("Tiw (Tyr)", "a Germanic god of war"),
        "Wednesday": ("Woden (Odin)", "the god of wisdom"),
        "Thursday": ("Thor", "the god of thunder"),
        "Friday": ("Frigg/Freya", "the goddess of love"),
        "Saturday": ("Saturn", "the Roman god"),
        "Sunday": ("Sun", "linked with the Sun"),
    }

    print(f"{CYAN}{BOLD}✏️  Worksheet : relie chaque jour à son origine !  ✏️{RESET}")
    print("Jours :")
    for i, day in enumerate(days, start=1):
        print(f"  {i}. {day}")

    root_options = list(origins.values())
    random.shuffle(root_options)
    letter_map: dict[str, str] = {}
    print("\nOrigines :")
    for idx, (root, meaning) in enumerate(root_options):
        letter = chr(ord("A") + idx)
        letter_map[root] = letter
        print(f"  {letter}. {root} - {meaning}")

    print("\nIndique la lettre correspondant à chaque jour :")
    score = 0
    answers: dict[str, str] = {}
    for day in days:
        reply = input(f"{day} -> ").strip().upper()
        answers[day] = reply
        correct_letter = letter_map[origins[day][0]]
        if reply == correct_letter:
            print(f"{GREEN}Bien vu ! ✅{RESET}")
            score += 1
        else:
            print(f"{RED}Oups ! ❌{RESET}")

    total = len(days)
    print(f"\n{BOLD}Corrections :{RESET}")
    for day in days:
        root, meaning = origins[day]
        print(f"{day} → {root} : {meaning}")

    print(f"\n{BOLD}Score final : {score}/{total}{RESET}")
    if score == total:
        print(f"{GREEN}Excellent ! Tu connais les origines par cœur ! 🥳{RESET}")
    elif score >= total / 2:
        print(f"{CYAN}Bravo ! Continue à pratiquer. 👍{RESET}")
    else:
        print(f"{RED}Relis la leçon et essaie encore ! 💪{RESET}")
    log_result("anglais_jours_semaine", score / total * 100)


if __name__ == "__main__":
    main()
