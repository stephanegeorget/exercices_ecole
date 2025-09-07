"""Leçon et quiz sur les changements d'état de la matière."""

from pydoc import pager


def main():
    """Présente la leçon puis un quiz corrigé."""
    # Leçon introductive affichée via un pager.
    lesson = (
        "Changements d'état de la matière\n"
        "(Tape 'q' pour passer au quiz)\n\n"
        "1. Fusion : passage de l'état solide à l'état liquide. \n"
        "   Exemple : la glace qui devient de l'eau.\n"
        "2. Solidification : passage du liquide au solide. \n"
        "   Exemple : l'eau qui gèle dans le congélateur.\n"
        "3. Vaporisation : passage du liquide au gaz. \n"
        "   Exemple : l'eau qui bout devient de la vapeur.\n"
        "4. Condensation : passage du gaz au liquide. \n"
        "   Exemple : la vapeur d'eau qui forme des gouttes sur une vitre froide.\n"
        "5. Sublimation : passage direct du solide au gaz sans devenir liquide. \n"
        "   Exemple : la glace sèche qui disparaît en fumée.\n"
        "6. Condensation solide : passage direct du gaz au solide. \n"
        "   Exemple : le givre qui se forme sur une fenêtre en hiver.\n\n"
        "(Tape 'q' pour passer au quiz)"
    )
    print("La leçon va s'afficher. Tape 'q' pour passer au quiz.")
    pager(lesson)

    # Définition des questions du quiz
    questions = [
        {
            "question": "Le passage de l'état solide à l'état liquide s'appelle...",
            "choices": ["la fusion", "la solidification", "la vaporisation"],
            "answer": 0,
        },
        {
            "question": "Le passage de l'état liquide à l'état solide s'appelle...",
            "choices": ["la fusion", "la condensation", "la solidification"],
            "answer": 2,
        },
        {
            "question": "Le passage de l'état liquide à l'état gazeux s'appelle...",
            "choices": ["la sublimation", "la vaporisation", "la condensation"],
            "answer": 1,
        },
        {
            "question": "Le passage de l'état gazeux à l'état liquide s'appelle...",
            "choices": ["la condensation", "la solidification", "la fusion"],
            "answer": 0,
        },
        {
            "question": "Le passage direct du solide au gaz s'appelle...",
            "choices": ["la condensation", "la vaporisation", "la sublimation"],
            "answer": 2,
        },
        {
            "question": "Le passage direct du gaz au solide s'appelle...",
            "choices": ["la fusion", "la condensation solide", "la sublimation"],
            "answer": 1,
        },
        {
            "question": "La glace qui fond dans un verre d'eau est un exemple de...",
            "choices": ["fusion", "condensation solide", "vaporisation"],
            "answer": 0,
        },
        {
            "question": "La buée qui se forme sur un miroir après une douche est due à...",
            "choices": ["la condensation", "la sublimation", "la fusion"],
            "answer": 0,
        },
        {
            "question": "Quand on met de l'eau au congélateur, l'eau subit...",
            "choices": ["la vaporisation", "la solidification", "la sublimation"],
            "answer": 1,
        },
        {
            "question": "La formation de givre sur un pare-brise par temps froid est un exemple de...",
            "choices": ["condensation solide", "vaporisation", "fusion", "condensation"],
            "answer": 0,
        },
    ]

    # Réponses de l'élève pour l'exemple (0 -> premier choix, 1 -> deuxième, ...)
    student_answers = [0, 2, 1, 2, 2, 1, 0, 0, 0, 0]

    print("Quiz : réponds mentalement à chaque question.")
    for i, q in enumerate(questions, start=1):
        print(f"\nQuestion {i}: {q['question']}")
        for j, choice in enumerate(q["choices"], start=1):
            print(f"  {j}. {choice}")

    print("\nCorrection :")
    score = 0
    for i, q in enumerate(questions, start=1):
        student = student_answers[i - 1]
        correct = q["answer"]
        student_text = q["choices"][student]
        correct_text = q["choices"][correct]
        if student == correct:
            print(f"Question {i}: {student + 1}. {student_text} ✔️")
            score += 1
        else:
            print(
                f"Question {i}: {student + 1}. {student_text} ❌ (bonne réponse : {correct + 1}. {correct_text})"
            )

    total = len(questions)
    print(f"\nScore final : {score}/{total}")
    if score == total:
        print("Excellent travail ! Tu maîtrises parfaitement les changements d'état.")
    elif score >= total / 2:
        print("Bravo ! Continue à réviser pour progresser encore.")
    else:
        print("Courage, relis la leçon et essaie à nouveau !")


if __name__ == "__main__":
    main()
