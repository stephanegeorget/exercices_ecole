"""Leçon et quiz sur les tables de multiplication de 1 à 9."""


def main():
    """Présente les tables de multiplication puis un quiz corrigé."""
    print("Tables de multiplication de 1 à 9\n")
    for i in range(1, 10):
        print(f"Table de {i} :")
        for j in range(1, 10):
            print(f"  {i} x {j} = {i * j}")
        print()

    questions = [
        {
            "question": "Combien font 3 x 4 ?",
            "choices": ["7", "12", "14"],
            "answer": 1,
        },
        {
            "question": "Combien font 7 x 8 ?",
            "choices": ["54", "56", "64"],
            "answer": 1,
        },
        {
            "question": "Combien font 9 x 9 ?",
            "choices": ["81", "72", "99"],
            "answer": 0,
        },
        {
            "question": "Combien font 6 x 7 ?",
            "choices": ["42", "36", "48"],
            "answer": 0,
        },
        {
            "question": "Combien font 5 x 6 ?",
            "choices": ["30", "28", "32"],
            "answer": 0,
        },
        {
            "question": "Combien font 4 x 8 ?",
            "choices": ["32", "36", "30"],
            "answer": 0,
        },
        {
            "question": "Combien font 2 x 9 ?",
            "choices": ["18", "16", "20"],
            "answer": 0,
        },
        {
            "question": "Combien font 3 x 7 ?",
            "choices": ["20", "21", "24"],
            "answer": 1,
        },
        {
            "question": "Combien font 8 x 8 ?",
            "choices": ["64", "72", "62"],
            "answer": 0,
        },
        {
            "question": "Combien font 9 x 5 ?",
            "choices": ["40", "45", "50"],
            "answer": 1,
        },
    ]

    student_answers = [1, 0, 0, 0, 0, 0, 1, 1, 0, 1]

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
        print("Excellent travail ! Tu maîtrises parfaitement les tables de multiplication.")
    elif score >= total / 2:
        print("Bravo ! Continue à t'entraîner pour progresser encore.")
    else:
        print("Courage, révise les tables et essaie à nouveau !")


if __name__ == "__main__":
    main()
