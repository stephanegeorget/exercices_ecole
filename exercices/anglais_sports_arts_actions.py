"""Exercise based on a worksheet about sports and arts action verbs."""

from __future__ import annotations

import random
from textwrap import dedent

from .logger import log_result
from .utils import show_lesson

DISPLAY_NAME = "Anglais : Sports and arts actions"

GREEN = "\033[92m"
RED = "\033[91m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

SPORTS_ACTIONS: list[str] = [
    "swim",
    "dive",
    "surf",
    "ski",
    "skate",
    "ice skate",
    "ride a horse",
    "ride a bike",
    "play rugby",
    "play soccer",
    "run fast",
    "do gymnastics",
]

ARTS_ACTIONS: list[str] = [
    "act",
    "paint",
    "draw",
    "juggle",
    "do magic tricks",
    "dance",
    "sing",
    "play the guitar",
    "play the piano",
    "play the violin",
    "play the drums",
]

TRANSLATION_ITEMS: list[tuple[str, str]] = [
    ("nager", "swim"),
    ("plonger", "dive"),
    ("surfer", "surf"),
    ("faire du ski", "ski"),
    ("patiner", "skate"),
    ("faire du patin à glace", "ice skate"),
    ("faire de l'équitation", "ride a horse"),
    ("faire du vélo", "ride a bike"),
    ("jouer au rugby", "play rugby"),
    ("jouer au football", "play soccer"),
    ("courir vite", "run fast"),
    ("faire de la gymnastique", "do gymnastics"),
    ("jouer la comédie", "act"),
    ("peindre", "paint"),
    ("dessiner", "draw"),
    ("jongler", "juggle"),
    ("faire des tours de magie", "do magic tricks"),
    ("danser", "dance"),
    ("chanter", "sing"),
    ("jouer de la guitare", "play the guitar"),
    ("jouer du piano", "play the piano"),
    ("jouer du violon", "play the violin"),
    ("jouer de la batterie", "play the drums"),
]

SOUND_GROUPS: dict[str, set[str]] = {
    "[ɪ]": {"swim", "sing"},
    "[iː]": {"ski", "guitar"},
    "[aɪ]": {"ride", "dive", "bike"},
    "[eɪ]": {"skate", "play", "paint"},
}


def _show_lesson() -> None:
    lesson = dedent(
        f"""
        {CYAN}{BOLD}Sports and arts actions{RESET}

        This exercise is inspired by your worksheet image.

        {BOLD}Sports verbs{RESET}
        • swim, dive, surf, ski, skate, ice skate
        • ride a horse, ride a bike
        • play rugby, play soccer
        • run fast, do gymnastics

        {BOLD}Arts verbs{RESET}
        • act, paint, draw, juggle, do magic tricks
        • dance, sing
        • play the guitar, play the piano, play the violin, play the drums

        {BOLD}Grammar tip{RESET}
        Use {BOLD}play{RESET} with team sports and instruments,
        but use {BOLD}do{RESET} with activities like gymnastics.

        Press {BOLD}q{RESET} when you are ready to start.
        """
    )
    show_lesson(lesson)


def _translation_quiz(num_questions: int = 8) -> tuple[int, int]:
    print(f"{BOLD}Part 1 - Translate into English{RESET}")
    score = 0
    sample = random.sample(TRANSLATION_ITEMS, k=min(num_questions, len(TRANSLATION_ITEMS)))

    for index, (french, english) in enumerate(sample, start=1):
        answer = input(f"{index}. Comment dit-on '{french}' ? ").strip().lower()
        if answer == english:
            print(f"{GREEN}Correct!{RESET}")
            score += 1
        else:
            print(f"{RED}Oops.{RESET} Correct answer: {english}")

    total = len(sample)
    print(f"Score part 1: {score}/{total}\n")
    return score, total


def _category_quiz(num_questions: int = 8) -> tuple[int, int]:
    print(f"{BOLD}Part 2 - Sports or Arts?{RESET}")
    score = 0
    all_actions = [(action, "sport") for action in SPORTS_ACTIONS] + [
        (action, "arts") for action in ARTS_ACTIONS
    ]
    sample = random.sample(all_actions, k=min(num_questions, len(all_actions)))

    for index, (action, expected) in enumerate(sample, start=1):
        answer = input(f"{index}. '{action}' -> sport or arts? ").strip().lower()
        accepted = "sport" if expected == "sport" else "arts"
        if answer == accepted:
            print(f"{GREEN}Yes!{RESET}")
            score += 1
        else:
            print(f"{RED}Not this time.{RESET} It is {accepted}.")

    total = len(sample)
    print(f"Score part 2: {score}/{total}\n")
    return score, total


def _pronunciation_quiz() -> tuple[int, int]:
    print(f"{BOLD}Part 3 - Pronunciation focus{RESET}")
    words = ["swim", "ride", "skate", "play", "sing", "dive", "paint", "ski", "guitar", "bike"]
    score = 0

    for word in words:
        answer = input(f"Sound of the highlighted vowel in '{word}' ([ɪ], [iː], [aɪ], [eɪ])? ").strip()
        expected = next(sound for sound, group_words in SOUND_GROUPS.items() if word in group_words)
        if answer == expected:
            print(f"{GREEN}Great ear!{RESET}")
            score += 1
        else:
            print(f"{RED}Try again next time.{RESET} Expected: {expected}")

    total = len(words)
    print(f"Score part 3: {score}/{total}\n")
    return score, total


def main() -> None:
    _show_lesson()
    part1_score, part1_total = _translation_quiz()
    part2_score, part2_total = _category_quiz()
    part3_score, part3_total = _pronunciation_quiz()

    total_score = part1_score + part2_score + part3_score
    total_questions = part1_total + part2_total + part3_total
    percentage = total_score / total_questions * 100 if total_questions else 0.0

    print(f"{CYAN}{BOLD}Final score{RESET}: {total_score}/{total_questions} ({percentage:.1f}%)")
    print("Keep practicing your sports and arts action words!\n")

    log_result("anglais_sports_arts_actions", percentage)


if __name__ == "__main__":
    main()
