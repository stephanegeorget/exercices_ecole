from __future__ import annotations

"""Révision des terminaisons du passé simple selon les groupes."""

DISPLAY_NAME = "Français : Passé simple – terminaisons"

from .logger import log_result
from .utils import show_lesson

LESSON = """
📚 **Rappel : conjuguer au passé simple**

Le passé simple raconte des actions brèves dans les récits. Chaque groupe de
verbes possède ses terminaisons propres. Dans ce quiz, tu dois taper uniquement
la **terminaison** du verbe (ex. `ai`, `as`, `îmes`).

🧠 **Terminaisons à connaître**

- **1er groupe (-er)** : -ai, -as, -a, -âmes, -âtes, -èrent.
- **2ᵉ groupe (-ir réguliers)** : -is, -is, -it, -îmes, -îtes, -irent.
- **3ᵉ groupe** : plusieurs modèles.
  - Modèle « prendre » : -is, -is, -it, -îmes, -îtes, -irent.
  - Modèle « recevoir » : -us, -us, -ut, -ûmes, -ûtes, -urent.

Les phrases indiquent toujours le groupe visé pour t'aider à repérer la bonne
terminaison.
"""

QUESTIONS = [
    {  # 1er groupe
        "prompt": "Je (parler) longtemps avec ma sœur : je parl__ avec elle.",
        "ending": ["ai"],
        "full_word": "parlai",
        "group": "1er groupe",
        "explanation": "Au 1er groupe, la 1ʳᵉ personne du singulier se termine par -ai.",
    },
    {
        "prompt": "Tu (regarder) les étoiles : tu regard__ le ciel.",
        "ending": ["as"],
        "full_word": "regardas",
        "group": "1er groupe",
        "explanation": "2ᵉ personne du singulier du 1er groupe → terminaison -as.",
    },
    {
        "prompt": "Il (marcher) des heures : il march__ longtemps.",
        "ending": ["a"],
        "full_word": "marcha",
        "group": "1er groupe",
        "explanation": "3ᵉ personne du singulier au 1er groupe → terminaison -a.",
    },
    {
        "prompt": "Nous (danser) sous la pluie : nous dans__ joyeusement.",
        "ending": ["âmes", "ames"],
        "full_word": "dansâmes",
        "group": "1er groupe",
        "explanation": "1ʳᵉ personne du pluriel du 1er groupe → -âmes.",
    },
    {
        "prompt": "Vous (chanter) en chœur : vous chant__ ensemble.",
        "ending": ["âtes", "ates"],
        "full_word": "chantâtes",
        "group": "1er groupe",
        "explanation": "2ᵉ personne du pluriel du 1er groupe → -âtes.",
    },
    {
        "prompt": "Ils (jouer) au ballon : ils jou__ tout l'après-midi.",
        "ending": ["èrent", "erent"],
        "full_word": "jouèrent",
        "group": "1er groupe",
        "explanation": "3ᵉ personne du pluriel du 1er groupe → -èrent.",
    },
    {  # 2e groupe
        "prompt": "Je (finir) mes devoirs : je fin__ tout rapidement.",
        "ending": ["is"],
        "full_word": "finis",
        "group": "2ᵉ groupe",
        "explanation": "Je finis : terminaison -is pour les verbes réguliers en -ir.",
    },
    {
        "prompt": "Tu (choisir) un livre : tu chois__ ce roman.",
        "ending": ["is"],
        "full_word": "choisis",
        "group": "2ᵉ groupe",
        "explanation": "Tu choisis : même terminaison -is.",
    },
    {
        "prompt": "Elle (grandir) très vite : elle grand__ en un été.",
        "ending": ["it"],
        "full_word": "grandit",
        "group": "2ᵉ groupe",
        "explanation": "Il/elle/on grandit : terminaison -it.",
    },
    {
        "prompt": "Nous (rougir) de timidité : nous roug__ un peu.",
        "ending": ["îmes", "imes"],
        "full_word": "rougîmes",
        "group": "2ᵉ groupe",
        "explanation": "Nous rougîmes : terminaison -îmes (accent obligatoire à l'écrit).",
    },
    {
        "prompt": "Vous (réfléchir) calmement : vous réfléch__ avant d'agir.",
        "ending": ["îtes", "ites"],
        "full_word": "réfléchîtes",
        "group": "2ᵉ groupe",
        "explanation": "Vous réfléchîtes : terminaison -îtes.",
    },
    {
        "prompt": "Ils (réussir) leur examen : ils réuss__ tous !",
        "ending": ["irent"],
        "full_word": "réussirent",
        "group": "2ᵉ groupe",
        "explanation": "Ils réussirent : terminaison -irent au 2ᵉ groupe.",
    },
    {  # 3e groupe - modèle prendre
        "prompt": "Je (prendre) un croissant : je pr__ un croissant croustillant.",
        "ending": ["is"],
        "full_word": "pris",
        "group": "3ᵉ groupe",
        "explanation": "Je pris : terminaison -is pour ce modèle du 3ᵉ groupe.",
    },
    {
        "prompt": "Tu (écrire) une lettre : tu écriv__ à ton amie.",
        "ending": ["is"],
        "full_word": "écrivis",
        "group": "3ᵉ groupe",
        "explanation": "Écrire suit la série en -is/-is/-it au passé simple.",
    },
    {
        "prompt": "Il (dire) la vérité : il d__ tout ce qu'il savait.",
        "ending": ["it"],
        "full_word": "dit",
        "group": "3ᵉ groupe",
        "explanation": "Il dit : terminaison -it comme beaucoup de verbes du 3ᵉ groupe.",
    },
    {
        "prompt": "Nous (venir) en aide : nous vîn__ immédiatement.",
        "ending": ["mes"],
        "full_word": "vînmes",
        "group": "3ᵉ groupe",
        "explanation": "Venir est irrégulier : nous vînmes (terminaison -mes).",
    },
    {
        "prompt": "Vous (recevoir) les consignes : vous reç__ toutes les instructions.",
        "ending": ["ûtes", "utes"],
        "full_word": "reçûtes",
        "group": "3ᵉ groupe",
        "explanation": "Recevoir suit le modèle en -us/-ut/-ûtes.",
    },
    {
        "prompt": "Ils (pouvoir) rentrer : ils pur__ enfin chez eux.",
        "ending": ["ent"],
        "full_word": "purent",
        "group": "3ᵉ groupe",
        "explanation": "Pouvoir → ils purent : terminaison -ent pour ce modèle.",
    },
]


def main() -> None:
    """Affiche la leçon puis lance le quiz sur le passé simple."""

    show_lesson(LESSON)
    print("Tape seulement la terminaison demandée (ex. `ai`, `is`, `ûtes`).")
    score = 0
    total = len(QUESTIONS)
    for index, question in enumerate(QUESTIONS, start=1):
        print(f"\nQuestion {index} – {question['group']}")
        print(question["prompt"])
        answer = input("Terminaison : ").strip().lower()
        valid = [ending.lower() for ending in question["ending"]]
        if answer in valid:
            print("✅ Bien joué !")
            score += 1
        else:
            correct = question["ending"][0]
            full_word = question["full_word"]
            print(
                f"❌ Mauvaise terminaison. Il fallait écrire `{correct}` pour obtenir `{full_word}`."
            )
            print(f"ℹ️ {question['explanation']}")
    print(f"\nScore final : {score}/{total}")
    percentage = score / total * 100 if total else 0.0
    log_result("francais_passe_simple_terminaisons", percentage)


if __name__ == "__main__":
    main()
