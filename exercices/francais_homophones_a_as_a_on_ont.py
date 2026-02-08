from __future__ import annotations

"""Exercices sur les homophones grammaticaux a/as/à et on/ont."""

DISPLAY_NAME = "Français : a/as/à et on/ont"

from .logger import log_result
from .utils import ask_choice_with_navigation, show_lesson

LESSON = """
📚 **Je veux écrire : a / as / à**

Pose-toi la question : **"Est-ce que cela veut dire AVOIR ?"**

- ✅ **Oui** : c'est le verbe **avoir**.
  - Sujet singulier (**il, elle, on**, ou un nom singulier) → **a**
  - Sujet **tu** → **as**
- ❌ **Non** : c'est la préposition → **à**

Astuce : on peut souvent essayer de remplacer par **avait**.
Si ça marche, on est bien sur le verbe **avoir**.

---

📚 **Je veux écrire : on / ont**

Pose-toi les questions :

1. Peut-on remplacer par **il / elle / quelqu'un** ?
   - ✅ Oui → c'est le pronom sujet **on**.
2. Cela veut-il dire **avoir** ?
   - ✅ Oui, avec un sujet pluriel (**ils, elles**, nom pluriel) → **ont**.

Astuce : si on peut remplacer par **avaient**, on écrit souvent **ont**.
"""

EXERCISES = [
    {
        "title": "Exercice 1 — a / as / à",
        "instruction": "Choisis la bonne écriture dans chaque phrase.",
        "choices": ["a", "as", "à"],
        "questions": [
            {
                "prompt": "1. Tu __ une nouvelle trousse.",
                "answer": 1,
                "explanation": "Avec le sujet 'tu' et le verbe avoir, on écrit 'as'.",
            },
            {
                "prompt": "2. Léa __ un chat noir.",
                "answer": 0,
                "explanation": "Sujet singulier (Léa) + verbe avoir : on écrit 'a'.",
            },
            {
                "prompt": "3. Demain, nous irons __ la piscine.",
                "answer": 2,
                "explanation": "Ici, ce n'est pas le verbe avoir : c'est la préposition 'à'.",
            },
            {
                "prompt": "4. On __ bien travaillé aujourd'hui.",
                "answer": 0,
                "explanation": "Sujet 'on' + verbe avoir : on écrit 'a'.",
            },
            {
                "prompt": "5. Tu penses __ ton exposé ?",
                "answer": 2,
                "explanation": "On ne peut pas remplacer par 'avait' : il faut la préposition 'à'.",
            },
            {
                "prompt": "6. Tu __ fini tes devoirs ?",
                "answer": 1,
                "explanation": "Sujet 'tu' + verbe avoir : on écrit 'as'.",
            },
        ],
    },
    {
        "title": "Exercice 2 — on / ont",
        "instruction": "Choisis entre 'on' et 'ont'.",
        "choices": ["on", "ont"],
        "questions": [
            {
                "prompt": "1. Ce matin, __ est partis tôt.",
                "answer": 0,
                "explanation": "On peut remplacer par 'il' : c'est le pronom sujet 'on'.",
            },
            {
                "prompt": "2. Les élèves __ rangé leurs cahiers.",
                "answer": 1,
                "explanation": "Cela exprime 'avoir' avec un sujet pluriel : on écrit 'ont'.",
            },
            {
                "prompt": "3. __ frappe à la porte.",
                "answer": 0,
                "explanation": "On peut dire 'il frappe à la porte' : on écrit 'on'.",
            },
            {
                "prompt": "4. Elles __ appris leur poésie.",
                "answer": 1,
                "explanation": "Sujet pluriel + verbe avoir : on écrit 'ont'.",
            },
            {
                "prompt": "5. À midi, __ mange à la cantine.",
                "answer": 0,
                "explanation": "Ici c'est le pronom sujet indéfini 'on'.",
            },
            {
                "prompt": "6. Mes cousins __ pris le train.",
                "answer": 1,
                "explanation": "Sujet pluriel + verbe avoir au présent : 'ont'.",
            },
        ],
    },
]


def _run_exercise(exercise: dict[str, object]) -> tuple[int, int]:
    score = 0
    questions = exercise["questions"]
    choices = exercise["choices"]

    for index, question in enumerate(questions, start=1):
        print(f"\nQuestion {index}")
        print(question["prompt"])
        student, option_letters, quit_requested = ask_choice_with_navigation(choices)

        if quit_requested:
            print("\nRetour au menu demandé. Fin de l'exercice.\n")
            return score, index - 1

        correct_index = question["answer"]
        correct_letter = option_letters[correct_index]
        correct_text = choices[correct_index]

        if student == correct_index:
            print("✅ Bravo !")
            score += 1
        else:
            print(
                "❌ Pas tout à fait. "
                f"Réponse attendue : {correct_letter}) {correct_text}"
            )
            print(f"ℹ️ {question['explanation']}")

    return score, len(questions)


def _display_exercise_menu() -> str:
    print("\nChoisis un exercice :")
    for index, exercise in enumerate(EXERCISES, start=1):
        print(f"{index}. {exercise['title']}")
    print("0. Retour")
    return input("Ton choix : ")


def main() -> None:
    """Affiche la leçon puis lance les deux exercices sur les homophones."""

    show_lesson(LESSON)
    print("\nAstuce : utilise les flèches du clavier, puis Entrée, pour choisir.")

    total_score = 0
    total_questions = 0

    while True:
        choice = _display_exercise_menu()
        if choice == "0":
            break

        try:
            exercise_index = int(choice) - 1
            exercise = EXERCISES[exercise_index]
        except (ValueError, IndexError):
            print("Choix invalide.")
            continue

        print(f"\n=== {exercise['title']} ===")
        print(exercise["instruction"])
        score, asked = _run_exercise(exercise)
        total_score += score
        total_questions += asked
        print(f"\nScore de l'exercice : {score}/{asked}")

    if total_questions:
        percentage = total_score / total_questions * 100
        log_result("francais_homophones_a_as_a_on_ont", percentage)


if __name__ == "__main__":
    main()
