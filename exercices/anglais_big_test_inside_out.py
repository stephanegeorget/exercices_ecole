"""Comprehensive Inside Out themed English test."""

from __future__ import annotations

import random

from .utils import show_lesson
from .logger import log_result

DISPLAY_NAME = "English : Big test - Inside Out"

BOLD = "\033[1m"
RESET = "\033[0m"


LESSON = f"""{BOLD}Inside Out – Feelings, colours and introductions{RESET}

🎯 {BOLD}Objectives{RESET}
• Review mood vocabulary (happy, sad, angry, scared, disgusted, calm, excited, worried).
• Name emotions and link them to Riley Andersen from {BOLD}Inside Out{RESET}.
• Practise colours used by each emotion character.
• Use personal subject pronouns (I, you, he, she, we, they).
• Conjugate the verb {BOLD}"to be"{RESET} in the simple present.
• Present yourself (name, age, nationality, hometown) and ask about feelings.

🧠 {BOLD}Key reminders{RESET}
• Personal pronouns: {BOLD}I{RESET}, you, he, she, it, we, they.
• "To be" in the present: {BOLD}I am{RESET}, you are, he/she/it is, we are, they are.
• Useful introductions: "My name is…", "I am … years old", "I am from…", "I am … (nationality)."
• Asking about feelings: "How are you?", "How are you feeling today?"
• Describing moods: "I am happy", "She feels angry", "They are calm".
• Riley's core emotion team:
  – Joy: yellow, cheerful / joyful.
  – Sadness: blue, gloomy / sad.
  – Anger: red, furious / angry.
  – Fear: purple, nervous / scared.
  – Disgust: green, annoyed / disgusted.

✍️ {BOLD}Mission{RESET}
Be ready to introduce yourself, share how you feel, ask about someone else's mood, and describe Riley Andersen's emotions with their colours and feelings.
"""


