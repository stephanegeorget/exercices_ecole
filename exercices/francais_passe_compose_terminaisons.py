from __future__ import annotations

"""Révision des terminaisons du participe passé au passé composé."""

DISPLAY_NAME = "Français : Passé composé – terminaisons"

from .logger import log_result
from .utils import show_lesson

LESSON = """
📚 **Rappel : former le passé composé**

Le passé composé se construit avec un auxiliaire (**avoir** ou **être**) et un
**participe passé**. C'est justement la terminaison de ce participe que tu vas
réviser : tape uniquement la **fin du mot** (ex. `é`, `i`, `is`…), pas tout le
mot.

🧠 **Terminaisons principales selon le groupe**

- **1er groupe** : les verbes en *-er* forment leur participe passé en **-é**.
  > chanter → chanté, regarder → regardé
- **2ᵉ groupe** : les verbes réguliers en *-ir* prennent **-i**.
  > finir → fini, grandir → grandi
- **3ᵉ groupe** : plusieurs modèles existent. Retenons ici quelques terminaisons
  fréquentes :
  - **-is / -it** (prendre → pris, faire → fait)
  - **-u** (vendre → vendu, pouvoir → pu)

Chaque question indique le groupe du verbe et la phrase à compléter. Tape la
bonne terminaison pour obtenir le participe passé correct !
"""

QUESTIONS = [
    {
        "prompt": "Je raconte ma journée : j'ai racont__ ma journée.",
        "ending": ["é", "e"],
        "full_word": "raconté",
        "group": "1er groupe",
        "explanation": "Les verbes du 1er groupe prennent -é au participe passé.",
    },
    {
        "prompt": "Tu as observé les oiseaux : tu as regard__ longtemps par la fenêtre.",
        "ending": ["é", "e"],
        "full_word": "regardé",
        "group": "1er groupe",
        "explanation": "Regarder appartient au 1er groupe : terminaison -é.",
    },
    {
        "prompt": "Nous avons choisi un film : nous avons chois__ une comédie.",
        "ending": ["i"],
        "full_word": "choisi",
        "group": "2ᵉ groupe",
        "explanation": "Les verbes en -ir du 2ᵉ groupe prennent -i.",
    },
    {
        "prompt": "Elles ont grandi vite : elles ont grand__ en une année.",
        "ending": ["i"],
        "full_word": "grandi",
        "group": "2ᵉ groupe",
        "explanation": "Grandir est un verbe régulier du 2ᵉ groupe → terminaison -i.",
    },
    {
        "prompt": "Il a pris son sac : il a pr__ son sac avant de partir.",
        "ending": ["is"],
        "full_word": "pris",
        "group": "3ᵉ groupe",
        "explanation": "Prendre fait partie du 3ᵉ groupe : participe passé en -is.",
    },
    {
        "prompt": "Elle a fait un dessin : elle a fa__ un beau paysage.",
        "ending": ["it"],
        "full_word": "fait",
        "group": "3ᵉ groupe",
        "explanation": "Faire (3ᵉ groupe) forme son participe passé en -it.",
    },
    {
        "prompt": "Nous avons vendu nos vélos : nous avons vend__ le nôtre.",
        "ending": ["u"],
        "full_word": "vendu",
        "group": "3ᵉ groupe",
        "explanation": "Beaucoup de verbes du 3ᵉ groupe prennent -u (vendre → vendu).",
    },
    {
        "prompt": "Vous avez pu finir : vous avez p__ terminer à temps !",
        "ending": ["u"],
        "full_word": "pu",
        "group": "3ᵉ groupe",
        "explanation": "Pouvoir est du 3ᵉ groupe et forme son participe passé en -u.",
    },
    {
        "prompt": "Ils ont applaudi : ils ont applaud__ très fort.",
        "ending": ["i"],
        "full_word": "applaudi",
        "group": "2ᵉ groupe",
        "explanation": "Applaudir suit le modèle des verbes réguliers en -ir → -i.",
    },
    {
        "prompt": "Tu as nettoyé ta chambre : tu as nettoy__ chaque étagère.",
        "ending": ["é", "e"],
        "full_word": "nettoyé",
        "group": "1er groupe",
        "explanation": "Nettoyer est un verbe du 1er groupe → terminaison -é.",
    },
]


def main() -> None:
    """Affiche la leçon puis lance le quiz sur les terminaisons du participe passé."""

    show_lesson(LESSON)
    print("Tape uniquement la terminaison demandée (par exemple `é`, `i`, `is`).")
    score = 0
    total = len(QUESTIONS)
    for index, question in enumerate(QUESTIONS, start=1):
        print(f"\nQuestion {index} – {question['group']}")
        print(question["prompt"])
        answer = input("Terminaison : ").strip().lower()
        valid = [ending.lower() for ending in question["ending"]]
        if answer in valid:
            print("✅ Bravo !")
            score += 1
        else:
            correct = question["ending"][0]
            full_word = question["full_word"]
            print(
                f"❌ Ce n'est pas ça. Il fallait écrire `{correct}` pour obtenir `{full_word}`."
            )
            print(f"ℹ️ {question['explanation']}")
    print(f"\nScore final : {score}/{total}")
    percentage = score / total * 100 if total else 0.0
    log_result("francais_passe_compose_terminaisons", percentage)


if __name__ == "__main__":
    main()
