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

QUESTIONS = [
    {
        "question": "1. Hier soir, le vent ___ très fort quand la fenêtre claqua.",
        "options": ["souffla", "soufflait", "soufflera"],
        "answer": 1,
        "context": "La description du vent qui dure dans le temps prend l'imparfait.",
    },
    {
        "question": "2. Tout à coup, le chat ___ sur la table et renversa le vase.",
        "options": ["saute", "sautait", "sauta"],
        "answer": 2,
        "context": "Action brève et ponctuelle → passé simple.",
    },
    {
        "question": "3. Chaque été, nous ___ chez nos cousins à la campagne.",
        "options": ["allâmes", "allions", "irons"],
        "answer": 1,
        "context": "Habitude répétée, on utilise l'imparfait.",
    },
    {
        "question": "4. Soudain, il ___ une lumière au loin.",
        "options": ["apercevait", "aperçut", "apercevra"],
        "answer": 1,
        "context": "La découverte ponctuelle est exprimée au passé simple.",
    },
    {
        "question": "5. Pendant que les enfants ___, la pluie commença à tomber.",
        "options": ["jouèrent", "jouaient", "joueront"],
        "answer": 1,
        "context": "Action en cours de déroulement : imparfait.",
    },
    {
        "question": "6. Ce matin-là, Marie ___ la porte et sortit sans bruit.",
        "options": ["fermait", "ferma", "fermerait"],
        "answer": 1,
        "context": "Action principale unique → passé simple.",
    },
    {
        "question": "7. Quand j'étais petit, je ___ des châteaux de sable pendant des heures.",
        "options": ["construisis", "construisais", "construirai"],
        "answer": 1,
        "context": "Souvenir prolongé, donc imparfait.",
    },
    {
        "question": "8. Il ___ soudain que quelqu'un frappait à la porte.",
        "options": ["sentait", "sentit", "sentira"],
        "answer": 1,
        "context": "Perception ponctuelle → passé simple.",
    },
    {
        "question": "9. Le soleil ___ derrière les collines tandis que nous rentrions.",
        "options": ["disparaissait", "disparut", "disparaîtra"],
        "answer": 0,
        "context": "Décor en arrière-plan → imparfait.",
    },
    {
        "question": "10. À ce moment précis, elle ___ son sac et partit.",
        "options": ["prit", "prenait", "prendra"],
        "answer": 0,
        "context": "Action qui fait avancer l'histoire, donc passé simple.",
    },
    {
        "question": "11. Les oiseaux ___ doucement pendant que l'aube se levait.",
        "options": ["chantèrent", "chantaient", "chanteront"],
        "answer": 1,
        "context": "Description d'arrière-plan → imparfait.",
    },
    {
        "question": "12. Tout à coup, la terre ___ et la foule paniqua.",
        "options": ["trembla", "tremblait", "tremblera"],
        "answer": 0,
        "context": "Événement unique : passé simple.",
    },
    {
        "question": "13. Chaque dimanche, ils ___ leurs grands-parents.",
        "options": ["visitaient", "visitèrent", "visiteront"],
        "answer": 0,
        "context": "Habitude régulière → imparfait.",
    },
    {
        "question": "14. Il ___ puis referma la lettre avec soin.",
        "options": ["lut", "lisait", "lira"],
        "answer": 0,
        "context": "Action ponctuelle principale → passé simple.",
    },
    {
        "question": "15. Dans le jardin, les fleurs ___ et embaumaient l'air.",
        "options": ["s'ouvriraient", "s'ouvrirent", "s'ouvraient"],
        "answer": 2,
        "context": "Description du décor → imparfait.",
    },
    {
        "question": "16. Quand la cloche ___, les élèves se levèrent d'un bond.",
        "options": ["sonna", "sonnait", "sonnerait"],
        "answer": 0,
        "context": "Signal ponctuel → passé simple.",
    },
    {
        "question": "17. La vieille pendule ___ toujours la même chanson.",
        "options": ["jouait", "joua", "jouera"],
        "answer": 0,
        "context": "Habitude durable → imparfait.",
    },
    {
        "question": "18. Ce jour-là, nous ___ la vérité sur leur voyage.",
        "options": ["apprenions", "apprîmes", "apprendrons"],
        "answer": 1,
        "context": "Révélation unique → passé simple.",
    },
    {
        "question": "19. Les vagues ___ sans relâche contre les rochers.",
        "options": ["se brisèrent", "se brisaient", "se briseront"],
        "answer": 1,
        "context": "Action longue et répétée → imparfait.",
    },
    {
        "question": "20. Après un long silence, il ___ enfin quelques mots.",
        "options": ["prononçait", "prononça", "prononcera"],
        "answer": 1,
        "context": "Action brève qui survient soudainement → passé simple.",
    },
    {
        "question": "21. Quand nous étions en classe de neige, il ___ presque tous les jours.",
        "options": ["neigea", "neigeait", "neigera"],
        "answer": 1,
        "context": "Fréquence répétée → imparfait.",
    },
    {
        "question": "22. À l'annonce du résultat, elle ___ de joie.",
        "options": ["sauta", "sautait", "saute"],
        "answer": 0,
        "context": "Réaction unique → passé simple.",
    },
    {
        "question": "23. Dans la forêt, les feuilles ___ sous nos pas.",
        "options": ["craquaient", "craquèrent", "craqueront"],
        "answer": 0,
        "context": "Décor sonore continu → imparfait.",
    },
    {
        "question": "24. Nous ___ la porte et découvrîmes une salle éclairée.",
        "options": ["ouvrions", "ouvrîmes", "ouvrirons"],
        "answer": 1,
        "context": "Action principale unique → passé simple.",
    },
    {
        "question": "25. Tous les soirs, il ___ une histoire à sa petite sœur.",
        "options": ["racontait", "raconta", "racontera"],
        "answer": 0,
        "context": "Habitude quotidienne → imparfait.",
    },
    {
        "question": "26. À minuit, l'horloge ___ douze coups retentissants.",
        "options": ["donnait", "donna", "donnera"],
        "answer": 1,
        "context": "Moment précis ponctuel → passé simple.",
    },
    {
        "question": "27. Les invités ___ encore la salle quand la musique démarra.",
        "options": ["occupaient", "occupèrent", "occuperont"],
        "answer": 0,
        "context": "Action en cours pendant un autre événement → imparfait.",
    },
    {
        "question": "28. Ce soir-là, nous ___ plus tard que prévu.",
        "options": ["rentions", "rentrâmes", "rentrions"],
        "answer": 1,
        "context": "Résultat ponctuel du récit → passé simple.",
    },
    {
        "question": "29. Les bougies ___ lentement tandis que le conteur parlait.",
        "options": ["se consumèrent", "se consumaient", "se consumeront"],
        "answer": 1,
        "context": "Description continue → imparfait.",
    },
    {
        "question": "30. Lorsque le tonnerre ___, tout le monde se tut.",
        "options": ["gronda", "grondait", "grondât"],
        "answer": 0,
        "context": "Événement soudain → passé simple.",
    },
]


LETTERS = ["a", "b", "c", "d"]


def main() -> None:
    """Affiche la leçon puis propose un quiz de 30 questions."""

    show_lesson(LESSON)
    print("Quiz : tape la lettre de la bonne réponse (a, b, c…).")
    score = 0
    for index, item in enumerate(QUESTIONS, start=1):
        question = item["question"]
        options = item["options"]
        answer = item["answer"]
        letters = LETTERS[: len(options)]
        print(f"\nQuestion {index} : {question}")
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

    total = len(QUESTIONS)
    percentage = score / total * 100
    print(f"\nScore final : {score}/{total} ({percentage:.1f} %)")
    if percentage == 100:
        print("Bravo ! Tu maîtrises parfaitement l'imparfait et le passé simple. 🌟")
    elif percentage >= 70:
        print("Très beau résultat, continue comme ça ! 💪")
    else:
        print("Courage, relis la leçon et recommence : tu progresseras vite ! 📖")

    log_result("francais_imparfait_passe_simple", percentage)


if __name__ == "__main__":
    main()
