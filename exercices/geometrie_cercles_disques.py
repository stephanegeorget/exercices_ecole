"""Leçon et quiz sur les cercles et les disques."""

from __future__ import annotations

from .utils import show_lesson
from .logger import log_result

BOLD = "\033[1m"
CYAN = "\033[96m"
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

DISPLAY_NAME = "Géométrie : Cercles et disques"


def main() -> None:
    """Affiche la leçon sur les cercles et disques puis lance un quiz."""

    lesson = f"""
{CYAN}{BOLD}🟢  Cercles et disques  🟢{RESET}

{BOLD}Définition :{RESET} Un cercle de centre O est constitué de tous les points situés à la
même distance du point O. Cette distance est appelée le {BOLD}rayon{RESET} et se note
souvent r.

             M
        •           •
     ╱                   ╲
   ╱                       ╲
 A •           O             • B
   ╲                       ╱
     ╲                   ╱
        •           •
             N

Les segments [OA], [OB], [OM] sont des {BOLD}rayons{RESET}. Ils ont tous la même longueur r.

{BOLD}Diamètre :{RESET} un diamètre est un segment qui passe par le centre O et relie deux
points opposés du cercle. Sa longueur vaut {BOLD}2 × r{RESET}.

    •-----•-----•
    A     O     C

{BOLD}Disque :{RESET} le disque de centre O et de rayon r est l'ensemble des points dont la
distance à O est {BOLD}inférieure ou égale{RESET} à r. Il comprend donc le cercle et tout
l'intérieur.

{BOLD}Propriété 1 :{RESET} Tous les points d'un cercle de centre O sont à la même distance r
de O.
{BOLD}Propriété 2 :{RESET} Si deux points M et N sont à la même distance de O, alors ils
appartiennent au cercle de centre O et de rayon r.

{BOLD}Exemples :{RESET}
- Si le rayon vaut 4 cm, alors un diamètre mesure 8 cm.
- Si OM = 4 cm et ON = 3,5 cm, alors M appartient au cercle de rayon 4 cm tandis que N
  appartient seulement au disque (car sa distance est plus petite que 4 cm).
"""

    show_lesson(lesson)

    questions = [
        {
            "prompt": "Un cercle de centre O possède un rayon de 5 cm. Quelle est la longueur du diamètre ?",
            "choices": ["2,5 cm", "5 cm", "10 cm"],
            "answer": 2,
            "explanation": "Le diamètre vaut deux fois le rayon : 2 × 5 = 10 cm.",
        },
        {
            "prompt": "Si M est un point du cercle de centre O et de rayon 3 cm, combien mesure OM ?",
            "choices": ["3 cm", "6 cm", "On ne peut pas savoir"],
            "answer": 0,
            "explanation": "Tous les points du cercle sont à la distance r du centre, ici 3 cm.",
        },
        {
            "prompt": "Le point P vérifie OP = 2,8 cm alors que le cercle de centre O a un rayon de 3 cm. Où se situe P ?",
            "choices": ["Sur le cercle", "À l'intérieur du disque", "À l'extérieur du disque"],
            "answer": 1,
            "explanation": "Sa distance au centre est plus petite que le rayon, il appartient au disque mais pas au cercle.",
        },
        {
            "prompt": "Quel segment correspond toujours à un diamètre ?",
            "choices": ["Un segment reliant deux points quelconques du cercle", "Un segment qui passe par O et relie deux points du cercle", "Un segment partant de O et allant vers un point du cercle"],
            "answer": 1,
            "explanation": "Un diamètre doit passer par le centre et relier deux points opposés du cercle.",
        },
        {
            "prompt": "On sait que Q et R sont tous deux à 4 cm du point O. Que peut-on affirmer ?",
            "choices": ["Q et R appartiennent au cercle de centre O et de rayon 4 cm", "Q appartient au cercle mais R au disque", "Ils sont à l'extérieur du disque"],
            "answer": 0,
            "explanation": "Deux points à la même distance r de O appartiennent au cercle de centre O et de rayon r.",
        },
        {
            "prompt": "Lequel de ces énoncés est correct ?",
            "choices": [
                "Le disque contient le cercle et tous les points situés à une distance strictement inférieure au rayon.",
                "Le disque correspond uniquement à l'intérieur du cercle, sans sa frontière.",
                "Le disque regroupe tous les points situés exactement à la distance r du centre.",
            ],
            "answer": 0,
            "explanation": "Par définition, le disque contient le cercle (distance = r) et les points dont la distance est plus petite.",
        },
    ]

    print("Réponds aux questions en choisissant le numéro de la bonne réponse :")

    score = 0
    for index, question in enumerate(questions, start=1):
        print(f"\nQuestion {index} : {question['prompt']}")
        for choice_index, choice in enumerate(question["choices"], start=1):
            print(f"  {choice_index}. {choice}")
        try:
            user_answer = int(input("Ta réponse : ")) - 1
        except ValueError:
            user_answer = -1
        if user_answer == question["answer"]:
            print(f"{GREEN}Bravo ! ✅{RESET}")
            score += 1
        else:
            correct_choice = question["choices"][question["answer"]]
            print(
                f"{RED}Raté. La bonne réponse était : {question['answer'] + 1}. {correct_choice}. ❌{RESET}"
            )
            print(f"{CYAN}Rappel : {question['explanation']}{RESET}")

    total = len(questions)
    print(f"\n{BOLD}Score final : {score}/{total}{RESET}")
    log_result("geometrie_cercles_disques", score / total * 100)


if __name__ == "__main__":
    main()
