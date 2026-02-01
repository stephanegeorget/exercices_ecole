from __future__ import annotations

"""Leçon et quiz sur le présent de l'impératif."""

DISPLAY_NAME = "Français : Présent de l'impératif"

from .logger import log_result
from .utils import show_lesson

LESSON = """
📚 **Le présent de l'impératif : donner un ordre, un conseil ou une consigne**

Le **présent de l'impératif** sert à **donner une instruction**, **un conseil**,
**un encouragement** ou **une interdiction**. Il se conjugue **sans sujet** et
seulement à **trois personnes** :

- **tu** (2ᵉ personne du singulier)
- **nous** (1ʳᵉ personne du pluriel)
- **vous** (2ᵉ personne du pluriel)

🧠 **Règles importantes**

- Les verbes du 1er groupe en **-er** perdent le **-s** à "tu" :
  > Regarde !, Marche !
- Mais on garde le **-s** devant **y** ou **en** :
  > Vas-y !, Manges-en !
- À la forme négative : **ne ... pas** encadre le verbe.
  > Ne crie pas !, Ne vous levez pas !

🎯 **Valeurs fréquentes de l'impératif**

- **Ordre** : Éteins la lumière !
- **Conseil** : Sois prudent.
- **Encouragement** : Allons, continue !
- **Interdiction** : Ne traverse pas la rue.

Prêt·e ? Réponds aux questions en t'inspirant des exemples.
"""

EXERCISES = [
    {
        "title": "Exercice 1",
        "instruction": (
            "Les verbes entre guillemets sont-ils conjugués à la 2ᵉ personne du "
            "singulier (tu) ou à la 2ᵉ personne du pluriel (vous) ?"
        ),
        "questions": [
            {
                "prompt": "1. « Mon cœur, mon cœur ne \"t'emballe\" pas. » (tu/vous)",
                "answers": ["tu"],
                "explanation": "« Ne t'emballe pas » est à la 2ᵉ personne du singulier.",
            },
            {
                "prompt": "2. « \"Fais\" comme si tu ne savais pas. » (tu/vous)",
                "answers": ["tu"],
                "explanation": "« Fais » est conjugué à tu.",
            },
            {
                "prompt": "3. « Mon cœur \"arrête\" de répéter... » (tu/vous)",
                "answers": ["tu"],
                "explanation": "« Arrête » est à la 2ᵉ personne du singulier.",
            },
            {
                "prompt": "4. « \"Souviens\"-toi qu'elle t'a déchiré. » (tu/vous)",
                "answers": ["tu"],
                "explanation": "« Souviens-toi » est conjugué avec tu.",
            },
            {
                "prompt": "5. « Mes amis ne me \"laissez\" pas. » (tu/vous)",
                "answers": ["vous"],
                "explanation": "« Laissez » est à la 2ᵉ personne du pluriel.",
            },
            {
                "prompt": "6. « \"Dites\"-moi, dites-moi qu'il ne faut pas... » (tu/vous)",
                "answers": ["vous"],
                "explanation": "« Dites » est conjugué à vous.",
            },
        ],
    },
    {
        "title": "Exercice 2",
        "instruction": (
            "Relève les verbes à l'impératif puis indique la personne (tu, nous, vous)."
        ),
        "questions": [
            {
                "prompt": "1. « Voyons, comment faire un carrosse ? » (tu/nous/vous)",
                "answers": ["nous"],
                "explanation": "« Voyons » est à la 1ʳᵉ personne du pluriel.",
            },
            {
                "prompt": "2. « Cendrillon, cours au jardin, et apporte-moi... » (tu/nous/vous)",
                "answers": ["tu"],
                "explanation": "« Cours » et « apporte » sont conjugués avec tu.",
            },
            {
                "prompt": "3. « Sois changé en carrosse doré. » (tu/nous/vous)",
                "answers": ["tu"],
                "explanation": "« Sois » est à la 2ᵉ personne du singulier.",
            },
            {
                "prompt": "4. « Métamorphosons-le ! » (tu/nous/vous)",
                "answers": ["nous"],
                "explanation": "« Métamorphosons » est à la 1ʳᵉ personne du pluriel.",
            },
            {
                "prompt": "5. « Vas-y et ne traîne pas ! » (tu/nous/vous)",
                "answers": ["tu"],
                "explanation": "« Vas-y » et « ne traîne pas » sont à tu.",
            },
            {
                "prompt": "6. « Deviens cocher ! » (tu/nous/vous)",
                "answers": ["tu"],
                "explanation": "« Deviens » est conjugué à tu.",
            },
            {
                "prompt": "7. « Cendrillon, trouve six lézards..., amène-les-moi. » (tu/nous/vous)",
                "answers": ["tu"],
                "explanation": "« Trouve » et « amène-les » sont à tu.",
            },
        ],
    },
    {
        "title": "Exercice 3",
        "instruction": "Relève les verbes au présent de l'impératif.",
        "questions": [
            {
                "prompt": (
                    "1. « Tu deviendras un jour papillon..., sois donc fier de toi ! »"
                ),
                "answers": ["sois"],
                "explanation": "Le verbe à l'impératif est « sois ».",
            },
            {
                "prompt": (
                    "2. « Dracula..., Mords et nourris-toi du sang de tes victimes ! »"
                ),
                "answers": ["mords et nourris-toi", "mords, nourris-toi", "mords nourris-toi"],
                "explanation": "On trouve « mords » et « nourris-toi ».",
            },
            {
                "prompt": "3. « Rends cette casquette..., et mets-toi en rang ! »",
                "answers": ["rends et mets-toi", "rends, mets-toi", "rends mets-toi"],
                "explanation": "Les verbes à l'impératif : « rends » et « mets-toi ».",
            },
            {
                "prompt": "4. « Battons en retraite ! »",
                "answers": ["battons"],
                "explanation": "Le verbe à l'impératif est « battons ».",
            },
            {
                "prompt": (
                    "5. « Tu es espionné..., N'aie pas peur : une haie sépare... »"
                ),
                "answers": ["n'aie pas peur", "n'aie pas peur:"],
                "explanation": "Le verbe à l'impératif est « n'aie pas peur ».",
            },
            {
                "prompt": (
                    "6. « Allons, fais un effort : cultive-toi et lis ! »"
                ),
                "answers": [
                    "allons, fais, cultive-toi et lis",
                    "allons fais cultive-toi et lis",
                    "allons, fais, cultive-toi, lis",
                ],
                "explanation": "Les verbes : « allons », « fais », « cultive-toi », « lis ».",
            },
            {
                "prompt": (
                    "7. « Tu as arraché..., palefrenier ! Crains la colère de son maître ! »"
                ),
                "answers": ["crains"],
                "explanation": "Le verbe à l'impératif est « crains ».",
            },
        ],
    },
    {
        "title": "Exercice 4",
        "instruction": "Indiquez la valeur des verbes à l'impératif.",
        "questions": [
            {
                "prompt": "1. Éteins la lumière ; je voudrais dormir.",
                "answers": ["ordre"],
                "explanation": "On donne un ordre.",
            },
            {
                "prompt": "2. Faites attention ; une sorcière habite dans cette forêt.",
                "answers": ["conseil", "avertissement"],
                "explanation": "On donne un conseil/avertissement.",
            },
            {
                "prompt": "3. N'envoie pas cette lettre : je ne l'ai pas encore signée.",
                "answers": ["interdiction", "defense", "défense"],
                "explanation": "Forme négative = interdiction.",
            },
            {
                "prompt": "4. Emmène Médor chez le vétérinaire.",
                "answers": ["ordre", "consigne"],
                "explanation": "On donne une consigne/ordre.",
            },
            {
                "prompt": (
                    "5. Ne traverse la rue que lorsque le petit bonhomme est vert."
                ),
                "answers": ["consigne", "interdiction", "regle", "règle"],
                "explanation": "C'est une règle de sécurité (consigne).",
            },
            {
                "prompt": "6. Viens t'asseoir à côté de moi.",
                "answers": ["invitation", "ordre"],
                "explanation": "On invite quelqu'un à s'asseoir.",
            },
            {
                "prompt": "7. Taisez-vous !",
                "answers": ["ordre", "interdiction"],
                "explanation": "On donne un ordre direct.",
            },
            {
                "prompt": "8. Jouons ensemble.",
                "answers": ["invitation", "proposition", "encouragement"],
                "explanation": "On propose de jouer ensemble.",
            },
        ],
    },
]