QUESTIONS = [
    {
        "prompt": "Choose the correct personal subject pronoun for yourself.\nChoisis le pronom personnel sujet correct pour toi-même.",
        "options": ["He", "I", "They"],
        "answer": 1,
    },
    {
        "prompt": "Select the correct form: '___ am 12 years old.'\nSélectionne la forme correcte : « ___ am 12 years old. »",
        "options": ["I", "He", "They"],
        "answer": 0,
    },
    {
        "prompt": "Which sentence correctly introduces name and age?\nQuelle phrase présente correctement le nom et l'âge ?",
        "options": [
            "My name is Emma and I am 11 years old.",
            "I is Emma and am 11 old years.",
            "The name my Emma am 11 year.",
        ],
        "answer": 0,
    },
    {
        "prompt": "Pick the right way to mention nationality.\nChoisis la bonne façon d'indiquer ta nationalité.",
        "options": [
            "I am French.",
            "I are French.",
            "I be French.",
        ],
        "answer": 0,
    },
    {
        "prompt": "Choose the correct colour for Joy in Inside Out.\nChoisis la couleur correcte pour Joie dans Vice-Versa.",
        "options": ["Blue", "Yellow", "Purple"],
        "answer": 1,
    },
    {
        "prompt": "Which emotion matches Joy?\nQuelle émotion correspond à Joie ?",
        "options": ["Sad", "Joyful", "Afraid"],
        "answer": 1,
    },
    {
        "prompt": "Select the correct sentence to say where you are from.\nSélectionne la phrase correcte pour dire d'où tu viens.",
        "options": [
            "I am from Paris.",
            "I from Paris am.",
            "Am I Paris from.",
        ],
        "answer": 0,
    },
    {
        "prompt": "How do you ask someone about their feelings?\nComment demandes-tu à quelqu'un comment il se sent ?",
        "options": [
            "How are you?",
            "Who are you?",
            "Where are you?",
        ],
        "answer": 0,
    },
    {
        "prompt": "Pick the correct pronoun for Riley.\nChoisis le pronom correct pour Riley.",
        "options": ["They", "He", "She"],
        "answer": 2,
    },
    {
        "prompt": "Complete: 'She ___ from Minnesota.'\nComplète : « She ___ from Minnesota. »",
        "options": ["is", "are", "am"],
        "answer": 0,
    },
    {
        "prompt": "Identify Sadness's colour.\nIdentifie la couleur de Tristesse.",
        "options": ["Green", "Red", "Blue"],
        "answer": 2,
    },
    {
        "prompt": "Which mood belongs to Sadness?\nQuelle humeur appartient à Tristesse ?",
        "options": ["Cheerful", "Gloomy", "Angry"],
        "answer": 1,
    },
    {
        "prompt": "Choose the correct way to state age and hometown together.\nChoisis la bonne façon d'indiquer ton âge et ta ville d'origine ensemble.",
        "options": [
            "I am 11 years old and I am from Lyon.",
            "I am 11 year old I from Lyon.",
            "Am 11 years I from Lyon.",
        ],
        "answer": 0,
    },
    {
        "prompt": "Pick the right pronoun to talk about you and a friend.\nChoisis le bon pronom pour parler de toi et d'un ami.",
        "options": ["They", "We", "She"],
        "answer": 1,
    },
    {
        "prompt": "Select the correct form: 'We ___ happy to meet you.'\nSélectionne la forme correcte : « We ___ happy to meet you. »",
        "options": ["am", "is", "are"],
        "answer": 2,
    },
    {
        "prompt": "How do you answer about your mood?\nComment réponds-tu sur ton humeur ?",
        "options": [
            "I am feeling great!",
            "Feeling I great am!",
            "Am great feeling I!",
        ],
        "answer": 0,
    },
    {
        "prompt": "Choose the correct form: 'You ___ very kind.'\nChoisis la forme correcte : « You ___ very kind. »",
        "options": ["am", "is", "are"],
        "answer": 2,
    },
    {
        "prompt": "Which sentence asks politely about feelings?\nQuelle phrase demande poliment comment quelqu'un se sent ?",
        "options": [
            "How are you feeling today?",
            "How old are you?",
            "Where is your house?",
        ],
        "answer": 0,
    },
    {
        "prompt": "Identify Anger's colour.\nIdentifie la couleur de Colère.",
        "options": ["Red", "Yellow", "Green"],
        "answer": 0,
    },
    {
        "prompt": "Which mood describes Anger?\nQuelle humeur décrit Colère ?",
        "options": ["Calm", "Furious", "Excited"],
        "answer": 1,
    },
    {
        "prompt": "Pick the correct pronoun for Riley's parents together.\nChoisis le pronom correct pour parler des parents de Riley ensemble.",
        "options": ["He", "They", "It"],
        "answer": 1,
    },
    {
        "prompt": "Complete: 'They ___ from San Francisco now.'\nComplète : « They ___ from San Francisco now. »",
        "options": ["is", "are", "am"],
        "answer": 1,
    },
    {
        "prompt": "Select the proper way to share nationality and age.\nSélectionne la bonne manière d'indiquer ta nationalité et ton âge.",
        "options": [
            "I am Canadian and I am 12 years old.",
            "I Canadian am 12 years old.",
            "Am Canadian I 12 old years.",
        ],
        "answer": 0,
    },
    {
        "prompt": "How do you say you feel worried?\nComment dis-tu que tu te sens inquiet/inquiète ?",
        "options": [
            "I am worried.",
            "I worried am.",
            "I am worry.",
        ],
        "answer": 0,
    },
    {
        "prompt": "Choose the correct colour for Fear.\nChoisis la couleur correcte pour Peur.",
        "options": ["Purple", "Orange", "Yellow"],
        "answer": 0,
    },
    {
        "prompt": "Which feeling matches Fear?\nQuel sentiment correspond à Peur ?",
        "options": ["Relaxed", "Nervous", "Joyful"],
        "answer": 1,
    },
    {
        "prompt": "Complete: 'Disgust ___ green and stylish.'\nComplète : « Disgust ___ green and stylish. »",
        "options": ["are", "is", "am"],
        "answer": 1,
    },
    {
        "prompt": "Identify Disgust's main mood word.\nIdentifie le mot d'humeur principal de Dégoût.",
        "options": ["Disgusted", "Happy", "Sleepy"],
        "answer": 0,
    },
    {
        "prompt": "Which sentence correctly states your origin and nationality?\nQuelle phrase indique correctement ton origine et ta nationalité ?",
        "options": [
            "I am from Dublin and I am Irish.",
            "I from Dublin I Irish am.",
            "From Dublin Irish I am I.",
        ],
        "answer": 0,
    },
    {
        "prompt": "Pick the correct way to say you feel excited.\nChoisis la bonne façon de dire que tu te sens excité(e).",
        "options": [
            "I am excited!",
            "Excited am I!",
            "I excited am!",
        ],
        "answer": 0,
    },
    {
        "prompt": "Which pronoun replaces 'Mr. Andersen'?\nQuel pronom remplace « Mr. Andersen » ?",
        "options": ["He", "She", "They"],
        "answer": 0,
    },
    {
        "prompt": "Select the correct conjugation: 'He ___ very patient.'\nSélectionne la conjugaison correcte : « He ___ very patient. »",
        "options": ["are", "am", "is"],
        "answer": 2,
    },
    {
        "prompt": "Identify the sentence asking for your name.\nIdentifie la phrase qui demande ton nom.",
        "options": [
            "What is your name?",
            "Where do you live?",
            "How are you feeling?",
        ],
        "answer": 0,
    },
    {
        "prompt": "Choose the best response to 'How are you?'\nChoisis la meilleure réponse à « How are you? »",
        "options": [
            "I am fine, thank you!",
            "I am from Canada.",
            "My favourite colour is blue.",
        ],
        "answer": 0,
    },
    {
        "prompt": "Complete: 'It ___ important to share your feelings.'\nComplète : « It ___ important to share your feelings. »",
        "options": ["am", "is", "are"],
        "answer": 1,
    },
    {
        "prompt": "Select the correct summary about Joy.\nSélectionne le résumé correct à propos de Joie.",
        "options": [
            "Joy is yellow and always cheerful.",
            "Joy are blue and sleepy.",
            "Joy am red and angry.",
        ],
        "answer": 0,
    },
    {
        "prompt": "Which statement correctly describes Sadness?\nQuelle affirmation décrit correctement Tristesse ?",
        "options": [
            "Sadness is blue and feels gloomy.",
            "Sadness are green and feels excited.",
            "Sadness am yellow and is angry.",
        ],
        "answer": 0,
    },
    {
        "prompt": "Choose the accurate description of Fear.\nChoisis la description exacte de Peur.",
        "options": [
            "Fear is purple and often nervous.",
            "Fear are red and happy.",
            "Fear am blue and calm.",
        ],
        "answer": 0,
    },
    {
        "prompt": "Pick the correct sentence about Disgust.\nChoisis la phrase correcte à propos de Dégoût.",
        "options": [
            "Disgust is green and hates gross things.",
            "Disgust are yellow and loves mud.",
            "Disgust am blue and sleepy.",
        ],
        "answer": 0,
    },
    {
        "prompt": "Select the accurate statement about Anger.\nSélectionne l'affirmation exacte à propos de Colère.",
        "options": [
            "Anger is red and gets furious quickly.",
            "Anger are green and calm.",
            "Anger am purple and shy.",
        ],
        "answer": 0,
    },
]


