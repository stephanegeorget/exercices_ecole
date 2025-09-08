from __future__ import annotations

"""Tables de multiplication avec quiz interactif."""

import random

from .logger import get_scores, log_result
from .utils import show_lesson

LETTERS = ["a", "b", "c", "d", "e"]


def multiplication_tables() -> str:
    """Return the multiplication tables from 1 to 10."""

    lines = []
    for i in range(1, 11):
        lines.append(f"Table de {i}")
        for j in range(1, 11):
            lines.append(f"{i} × {j} = {i * j}")
        lines.append("")
    return "\n".join(lines)


def _generate_choices(n: int, m: int, hard_mode: bool) -> list[int]:
    """Create answer choices for ``n × m`` respecting difficulty."""

    correct = n * m
    wrong: set[int] = set()

    if hard_mode:
        variations = [(n - 1, m), (n + 1, m), (n, m - 1), (n, m + 1)]
        if random.random() < 0.5:
            idx = random.randrange(len(variations))
            variations[idx] = (n - 1, m + 1)
        for a, b in variations:
            product = a * b
            if product != correct:
                wrong.add(product)
        while len(wrong) < 4:
            candidate = correct + random.choice([-3, -2, -1, 1, 2, 3])
            if candidate != correct:
                wrong.add(candidate)
    else:
        while len(wrong) < 2:
            a = random.randint(1, 5)
            b = random.randint(1, 5)
            if a + b > 3:
                product = (n + a) * (m + b)
                if product != correct:
                    wrong.add(product)

    choices = list(wrong) + [correct]
    random.shuffle(choices)
    return choices


def _generate_question(hard_mode: bool) -> tuple[str, list[int], int]:
    """Return a question, choices and index of the correct answer."""

    if hard_mode:
        n = random.randint(2, 9)
        m = random.randint(2, 9)
    else:
        n = random.randint(1, 10)
        m = random.randint(1, 10)
    question = f"Combien font {n} × {m} ?"
    choices = _generate_choices(n, m, hard_mode)
    answer_index = choices.index(n * m)
    return question, choices, answer_index


def main() -> None:
    """Affiche les tables de multiplication puis un quiz."""

    show_lesson(multiplication_tables())

    previous = get_scores("math_tables_multiplication", limit=5)
    hard_mode = bool(previous) and sum(previous) / len(previous) > 75

    print("Quiz : réponds en tapant la lettre de la bonne réponse.")
    score = 0
    total = 20
    for i in range(1, total + 1):
        question, choices, answer = _generate_question(hard_mode)
        letters = LETTERS[: len(choices)]
        print(f"\nQuestion {i}: {question}")
        for letter, choice in zip(letters, choices):
            print(f"  {letter}. {choice}")
        student = input("Votre réponse : ").strip().lower()
        index = letters.index(student) if student in letters else -1
        correct_text = choices[answer]
        if index == answer:
            print("Exact ! ✅")
            score += 1
        else:
            print(f"Non, la bonne réponse était {letters[answer]}. {correct_text} ❌")

    print(f"\nScore final : {score}/{total}")
    log_result("math_tables_multiplication", score / total * 100)


if __name__ == "__main__":
    main()
