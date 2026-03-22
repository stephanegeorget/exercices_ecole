"""Chapitre 6 : calcul réfléchi et priorités de calcul (quiz très guidés)."""

from __future__ import annotations

from .logger import log_result
from .utils import ask_choice_with_navigation, show_lesson

DISPLAY_NAME = "Maths : Chapitre 6 — calcul réfléchi (menu par exercice)"

GREEN = "\033[92m"
RED = "\033[91m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"


def _ask_question(question: dict[str, object]) -> bool:
    print(f"\n{BOLD}{question['question']}{RESET}")
    choices = list(question["choices"])
    selected, _, wants_exit = ask_choice_with_navigation(choices)
    if wants_exit:
        raise KeyboardInterrupt
    if selected is None or selected < 0:
        print(f"{RED}Réponse invalide.{RESET}")
        return False

    ok = selected == question["answer"]
    if ok:
        print(f"{GREEN}Oui, c'est ça.{RESET}")
    else:
        print(f"{RED}Pas encore. On corrige ensemble.{RESET}")
    print(f"{CYAN}Indice / explication : {question['explain']}{RESET}")
    return ok


def _run_guided_quiz(exercise_key: str, title: str, intro: str, questions: list[dict[str, object]]) -> None:
    show_lesson(
        f"""
{CYAN}{BOLD}Chapitre 6 — {title}{RESET}

{intro}

Objectif : avancer {BOLD}très lentement{RESET}, une mini-idée à la fois.
Tape 'q' à tout moment pour revenir au menu du chapitre.
"""
    )

    score = 0
    total = len(questions)
    try:
        for index, question in enumerate(questions, start=1):
            print(f"\n{CYAN}Étape {index}/{total}{RESET}")
            if _ask_question(question):
                score += 1
    except KeyboardInterrupt:
        print("\nRetour au menu du chapitre demandé.")

    percentage = (score / total) * 100 if total else 0
    print(f"\n{BOLD}Résultat :{RESET} {score}/{total} ({percentage:.1f}%).")
    log_result(f"math_chapitre_6_{exercise_key}", percentage)


def _exercise_1() -> None:
    questions = [
        {
            "question": "[Exercice 1a] Dans 0,1 × 25 × 10 × 4, quelle paire est la plus astucieuse à regrouper d'abord ?",
            "choices": ["25 et 4", "0,1 et 10", "25 et 10"],
            "answer": 1,
            "explain": "0,1 × 10 = 1 : ça simplifie immédiatement l'expression.",
        },
        {
            "question": "Après ce regroupement, l'expression devient...",
            "choices": ["1 × 25 × 4", "0,1 × 25 × 40", "10 × 25 × 4"],
            "answer": 0,
            "explain": "On remplace seulement 0,1 × 10 par 1.",
        },
        {
            "question": "Que vaut ensuite 25 × 4 ?",
            "choices": ["10", "100", "1 000"],
            "answer": 1,
            "explain": "25 × 4 = 100, un produit remarquable à connaître.",
        },
        {
            "question": "Donc 0,1 × 25 × 10 × 4 = ...",
            "choices": ["100", "10", "1"],
            "answer": 0,
            "explain": "0,1 × 10 = 1, puis 1 × 25 × 4 = 100.",
        },
        {
            "question": "[Exercice 1b] 0,01 × 45,67 × 10 revient à multiplier 45,67 par...",
            "choices": ["0,1", "1", "10"],
            "answer": 0,
            "explain": "0,01 × 10 = 0,1.",
        },
        {
            "question": "45,67 × 0,1 =",
            "choices": ["4,567", "45,67", "456,7"],
            "answer": 0,
            "explain": "Multiplier par 0,1 décale la virgule d'un rang vers la gauche.",
        },
        {
            "question": "[Exercice 1c] 328,9 × 100 × 0,1 équivaut à 328,9 × ...",
            "choices": ["1", "10", "100"],
            "answer": 1,
            "explain": "100 × 0,1 = 10.",
        },
        {
            "question": "Donc 328,9 × 10 =",
            "choices": ["32,89", "328,9", "3 289"],
            "answer": 2,
            "explain": "Multiplier par 10 décale la virgule d'un rang vers la droite.",
        },
    ]
    _run_guided_quiz(
        "ex1",
        "Exercice 1 : calculer astucieusement",
        "On apprend à regrouper les facteurs qui donnent 1, 10, 100...",
        questions,
    )


