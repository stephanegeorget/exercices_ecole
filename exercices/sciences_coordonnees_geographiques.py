"""Leçon et quiz sur les coordonnées géographiques : latitude, longitude, méridiens et parallèles."""

# Nom lisible de l'exercice pour le menu principal
DISPLAY_NAME = "Sciences : Coordonnées géographiques (latitude et longitude)"

from .utils import ask_choice_with_navigation, show_lesson
from .logger import log_result


GREEN = "\033[92m"
RED = "\033[91m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"


def main() -> None:
    """Présente la leçon puis un quiz corrigé."""

    lesson = f"""
{CYAN}{BOLD}🌍 Se repérer sur la Terre avec des coordonnées 🌍{RESET}

Pour trouver un lieu sur la Terre, on utilise deux nombres : la {BOLD}latitude{RESET}
et la {BOLD}longitude{RESET}. On les écrit en degrés (°).

{BOLD}1. L'équateur et les parallèles{RESET}
- L'équateur est la ligne imaginaire qui fait le tour de la Terre au milieu,
  entre le pôle Nord et le pôle Sud.
- Les {BOLD}parallèles{RESET} sont des cercles imaginaires parallèles à l'équateur.
- La {BOLD}latitude{RESET} mesure la distance angulaire à l'équateur :
  elle va de 0° (équateur) à 90° Nord (pôle Nord) ou 90° Sud (pôle Sud).

{BOLD}2. Les méridiens{RESET}
- Les {BOLD}méridiens{RESET} sont des demi-cercles qui relient le pôle Nord au pôle Sud.
- Le méridien de référence, ou méridien 0°, passe par {BOLD}Greenwich{RESET}, près de Londres.
- La {BOLD}longitude{RESET} mesure la distance angulaire à ce méridien :
  elle va de 0° à 180° Est ou à 180° Ouest.

{BOLD}3. Les points cardinaux{RESET}
- Nord : vers le pôle Nord ; Sud : vers le pôle Sud.
- Est : à droite de Greenwich quand on regarde vers le Nord ; Ouest : à gauche.

{BOLD}4. À quoi ressemble une coordonnée ?{RESET}
Exemple pour Paris, environ {BOLD}48° N ; 2° E{RESET} :
- {BOLD}48° N{RESET} : la latitude, 48° au Nord de l'équateur ;
- {BOLD}2° E{RESET} : la longitude, 2° à l'Est de Greenwich.

{BOLD}Activité :{RESET}
Cherche sur une carte la latitude et la longitude de ta ville ou de ton école.
"""
    show_lesson(lesson)

    questions = [
        {
            "question": "Quel est le méridien de référence, celui qui vaut 0° de longitude ?",
            "choices": ["Greenwich", "l'équateur", "le pôle Nord"],
            "answer": 0,
            "explanation": "Le méridien de référence passe par Greenwich, près de Londres.",
        },
        {
            "question": "Quelle est la latitude de l'équateur ?",
            "choices": ["90°", "0°", "180°"],
            "answer": 1,
            "explanation": "L'équateur est à 0° de latitude.",
        },
        {
            "question": "Quelle est la latitude du pôle Nord ?",
            "choices": ["0°", "90° N", "180° E"],
            "answer": 1,
            "explanation": "Le pôle Nord est à 90° de latitude Nord.",
        },
        {
            "question": "Quelle direction relie le pôle Nord au pôle Sud ?",
            "choices": ["les parallèles", "les méridiens", "l'équateur"],
            "answer": 1,
            "explanation": "Les méridiens relient le pôle Nord au pôle Sud ; les parallèles sont parallèles à l'équateur.",
        },
        {
            "question": "Dans la coordonnée 48° N ; 2° E, quel nombre donne la latitude ?",
            "choices": ["2", "48", "90"],
            "answer": 1,
            "explanation": "La latitude vient en premier : 48° N.",
        },
        {
            "question": "Paris est-il à l'est ou à l'ouest de Greenwich ?",
            "choices": ["à l'ouest", "à l'est"],
            "answer": 1,
            "explanation": "Paris est à environ 2° à l'Est de Greenwich.",
        },
        {
            "question": "Comment appelle-t-on les lignes imaginaires parallèles à l'équateur ?",
            "choices": ["les méridiens", "les parallèles", "les pôles"],
            "answer": 1,
            "explanation": "Ce sont les parallèles.",
        },
    ]

    print("Quiz : choisis la bonne réponse avec les flèches, ou tape la lettre puis Entrée.")
    score = 0
    total = len(questions)
    for index, question in enumerate(questions, start=1):
        print(f"\nQuestion {index}")
        print(question["question"])
        choices = question["choices"]
        student, option_letters, quit_requested = ask_choice_with_navigation(choices)
        if quit_requested:
            print("\nRetour au menu demandé. Fin de l'exercice.\n")
            return
        correct_index = question["answer"]
        correct_letter = option_letters[correct_index]
        correct_text = choices[correct_index]
        if student == correct_index:
            print(f"{GREEN}Bien joué ! ✅{RESET}")
            score += 1
        else:
            print(f"{RED}Pas tout à fait. ❌ Réponse attendue : {correct_letter}) {correct_text}{RESET}")
            print(f"ℹ️ {question['explanation']}")

    print(f"\n{BOLD}Score final : {score}/{total}{RESET}")
    if score == total:
        print(f"{GREEN}Excellent ! Tu sais te repérer sur la Terre ! 🥳{RESET}")
    elif score >= total / 2:
        print(f"{CYAN}Bravo ! Relis les méridiens et les parallèles. 👍{RESET}")
    else:
        print(f"{RED}Relis la leçon et réessaie ! 💪{RESET}")
    percentage = score / total * 100 if total else 0.0
    log_result("sciences_coordonnees_geographiques", percentage)


if __name__ == "__main__":
    main()
