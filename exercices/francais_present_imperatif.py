from __future__ import annotations

"""Leçon et quiz sur le présent de l'impératif."""

DISPLAY_NAME = "Français : Présent de l'impératif"

from .logger import log_result
from .utils import show_lesson

LESSON = """
📚 **Le présent de l'impératif : donner un ordre, un conseil ou une consigne**

Le **présent de l'impératif** sert à **donner une instruction**, **un conseil**,
**un encouragement** ou **une interdiction**. Il se conjugue **sans sujet** et
seulement à **trois personnes** :

- **tu** (2ᵉ personne du singulier)
- **nous** (1ʳᵉ personne du pluriel)
- **vous** (2ᵉ personne du pluriel)

🧠 **Règles importantes**

- Les verbes du 1er groupe en **-er** perdent le **-s** à "tu" :
  > Regarde !, Marche !
- Mais on garde le **-s** devant **y** ou **en** :
  > Vas-y !, Manges-en !
- À la forme négative : **ne ... pas** encadre le verbe.
  > Ne crie pas !, Ne vous levez pas !

🎯 **Valeurs fréquentes de l'impératif**

- **Ordre** : Éteins la lumière !
- **Conseil** : Sois prudent.
- **Encouragement** : Allons, continue !
- **Interdiction** : Ne traverse pas la rue.

Prêt·e ? Réponds aux questions en t'inspirant des exemples.
"""

QUESTIONS = [
    {
        "prompt": "1. Indique la personne : \"Fais attention en classe.\" (tu/nous/vous)",
        "answers": ["tu"],
        "explanation": "Fais correspond à la 2ᵉ personne du singulier.",
    },
    {
        "prompt": "2. Indique la personne : \"Dites-moi la vérité.\" (tu/nous/vous)",
        "answers": ["vous"],
        "explanation": "Dites est la forme de politesse/pluriel : vous.",
    },
    {
        "prompt": "3. Indique la personne : \"Ne laissons pas tomber.\" (tu/nous/vous)",
        "answers": ["nous"],
        "explanation": "Laissons est l'impératif à la 1ʳᵉ personne du pluriel.",
    },
    {
        "prompt": "4. Conjugue (venir) à l'impératif, tu : ___ !",
        "answers": ["viens"],
        "explanation": "Venir → viens à l'impératif, 2ᵉ pers. du singulier.",
    },
    {
        "prompt": "5. Complète avec (aller) + y : ___-y ! (tu)",
        "answers": ["vas"],
        "explanation": "Avec y, on garde le -s : vas-y !",
    },
    {
        "prompt": "6. Conjugue (prendre) à l'impératif, nous : ___ la route.",
        "answers": ["prenons"],
        "explanation": "Prendre → prenons à la 1ʳᵉ personne du pluriel.",
    },
    {
        "prompt": "7. Conjugue (être) à l'impératif, vous : ___ patients.",
        "answers": ["soyez"],
        "explanation": "Être est irrégulier : soyez (vous).",
    },
    {
        "prompt": "8. Valeur de l'impératif : \"Éteins la lumière !\"",
        "answers": ["ordre"],
        "explanation": "On donne un ordre clair.",
    },
    {
        "prompt": "9. Valeur de l'impératif : \"Ne traverse pas la rue.\"",
        "answers": ["interdiction", "defense", "défense"],
        "explanation": "La forme négative exprime une interdiction.",
    },
    {
        "prompt": "10. Valeur de l'impératif : \"Soyons prudents.\"",
        "answers": ["conseil"],
        "explanation": "On propose un conseil collectif.",
    },
    {
        "prompt": "11. Valeur de l'impératif : \"Allons, fais un effort.\"",
        "answers": ["encouragement", "conseil"],
        "explanation": "L'impératif sert ici à encourager.",
    },
    {
        "prompt": "12. Conjugue (se lever) à l'impératif, tu : ___ !",
        "answers": ["leve-toi", "lève-toi", "leve toi", "lève toi"],
        "explanation": "À l'impératif, le pronom est après le verbe : lève-toi !",
    },
    {
        "prompt": "13. Conjugue (ne pas se lever) à l'impératif, vous : ___ !",
        "answers": [
            "ne vous levez pas",
            "ne vous levez pas!",
            "ne vous levez pas.",
            "ne vous levez-pas",
        ],
        "explanation": "À la forme négative : Ne vous levez pas !",
    },
]


def _normalise_answer(answer: str) -> str:
    return answer.strip().lower().replace("’", "'")


def main() -> None:
    """Affiche la leçon puis lance le quiz sur l'impératif."""

    show_lesson(LESSON)
    print("Réponds en toutes lettres (ex. tu, nous, vous, ordre, conseil...).")

    score = 0
    total = len(QUESTIONS)
    for index, question in enumerate(QUESTIONS, start=1):
        print(f"\nQuestion {index}")
        print(question["prompt"])
        answer = _normalise_answer(input("Ta réponse : "))
        valid = {_normalise_answer(item) for item in question["answers"]}
        if answer in valid:
            print("✅ Bravo !")
            score += 1
        else:
            print("❌ Pas tout à fait.")
            print(f"✅ Réponse attendue : {question['answers'][0]}")
            print(f"ℹ️ {question['explanation']}")

    print(f"\nScore final : {score}/{total}")
    percentage = score / total * 100 if total else 0.0
    log_result("francais_present_imperatif", percentage)


if __name__ == "__main__":
    main()
