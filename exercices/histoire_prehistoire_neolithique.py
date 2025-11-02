"""Leçon et quiz sur la Préhistoire et la révolution néolithique."""

from __future__ import annotations

import textwrap

from .logger import log_result
from .utils import CheckboxPrompt, show_lesson

DISPLAY_NAME = "Histoire : De la Préhistoire au Néolithique"


LESSON = textwrap.dedent(
    """
    🗿 Résumé express

    • Les premiers humains apparaissent en Afrique il y a plus de 2,5 millions d'années.
    • Homo sapiens naît en Afrique puis migre vers tous les continents habités.
    • Au Paléolithique, les groupes sont nomades, chassent et produisent des œuvres d'art pariétal.
    • La grotte de Lascaux (✦ 18 000 ans) est protégée : seule une réplique accueille le public.
    • Entre 10 000 et 3 000 av. J.-C., le Néolithique voit l'agriculture, l'élevage et la sédentarisation.
    • Les villages néolithiques inventent la poterie, les meules, les haches polies et stockent des surplus.
    """
).strip()


def main() -> None:
    """Affiche la leçon puis lance le quiz de 40 questions."""

    show_lesson(LESSON)
    print("\nPlace au quiz ! Réponds en tapant le numéro ou 'vrai/faux' selon les consignes.")

    score = 0
    for index, question in enumerate(QUESTIONS, start=1):
        print("\n" + "=" * 70)
        print(f"Question {index}/{len(QUESTIONS)}")
        q_type = question["type"]
        if q_type == "tf":
            if ask_true_false(question["prompt"], question["answer"], question["explanation"]):
                score += 1
        elif q_type == "single":
            if ask_single_choice(
                question["prompt"], question["options"], question["answer"], question["explanation"]
            ):
                score += 1
        elif q_type == "multi":
            if ask_multi_choice(
                question["prompt"],
                question["options"],
                question["answers"],
                question["explanation"],
            ):
                score += 1
        else:  # pragma: no cover - defensive programming
            raise ValueError(f"Type de question inconnu: {q_type}")

    percentage = score / len(QUESTIONS) * 100
    print("\n" + "=" * 70)
    print(f"Résultat final : {score}/{len(QUESTIONS)} (soit {percentage:.1f} %)")
    if percentage == 100:
        print("Bravo ! Tu maîtrises toute la leçon. 🥳")
    elif percentage >= 75:
        print("Très bien ! Encore un petit effort pour viser la perfection.")
    elif percentage >= 50:
        print("Bon début, relis la leçon et réessaie.")
    else:
        print("Courage ! Revois la frise chronologique et les mots-clés du cours.")

    log_result("histoire_prehistoire_neolithique", percentage)


def ask_true_false(prompt: str, answer: bool, explanation: str) -> bool:
    """Pose une question Vrai/Faux et renvoie ``True`` si la réponse est correcte."""

    print(prompt)
    while True:
        choice = input("Tape 'v' pour vrai ou 'f' pour faux : ").strip().lower()
        if choice in {"v", "f"}:
            break
        print("Réponse attendue : 'v' ou 'f'.")

    is_true = choice == "v"
    if is_true == answer:
        print("✅ Bonne réponse !", explanation)
        return True
    print("❌ Ce n'est pas ça.", explanation)
    return False


def ask_single_choice(prompt: str, options: list[str], answer: int, explanation: str) -> bool:
    """Pose une question à choix unique."""

    print(prompt)
    for idx, option in enumerate(options, start=1):
        print(f"  {idx}. {option}")

    while True:
        raw = input("Votre choix : ").strip()
        if raw.isdigit():
            index = int(raw) - 1
            if 0 <= index < len(options):
                break
        print("Entre un numéro parmi les propositions.")

    if index == answer:
        print("✅ Correct !", explanation)
        return True
    print("❌ Mauvaise réponse.", explanation)
    return False


