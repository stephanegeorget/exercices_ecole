"""Vocabulaire anglais sur les vêtements d'un uniforme scolaire."""

from __future__ import annotations

import random
from textwrap import dedent

from .logger import log_result
from .utils import ask_choice_with_navigation, show_lesson

DISPLAY_NAME = "Anglais : School uniform vocabulary"

GREEN = "\033[92m"
RED = "\033[91m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

THINGS: list[dict[str, str]] = [
    {"en": "a white collar", "fr": "un col blanc"},
    {"en": "a white bow tie", "fr": "un nœud papillon blanc"},
    {"en": "a black waistcoat", "fr": "un gilet noir"},
    {"en": "a black tailcoat", "fr": "une queue-de-pie noire"},
    {"en": "black trousers", "fr": "un pantalon noir"},
    {"en": "a white shirt", "fr": "une chemise blanche"},
    {"en": "a tie", "fr": "une cravate"},
    {"en": "a blazer", "fr": "un blazer"},
    {"en": "a skirt", "fr": "une jupe"},
    {"en": "tights", "fr": "des collants"},
    {"en": "a school badge", "fr": "un écusson d'école"},
    {"en": "a polo shirt", "fr": "un polo"},
    {"en": "trainers", "fr": "des baskets"},
    {"en": "socks", "fr": "des chaussettes"},
    {"en": "shoes", "fr": "des chaussures"},
    {"en": "a cardigan", "fr": "un gilet en laine"},
    {"en": "a jumper", "fr": "un pull"},
    {"en": "red shoes", "fr": "des chaussures rouges"},
    {"en": "blue socks", "fr": "des chaussettes bleues"},
    {"en": "a red tie", "fr": "une cravate rouge"},
    {"en": "a blue blazer", "fr": "un blazer bleu"},
    {"en": "a green cardigan", "fr": "un gilet en laine vert"},
    {"en": "a grey jumper", "fr": "un pull gris"},
    {"en": "a black skirt", "fr": "une jupe noire"},
    {"en": "white tights", "fr": "des collants blancs"},
    {"en": "a blue polo shirt", "fr": "un polo bleu"},
    {"en": "black trainers", "fr": "des baskets noires"},
    {"en": "a red school badge", "fr": "un écusson d'école rouge"},
    {"en": "a green tie", "fr": "une cravate verte"},
    {"en": "brown shoes", "fr": "des chaussures marron"},
]


def _mask_word(text: str) -> str:
    return "".join("_" if char.isalpha() else char for char in text)


def _quiz_en_from_fr(item: dict[str, str], pool: list[dict[str, str]]) -> bool:
    prompt = f"Choisis l'expression anglaise pour : {item['fr']}"
    distractors = [candidate["en"] for candidate in pool if candidate["en"] != item["en"]]
    options = random.sample(distractors, k=3) + [item["en"]]
    random.shuffle(options)

    print(f"\n{BOLD}Quiz 1/2{RESET} — {prompt}")
    selected, _, wants_exit = ask_choice_with_navigation(options)
    if wants_exit:
        raise KeyboardInterrupt
    if selected is None or selected < 0:
        print(f"{RED}Réponse invalide.{RESET}")
        return False

    ok = options[selected] == item["en"]
    if ok:
        print(f"{GREEN}Bravo !{RESET} {item['en']} = {item['fr']}.")
    else:
        print(f"{RED}Raté.{RESET} La bonne réponse était : {item['en']}.")
    return ok


def _quiz_fr_from_en(item: dict[str, str], pool: list[dict[str, str]]) -> bool:
    prompt = f"Choisis la description française de : {item['en']}"
    distractors = [candidate["fr"] for candidate in pool if candidate["fr"] != item["fr"]]
    options = random.sample(distractors, k=3) + [item["fr"]]
    random.shuffle(options)

    print(f"\n{BOLD}Quiz 2/2{RESET} — {prompt}")
    selected, _, wants_exit = ask_choice_with_navigation(options)
    if wants_exit:
        raise KeyboardInterrupt
    if selected is None or selected < 0:
        print(f"{RED}Réponse invalide.{RESET}")
        return False

    ok = options[selected] == item["fr"]
    if ok:
        print(f"{GREEN}Excellent !{RESET} {item['en']} signifie {item['fr']}.")
    else:
        print(f"{RED}Raté.{RESET} La bonne réponse était : {item['fr']}.")
    return ok


def _copy_word(item: dict[str, str]) -> bool:
    mask = _mask_word(item["en"])
    print(f"\n{BOLD}Écriture clavier{RESET}")
    print(f"Recopie le mot/les mots en anglais : {item['fr']}")
    print(f"Modèle à compléter : {CYAN}{mask}{RESET}")
    typed = input("Ta réponse : ").strip().lower()

    ok = typed == item["en"].lower()
    if ok:
        print(f"{GREEN}Parfait, orthographe correcte !{RESET}")
    else:
        print(f"{RED}Presque.{RESET} Il fallait écrire : {item['en']}")
    return ok


def main() -> None:
    lesson = dedent(
        f"""
        {CYAN}{BOLD}School uniform vocabulary (30 things){RESET}

        Objectif : apprendre le vocabulaire des vêtements et accessoires d'un uniforme.
        Pour chaque élément, tu auras :
          1) un rappel avec la description en français ;
          2) deux quiz à choix multiple (navigation avec les flèches) ;
          3) une recopie au clavier avec des tirets bas comme dans une dictée à trous.

        Astuce : respecte les espaces quand il y a plusieurs mots (ex: "a red tie").
        Tape q dans un quiz pour quitter et revenir au menu.
        """
    )
    show_lesson(lesson)

    print(f"{BOLD}Début de l'entraînement : 30 éléments.{RESET}")
    score = 0
    total = len(THINGS) * 3

    try:
        for index, item in enumerate(THINGS, start=1):
            print(f"\n{CYAN}{BOLD}Élément {index}/30{RESET}")
            print(f"À apprendre : {BOLD}{item['en']}{RESET} → {item['fr']}")

            if _quiz_en_from_fr(item, THINGS):
                score += 1
            if _quiz_fr_from_en(item, THINGS):
                score += 1
            if _copy_word(item):
                score += 1
    except KeyboardInterrupt:
        print("\nRetour au menu demandé.")

    percentage = score / total * 100
    print(f"\n{BOLD}Résultat final :{RESET} {score}/{total} ({percentage:.1f}%).")
    log_result("anglais_school_uniform", percentage)


if __name__ == "__main__":
    main()
