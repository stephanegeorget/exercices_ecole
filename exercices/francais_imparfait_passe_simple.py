from __future__ import annotations

"""Leçon et quiz sur l'imparfait et le passé simple."""

DISPLAY_NAME = "Français : Imparfait ou passé simple ?"

from .logger import log_result
from .utils import show_lesson

LESSON = """
📚 **L'imparfait et le passé simple : deux temps du récit**

Dans un récit au passé, on rencontre très souvent **l'imparfait** et le **passé simple**.
Ils ne racontent pas la même chose :

- L'**imparfait** décrit un décor, une habitude, une action qui dure ou se répète.
  On peut souvent le remplacer par « pendant que », « tous les… », « habituellement ».
  Exemple : « Le vent soufflait et la pluie tombait. »
- Le **passé simple** exprime une action ponctuelle et achevée, un événement qui fait
  avancer l'histoire. On peut souvent le remplacer par « soudain », « alors », « tout à coup ».
  Exemple : « Soudain, la porte s'ouvrit. »

🎯 **Astuces pour choisir le bon temps**

1. Observe si l'action est en arrière-plan (imparfait) ou au premier plan (passé simple).
2. Demande-toi si elle dure dans le temps ou si elle est brève et unique.
3. Regarde les marqueurs temporels : « chaque matin », « souvent » → imparfait ;
   « ce jour-là », « puis », « tout à coup » → passé simple.
4. Dans un même paragraphe, l'imparfait installe le décor et le passé simple raconte les actions principales.

✍️ **Conjugaison rapide**

- Imparfait : radical de la 1re personne du pluriel au présent + terminaison (-ais, -ais,
  -ait, -ions, -iez, -aient).
  > nous chantons → je chantais, nous chantions
- Passé simple des verbes du 1er groupe (-er) : -ai, -as, -a, -âmes, -âtes, -èrent.
  > il marcha, nous parlâmes
- Passé simple du 2e groupe (-ir) : -is, -is, -it, -îmes, -îtes, -irent.
  > ils finirent
- Passé simple des verbes du 3e groupe varie davantage : « je pris », « nous vînmes »,
  « ils purent ». Il faut les apprendre progressivement.

Prêt·e ? Lis chaque phrase, choisis le temps qui convient et vérifie ton intuition !
"""

TENSE_INFO = {
    "imparfait": ("i", "imparfait"),
    "passé simple": ("p", "passé simple"),
    "autre": (
        "a",
        "autre temps (présent, futur, conditionnel, subjonctif, etc.)",
    ),
}


def _normalise_tense_answer(raw: str) -> str:
    """Normalise la saisie de l'élève en renvoyant la clé de temps attendue."""

    answer = raw.strip().lower()
    for key, (short, label) in TENSE_INFO.items():
        if answer in {key, short, label.lower()}:
            return key
    return ""