def _exercise_2() -> None:
    questions = [
        {
            "question": "[Exercice 2a] (67 + 4) × 5 : que calcule-t-on en premier ?",
            "choices": ["67 + 4", "× 5", "les deux en même temps"],
            "answer": 0,
            "explain": "Les parenthèses sont prioritaires.",
        },
        {
            "question": "67 + 4 =",
            "choices": ["61", "71", "72"],
            "answer": 1,
            "explain": "Addition simple avant la multiplication.",
        },
        {
            "question": "(67 + 4) × 5 = 71 × 5 =",
            "choices": ["305", "355", "405"],
            "answer": 1,
            "explain": "71 × 5 = (70 × 5) + (1 × 5) = 350 + 5.",
        },
        {
            "question": "[Exercice 2b] 78 × (57 − 6) : l'opération prioritaire est...",
            "choices": ["57 − 6", "78 × 57", "78 × 6"],
            "answer": 0,
            "explain": "Encore une fois : d'abord les parenthèses.",
        },
        {
            "question": "57 − 6 =",
            "choices": ["51", "61", "63"],
            "answer": 0,
            "explain": "Soustraction directe.",
        },
        {
            "question": "78 × 51 =",
            "choices": ["3 978", "3 588", "4 078"],
            "answer": 0,
            "explain": "78 × (50 + 1) = 3 900 + 78.",
        },
    ]
    _run_guided_quiz(
        "ex2",
        "Exercice 2 : priorités de calcul",
        "On souligne mentalement l'opération à faire en premier.",
        questions,
    )


def _exercise_2_bis() -> None:
    questions = [
        {
            "question": "[Exercice 2 bis] (13 − 3) × 29 : première étape ?",
            "choices": ["13 − 3", "10 × 29 directement", "29 − 3"],
            "answer": 0,
            "explain": "On calcule la parenthèse avant tout.",
        },
        {
            "question": "(13 − 3) × 29 =",
            "choices": ["290", "260", "319"],
            "answer": 0,
            "explain": "13 − 3 = 10 puis 10 × 29 = 290.",
        },
        {
            "question": "[Exercice 2 bis] 35 − (7 + 4 × 5) : dans la parenthèse, d'abord...",
            "choices": ["7 + 4", "4 × 5", "35 − 7"],
            "answer": 1,
            "explain": "Dans une parenthèse aussi, × est prioritaire sur +.",
        },
        {
            "question": "4 × 5 =",
            "choices": ["9", "20", "45"],
            "answer": 1,
            "explain": "On remplace ensuite la parenthèse par 7 + 20.",
        },
        {
            "question": "7 + 20 =",
            "choices": ["27", "13", "70"],
            "answer": 0,
            "explain": "La parenthèse vaut 27.",
        },
        {
            "question": "35 − 27 =",
            "choices": ["8", "18", "62"],
            "answer": 0,
            "explain": "Dernière étape : soustraction finale.",
        },
    ]
    _run_guided_quiz(
        "ex2_bis",
        "Exercice 2 bis : priorités avec parenthèses imbriquées",
        "On avance micro-étape par micro-étape pour éviter les erreurs de priorité.",
        questions,
    )


def _exercise_3() -> None:
    questions = [
        {
            "question": "[Exercice 3] Léo achète 3 croissants à 1,25 €. L'expression correcte est...",
            "choices": ["3 × 1,25", "3 + 1,25", "1,25 ÷ 3"],
            "answer": 0,
            "explain": "Prix répété 3 fois = multiplication.",
        },
        {
            "question": "Pour 1 baguette à 0,85 €, on ajoute...",
            "choices": ["0,85", "1 × 0,85 × 3", "0,85 ÷ 1"],
            "answer": 0,
            "explain": "Un seul objet : on ajoute juste son prix.",
        },
        {
            "question": "Pour 2 pains à 2,75 €, l'expression est...",
            "choices": ["2 × 2,75", "2 + 2,75", "2,75 − 2"],
            "answer": 0,
            "explain": "Deux fois le même prix => produit.",
        },
        {
            "question": "Parmi les réponses proposées sur la fiche, qui a la bonne structure ?",
            "choices": ["Imane", "Enzo", "Karim"],
            "answer": 2,
            "explain": "(3 × 1,25) + 0,85 + (2 × 2,75) traduit exactement l'énoncé.",
        },
        {
            "question": "3 × 1,25 =",
            "choices": ["3,25", "3,75", "4,25"],
            "answer": 1,
            "explain": "1,25 + 1,25 + 1,25 = 3,75.",
        },
        {
            "question": "2 × 2,75 =",
            "choices": ["4,50", "5,50", "6,25"],
            "answer": 1,
            "explain": "Double de 2,75.",
        },
        {
            "question": "Total à payer = 3,75 + 0,85 + 5,50 =",
            "choices": ["10,10 €", "9,10 €", "11,10 €"],
            "answer": 0,
            "explain": "3,75 + 0,85 = 4,60 puis + 5,50 = 10,10 €.",
        },
    ]
    _run_guided_quiz(
        "ex3",
        "Exercice 3 : problème de courses",
        "On traduit l'énoncé en expression correcte, puis on calcule proprement.",
        questions,
    )


