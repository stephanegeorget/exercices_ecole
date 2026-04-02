from __future__ import annotations

"""Leçon et quiz QCM sur le plus-que-parfait."""

DISPLAY_NAME = "Français : Plus-que-parfait (quiz)"

from .logger import log_result
from .utils import show_lesson

LESSON = """
📚 **Le plus-que-parfait**

Le plus-que-parfait sert à parler d'une action **déjà terminée dans le passé**,
avant une autre action passée.

✅ Formation :
- auxiliaire **être** ou **avoir** à l'imparfait
- + participe passé

Exemples :
- *J'avais fini mes devoirs quand tu es arrivé.*
- *Elles étaient parties avant la pluie.*

Dans ce quiz, choisis la bonne forme parmi **3 réponses**.
"""

QUESTIONS = [
    {
        "prompt": "Quand je suis entré, il ____ déjà son repas.",
        "choices": ["a terminé", "avait terminé", "terminait"],
        "answer": 2,
        "explanation": "Plus-que-parfait = imparfait de avoir + participe passé : avait terminé.",
    },
    {
        "prompt": "Nous ____ nos chaussures avant de sortir sous la pluie.",
        "choices": ["avions mis", "mettons", "avons mis"],
        "answer": 1,
        "explanation": "L'action est antérieure à une autre action passée : avions mis.",
    },
    {
        "prompt": "Elles ____ très tôt, donc la maison était vide.",
        "choices": ["étaient parties", "sont parties", "partaient"],
        "answer": 1,
        "explanation": "Avec partir, on utilise être : elles étaient parties.",
    },
    {
        "prompt": "Tu m'as rendu le livre que tu ____ à la bibliothèque.",
        "choices": ["empruntais", "avais emprunté", "as emprunté"],
        "answer": 2,
        "explanation": "Action plus ancienne dans le passé : avais emprunté.",
    },
    {
        "prompt": "Avant ce voyage, je n'____ jamais l'avion.",
        "choices": ["avais pris", "ai pris", "prenais"],
        "answer": 1,
        "explanation": "Négation au plus-que-parfait : n'avais jamais pris.",
    },
    {
        "prompt": "Vous ____ la porte avant que le vent ne souffle fort.",
        "choices": ["aviez fermé", "fermez", "avez fermé"],
        "answer": 1,
        "explanation": "Plus-que-parfait de fermer : aviez fermé.",
    },
    {
        "prompt": "Ils étaient contents parce qu'ils ____ leur match.",
        "choices": ["avaient gagné", "gagnaient", "ont gagné"],
        "answer": 1,
        "explanation": "Cause antérieure dans le passé : avaient gagné.",
    },
    {
        "prompt": "On a retrouvé le chat qui ____ par la fenêtre.",
        "choices": ["s'échappait", "s'est échappé", "s'était échappé"],
        "answer": 3,
        "explanation": "Verbe pronominal au plus-que-parfait : s'était échappé.",
    },
    {
        "prompt": "Après qu'elle ____ ses affaires, elle est partie.",
        "choices": ["rangeait", "avait rangé", "a rangé"],
        "answer": 2,
        "explanation": "Action accomplie avant le départ : avait rangé.",
    },
    {
        "prompt": "Nous avons vu le film que vous nous ____ hier.",
        "choices": ["aviez conseillé", "conseillez", "avez conseillé"],
        "answer": 1,
        "explanation": "Conseil donné avant le moment raconté : aviez conseillé.",
    },
]


def _ask_choice() -> int | None:
    raw = input("Ton choix (1, 2 ou 3) : ").strip()
    if raw not in {"1", "2", "3"}:
        return None
    return int(raw)


def main() -> None:
    show_lesson(LESSON)
    score = 0
    total = len(QUESTIONS)

    for index, question in enumerate(QUESTIONS, start=1):
        print(f"\nQuestion {index}/{total}")
        print(question["prompt"])
        for choice_index, choice in enumerate(question["choices"], start=1):
            print(f"  {choice_index}. {choice}")

        answer = _ask_choice()
        if answer is None:
            print("❌ Réponse invalide. Il faut taper 1, 2 ou 3.")
            print(
                f"ℹ️ Bonne réponse : {question['answer']}. {question['choices'][question['answer'] - 1]}"
            )
            print(f"ℹ️ {question['explanation']}")
            continue

        if answer == question["answer"]:
            print("✅ Bravo !")
            score += 1
        else:
            print("❌ Ce n'est pas la bonne réponse.")
            print(
                f"ℹ️ Bonne réponse : {question['answer']}. {question['choices'][question['answer'] - 1]}"
            )
            print(f"ℹ️ {question['explanation']}")

    percentage = score / total * 100 if total else 0.0
    print(f"\nScore final : {score}/{total} ({percentage:.1f} %)")
    log_result("francais_plus_que_parfait_quizz", percentage)


if __name__ == "__main__":
    main()