def run_quiz() -> float:
    """Run the quiz and return the score percentage."""

    questions = QUESTIONS.copy()
    random.shuffle(questions)
    score = 0

    for idx, question in enumerate(questions, start=1):
        print(f"\n{BOLD}Question {idx}/{len(questions)}{RESET}")
        print(question["prompt"])
        for option_index, option in enumerate(question["options"], start=1):
            print(f"  {option_index}. {option}")
        while True:
            choice = input("Your answer (number): ").strip()
            try:
                selection = int(choice) - 1
            except ValueError:
                print("Enter the number of your choice.")
                continue
            if selection < 0 or selection >= len(question["options"]):
                print("Choose a valid option number.")
                continue
            break
        if selection == question["answer"]:
            print("✅ Correct!")
            score += 1
        else:
            correct_option = question["options"][question["answer"]]
            print(f"❌ Not quite. Correct answer: {correct_option}")

    percentage = score / len(questions) * 100
    print(f"\n{BOLD}Final score: {score}/{len(questions)} ({percentage:.1f}%) {RESET}")
    return percentage


def main() -> None:
    """Display the lesson then launch the quiz."""

    show_lesson(LESSON)
    percentage = run_quiz()
    log_result("anglais_big_test_inside_out", percentage)


if __name__ == "__main__":
    main()