def _exercise_4() -> None:
    questions = [
        {
            "question": "[Exercice 4] Le parterre compte...",
            "choices": ["27 rangées de 56 sièges", "56 rangées de 27 sièges", "27 sièges en tout"],
            "answer": 0,
            "explain": "C'est la donnée du texte.",
        },
        {
            "question": "Le balcon compte...",
            "choices": ["13 rangées de 56 sièges", "56 rangées de 13 sièges", "13 sièges en tout"],
            "answer": 0,
            "explain": "Même logique que le parterre.",
        },
        {
            "question": "Une première expression correcte du total est...",
            "choices": ["(27 × 56) + (13 × 56)", "27 × (56 + 13)", "56 + 27 + 13"],
            "answer": 0,
            "explain": "On additionne les deux blocs de sièges.",
        },
        {
            "question": "Une deuxième expression équivalente est...",
            "choices": ["(27 + 13) × 56", "27 + 13 × 56", "27 × 13 × 56"],
            "answer": 0,
            "explain": "On factorise par 56.",
        },
        {
            "question": "27 + 13 =",
            "choices": ["30", "40", "50"],
            "answer": 1,
            "explain": "Total des rangées.",
        },
        {
            "question": "40 × 56 =",
            "choices": ["2 040", "2 240", "2 340"],
            "answer": 1,
            "explain": "4 × 56 = 224 puis ×10 => 2 240.",
        },
    ]
    _run_guided_quiz(
        "ex4",
        "Exercice 4 : nombre total de sièges",
        "On écrit deux expressions différentes et on conclut.",
        questions,
    )


def _exercise_4_bis() -> None:
    questions = [
        {
            "question": "[Exercice 4 bis] Coût d'un élève =",
            "choices": ["7,20 + 2,80", "7,20 × 2,80", "7,20 − 2,80"],
            "answer": 0,
            "explain": "Prix place + transport.",
        },
        {
            "question": "7,20 + 2,80 =",
            "choices": ["9,00", "10,00", "10,20"],
            "answer": 1,
            "explain": "Somme des deux coûts unitaires.",
        },
        {
            "question": "Pour 57 élèves, expression compacte :",
            "choices": ["57 × (7,20 + 2,80)", "57 + 7,20 + 2,80", "(57 × 7,20) + 2,80"],
            "answer": 0,
            "explain": "Même coût unitaire répété 57 fois.",
        },
        {
            "question": "57 × 10 =",
            "choices": ["570", "57", "5 700"],
            "answer": 0,
            "explain": "Multiplication par 10.",
        },
        {
            "question": "Le coût total de la sortie est donc...",
            "choices": ["57 €", "570 €", "5 700 €"],
            "answer": 1,
            "explain": "Chaque élève coûte 10 €, pour 57 élèves.",
        },
    ]
    _run_guided_quiz(
        "ex4_bis",
        "Exercice 4 bis : sortie au cinéma",
        "On combine coût unitaire puis coût total de groupe.",
        questions,
    )