QUESTIONS = [
    {
        "question": "1. Hier soir, le vent ___ très fort quand la fenêtre claqua.",
        "options": ["souffla", "soufflait", "soufflera"],
        "tenses": ["passé simple", "imparfait", "autre"],
        "answer": 1,
        "context": "La description du vent qui dure dans le temps prend l'imparfait.",
    },
    {
        "question": "2. Tout à coup, le chat ___ sur la table et renversa le vase.",
        "options": ["saute", "sautait", "sauta"],
        "tenses": ["autre", "imparfait", "passé simple"],
        "answer": 2,
        "context": "Action brève et ponctuelle → passé simple.",
    },
    {
        "question": "3. Chaque été, nous ___ chez nos cousins à la campagne.",
        "options": ["allâmes", "allions", "irons"],
        "tenses": ["passé simple", "imparfait", "autre"],
        "answer": 1,
        "context": "Habitude répétée, on utilise l'imparfait.",
    },
    {
        "question": "4. Soudain, il ___ une lumière au loin.",
        "options": ["apercevait", "aperçut", "apercevra"],
        "tenses": ["imparfait", "passé simple", "autre"],
        "answer": 1,
        "context": "La découverte ponctuelle est exprimée au passé simple.",
    },
    {
        "question": "5. Pendant que les enfants ___, la pluie commença à tomber.",
        "options": ["jouèrent", "jouaient", "joueront"],
        "tenses": ["passé simple", "imparfait", "autre"],
        "answer": 1,
        "context": "Action en cours de déroulement : imparfait.",
    },
    {
        "question": "6. Ce matin-là, Marie ___ la porte et sortit sans bruit.",
        "options": ["fermait", "ferma", "fermerait"],
        "tenses": ["imparfait", "passé simple", "autre"],
        "answer": 1,
        "context": "Action principale unique → passé simple.",
    },
    {
        "question": "7. Quand j'étais petit, je ___ des châteaux de sable pendant des heures.",
        "options": ["construisis", "construisais", "construirai"],
        "tenses": ["passé simple", "imparfait", "autre"],
        "answer": 1,
        "context": "Souvenir prolongé, donc imparfait.",
    },
    {
        "question": "8. Il ___ soudain que quelqu'un frappait à la porte.",
        "options": ["sentait", "sentit", "sentira"],
        "tenses": ["imparfait", "passé simple", "autre"],
        "answer": 1,
        "context": "Perception ponctuelle → passé simple.",
    },
    {
        "question": "9. Le soleil ___ derrière les collines tandis que nous rentrions.",
        "options": ["disparaissait", "disparut", "disparaîtra"],
        "tenses": ["imparfait", "passé simple", "autre"],
        "answer": 0,
        "context": "Décor en arrière-plan → imparfait.",
    },
    {
        "question": "10. À ce moment précis, elle ___ son sac et partit.",
        "options": ["prit", "prenait", "prendra"],
        "tenses": ["passé simple", "imparfait", "autre"],
        "answer": 0,
        "context": "Action qui fait avancer l'histoire, donc passé simple.",
    },
    {
        "question": "11. Les oiseaux ___ doucement pendant que l'aube se levait.",
        "options": ["chantèrent", "chantaient", "chanteront"],
        "tenses": ["passé simple", "imparfait", "autre"],
        "answer": 1,
        "context": "Description d'arrière-plan → imparfait.",
    },
    {
        "question": "12. Tout à coup, la terre ___ et la foule paniqua.",
        "options": ["trembla", "tremblait", "tremblera"],
        "tenses": ["passé simple", "imparfait", "autre"],
        "answer": 0,
        "context": "Événement unique : passé simple.",
    },
    {
        "question": "13. Chaque dimanche, ils ___ leurs grands-parents.",
        "options": ["visitaient", "visitèrent", "visiteront"],
        "tenses": ["imparfait", "passé simple", "autre"],
        "answer": 0,
        "context": "Habitude régulière → imparfait.",
    },
    {
        "question": "14. Il ___ puis referma la lettre avec soin.",
        "options": ["lut", "lisait", "lira"],
        "tenses": ["passé simple", "imparfait", "autre"],
        "answer": 0,
        "context": "Action ponctuelle principale → passé simple.",
    },
    {
        "question": "15. Dans le jardin, les fleurs ___ et embaumaient l'air.",
        "options": ["s'ouvriraient", "s'ouvrirent", "s'ouvraient"],
        "tenses": ["autre", "passé simple", "imparfait"],
        "answer": 2,
        "context": "Description du décor → imparfait.",
    },
    {
        "question": "16. Quand la cloche ___, les élèves se levèrent d'un bond.",
        "options": ["sonna", "sonnait", "sonnerait"],
        "tenses": ["passé simple", "imparfait", "autre"],
        "answer": 0,
        "context": "Signal ponctuel → passé simple.",
    },
    {
        "question": "17. La vieille pendule ___ toujours la même chanson.",
        "options": ["jouait", "joua", "jouera"],
        "tenses": ["imparfait", "passé simple", "autre"],
        "answer": 0,
        "context": "Habitude durable → imparfait.",
    },
    {
        "question": "18. Ce jour-là, nous ___ la vérité sur leur voyage.",
        "options": ["apprenions", "apprîmes", "apprendrons"],
        "tenses": ["imparfait", "passé simple", "autre"],
        "answer": 1,
        "context": "Révélation unique → passé simple.",
    },
    {
        "question": "19. Les vagues ___ sans relâche contre les rochers.",
        "options": ["se brisèrent", "se brisaient", "se briseront"],
        "tenses": ["passé simple", "imparfait", "autre"],
        "answer": 1,
        "context": "Action longue et répétée → imparfait.",
    },
    {
        "question": "20. Après un long silence, il ___ enfin quelques mots.",
        "options": ["prononçait", "prononça", "prononcera"],
        "tenses": ["imparfait", "passé simple", "autre"],
        "answer": 1,
        "context": "Action brève qui survient soudainement → passé simple.",
    },
    {
        "question": "21. Quand nous étions en classe de neige, il ___ presque tous les jours.",
        "options": ["neigea", "neigeait", "neigera"],
        "tenses": ["passé simple", "imparfait", "autre"],
        "answer": 1,
        "context": "Fréquence répétée → imparfait.",
    },
    {
        "question": "22. À l'annonce du résultat, elle ___ de joie.",
        "options": ["sauta", "sautait", "saute"],
        "tenses": ["passé simple", "imparfait", "autre"],
        "answer": 0,
        "context": "Réaction unique → passé simple.",
    },
    {
        "question": "23. Dans la forêt, les feuilles ___ sous nos pas.",
        "options": ["craquaient", "craquèrent", "craqueront"],
        "tenses": ["imparfait", "passé simple", "autre"],
        "answer": 0,
        "context": "Décor sonore continu → imparfait.",
    },
    {
        "question": "24. Nous ___ la porte et découvrîmes une salle éclairée.",
        "options": ["ouvrions", "ouvrîmes", "ouvrirons"],
        "tenses": ["imparfait", "passé simple", "autre"],
        "answer": 1,
        "context": "Action principale unique → passé simple.",
    },
    {
        "question": "25. Tous les soirs, il ___ une histoire à sa petite sœur.",
        "options": ["racontait", "raconta", "racontera"],
        "tenses": ["imparfait", "passé simple", "autre"],
        "answer": 0,
        "context": "Habitude quotidienne → imparfait.",
    },
    {
        "question": "26. À minuit, l'horloge ___ douze coups retentissants.",
        "options": ["donnait", "donna", "donnera"],
        "tenses": ["imparfait", "passé simple", "autre"],
        "answer": 1,
        "context": "Moment précis ponctuel → passé simple.",
    },
    {
        "question": "27. Les invités ___ encore la salle quand la musique démarra.",
        "options": ["occupaient", "occupèrent", "occuperont"],
        "tenses": ["imparfait", "passé simple", "autre"],
        "answer": 0,
        "context": "Action en cours pendant un autre événement → imparfait.",
    },
    {
        "question": "28. Ce soir-là, nous ___ plus tard que prévu.",
        "options": ["rentrâmes", "rentrions", "rentrerons"],
        "tenses": ["passé simple", "imparfait", "autre"],
        "answer": 0,
        "context": "Résultat ponctuel du récit → passé simple.",
    },
    {
        "question": "29. Les bougies ___ lentement tandis que le conteur parlait.",
        "options": ["se consumèrent", "se consumaient", "se consumeront"],
        "tenses": ["passé simple", "imparfait", "autre"],
        "answer": 1,
        "context": "Description continue → imparfait.",
    },
    {
        "question": "30. Lorsque le tonnerre ___, tout le monde se tut.",
        "options": ["gronda", "grondait", "grondât"],
        "tenses": ["passé simple", "imparfait", "autre"],
        "answer": 0,
        "context": "Événement soudain → passé simple.",
    },
]


