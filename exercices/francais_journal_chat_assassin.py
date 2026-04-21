from __future__ import annotations

"""Quiz de compréhension par chapitres sur *Journal d'un chat assassin*."""

DISPLAY_NAME = "Français : Journal d'un chat assassin (chapitres)"

from .logger import log_result
from .utils import ask_choice_with_navigation, show_lesson

LESSON = """
📖 **Compréhension de lecture — Journal d'un chat assassin**

Tu vas répondre à des questions sur 7 chapitres :
- Lundi
- Mardi
- Mercredi
- Jeudi
- Vendredi
- Toujours vendredi
- Samedi

Chaque chapitre contient **10 questions**.
Lis bien chaque proposition avant de répondre.
"""


CHAPTERS = [
    {
        "title": "Chapitre 1 — Lundi",
        "questions": [
            {"prompt": "1. Qui raconte l'histoire ?", "choices": ["Ellie", "Tuffy le chat", "Le voisin"], "answer": 1},
            {"prompt": "2. Que dit Tuffy avoir tué ?", "choices": ["Une souris", "Un lapin", "Un oiseau"], "answer": 2},
            {"prompt": "3. Où Tuffy abandonne-t-il l'animal ?", "choices": ["Sur le tapis", "Dans le jardin", "Sous la table"], "answer": 0},
            {"prompt": "4. Comment réagit Ellie ?", "choices": ["Elle rit", "Elle pleure", "Elle ne dit rien"], "answer": 1},
            {"prompt": "5. Que fait la mère d'Ellie ?", "choices": ["Elle appelle les voisins", "Elle prend de vieux journaux", "Elle ferme la chatière"], "answer": 1},
            {"prompt": "6. Que prépare le père d'Ellie ?", "choices": ["Un seau d'eau savonneuse", "Une cage", "Un piège"], "answer": 0},
            {"prompt": "7. Comment Tuffy justifie-t-il son geste ?", "choices": ["Il voulait jouer", "Il est un chat, c'est son instinct", "Il a obéi à Ellie"], "answer": 1},
            {"prompt": "8. Selon Tuffy, l'oiseau aurait pu...", "choices": ["L'aider", "Le blesser", "S'enfuir en voiture"], "answer": 1},
            {"prompt": "9. Que pense Tuffy de toute cette affaire ?", "choices": ["C'est une histoire exagérée", "C'est normal", "C'est amusant pour Ellie"], "answer": 0},
            {"prompt": "10. Quelle expression revient au début et à la fin du chapitre ?", "choices": ["Vive les chats !", "Pendez-moi", "Bonne chance"], "answer": 1},
        ],
    },
    {
        "title": "Chapitre 2 — Mardi",
        "questions": [
            {"prompt": "1. Quel événement a lieu dans le jardin ?", "choices": ["Un concours", "Un petit enterrement", "Un anniversaire"], "answer": 1},
            {"prompt": "2. Qui pleure encore l'oiseau ?", "choices": ["Le père", "La mère", "Ellie"], "answer": 2},
            {"prompt": "3. Dans quoi Ellie place-t-elle l'oiseau ?", "choices": ["Une boîte", "Une serviette", "Un panier"], "answer": 0},
            {"prompt": "4. Que reprochent les adultes à Tuffy dans le jardin ?", "choices": ["Il casse les fleurs", "Il mord la porte", "Il mange les rideaux"], "answer": 0},
            {"prompt": "5. Que dit le père d'Ellie à Tuffy ?", "choices": ["Viens ici", "Fiche le camp", "Merci"], "answer": 1},
            {"prompt": "6. Comment Tuffy réagit-il à cette phrase ?", "choices": ["Il s'enfuit", "Il s'excuse", "Il fait un clin d'œil"], "answer": 2},
            {"prompt": "7. Selon Tuffy, qui connaissait l'oiseau depuis le plus longtemps ?", "choices": ["Ellie", "Lui-même", "La voisine"], "answer": 1},
            {"prompt": "8. Quelle ambiance domine ce chapitre ?", "choices": ["Sérieuse et triste pour les humains", "Festive", "Silencieuse et neutre"], "answer": 0},
            {"prompt": "9. Pourquoi Tuffy estime-t-il avoir sa place au jardin ?", "choices": ["C'est autant son jardin que le leur", "Il paye un loyer", "Il garde la maison"], "answer": 0},
            {"prompt": "10. Comment Tuffy considère-t-il l'attitude du père d'Ellie ?", "choices": ["Polie", "Grossière", "Courageuse"], "answer": 1},
        ],
    },
    {
        "title": "Chapitre 3 — Mercredi",
        "questions": [
            {"prompt": "1. Qu'apporte Tuffy à la maison ?", "choices": ["Un poisson", "Une souris morte", "Un oiseau vivant"], "answer": 1},
            {"prompt": "2. Tuffy affirme qu'il...", "choices": ["A tué la souris", "N'a pas tué la souris", "A acheté la souris"], "answer": 1},
            {"prompt": "3. Qu'évoque Tuffy comme danger dans la rue ?", "choices": ["La neige", "La mort-aux-rats et les voitures", "Les travaux"], "answer": 1},
            {"prompt": "4. Que dit Ellie à propos de cette nouvelle scène ?", "choices": ["C'est la deuxième fois cette semaine", "Ce n'est rien", "C'est la première fois"], "answer": 0},
            {"prompt": "5. Ellie demande à Tuffy de...", "choices": ["Sortir davantage", "Arrêter de recommencer", "Chasser mieux"], "answer": 1},
            {"prompt": "6. Comment essaie-t-il de répondre ?", "choices": ["Par un clin d'œil", "Par un miaulement long", "Par une fuite"], "answer": 0},
            {"prompt": "7. Quelle réaction d'Ellie revient encore ?", "choices": ["Elle rit", "Elle éclate en sanglots", "Elle applaudit"], "answer": 1},
            {"prompt": "8. Que se passe-t-il encore après cet épisode ?", "choices": ["Un bain du chat", "Un enterrement", "Une visite des voisins"], "answer": 1},
            {"prompt": "9. Tuffy qualifie la maison de...", "choices": ["Musée du silence", "Maison de la Rigolade", "Château des chats"], "answer": 1},
            {"prompt": "10. Le ton de Tuffy face aux reproches est surtout...", "choices": ["Culpabilisé", "Ironique", "Paniqué"], "answer": 1},
        ],
    },
    {
        "title": "Chapitre 4 — Jeudi",
        "questions": [
            {"prompt": "1. Quel animal Tuffy ramène-t-il cette fois ?", "choices": ["Un pigeon", "Un lapin", "Un hérisson"], "answer": 1},
            {"prompt": "2. Par où le lapin est-il passé ?", "choices": ["La fenêtre", "La chatière", "La cheminée"], "answer": 1},
            {"prompt": "3. Comment Ellie reconnaît-elle le lapin ?", "choices": ["C'est Thumper, le lapin d'à côté", "C'est un lapin sauvage", "C'est le lapin de l'école"], "answer": 0},
            {"prompt": "4. Quelle est la première peur des parents ?", "choices": ["Perdre Tuffy", "Avoir un problème avec les voisins", "Manquer de nourriture"], "answer": 1},
            {"prompt": "5. Dans quel état est Thumper quand il arrive ?", "choices": ["Propre et sec", "Plein de boue et d'herbe", "Blessé mais vivant"], "answer": 1},
            {"prompt": "6. Que font les adultes avec Thumper ?", "choices": ["Ils l'enterrent immédiatement", "Ils le lavent au savon", "Ils appellent la police"], "answer": 1},
            {"prompt": "7. Quel objet Ellie apporte-t-elle ?", "choices": ["Une pelle", "Le sèche-cheveux", "Une couverture"], "answer": 1},
            {"prompt": "8. Après le brushing, Thumper est décrit comme...", "choices": ["Superbe", "Effrayant", "Méconnaissable et sale"], "answer": 0},
            {"prompt": "9. Où Tuffy observe-t-il la scène ?", "choices": ["Sur le buffet", "Sous le lit", "Dans la rue"], "answer": 0},
            {"prompt": "10. À la fin, Tuffy comprend que les adultes vont...", "choices": ["Préparer une fête", "Remettre Thumper chez les voisins", "Vendre la maison"], "answer": 1},
        ],
    },
    {
        "title": "Chapitre 5 — Vendredi",
        "questions": [
            {"prompt": "1. À quelle heure commence leur expédition ?", "choices": ["À midi", "Après minuit", "À l'aube"], "answer": 1},
            {"prompt": "2. Comment est habillé le père d'Ellie ?", "choices": ["En blanc", "En noir de la tête aux pieds", "En pyjama"], "answer": 1},
            {"prompt": "3. Pourquoi refuse-t-il d'allumer dehors ?", "choices": ["Pour économiser", "Pour ne pas être vu", "Parce qu'il pleut"], "answer": 1},
            {"prompt": "4. Que dit la mère d'Ellie à Tuffy ?", "choices": ["Tu viens avec nous", "Tu restes à l'intérieur", "Tu surveilles Ellie"], "answer": 1},
            {"prompt": "5. Qui raconte ensuite les détails à Tuffy ?", "choices": ["Les voisins", "Bella, Tiger et Pusskins", "Le vétérinaire"], "answer": 1},
            {"prompt": "6. Que transporte le père d'Ellie ?", "choices": ["Un seau", "Thumper dans un cabas", "Un collier"], "answer": 1},
            {"prompt": "7. Où remet-il Thumper ?", "choices": ["Dans une boîte neuve", "Dans le clapier", "Dans la cave"], "answer": 1},
            {"prompt": "8. Dans quelle position place-t-il le lapin ?", "choices": ["Sur le dos", "Bien roulé en boule comme s'il dormait", "Debout"], "answer": 1},
            {"prompt": "9. De quoi Tuffy dit-il être puni ?", "choices": ["De vol", "De lapincide avec préméditation", "D'avoir cassé une vitre"], "answer": 1},
            {"prompt": "10. Que crie le père depuis la fenêtre ?", "choices": ["Fermez la porte !", "Comment as-tu fait pour sortir, sale bête ?", "Reviens, Tuffy !"], "answer": 1},
        ],
    },
    {
        "title": "Chapitre 6 — Toujours vendredi",
        "questions": [
            {"prompt": "1. Que fait le père d'Ellie à la chatière ?", "choices": ["Il la peint", "Il la cloue", "Il la remplace"], "answer": 1},
            {"prompt": "2. Avec quoi travaille-t-il ?", "choices": ["Marteau et clous", "Scie et colle", "Tournevis"], "answer": 0},
            {"prompt": "3. Quel bruit Tuffy décrit-il ?", "choices": ["Pan, pan, pan", "Boum, boum", "Clic, clic"], "answer": 0},
            {"prompt": "4. Quel système impose le père ?", "choices": ["Chatière fermée en permanence", "Chatière à sens unique", "Chatière électronique"], "answer": 1},
            {"prompt": "5. Selon lui, Tuffy peut...", "choices": ["Sortir mais ne rien rapporter", "Seulement entrer", "Rester toujours dedans"], "answer": 0},
            {"prompt": "6. S'il revient, où doit attendre Tuffy ?", "choices": ["Dans la cave", "Sur le paillasson", "Chez les voisins"], "answer": 1},
            {"prompt": "7. Que menace le père si Tuffy rapporte encore un animal ?", "choices": ["De l'emmener loin", """Malheur à toi""", "De vendre la chatière"], "answer": 1},
            {"prompt": "8. Comment Tuffy juge-t-il l'expression ""Malheur à toi"" ?", "choices": ["Élégante", "Stupide", "Drôle"], "answer": 1},
            {"prompt": "9. Le regard de Tuffy envers le père est surtout...", "choices": ["Admiration", "Opposition", "Indifférence joyeuse"], "answer": 1},
            {"prompt": "10. Quelle idée résume ce chapitre ?", "choices": ["Punir Tuffy en contrôlant ses allées et venues", "Organiser une fête", "Soigner Thumper"], "answer": 0},
        ],
    },
    {
        "title": "Chapitre 7 — Samedi",
        "questions": [
            {"prompt": "1. Pourquoi le père veut-il emmener Tuffy ?", "choices": ["Au parc", "Chez le vétérinaire pour un vaccin", "Chez les voisins"], "answer": 1},
            {"prompt": "2. Quelle inscription Ellie prépare-t-elle ?", "choices": ["Ici repose Tuffy", "Thumper repose en paix", "Bienvenue au jardin"], "answer": 1},
            {"prompt": "3. Quel animal Tuffy dit-il avoir un peu sifflé dans la salle d'attente ?", "choices": ["Le terrier des Fischer", "Un canari", "Un hamster"], "answer": 0},
            {"prompt": "4. Que note la réception sur son dossier ?", "choices": ["Très calme", "À manipuler avec précaution", "Vaccin urgent"], "answer": 1},
            {"prompt": "5. Comment le père cache-t-il Tuffy dans la salle d'attente ?", "choices": ["Sous une table", "Avec son imperméable sur la cage", "Dans le coffre"], "answer": 1},
            {"prompt": "6. Chez la vétérinaire, que se passe-t-il ?", "choices": ["Tout se passe bien", "Tuffy casse et renverse du matériel", "La vétérinaire s'évanouit"], "answer": 1},
            {"prompt": "7. Au supermarché, quel détail fait pleurer Ellie ?", "choices": ["Le prix des boîtes", "Des morceaux de lapin dans la nourriture", "La pluie"], "answer": 1},
            {"prompt": "8. Que révèle la voisine sur Thumper ?", "choices": ["Il était en voyage", "Il est mort puis a disparu et réapparu toiletté", "Il a été volé vivant"], "answer": 1},
            {"prompt": "9. Quelle est la conclusion des parents en rentrant ?", "choices": ["Tuffy est un imposteur", "Tuffy est innocent et sage", "Ils n'en parlent plus"], "answer": 0},
            {"prompt": "10. Qui défend Tuffy jusqu'au bout ?", "choices": ["Le père", "La voisine", "Ellie"], "answer": 2},
        ],
    },
]