def ask_multi_choice(prompt: str, options: list[str], answers: set[int], explanation: str) -> bool:
    """Pose une question à réponses multiples utilisant :class:`CheckboxPrompt`."""

    widget = CheckboxPrompt(prompt, options)
    selected = set(widget.ask())
    if selected == answers:
        print("✅ Exact !", explanation)
        return True
    print("❌ Ce n'était pas le bon ensemble.", explanation)
    return False


QUESTIONS: list[dict[str, object]] = [
    {
        "type": "tf",
        "prompt": "1️⃣ La Préhistoire commence avec l'apparition des premiers hominidés.",
        "answer": True,
        "explanation": "Elle couvre toute la période précédant l'invention de l'écriture.",
    },
    {
        "type": "tf",
        "prompt": "2️⃣ L'invention de l'écriture marque la fin de la Préhistoire.",
        "answer": True,
        "explanation": "On parle ensuite d'Histoire car les sociétés laissent des textes.",
    },
    {
        "type": "single",
        "prompt": "Où apparaît Homo sapiens ?",
        "options": ["En Afrique", "En Europe", "En Océanie"],
        "answer": 0,
        "explanation": "Les plus anciens fossiles de sapiens sont africains.",
    },
    {
        "type": "single",
        "prompt": "Quelle espèce humaine précède Homo erectus ?",
        "options": ["Homo habilis", "Homo sapiens", "Homo neanderthalensis"],
        "answer": 0,
        "explanation": "Homo habilis est attesté dès 2,5 millions d'années.",
    },
    {
        "type": "single",
        "prompt": "Quelle suite chronologique est correcte ?",
        "options": [
            "Homo habilis → Homo erectus → Homo neanderthalensis → Homo sapiens",
            "Homo erectus → Homo habilis → Homo sapiens → Homo neanderthalensis",
            "Homo sapiens → Homo neanderthalensis → Homo habilis → Homo erectus",
        ],
        "answer": 0,
        "explanation": "Les espèces se succèdent globalement dans cet ordre.",
    },
    {
        "type": "tf",
        "prompt": "3️⃣ Homo sapiens a cohabité un temps avec les Néandertaliens en Europe.",
        "answer": True,
        "explanation": "Les deux groupes se croisent pendant plusieurs millénaires.",
    },
    {
        "type": "single",
        "prompt": "Les premières migrations de sapiens hors d'Afrique commencent vers…",
        "options": ["-100 000", "-10 000", "-1 000"],
        "answer": 0,
        "explanation": "Les sorties d'Afrique débutent autour de 100 000 ans avant aujourd'hui.",
    },
    {
        "type": "tf",
        "prompt": "4️⃣ Homo sapiens atteint l'Australie avant l'Amérique.",
        "answer": True,
        "explanation": "Les traversées vers l'Australie datent d'environ 50 000 ans, l'Amérique est peuplée bien plus tard.",
    },
    {
        "type": "single",
        "prompt": "Comment les groupes humains rejoignent-ils l'Amérique ?",
        "options": ["Par le détroit de Béring", "En traversant la Méditerranée", "En suivant le Nil"],
        "answer": 0,
        "explanation": "Un pont de glace reliait l'Asie à l'Amérique du Nord.",
    },
    {
        "type": "tf",
        "prompt": "5️⃣ Le campement de Pincevent montre un peuple d'agriculteurs sédentaires.",
        "answer": False,
        "explanation": "Il s'agit d'un campement de chasseurs nomades spécialisés dans le renne.",
    },
    {
        "type": "tf",
        "prompt": "6️⃣ Au Paléolithique, la plupart des groupes sont nomades.",
        "answer": True,
        "explanation": "Ils se déplacent pour suivre les animaux et les ressources.",
    },
    {
        "type": "single",
        "prompt": "Quel animal est principalement chassé à Pincevent ?",
        "options": ["Le renne", "Le bison", "Le sanglier"],
        "answer": 0,
        "explanation": "Les restes de rennes sont très nombreux sur le site.",
    },
    {
        "type": "single",
        "prompt": "Quel outil permet de lancer une sagaie plus loin ?",
        "options": ["Le propulseur", "La faucille", "La houe"],
        "answer": 0,
        "explanation": "Le propulseur augmente la puissance du bras.",
    },
    {
        "type": "tf",
        "prompt": "7️⃣ Un lissoir sert à assouplir les peaux.",
        "answer": True,
        "explanation": "Cet outil en os permet d'obtenir un cuir plus souple.",
    },
    {
        "type": "tf",
        "prompt": "8️⃣ Les pigments de Lascaux proviennent de minéraux comme l'ocre.",
        "answer": True,
        "explanation": "Les artistes broient des terres colorées (ocre, manganèse, charbon).",
    },
    {
        "type": "single",
        "prompt": "En quelle année la grotte de Lascaux est-elle découverte ?",
        "options": ["1940", "1840", "1990"],
        "answer": 0,
        "explanation": "Quatre adolescents périgourdins la trouvent en septembre 1940.",
    },
    {
        "type": "tf",
        "prompt": "9️⃣ On peut encore visiter librement la grotte originale de Lascaux.",
        "answer": False,
        "explanation": "Elle est fermée pour éviter la détérioration des peintures.",
    },
    {
        "type": "single",
        "prompt": "Quelle solution protège Lascaux tout en accueillant le public ?",
        "options": [
            "Une réplique (Lascaux II puis IV)",
            "Un chauffage permanent des parois",
            "Un éclairage puissant 24h/24",
        ],
        "answer": 0,
        "explanation": "Les visiteurs découvrent aujourd'hui une reproduction fidèle.",
    },
    {
        "type": "tf",
        "prompt": "🔟 Les peintures de Lascaux datent d'environ 18 000 ans.",
        "answer": True,
        "explanation": "Elles appartiennent au Magdalénien du Paléolithique supérieur.",
    },
    {
        "type": "single",
        "prompt": "Quels animaux dominent les représentations de Lascaux ?",
        "options": ["Chevaux et bisons", "Poissons", "Chiens domestiques"],
        "answer": 0,
        "explanation": "La salle des Taureaux montre chevaux, bisons et aurochs monumentaux.",
    },
    {
        "type": "tf",
        "prompt": "1️⃣1️⃣ Les artistes préhistoriques obtiennent le noir grâce au charbon de bois.",
        "answer": True,
        "explanation": "Le charbon écrasé donne un pigment sombre facile à appliquer.",
    },
    {
        "type": "tf",
        "prompt": "1️⃣2️⃣ La néolithisation commence au Proche-Orient avant d'atteindre l'Europe.",
        "answer": True,
        "explanation": "Les premiers villages agricoles se situent au Croissant fertile.",
    },
    {
        "type": "single",
        "prompt": "Quelle activité apparaît au Néolithique ?",
        "options": ["L'agriculture", "La navigation spatiale", "L'imprimerie"],
        "answer": 0,
        "explanation": "Cultiver les plantes nourrit les villages sédentaires.",
    },
    {
        "type": "single",
        "prompt": "Quel outil est emblématique du Néolithique ?",
        "options": ["La hache polie", "Le biface taillé", "Le propulseur"],
        "answer": 0,
        "explanation": "Le polissage donne des lames plus solides et régulières.",
    },
    {
        "type": "tf",
        "prompt": "1️⃣3️⃣ Au Néolithique, les communautés deviennent sédentaires.",
        "answer": True,
        "explanation": "Les maisons se regroupent en villages près des champs.",
    },
    {
        "type": "single",
        "prompt": "De quoi sont faites les parois des maisons néolithiques ?",
        "options": [
            "De poteaux en bois et de torchis",
            "De béton armé",
            "De vitres et d'acier",
        ],
        "answer": 0,
        "explanation": "Le torchis (terre + paille) recouvre une armature de bois.",
    },
    {
        "type": "tf",
        "prompt": "1️⃣4️⃣ Les céréales cultivées sont broyées grâce à des meules.",
        "answer": True,
        "explanation": "Meule dormante et molette transforment le grain en farine.",
    },
    {
        "type": "single",
        "prompt": "Quel animal est domestiqué très tôt au Néolithique ?",
        "options": ["Le mouton", "Le lion", "Le renard polaire"],
        "answer": 0,
        "explanation": "Le mouton fournit viande, lait et laine.",
    },
    {
        "type": "tf",
        "prompt": "1️⃣5️⃣ Les surplus agricoles sont stockés dans des silos et des jarres.",
        "answer": True,
        "explanation": "Cela sécurise l'alimentation d'une année sur l'autre.",
    },
    {
        "type": "single",
        "prompt": "Pourquoi polit-on la pierre des haches néolithiques ?",
        "options": [
            "Pour renforcer la lame",
            "Pour la colorer en rouge",
            "Pour y incruster des coquillages",
        ],
        "answer": 0,
        "explanation": "Le polissage rend le tranchant plus résistant et efficace.",
    },
    {
        "type": "tf",
        "prompt": "1️⃣6️⃣ Le Néolithique débute autour de 10 000 ans avant notre ère.",
        "answer": True,
        "explanation": "Les premiers indices agricoles datent d'entre -10 000 et -9 000.",
    },
    {
        "type": "tf",
        "prompt": "1️⃣7️⃣ La métallurgie du fer appartient déjà au Néolithique.",
        "answer": False,
        "explanation": "Le travail du fer se développe bien plus tard, à l'Âge du fer.",
    },
    {
        "type": "single",
        "prompt": "Quelle plante est largement cultivée en Europe néolithique ?",
        "options": ["Le blé", "Le café", "La canne à sucre"],
        "answer": 0,
        "explanation": "Le blé et l'orge sont au cœur de l'agriculture.",
    },
    {
        "type": "tf",
        "prompt": "1️⃣8️⃣ Les premières maisons néolithiques sont regroupées en villages.",
        "answer": True,
        "explanation": "La vie collective s'organise autour de places, foyers et silos.",
    },
    {
        "type": "multi",
        "prompt": "Coche les innovations majeures du Néolithique :",
        "options": [
            "La sédentarisation",
            "La chasse exclusive au mammouth",
            "La poterie",
            "La domestication des animaux",
            "Les fusées spatiales",
        ],
        "answers": {0, 2, 3},
        "explanation": "Sédentarisation, poterie et élevage transforment la vie quotidienne.",
    },
    {
        "type": "multi",
        "prompt": "Quels espaces sont occupés par Homo sapiens à la fin de la Préhistoire ?",
        "options": [
            "Afrique",
            "Europe",
            "Asie",
            "Océanie",
            "Amérique",
            "Antarctique",
        ],
        "answers": {0, 1, 2, 3, 4},
        "explanation": "Tous les continents habités sont atteints sauf l'Antarctique glacé.",
    },
    {
        "type": "multi",
        "prompt": "Coche les outils appartenant au Paléolithique supérieur :",
        "options": [
            "Propulseur",
            "Harpon à barbelures",
            "Faucille en pierre polie",
            "Lissoir en os",
            "Charrue en métal",
        ],
        "answers": {0, 1, 3},
        "explanation": "Propulseur, harpons et lissoirs sont attestés chez les chasseurs-cueilleurs.",
    },
    {
        "type": "multi",
        "prompt": "Quelles transformations résument la révolution néolithique ?",
        "options": [
            "Agriculture des plantes",
            "Sédentarisation des groupes",
            "Invention de l'imprimerie",
            "Élevage des animaux",
            "Apparition d'Internet",
        ],
        "answers": {0, 1, 3},
        "explanation": "Cultiver, se fixer et élever transforment durablement les sociétés.",
    },
    {
        "type": "multi",
        "prompt": "Quelles activités deviennent possibles grâce à la sédentarisation ?",
        "options": [
            "Construire des maisons durables",
            "Suivre les troupeaux en permanence",
            "Aménager des champs",
            "Fonder une base lunaire",
        ],
        "answers": {0, 2},
        "explanation": "Rester au même endroit permet de bâtir et de cultiver durablement.",
    },
    {
        "type": "tf",
        "prompt": "2️⃣0️⃣ Les villages néolithiques s'installent près d'un point d'eau.",
        "answer": True,
        "explanation": "L'eau est indispensable pour boire, irriguer et façonner l'argile.",
    },
]
