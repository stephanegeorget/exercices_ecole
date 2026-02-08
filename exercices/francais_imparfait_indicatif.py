from __future__ import annotations

"""Leçon et quiz sur l'imparfait de l'indicatif."""

DISPLAY_NAME = "Français : Imparfait de l'indicatif"

from .logger import log_result
from .utils import show_lesson

LESSON = """
📚 **L'imparfait de l'indicatif**

1) L'imparfait est **un temps du passé** utilisé :
- pour une description : *Le ciel était gris.*
- pour une action répétée : *Chaque soir, il lisait.*
- pour une action qui dure : *Je travaillais quand tu as appelé.*

2) À l'imparfait, **tous les verbes prennent les mêmes terminaisons** :
- `-ais`, `-ais`, `-ait`, `-ions`, `-iez`, `-aient`

3) On forme l'imparfait avec le radical de **nous** au présent + terminaison.
- nous chantons → je chant**ais**
- nous finissons → tu finiss**ais**
- nous prenons → ils pren**aient**

🧠 **Mémo 1er groupe**
- Verbes en `-cer` : *nous lançons* → *je lançais*.
- Verbes en `-ger` : *nous plongeons* → *il plongeait*.
- Verbes en `-ier/-yer` gardent souvent le `i`/`y` :
  *nous criions*, *vous payiez*.

🧠 **Mémo 2ᵉ groupe**
- On place **-iss-** entre le radical et la terminaison :
  *finiss-ais, finiss-ions, finiss-aient*.

🧠 **Mémo 3ᵉ groupe (particularités de radical)**
- *faire* → je faisais, nous faisions
- *voir* → je voyais, nous voyions
- *être* est irrégulier : j'étais, tu étais, il était, nous étions, vous étiez, ils étaient.

Dans ce quiz, tu complètes seulement **la fin du verbe** (la partie manquante après le radical affiché).
"""

GROUP_LABELS = {
    "1": "1er groupe",
    "2": "2ᵉ groupe",
    "3": "3ᵉ groupe",
}

QUESTIONS = [
    # 1er groupe
    {"group": "1", "sentence": "Tous les soirs, je (chanter) chant____ avant de dormir.", "base": "chant", "ending": "ais"},
    {"group": "1", "sentence": "Quand il pleuvait, tu (porter) port____ ton manteau rouge.", "base": "port", "ending": "ais"},
    {"group": "1", "sentence": "À l'époque, elle (jouer) jou____ du piano chaque mercredi.", "base": "jou", "ending": "ait"},
    {"group": "1", "sentence": "Petits, nous (regarder) regard____ les étoiles en été.", "base": "regard", "ending": "ions"},
    {"group": "1", "sentence": "En CE2, vous (dessiner) dessin____ pendant la récréation.", "base": "dessin", "ending": "iez"},
    {"group": "1", "sentence": "Autrefois, ils (habiter) habit____ dans ce village.", "base": "habit", "ending": "aient"},
    {"group": "1", "sentence": "Pendant la dictée, je (lancer) lanç____ mon regard vers le tableau.", "base": "lanç", "ending": "ais"},
    {"group": "1", "sentence": "L'été, il (plonger) plonge____ dans la rivière.", "base": "plonge", "ending": "ait"},
    {"group": "1", "sentence": "En chorale, nous (crier) cri____ de joie à la fin du spectacle.", "base": "cri", "ending": "ions"},
    {"group": "1", "sentence": "Au marché, vous (payer) pay____ en pièces jaunes.", "base": "pay", "ending": "iez"},
    # 2e groupe
    {"group": "2", "sentence": "Le week-end, je (finir) finiss____ mes devoirs tôt.", "base": "finiss", "ending": "ais"},
    {"group": "2", "sentence": "À la cantine, tu (choisir) choisiss____ toujours le même plat.", "base": "choisiss", "ending": "ais"},
    {"group": "2", "sentence": "Au printemps, le chiot (grandir) grandiss____ vite.", "base": "grandiss", "ending": "ait"},
    {"group": "2", "sentence": "En classe, nous (réfléchir) réfléchiss____ avant de répondre.", "base": "réfléchiss", "ending": "ions"},
    {"group": "2", "sentence": "À ce jeu, vous (réussir) réussiss____ souvent les niveaux difficiles.", "base": "réussiss", "ending": "iez"},
    {"group": "2", "sentence": "Petites, elles (rougir) rougiss____ de timidité.", "base": "rougiss", "ending": "aient"},
    # 3e groupe
    {"group": "3", "sentence": "Hier, la télé (être) ét____ en panne.", "base": "ét", "ending": "ait"},
    {"group": "3", "sentence": "Chaque matin, j' (avoir) av____ du mal à me lever.", "base": "av", "ending": "ais"},
    {"group": "3", "sentence": "Avant, il (faire) fais____ du vélo pour aller à l'école.", "base": "fais", "ending": "ait"},
    {"group": "3", "sentence": "À cette époque, nous (faire) fais____ tout à la main.", "base": "fais", "ending": "ions"},
    {"group": "3", "sentence": "Pendant les vacances, vous (voir) voy____ vos cousins tous les jours.", "base": "voy", "ending": "iez"},
    {"group": "3", "sentence": "Dans le jardin, nous (voir) voy____ souvent des hérissons.", "base": "voy", "ending": "ions"},
    {"group": "3", "sentence": "Le soir, ils (venir) ven____ nous dire bonsoir.", "base": "ven", "ending": "aient"},
]