def _normalise_answer(answer: str) -> str:
    return answer.strip().lower().replace("’", "'")


def _run_quiz(questions: list[dict[str, object]]) -> None:
    score = 0
    total = len(questions)
    for index, question in enumerate(questions, start=1):
        print(f"\nQuestion {index}")
        print(question["prompt"])
        answer = _normalise_answer(input("Ta réponse : "))
        valid = {_normalise_answer(item) for item in question["answers"]}
        if answer in valid:
            print("✅ Bravo !")
            score += 1
        else:
            print("❌ Pas tout à fait.")
            print(f"✅ Réponse attendue : {question['answers'][0]}")
            print(f"ℹ️ {question['explanation']}")

    print(f"\nScore final : {score}/{total}")
    percentage = score / total * 100 if total else 0.0
    log_result("francais_present_imperatif", percentage)


def _display_exercise_menu() -> str:
    print("\nChoisis un exercice :")
    for index, exercise in enumerate(EXERCISES, start=1):
        print(f"{index}. {exercise['title']}")
    print("0. Retour")
    return input("Ton choix : ")


def main() -> None:
    """Affiche la leçon puis lance les exercices sur l'impératif."""

    show_lesson(LESSON)
    print("Réponds en toutes lettres (ex. tu, nous, vous, ordre, conseil...).")

    while True:
        choice = _display_exercise_menu()
        if choice == "0":
            break

        try:
            exercise_index = int(choice) - 1
            exercise = EXERCISES[exercise_index]
        except (ValueError, IndexError):
            print("Choix invalide.")
            continue

        print(f"\n=== {exercise['title']} ===")
        print(exercise["instruction"])
        _run_quiz(exercise["questions"])


if __name__ == "__main__":
    main()
