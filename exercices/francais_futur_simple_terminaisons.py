from __future__ import annotations

"""Leçon et quiz sur les terminaisons du futur simple."""

DISPLAY_NAME = "Français : Futur simple (terminaisons)"

from .logger import log_result
from .utils import show_lesson

LESSON = """
📘 **Le futur simple : les terminaisons à connaître**

Au futur simple, les terminaisons sont les mêmes pour tous les groupes :
- je **-ai**
- tu **-as**
- il/elle/on **-a**
- nous **-ons**
- vous **-ez**
- ils/elles **-ont**

✅ **1er groupe (-er)** : on garde l'infinitif + terminaison.
> parler → je parlerai

✅ **2ᵉ groupe (-ir)** : on garde l'infinitif + terminaison.
> finir → nous finirons

✅ **3ᵉ groupe** : même terminaisons, mais parfois un radical irrégulier.
> venir → je viendrai, pouvoir → ils pourront

🎯 Dans ce quiz, tu dois écrire **uniquement la terminaison** qui manque.
Exemple : "je parler___" → réponse : **ai**
"""

QUESTIONS = [
    {
        "prompt": "1. 1er groupe (chanter) — Je chanter___ ce soir.",
        "answers": ["ai"],
        "verb": "chanter",
        "group": "1er groupe",
        "explanation": "Avec je au futur simple, la terminaison est -ai.",
    },
    {
        "prompt": "2. 1er groupe (jouer) — Tu jouer___ avec nous.",
        "answers": ["as"],
        "verb": "jouer",
        "group": "1er groupe",
        "explanation": "Avec tu, on utilise la terminaison -as.",
    },
    {
        "prompt": "3. 1er groupe (regarder) — Elle regarder___ la carte.",
        "answers": ["a"],
        "verb": "regarder",
        "group": "1er groupe",
        "explanation": "Avec elle, la terminaison du futur est -a.",
    },
    {
        "prompt": "4. 1er groupe (aimer) — Nous aimer___ ce film.",
        "answers": ["ons"],
        "verb": "aimer",
        "group": "1er groupe",
        "explanation": "Avec nous, la terminaison du futur simple est -ons.",
    },
    {
        "prompt": "5. 1er groupe (danser) — Vous danser___ demain.",
        "answers": ["ez"],
        "verb": "danser",
        "group": "1er groupe",
        "explanation": "Avec vous, on met -ez au futur simple.",
    },
    {
        "prompt": "6. 1er groupe (parler) — Ils parler___ plus tard.",
        "answers": ["ont"],
        "verb": "parler",
        "group": "1er groupe",
        "explanation": "Avec ils, la terminaison est -ont.",
    },
    {
        "prompt": "7. 1er groupe (travailler) — Je travailler___ ici l'an prochain.",
        "answers": ["ai"],
        "verb": "travailler",
        "group": "1er groupe",
        "explanation": "Je + futur simple prend -ai.",
    },
    {
        "prompt": "8. 1er groupe (marcher) — Tu marcher___ jusqu'à l'école.",
        "answers": ["as"],
        "verb": "marcher",
        "group": "1er groupe",
        "explanation": "Tu + futur simple prend -as.",
    },
    {
        "prompt": "9. 1er groupe (arriver) — On arriver___ avant midi.",
        "answers": ["a"],
        "verb": "arriver",
        "group": "1er groupe",
        "explanation": "On se conjugue comme il/elle : terminaison -a.",
    },
    {
        "prompt": "10. 1er groupe (visiter) — Elles visiter___ le musée.",
        "answers": ["ont"],
        "verb": "visiter",
        "group": "1er groupe",
        "explanation": "Elles au futur simple prennent la terminaison -ont.",
    },
    {
        "prompt": "11. 2ᵉ groupe (finir) — Je finir___ mes devoirs.",
        "answers": ["ai"],
        "verb": "finir",
        "group": "2ᵉ groupe",
        "explanation": "Les verbes du 2ᵉ groupe gardent aussi les terminaisons du futur : -ai avec je.",
    },
    {
        "prompt": "12. 2ᵉ groupe (choisir) — Tu choisir___ un livre.",
        "answers": ["as"],
        "verb": "choisir",
        "group": "2ᵉ groupe",
        "explanation": "Avec tu, la terminaison est -as.",
    },
    {
        "prompt": "13. 2ᵉ groupe (grandir) — Il grandir___ vite.",
        "answers": ["a"],
        "verb": "grandir",
        "group": "2ᵉ groupe",
        "explanation": "Avec il, on met la terminaison -a.",
    },
    {
        "prompt": "14. 2ᵉ groupe (réussir) — Nous réussir___ ensemble.",
        "answers": ["ons"],
        "verb": "réussir",
        "group": "2ᵉ groupe",
        "explanation": "Avec nous, la terminaison est -ons.",
    },
    {
        "prompt": "15. 2ᵉ groupe (rougir) — Vous rougir___ facilement.",
        "answers": ["ez"],
        "verb": "rougir",
        "group": "2ᵉ groupe",
        "explanation": "Avec vous, la terminaison est -ez.",
    },
    {
        "prompt": "16. 2ᵉ groupe (obéir) — Ils obéir___ aux règles.",
        "answers": ["ont"],
        "verb": "obéir",
        "group": "2ᵉ groupe",
        "explanation": "Ils + futur simple = terminaison -ont.",
    },
    {
        "prompt": "17. 2ᵉ groupe (applaudir) — J'applaudir___ la troupe.",
        "answers": ["ai"],
        "verb": "applaudir",
        "group": "2ᵉ groupe",
        "explanation": "Je (j') prend la terminaison -ai.",
    },
    {
        "prompt": "18. 2ᵉ groupe (maigrir) — Tu maigrir___ pendant l'été.",
        "answers": ["as"],
        "verb": "maigrir",
        "group": "2ᵉ groupe",
        "explanation": "Tu au futur simple prend -as.",
    },
    {
        "prompt": "19. 2ᵉ groupe (remplir) — Elle remplir___ la bouteille.",
        "answers": ["a"],
        "verb": "remplir",
        "group": "2ᵉ groupe",
        "explanation": "Elle + futur simple = terminaison -a.",
    },
    {
        "prompt": "20. 2ᵉ groupe (punir) — Elles punir___ les tricheurs.",
        "answers": ["ont"],
        "verb": "punir",
        "group": "2ᵉ groupe",
        "explanation": "Avec elles, la terminaison est -ont.",
    },
    {
        "prompt": "21. 3ᵉ groupe (venir) — Je viendr___ tôt.",
        "answers": ["ai"],
        "verb": "venir",
        "group": "3ᵉ groupe",
        "explanation": "Même avec un radical irrégulier (viendr-), je garde la terminaison -ai.",
    },
    {
        "prompt": "22. 3ᵉ groupe (pouvoir) — Tu pourr___ nous aider.",
        "answers": ["as"],
        "verb": "pouvoir",
        "group": "3ᵉ groupe",
        "explanation": "Tu + radical pourr- + terminaison -as.",
    },
    {
        "prompt": "23. 3ᵉ groupe (être) — Il ser___ prêt.",
        "answers": ["a"],
        "verb": "être",
        "group": "3ᵉ groupe",
        "explanation": "Le verbe être a le radical ser-, puis la terminaison -a.",
    },
    {
        "prompt": "24. 3ᵉ groupe (avoir) — Nous aur___ de la chance.",
        "answers": ["ons"],
        "verb": "avoir",
        "group": "3ᵉ groupe",
        "explanation": "Avoir au futur : aur- + -ons avec nous.",
    },
    {
        "prompt": "25. 3ᵉ groupe (faire) — Vous fer___ un dessin.",
        "answers": ["ez"],
        "verb": "faire",
        "group": "3ᵉ groupe",
        "explanation": "Faire au futur : fer- + terminaison -ez.",
    },
    {
        "prompt": "26. 3ᵉ groupe (voir) — Ils verr___ la mer.",
        "answers": ["ont"],
        "verb": "voir",
        "group": "3ᵉ groupe",
        "explanation": "Avec ils, la terminaison est -ont même si le radical est verr-.",
    },
    {
        "prompt": "27. 3ᵉ groupe (devoir) — Je devr___ partir tôt.",
        "answers": ["ai"],
        "verb": "devoir",
        "group": "3ᵉ groupe",
        "explanation": "Je + futur simple = terminaison -ai (devrai).",
    },
    {
        "prompt": "28. 3ᵉ groupe (vouloir) — Tu voudr___ un chocolat.",
        "answers": ["as"],
        "verb": "vouloir",
        "group": "3ᵉ groupe",
        "explanation": "Tu + voudr- + -as.",
    },
    {
        "prompt": "29. 3ᵉ groupe (aller) — Elle ir___ à Paris.",
        "answers": ["a"],
        "verb": "aller",
        "group": "3ᵉ groupe",
        "explanation": "Aller au futur : ir- + terminaison -a.",
    },
    {
        "prompt": "30. 3ᵉ groupe (savoir) — Elles saur___ la réponse.",
        "answers": ["ont"],
        "verb": "savoir",
        "group": "3ᵉ groupe",
        "explanation": "Elles + saur- + terminaison -ont.",
    },
]


def main() -> None:
    """Affiche la leçon puis lance le quiz sur les terminaisons du futur simple."""

    show_lesson(LESSON)
    print("Tape uniquement la terminaison manquante (exemple : ai, as, a, ons, ez, ont).")
    score = 0
    total = len(QUESTIONS)
    for question in QUESTIONS:
        print(f"\n{question['prompt']}")
        answer = input("Terminaison : ").strip().lower().replace("-", "")
        valid_answers = [option.lower() for option in question["answers"]]
        if answer in valid_answers:
            print("✅ Bravo !")
            score += 1
        else:
            correct = question["answers"][0]
            print(
                "❌ Ce n'est pas la bonne terminaison. "
                f"Pour '{question['verb']}', la réponse attendue est : {correct}."
            )
            print(f"ℹ️ {question['explanation']}")
    print(f"\nScore final : {score}/{total}")
    percentage = score / total * 100 if total else 0.0
    log_result("francais_futur_simple_terminaisons", percentage)


if __name__ == "__main__":
    main()
