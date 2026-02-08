from __future__ import annotations

"""Leçon et quiz sur l'imparfait de l'indicatif."""

import sys

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

Dans ce quiz, tu peux t'entraîner en mode **facile** (fin du verbe) ou **difficile** (verbe complet).
"""

GROUP_LABELS = {
    "1": "1er groupe",
    "2": "2ᵉ groupe",
    "3": "3ᵉ groupe",
}

MODE_LABELS = {
    "easy": "Facile (écrire la fin du verbe)",
    "hard": "Difficile (écrire le verbe complet)",
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
    # 2e groupe (l'élève doit aussi écrire "iss" en mode facile)
    {"group": "2", "sentence": "Le week-end, je (finir) fin____ mes devoirs tôt.", "base": "fin", "ending": "issais"},
    {"group": "2", "sentence": "À la cantine, tu (choisir) chois____ toujours le même plat.", "base": "chois", "ending": "issais"},
    {"group": "2", "sentence": "Au printemps, le chiot (grandir) grand____ vite.", "base": "grand", "ending": "issait"},
    {"group": "2", "sentence": "En classe, nous (réfléchir) réfléch____ avant de répondre.", "base": "réfléch", "ending": "issions"},
    {"group": "2", "sentence": "À ce jeu, vous (réussir) réuss____ souvent les niveaux difficiles.", "base": "réuss", "ending": "issiez"},
    {"group": "2", "sentence": "Petites, elles (rougir) roug____ de timidité.", "base": "roug", "ending": "issaient"},
    # 3e groupe
    {"group": "3", "sentence": "Hier, la télé (être) ét____ en panne.", "base": "ét", "ending": "ait"},
    {"group": "3", "sentence": "Chaque matin, j' (avoir) av____ du mal à me lever.", "base": "av", "ending": "ais"},
    {"group": "3", "sentence": "Avant, il (faire) fais____ du vélo pour aller à l'école.", "base": "fais", "ending": "ait"},
    {"group": "3", "sentence": "À cette époque, nous (faire) fais____ tout à la main.", "base": "fais", "ending": "ions"},
    {"group": "3", "sentence": "Pendant les vacances, vous (voir) voy____ vos cousins tous les jours.", "base": "voy", "ending": "iez"},
    {"group": "3", "sentence": "Dans le jardin, nous (voir) voy____ souvent des hérissons.", "base": "voy", "ending": "ions"},
    {"group": "3", "sentence": "Le soir, ils (venir) ven____ nous dire bonsoir.", "base": "ven", "ending": "aient"},
]


def _normalise_text(raw: str) -> str:
    answer = raw.strip().lower().replace(" ", "")
    while answer.startswith("-"):
        answer = answer[1:]
    return answer


def _menu_choice(selected_groups: set[str], mode: str) -> str:
    print("\n=== Imparfait de l'indicatif ===")
    print("1. Voir la leçon")
    for group_key in ("1", "2", "3"):
        mark = "x" if group_key in selected_groups else " "
        print(f"{int(group_key) + 1}. [{mark}] {GROUP_LABELS[group_key]}")
    print(f"5. Mode actuel : {MODE_LABELS[mode]}")
    print("6. Lancer le quiz")
    print("0. Retour")
    return input("Votre choix : ").strip()


def _inline_sentence_input(before: str, after: str, slot_width: int) -> str:
    slot = " " * max(1, slot_width)

    if sys.stdout.isatty() and sys.stdin.isatty():
        print(f"{before}{slot}{after}", end="", flush=True)
        print(f"\033[{len(after) + len(slot)}D", end="", flush=True)
        return input()

    return input(before)


def _ask_with_preview(question: dict[str, str], mode: str) -> str:
    sentence = question["sentence"]
    base = question["base"]
    ending = question["ending"]

    if mode == "easy":
        before, after = sentence.split("____", 1)
        return _inline_sentence_input(before, after, len(ending) + 2)

    target = f"{base}____"
    if target in sentence:
        before, after = sentence.split(target, 1)
        return _inline_sentence_input(before, after, len(base + ending) + 2)

    before, after = sentence.split("____", 1)
    return _inline_sentence_input(before, after, len(base + ending) + 2)


def _run_quiz(selected_groups: set[str], mode: str) -> None:
    active_questions = [q for q in QUESTIONS if q["group"] in selected_groups]
    if not active_questions:
        print("\n⚠️ Tu dois cocher au moins un groupe avant de lancer le quiz.")
        return

    if mode == "easy":
        print("\nMode facile : écris la fin manquante (ex. ais, issions, aient...).")
    else:
        print("\nMode difficile : écris le verbe conjugué en entier.")

    score = 0
    total = len(active_questions)

    for index, question in enumerate(active_questions, start=1):
        print(f"\nQuestion {index}/{total}")
        print("Écris le verbe entre parenthèses à l'imparfait, puis appuie sur [ENTER].")
        raw_answer = _ask_with_preview(question, mode)
        answer = _normalise_text(raw_answer)

        expected_full = f"{question['base']}{question['ending']}"
        expected = question["ending"] if mode == "easy" else expected_full

        if answer == expected:
            print("✅ Exact !")
            score += 1
        else:
            if mode == "easy":
                print(f"❌ Non. La bonne fin était « {question['ending']} ».")
            else:
                print(f"❌ Non. Le verbe attendu était « {expected_full} ».")
            print(f"   Forme complète : {expected_full}")

    percentage = score / total * 100 if total else 0.0
    print(f"\nScore final : {score}/{total} ({percentage:.1f} %)")
    log_result("francais_imparfait_indicatif", percentage)


def main() -> None:
    selected_groups = {"1", "2", "3"}
    mode = "easy"

    while True:
        choice = _menu_choice(selected_groups, mode)

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
            mode = "hard" if mode == "easy" else "easy"
            continue
        if choice == "6":
            _run_quiz(selected_groups, mode)
            continue

        print("Choix invalide.")


if __name__ == "__main__":
    main()