def _normalise_ending(raw: str) -> str:
    answer = raw.strip().lower().replace(" ", "")
    while answer.startswith("-"):
        answer = answer[1:]
    return answer


def _menu_choice(selected_groups: set[str]) -> str:
    print("\n=== Imparfait de l'indicatif ===")
    print("1. Voir la leçon")
    for group_key in ("1", "2", "3"):
        mark = "x" if group_key in selected_groups else " "
        print(f"{int(group_key) + 1}. [{mark}] {GROUP_LABELS[group_key]}")
    print("5. Lancer le quiz")
    print("0. Retour")
    return input("Votre choix : ").strip()


def _run_quiz(selected_groups: set[str]) -> None:
    active_questions = [q for q in QUESTIONS if q["group"] in selected_groups]
    if not active_questions:
        print("\n⚠️ Tu dois cocher au moins un groupe avant de lancer le quiz.")
        return

    print("\nComplète uniquement la fin du verbe (exemple : ais, ait, ions...).")
    score = 0
    total = len(active_questions)

    for index, question in enumerate(active_questions, start=1):
        print(f"\nQuestion {index}/{total}")
        print(question["sentence"])
        answer = _normalise_ending(input("Terminaison : "))

        if answer == question["ending"]:
            print("✅ Exact !")
            score += 1
        else:
            full_form = f"{question['base']}{question['ending']}"
            print(f"❌ Non. La bonne terminaison était « {question['ending']} ».")
            print(f"   Forme complète : {full_form}")

    percentage = score / total * 100 if total else 0.0
    print(f"\nScore final : {score}/{total} ({percentage:.1f} %)")
    log_result("francais_imparfait_indicatif", percentage)


def main() -> None:
    selected_groups = {"1", "2", "3"}

    while True:
        choice = _menu_choice(selected_groups)

        if choice == "0":
            return
        if choice == "1":
            show_lesson(LESSON)
            continue
        if choice in {"2", "3", "4"}:
            group_key = str(int(choice) - 1)
            if group_key in selected_groups:
                selected_groups.remove(group_key)
            else:
                selected_groups.add(group_key)
            continue
        if choice == "5":
            _run_quiz(selected_groups)
            continue

        print("Choix invalide.")


if __name__ == "__main__":
    main()
