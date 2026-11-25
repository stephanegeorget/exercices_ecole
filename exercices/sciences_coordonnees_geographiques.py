"""Leçon et quiz sur les coordonnées géographiques : latitude, longitude, méridiens et parallèles."""

# Nom lisible de l'exercice pour le menu principal
DISPLAY_NAME = "Sciences : Coordonnées géographiques (latitude et longitude)"

import unicodedata

from .utils import show_lesson
from .logger import log_result

GREEN = "\033[92m"
RED = "\033[91m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"


def _normalise(text: str) -> str:
    """Met la réponse en minuscules, sans accents, espaces ni symbole ° autour."""

    decomposed = unicodedata.normalize("NFKD", text)
    without_accents = "".join(c for c in decomposed if not unicodedata.combining(c))
    return without_accents.strip().lower().replace("°", "").replace("degres", "").replace(" ", "")


def _is_correct(reply: str, accepted: tuple[str, ...]) -> bool:
    """Vérifie que la réponse correspond à l'une des formes acceptées."""

    return _normalise(reply) in {_normalise(option) for option in accepted}


def main() -> None:
    """Présente la leçon puis un quiz corrigé."""

    lesson = f"""
{CYAN}{BOLD}🌍 Se repérer sur la Terre avec des coordonnées 🌍{RESET}

Pour trouver un lieu sur la Terre, on utilise deux nombres : la {BOLD}latitude{RESET}
et la {BOLD}longitude{RESET}. On les écrit en degrés (°).

{BOLD}1. L'équateur et les parallèles{RESET}
- L'équateur est la ligne imaginaire qui fait le tour de la Terre au milieu,
  entre le pôle Nord et le pôle Sud.
- Les {BOLD}parallèles{RESET} sont des cercles imaginaires parallèles à l'équateur.
- La {BOLD}latitude{RESET} mesure la distance angulaire à l'équateur :
  elle va de 0° (équateur) à 90° Nord (pôle Nord) ou 90° Sud (pôle Sud).

{BOLD}2. Les méridiens{RESET}
- Les {BOLD}méridiens{RESET} sont des demi-cercles qui relient le pôle Nord au pôle Sud.
- Le méridien de référence, ou méridien 0°, passe par {BOLD}Greenwich{RESET}, près de Londres.
- La {BOLD}longitude{RESET} mesure la distance angulaire à ce méridien :
  elle va de 0° à 180° Est ou à 180° Ouest.

{BOLD}3. Les points cardinaux{RESET}
- Nord : vers le pôle Nord ; Sud : vers le pôle Sud.
- Est : à droite de Greenwich quand on regarde vers le Nord ; Ouest : à gauche.

{BOLD}4. À quoi ressemble une coordonnée ?{RESET}
Exemple pour Paris, environ {BOLD}48° N ; 2° E{RESET} :
- {BOLD}48° N{RESET} : la latitude, 48° au Nord de l'équateur ;
- {BOLD}2° E{RESET} : la longitude, 2° à l'Est de Greenwich.

{BOLD}Activité :{RESET}
Cherche sur une carte la latitude et la longitude de ta ville ou de ton école.
"""
    show_lesson(lesson)

    questions = [
        (
            "Quel est le méridien de référence, celui qui vaut 0° de longitude ?",
            ("Greenwich",),
            "Le méridien de référence passe par Greenwich, près de Londres.",
        ),
        (
            "Quelle est la latitude de l'équateur (en degrés) ?",
            ("0",),
            "L'équateur est à 0° de latitude.",
        ),
        (
            "Quelle est la latitude du pôle Nord (en degrés) ?",
            ("90", "90 N", "90 Nord"),
            "Le pôle Nord est à 90° de latitude Nord.",
        ),
        (
            "Les méridiens relient-ils le pôle Nord au pôle Sud, ou sont-ils des cercles parallèles à l'équateur ?",
            ("pôle Nord au pôle Sud", "pole nord au pole sud", "nord-sud", "nord sud"),
            "Les méridiens relient le pôle Nord au pôle Sud ; les parallèles sont parallèles à l'équateur.",
        ),
        (
            "Dans la coordonnée 48° N ; 2° E, quel nombre donne la latitude ?",
            ("48", "48 N", "48°N"),
            "La latitude vient en premier : 48° N.",
        ),
        (
            "Paris est-il à l'est ou à l'ouest de Greenwich ?",
            ("est", "Est", "E"),
            "Paris est à environ 2° à l'Est de Greenwich.",
        ),
        (
            "Quel nom donne-t-on aux lignes imaginaires parallèles à l'équateur ?",
            ("parallèles", "parallele", "parallèle", "parallèles"),
            "Ce sont les parallèles.",
        ),
    ]

    print(f"{CYAN}{BOLD}✏️  Quiz : réponds à chaque question !  ✏️{RESET}")
    score = 0
    for question, accepted, explanation in questions:
        reply = input(f"\n{question}\n-> ").strip()
        if _is_correct(reply, accepted):
            print(f"{GREEN}Bien joué ! ✅{RESET}")
            score += 1
        else:
            print(f"{RED}Oups ! ❌ {explanation}{RESET}")

    total = len(questions)
    print(f"\n{BOLD}Score final : {score}/{total}{RESET}")
    if score == total:
        print(f"{GREEN}Excellent ! Tu sais te repérer sur la Terre ! 🥳{RESET}")
    elif score >= total / 2:
        print(f"{CYAN}Bravo ! Relis les méridiens et les parallèles. 👍{RESET}")
    else:
        print(f"{RED}Relis la leçon et réessaie ! 💪{RESET}")
    log_result("sciences_coordonnees_geographiques", score / total * 100)


if __name__ == "__main__":
    main()
