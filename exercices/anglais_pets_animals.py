"""Lesson and interactive activities about pets and animals."""

from __future__ import annotations

# Nom lisible de l'exercice pour le menu principal
DISPLAY_NAME = "Anglais : Pets and animals"

import random
from textwrap import dedent

from .utils import show_lesson
from .logger import log_result

GREEN = "\033[92m"
RED = "\033[91m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

PETS_TRANSLATIONS: list[tuple[str, str]] = [
    ("chien", "dog"),
    ("chat", "cat"),
    ("lapin", "rabbit"),
    ("poisson", "fish"),
    ("tortue", "turtle"),
    ("oiseau", "bird"),
    ("hamster", "hamster"),
    ("cochon d'Inde", "guinea pig"),
    ("cheval", "horse"),
    ("serpent", "snake"),
]

QUIZ_QUESTIONS: list[dict[str, object]] = [
    {
        "question": "Which animal loves to chase mice and purrs when it is happy?",
        "choices": ["cat", "parrot", "turtle"],
        "answer": "cat",
    },
    {
        "question": "Which pet has fins and breathes underwater?",
        "choices": ["fish", "rabbit", "hamster"],
        "answer": "fish",
    },
    {
        "question": "Which animal can learn tricks like 'sit' and 'roll over'?",
        "choices": ["dog", "snake", "mouse"],
        "answer": "dog",
    },
    {
        "question": "Which small pet stores food in its cheeks?",
        "choices": ["hamster", "turtle", "horse"],
        "answer": "hamster",
    },
    {
        "question": "Which pet has a shell to protect its body?",
        "choices": ["turtle", "cat", "guinea pig"],
        "answer": "turtle",
    },
    {
        "question": "Which animal neighs and has a mane?",
        "choices": ["horse", "snake", "bird"],
        "answer": "horse",
    },
    {
        "question": "Which animal can repeat words it hears?",
        "choices": ["parrot", "rabbit", "dog"],
        "answer": "parrot",
    },
]

SPELLING_WORDS: list[str] = [
    "dog",
    "cat",
    "rabbit",
    "guinea pig",
    "hamster",
    "turtle",
    "snake",
    "parrot",
    "horse",
    "goldfish",
]


def show_pets_lesson() -> None:
    """Display the lesson about pet vocabulary and expressions."""

    lesson = dedent(
        f"""
        {CYAN}{BOLD}🐾 Pets and animals - Lesson{RESET}

        {BOLD}Vocabulary focus{RESET}
        • a dog /dɒg/ → loves to run and play fetch.
        • a cat /kæt/ → purrs, likes to nap in the sun.
        • a rabbit /ˈræb.ɪt/ → has long ears and hops.
        • a fish /fɪʃ/ → swims with fins in water.
        • a bird /bɜːd/ → has wings and can fly or sing.
        • a turtle /ˈtɜː.təl/ → carries its house, a shell.
        • a hamster /ˈhæm.stər/ → tiny pet that stores food in its cheeks.
        • a guinea pig /ˈɡɪn.i pɪɡ/ → gentle rodent that squeaks.
        • a horse /hɔːs/ → large pet or farm animal you can ride.
        • a snake /sneɪk/ → long body, moves by slithering.

        {BOLD}Useful sentences{RESET}
        • This is my pet dog. His name is Max.
        • I feed my rabbit every morning.
        • The goldfish swims in its bowl.
        • My favourite animal is the turtle because it is calm.

        {BOLD}Pronunciation tip{RESET}
        Clap once for every syllable when you say the word:
        rab-bit (2 claps), tur-tle (2 claps), guin-ea pig (3 claps).

        When you are ready, press {BOLD}q{RESET} to start the quiz.
        """
    )
    show_lesson(lesson)


def animals_quiz(num_questions: int = 5) -> tuple[int, int]:
    """Run a multiple-choice quiz about pets."""

    print(f"{BOLD}🧐 Quiz time: choose the correct answer.{RESET}")
    questions = random.sample(QUIZ_QUESTIONS, k=min(num_questions, len(QUIZ_QUESTIONS)))
    score = 0
    for index, question in enumerate(questions, start=1):
        prompt = question["question"]
        choices: list[str] = list(question["choices"])  # type: ignore[index]
        answer: str = question["answer"]  # type: ignore[assignment]
        print(f"\nQuestion {index}: {prompt}")
        random.shuffle(choices)
        for number, choice in enumerate(choices, start=1):
            print(f"  {number}. {choice}")
        reply = input("Your answer (number): ").strip()
        try:
            choice_index = int(reply) - 1
            selected = choices[choice_index]
        except (ValueError, IndexError):
            selected = ""
        if selected == answer:
            print(f"{GREEN}Great! {answer.title()} is correct.{RESET}")
            score += 1
        else:
            print(f"{RED}Not quite. The correct answer was {answer}.{RESET}")
    total = len(questions)
    print(f"\nYou scored {score}/{total} on the quiz.\n")
    return score, total


def spelling_practice(words: list[str] | None = None) -> tuple[int, int]:
    """Ask learners to spell pet vocabulary words."""

    if words is None:
        words = SPELLING_WORDS
    print(f"{BOLD}🔤 Spelling bee: spell each animal correctly.{RESET}")
    score = 0
    for word in words:
        answer = input(
            "Spell this animal (use letters with hyphens or spaces, e.g. c-a-t): "
            f"{word}: "
        ).strip().lower()
        normalized = answer.replace(" ", "").replace("-", "")
        expected = word.replace(" ", "")
        if normalized == expected:
            print(f"{GREEN}Excellent! {word} is spelled correctly.{RESET}")
            score += 1
        else:
            spelled = "-".join(list(word.replace(" ", "")))
            print(f"{RED}Check again. {word} spells {spelled}.{RESET}")
    total = len(words)
    print(f"\nSpelling score: {score}/{total}.\n")
    return score, total


def translation_flashcards() -> None:
    """Offer a quick translation exercise without scoring."""

    print(f"{BOLD}📚 Bonus: translate these pets from French to English.{RESET}")
    sample = random.sample(PETS_TRANSLATIONS, k=min(5, len(PETS_TRANSLATIONS)))
    for french, english in sample:
        reply = input(f"Comment dit-on « {french} » en anglais ? ").strip().lower()

        acceptable = {english}
        if french == "tortue":
            acceptable.add("tortoise")

        if reply in acceptable:
            print(f"{GREEN}Yes, « {french} » is {english}.{RESET}")
        else:
            alternatives = ", ".join(sorted(acceptable))
            print(f"{RED}The correct word is {alternatives}.{RESET}")
    print()


def main() -> None:
    """Launch the pets lesson, quiz and spelling practice."""

    show_pets_lesson()
    quiz_score, quiz_total = animals_quiz()
    spell_score, spell_total = spelling_practice()
    translation_flashcards()

    total_questions = quiz_total + spell_total
    total_score = quiz_score + spell_score
    final_percentage = (total_score / total_questions * 100) if total_questions else None

    print(f"{CYAN}{BOLD}Summary{RESET}")
    print(f"Quiz: {quiz_score}/{quiz_total}")
    print(f"Spelling: {spell_score}/{spell_total}")
    print("Keep practising your favourite pet words every day!\n")

    log_result("anglais_pets_animals", final_percentage)


if __name__ == "__main__":
    main()
