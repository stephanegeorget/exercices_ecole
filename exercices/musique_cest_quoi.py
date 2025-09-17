"""Leçon et quiz colorés pour découvrir les bases de la musique."""

# Nom lisible de l'exercice pour le menu principal
DISPLAY_NAME = "Musique : C'est quoi la musique ?"

from .utils import show_lesson
from .logger import log_result

MAGENTA = "\033[95m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
GREEN = "\033[92m"
RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"


def main() -> None:
    """Présente la leçon puis lance un quiz inspiré du support papier."""

    lesson = rf"""
{BOLD}{MAGENTA}🎵 C'EST QUOI LA MUSIQUE ?{RESET}

{BOLD}{CYAN}La portée 🎼{RESET}
Une portée est un ensemble de {BOLD}5 lignes{RESET} et de {BOLD}4 interlignes{RESET}.
Les notes se placent {BOLD}sur{RESET} les lignes et {BOLD}entre{RESET} les lignes.
{YELLOW}
        ┌──────────────────────────────┐
        │ 5 ────────────────────────── │ ← ligne 5
        │ 4 ────────────────────────── │
        │ 3 ────────────────────────── │
        │ 2 ────────────────────────── │ ← ligne 2
        │ 1 ────────────────────────── │
        │    ≈≈≈≈  Interlignes  ≈≈≈≈   │
        └──────────────────────────────┘
{RESET}

{BOLD}{BLUE}La clé de sol 🎯{RESET}
Pour lire les notes, on place une {BOLD}clé de sol{RESET} au début de la portée.
Elle s'enroule autour de la {BOLD}2ᵉ ligne{RESET}, celle qui porte la note {BOLD}sol{RESET}.
{GREEN}
           ___
          |   \
          |    )
          |   /
          \  /
           |/
           /
          /|
         / ___  
        / (|  \
       (  \🎯 | 
        \._|._/
           |        
           |
        .  |
         \/
{RESET}

{BOLD}{YELLOW}Les notes 🎶{RESET}
Dans l'ordre montant, on rencontre :
{BOLD}DO, RÉ, MI, FA, SOL, LA, SI{RESET}.
Chaque ligne ou espace correspond à l'une de ces notes.
{YELLOW}
        SI ────────●──────────────
        LA ───────●───────────────
        SOL ─────●───────────────
        FA ────●───────────────
        MI ──●───────────────
        RÉ ─●───────────────
        DO ●───────────────
{RESET}

{BOLD}{MAGENTA}Les rythmes et les silences 🥁🤫{RESET}
Nous connaissons 4 rythmes. Chaque rythme a son silence jumeau.
{CYAN}+--------------------+----------------------------+{RESET}
{CYAN}| {BOLD}Rythme{RESET}{CYAN}               | {BOLD}Durée & Silence{RESET}{CYAN}           |{RESET}
{CYAN}+--------------------+----------------------------+{RESET}
{CYAN}|  ( )  {BOLD}Ronde{RESET}      | 4 temps → 😴 {BOLD}Pause{RESET}              |{RESET}
{CYAN}| (  )  {BOLD}Blanche{RESET}    | 2 temps → 😌 {BOLD}Demi-pause{RESET}         |{RESET}
{CYAN}| ♪    {BOLD}Noire{RESET}       | 1 temps → 🙂 {BOLD}Soupir{RESET}             |{RESET}
{CYAN}| ♫    {BOLD}Croche{RESET}      | 1/2 temps → 🤫 {BOLD}Demi-soupir{RESET}     |{RESET}
{CYAN}+--------------------+----------------------------+{RESET}

👉 Souviens-toi : la musique combine {BOLD}hauteurs{RESET} (les notes) et {BOLD}rythmes{RESET}.
"""

    show_lesson(lesson)

    questions = [
        {
            "question": "Combien de lignes a une portée ?",
            "choices": ["5 lignes", "4 lignes", "6 lignes"],
            "answer": 0,
        },
        {
            "question": "Combien d'interlignes comporte une portée ?",
            "choices": ["3 interlignes", "4 interlignes", "5 interlignes"],
            "answer": 1,
        },
        {
            "question": "Sur quelle ligne s'enroule la clé de sol ?",
            "choices": ["Sur la 1re ligne", "Sur la 2e ligne", "Sur la 5e ligne"],
            "answer": 1,
        },
        {
            "question": "Quelle série représente l'ordre des notes du grave vers l'aigu ?",
            "choices": [
                "Do Ré Mi Fa Sol La Si",
                "Do Mi Sol Si Ré Fa La",
                "Si La Sol Fa Mi Ré Do",
            ],
            "answer": 0,
        },
        {
            "question": "Quel rythme vaut 4 temps ?",
            "choices": ["La ronde", "La noire", "La croche"],
            "answer": 0,
        },
        {
            "question": "Quel silence dure le même temps qu'une noire ?",
            "choices": ["La pause", "La demi-pause", "Le soupir"],
            "answer": 2,
        },
        {
            "question": "Combien de temps dure une croche ?",
            "choices": ["1 temps", "1/2 temps", "2 temps"],
            "answer": 1,
        },
    ]

    print("Quiz : réponds à chaque question en choisissant le numéro de la bonne réponse.")
    score = 0
    for i, q in enumerate(questions, start=1):
        print(f"\nQuestion {i} : {q['question']}")
        for j, choice in enumerate(q["choices"], start=1):
            print(f"  {j}. {choice}")
        try:
            student = int(input("Votre réponse : ")) - 1
        except ValueError:
            student = -1
        correct = q["answer"]
        correct_text = q["choices"][correct]
        if student == correct:
            print(f"{GREEN}Exact 🎉 !{RESET}")
            score += 1
        else:
            print(f"{RED}Oups… la bonne réponse était {correct + 1}. {correct_text}. 🎯{RESET}")

    total = len(questions)
    print(f"\n{BOLD}Score final : {score}/{total}{RESET}")
    if score == total:
        print(f"{GREEN}Bravo maestro, tu maîtrises la leçon ! 🎼🌟{RESET}")
    elif score >= total / 2:
        print(f"{CYAN}Beau travail, continue à t'entraîner. 🎶👍{RESET}")
    else:
        print(f"{RED}Pas de panique, relis la leçon et réessaie. 💪{RESET}")

    log_result("musique_cest_quoi", score / total * 100)


if __name__ == "__main__":
    main()
