from __future__ import annotations

"""Exercices sur les homophones grammaticaux ai/es/est/et et son/sont."""

DISPLAY_NAME = "Français : ai/es/est/et et son/sont"

from .logger import log_result
from .utils import ask_choice_with_navigation, show_lesson

LESSON = """
📚 **Je veux écrire : ai / es / est / et**

Pose-toi les questions :

1. **Cela veut-il dire AVOIR ?**
   - Sujet **je / j'** → **ai**
2. **Cela veut-il dire ÊTRE ?**
   - Sujet **tu** → **es**
   - Sujet singulier (**il, elle, on**, ou un nom singulier) → **est**
3. **Cela veut-il dire ET PUIS ?**
   - ✅ Oui : c'est la conjonction de coordination **et**

---

📚 **Je veux écrire : son / sont**

Pose-toi les questions :

1. **Cela veut-il dire LE SIEN ?**
   - ✅ Oui : c'est le déterminant possessif **son**
2. **Cela veut-il dire ÊTRE ?**
   - Sujet pluriel (**ils, elles**, ou un nom pluriel) → **sont**

Astuce :
- On peut parfois remplacer **sont** par **étaient**.
- **son** peut aussi être un nom commun (le son de la cloche).
"""

EXERCISES = [
    {
        "title": "Exercice 1 — ai / es / est / et",
        "instruction": "Choisis la bonne écriture pour compléter chaque phrase.",
        "choices": ["ai", "es", "est", "et"],
        "questions": [
            {
                "prompt": "1. J'__ perdu ma gomme.",
                "answer": 0,
                "explanation": "Avec le sujet 'je' et le verbe avoir, on écrit 'ai'.",
            },
            {
                "prompt": "2. Tu __ en avance ce matin.",
                "answer": 1,
                "explanation": "Avec le sujet 'tu' et le verbe être, on écrit 'es'.",
            },
            {
                "prompt": "3. Le cartable __ sous la table.",
                "answer": 2,
                "explanation": "Sujet singulier + verbe être : on écrit 'est'.",
            },
            {
                "prompt": "4. Nina prend son cahier __ son livre.",
                "answer": 3,
                "explanation": "Ici, on relie deux groupes : on écrit la conjonction 'et'.",
            },
            {
                "prompt": "5. Tu __ mon meilleur ami.",
                "answer": 1,
                "explanation": "Sujet 'tu' + verbe être : 'es'.",
            },
            {
                "prompt": "6. J'__ très faim après le sport.",
                "answer": 0,
                "explanation": "Sujet 'j'' + verbe avoir : 'ai'.",
            },
            {
                "prompt": "7. Mon frère __ dans la cour.",
                "answer": 2,
                "explanation": "Sujet singulier (mon frère) + être : 'est'.",
            },
            {
                "prompt": "8. Lila __ Tom jouent aux billes.",
                "answer": 3,
                "explanation": "On coordonne deux noms : il faut 'et'.",
            },
            {
                "prompt": "9. J'__ un nouveau stylo bleu.",
                "answer": 0,
                "explanation": "Le verbe avoir au présent avec 'je' s'écrit 'ai'.",
            },
            {
                "prompt": "10. Tu __ prêt pour la dictée ?",
                "answer": 1,
                "explanation": "Avec 'tu', le verbe être s'écrit 'es'.",
            },
            {
                "prompt": "11. La classe __ silencieuse.",
                "answer": 2,
                "explanation": "Sujet singulier (la classe) + être : 'est'.",
            },
            {
                "prompt": "12. J'écris __ je relis ma phrase.",
                "answer": 3,
                "explanation": "On peut comprendre 'et puis' : il faut écrire 'et'.",
            },
            {
                "prompt": "13. J'__ oublié mon écharpe.",
                "answer": 0,
                "explanation": "Avec le sujet 'j'', le verbe avoir donne 'ai'.",
            },
            {
                "prompt": "14. Tu __ content de ta note.",
                "answer": 1,
                "explanation": "Sujet 'tu' + verbe être : 'es'.",
            },
            {
                "prompt": "15. Le chat saute __ attrape la balle.",
                "answer": 3,
                "explanation": "On relie deux actions : c'est la conjonction 'et'.",
            },
        ],
    },
    {
        "title": "Exercice 2 — son / sont",
        "instruction": "Choisis entre 'son' et 'sont' dans chaque phrase.",
        "choices": ["son", "sont"],
        "questions": [
            {
                "prompt": "1. Léo range __ cahier dans son cartable.",
                "answer": 0,
                "explanation": "'Le sien' : c'est le déterminant possessif 'son'.",
            },
            {
                "prompt": "2. Les enfants __ dans la cour.",
                "answer": 1,
                "explanation": "Sujet pluriel + verbe être : on écrit 'sont'.",
            },
            {
                "prompt": "3. Mila a perdu __ bonnet rouge.",
                "answer": 0,
                "explanation": "On parle du bonnet qui est le sien : 'son'.",
            },
            {
                "prompt": "4. Ils __ arrivés tôt à l'école.",
                "answer": 1,
                "explanation": "Sujet pluriel 'ils' + être : 'sont'.",
            },
            {
                "prompt": "5. Papa cherche __ téléphone.",
                "answer": 0,
                "explanation": "C'est le téléphone qui lui appartient : 'son'.",
            },
            {
                "prompt": "6. Les pommes __ dans le panier.",
                "answer": 1,
                "explanation": "Sujet pluriel (les pommes) + être : 'sont'.",
            },
            {
                "prompt": "7. Zoé prête __ livre à Emma.",
                "answer": 0,
                "explanation": "'Le sien' : on écrit 'son'.",
            },
            {
                "prompt": "8. Elles __ prêtes pour le spectacle.",
                "answer": 1,
                "explanation": "Sujet pluriel 'elles' + être : 'sont'.",
            },
            {
                "prompt": "9. Hugo ferme __ manteau.",
                "answer": 0,
                "explanation": "Manteau appartenant à Hugo : 'son'.",
            },
            {
                "prompt": "10. Les cahiers __ bien alignés.",
                "answer": 1,
                "explanation": "On peut remplacer par 'étaient' : on écrit 'sont'.",
            },
            {
                "prompt": "11. Ma sœur nourrit __ lapin.",
                "answer": 0,
                "explanation": "Il s'agit de son lapin : déterminant possessif 'son'.",
            },
            {
                "prompt": "12. Les élèves __ calmes en classe.",
                "answer": 1,
                "explanation": "Sujet pluriel + verbe être : 'sont'.",
            },
            {
                "prompt": "13. Karim a oublié __ ardoise.",
                "answer": 0,
                "explanation": "Ardoise qui lui appartient : 'son'.",
            },
            {
                "prompt": "14. Mes cousins __ en vacances.",
                "answer": 1,
                "explanation": "Sujet pluriel 'mes cousins' + être : 'sont'.",
            },
            {
                "prompt": "15. Lina montre __ dessin à la maîtresse.",
                "answer": 0,
                "explanation": "C'est le dessin qui est le sien : 'son'.",
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
    """Affiche la leçon puis lance les exercices d'homophones."""

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
        log_result("francais_homophones_ai_es_est_et_son_sont", percentage)


if __name__ == "__main__":
    main()