def _run_chapter(chapter: dict[str, object]) -> tuple[int, int]:
    score = 0
    questions = chapter["questions"]

    for index, question in enumerate(questions, start=1):
        print(f"\nQuestion {index}")
        print(question["prompt"])
        student, option_letters, quit_requested = ask_choice_with_navigation(question["choices"])

        if quit_requested:
            print("\nRetour au menu des chapitres.\n")
            return score, index - 1

        correct_index = question["answer"]
        correct_letter = option_letters[correct_index]
        correct_text = question["choices"][correct_index]

        if student == correct_index:
            print("✅ Bonne réponse !")
            score += 1
        else:
            print(f"❌ Réponse attendue : {correct_letter}) {correct_text}")

    return score, len(questions)


def _display_chapter_menu() -> str:
    print("\nChoisis un chapitre :")
    for index, chapter in enumerate(CHAPTERS, start=1):
        print(f"{index}. {chapter['title']}")
    print("0. Retour")
    return input("Ton choix : ")


def main() -> None:
    """Affiche la leçon et lance les quiz par chapitre."""

    show_lesson(LESSON)
    print("\nAstuce : flèches + Entrée, ou lettre + Entrée. Tape 'q' pour revenir.")

    total_score = 0
    total_questions = 0

    while True:
        choice = _display_chapter_menu()
        if choice == "0":
            break

        try:
            chapter_index = int(choice) - 1
            chapter = CHAPTERS[chapter_index]
        except (ValueError, IndexError):
            print("Choix invalide.")
            continue

        print(f"\n=== {chapter['title']} ===")
        score, asked = _run_chapter(chapter)
        total_score += score
        total_questions += asked
        print(f"\nScore du chapitre : {score}/{asked}")

    if total_questions:
        percentage = total_score / total_questions * 100
        log_result("francais_journal_chat_assassin", percentage)


if __name__ == "__main__":
    main()