def _exercise_5() -> None:
    questions = [
        {
            "question": "[Exercice 5a] « La somme de 0,7 et du produit de 0,3 par 0,6 » s'écrit...",
            "choices": ["0,7 + (0,3 × 0,6)", "(0,7 + 0,3) × 0,6", "0,7 × 0,3 × 0,6"],
            "answer": 0,
            "explain": "Mot-clé : somme de ... et du produit ...",
        },
        {
            "question": "0,3 × 0,6 =",
            "choices": ["0,18", "0,9", "1,8"],
            "answer": 0,
            "explain": "3 × 6 = 18 et deux décimales au total.",
        },
        {
            "question": "0,7 + 0,18 =",
            "choices": ["0,88", "0,78", "0,98"],
            "answer": 0,
            "explain": "Aligner les virgules : 0,70 + 0,18.",
        },
        {
            "question": "[Exercice 5b] « Le produit de 0,5 par la différence de 4,8 et de 2,8 » s'écrit...",
            "choices": ["0,5 × (4,8 − 2,8)", "(0,5 × 4,8) − 2,8", "0,5 + (4,8 − 2,8)"],
            "answer": 0,
            "explain": "Produit de 0,5 par [quelque chose] => 0,5 × (...)",
        },
        {
            "question": "4,8 − 2,8 =",
            "choices": ["1", "2", "2,2"],
            "answer": 1,
            "explain": "Différence entre 4,8 et 2,8.",
        },
        {
            "question": "0,5 × 2 =",
            "choices": ["1", "2", "0,5"],
            "answer": 0,
            "explain": "Prendre la moitié de 2 donne 1.",
        },
    ]
    _run_guided_quiz(
        "ex5",
        "Exercice 5 : traduire des phrases en expressions",
        "On repère les mots-clés : somme, produit, différence.",
        questions,
    )


def _exercise_5_bis() -> None:
    questions = [
        {
            "question": "[Exercice 5 bis a] « La différence de 10,5 et du produit de 2,5 par 4 » s'écrit...",
            "choices": ["10,5 − (2,5 × 4)", "(10,5 − 2,5) × 4", "10,5 + (2,5 × 4)"],
            "answer": 0,
            "explain": "Différence de A et de B => A − B.",
        },
        {
            "question": "2,5 × 4 =",
            "choices": ["10", "6,5", "1"],
            "answer": 0,
            "explain": "2,5 multiplié par 4 vaut 10.",
        },
        {
            "question": "10,5 − 10 =",
            "choices": ["0,5", "1,5", "10,5"],
            "answer": 0,
            "explain": "Soustraction finale.",
        },
        {
            "question": "[Exercice 5 bis b] « Le produit de 0,01 par la somme de 12,3 et 56,6 » s'écrit...",
            "choices": ["0,01 × (12,3 + 56,6)", "(0,01 × 12,3) + 56,6", "0,01 + 12,3 + 56,6"],
            "answer": 0,
            "explain": "Produit par la somme => 0,01 × (...)",
        },
        {
            "question": "12,3 + 56,6 =",
            "choices": ["68,9", "69,9", "67,9"],
            "answer": 0,
            "explain": "Addition de décimaux.",
        },
        {
            "question": "0,01 × 68,9 =",
            "choices": ["6,89", "0,689", "0,0689"],
            "answer": 1,
            "explain": "Multiplier par 0,01 revient à diviser par 100.",
        },
    ]
    _run_guided_quiz(
        "ex5_bis",
        "Exercice 5 bis : traduire puis calculer",
        "On continue l'entraînement sur le vocabulaire mathématique.",
        questions,
    )


def main() -> None:
    show_lesson(
        f"""
{CYAN}{BOLD}Chapitre 6 — Calcul réfléchi (inspiré de la fiche en photo){RESET}

Dans ce chapitre, tu choisis un exercice précis puis tu suis un quiz guidé.
Chaque quiz est découpé en mini-étapes pour ralentir le raisonnement :
- repérer l'opération prioritaire ;
- écrire la bonne expression ;
- calculer sans sauter d'étape ;
- vérifier le résultat.
"""
    )

    menu = [
        ("Exercice 1 — Calculer astucieusement", _exercise_1),
        ("Exercice 2 — Priorités de calcul", _exercise_2),
        ("Exercice 2 bis — Priorités et parenthèses", _exercise_2_bis),
        ("Exercice 3 — Problème de courses", _exercise_3),
        ("Exercice 4 — Salle de théâtre", _exercise_4),
        ("Exercice 4 bis — Sortie au cinéma", _exercise_4_bis),
        ("Exercice 5 — Expressions et phrases", _exercise_5),
        ("Exercice 5 bis — Expressions et phrases", _exercise_5_bis),
    ]

    while True:
        print(f"\n{BOLD}Menu du chapitre 6{RESET}")
        for index, (label, _) in enumerate(menu, start=1):
            print(f"{index}. {label}")
        print("0. Retour")
        choice = input("Votre choix : ").strip()

        if choice == "0":
            break

        try:
            selected = int(choice) - 1
            _, action = menu[selected]
        except (ValueError, IndexError):
            print(f"{RED}Choix invalide.{RESET}")
            continue

        action()


if __name__ == "__main__":
    main()