LETTERS = ["a", "b", "c", "d"]


def main() -> None:
    """Affiche la leçon puis propose un quiz de 30 questions."""

    show_lesson(LESSON)
    print(
        "Quiz : identifie d'abord le temps de chaque verbe (i, p, a),"
        " puis choisis la bonne réponse (a, b, c…)."
    )
    score = 0
    for index, item in enumerate(QUESTIONS, start=1):
        question = item["question"]
        options = item["options"]
        tenses = item["tenses"]
        answer = item["answer"]
        letters = LETTERS[: len(options)]
        print(f"\nQuestion {index} : {question}")
        for letter, option in zip(letters, options):
            print(f"  {letter}. {option}")

        remaining_tenses = ["imparfait", "passé simple", "autre"]
        for opt_index, option in enumerate(options):
            expected_tense = tenses[opt_index]
            expected_key, expected_label = TENSE_INFO[expected_tense]
            print(f"\n🔍 Quel est le temps du verbe {letters[opt_index]}. {option} ?")
            print("Choix possibles :")
            for tense_name in remaining_tenses:
                short, label = TENSE_INFO[tense_name]
                print(f"  {short}. {label}")
            raw_choice = input("Votre choix : ")
            student_choice = _normalise_tense_answer(raw_choice)
            if student_choice == expected_tense:
                print("Exact, tu as identifié le bon temps ! ✅")
                score += 1
            else:
                print(
                    f"Non, {option} est au {expected_label}. ({expected_key}) ❌"
                )
            if expected_tense in remaining_tenses:
                remaining_tenses.remove(expected_tense)

        print("\nMaintenant, choisis le verbe qui complète la phrase :")
        for letter, option in zip(letters, options):
            print(f"  {letter}. {option}")
        student = input("Votre réponse : ").strip().lower()
        chosen = letters.index(student) if student in letters else -1
        correct_letter = letters[answer]
        correct_text = options[answer]
        if chosen == answer:
            print("Exact ! ✅")
            score += 1
        else:
            print(f"Non, la bonne réponse était {correct_letter}. {correct_text} ❌")
            explanation = item.get("context")
            if explanation:
                print(f"ℹ️ {explanation}")

    total = len(QUESTIONS) * 4
    percentage = score / total * 100
    print(f"\nScore final : {score}/{total} ({percentage:.1f} %)")
    if percentage == 100:
        print("Bravo ! Tu maîtrises parfaitement l'imparfait et le passé simple. 🌟")
    elif percentage >= 70:
        print("Très beau résultat, continue comme ça ! 💪")
    else:
        print(
            "Courage, relis la leçon et recommence : tu progresseras vite ! 📖"
        )

    log_result("francais_imparfait_passe_simple", percentage)


if __name__ == "__main__":
    main()
