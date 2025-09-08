"""Tables de multiplication avec quiz interactif."""

from .utils import show_lesson


LETTERS = ["a", "b", "c"]


def multiplication_tables() -> str:
    """Return the multiplication tables from 1 to 10."""

    lines = []
    for i in range(1, 11):
        lines.append(f"Table de {i}")
        for j in range(1, 11):
            lines.append(f"{i} × {j} = {i * j}")
        lines.append("")
    return "\n".join(lines)


def main() -> None:
    """Affiche les tables de multiplication puis un quiz."""

    show_lesson(multiplication_tables())

    questions = [
        {
            "question": "Combien font 3 × 4 ?",
            "choices": ["7", "12", "9"],
            "answer": 1,
        },
        {
            "question": "Combien font 5 × 6 ?",
            "choices": ["11", "30", "28"],
            "answer": 1,
        },
        {
            "question": "Combien font 9 × 8 ?",
            "choices": ["72", "81", "64"],
            "answer": 0,
        },
    ]

    print("Quiz : réponds en tapant la lettre de la bonne réponse.")
    score = 0
    for i, q in enumerate(questions, start=1):
        print(f"\nQuestion {i}: {q['question']}")
        for letter, choice in zip(LETTERS, q["choices"]):
            print(f"  {letter}. {choice}")
        student = input("Votre réponse : ").strip().lower()
        index = LETTERS.index(student) if student in LETTERS else -1
        correct = q["answer"]
        correct_text = q["choices"][correct]
        if index == correct:
            print("Exact ! ✅")
            score += 1
        else:
            print(f"Non, la bonne réponse était {LETTERS[correct]}. {correct_text} ❌")

    total = len(questions)
    print(f"\nScore final : {score}/{total}")


if __name__ == "__main__":
    main()

