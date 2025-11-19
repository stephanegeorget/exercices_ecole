"""Leçon et quiz sur les premiers États et les premières écritures."""

from __future__ import annotations

import textwrap

from .histoire_prehistoire_neolithique import ask_multi_choice, ask_single_choice, ask_true_false
from .logger import log_result
from .utils import show_lesson

DISPLAY_NAME = "Histoire : Premiers États et premières écritures"

LESSON = textwrap.dedent(
    """
    🏺 Carte éclair
    • Au IVe et IIIe millénaires avant J.-C., les premiers États apparaissent en Mésopotamie
      (entre le Tigre et l'Euphrate) et en Égypte (le long du Nil et de son delta).
    • Les fleuves apportent de l'eau, du limon fertile, des voies de transport et permettent
      l'irrigation : les premières villes se regroupent donc à proximité.
    • En Égypte, le pharaon protège son peuple, rend la justice, conduit les armées et organise
      les travaux collectifs liés au fleuve.

    ✏️ Premières écritures
    • Les pictogrammes mésopotamiens (≈ 3500 av. J.-C.) sont de simples dessins gravés au roseau
      sur des tablettes d'argile, sans cases séparées.
    • L'écriture cunéiforme transforme ces dessins en clous en forme de coin, enfoncés au calame
      dans l'argile et souvent disposés dans de grands compartiments.
    • Les hiéroglyphes égyptiens mélangent dessins et signes pour les sons ; ils sont tracés au
      roseau taillé ou gravés sur la pierre, le bois ou le papyrus, en colonnes verticales.

    🎓 Les scribes
    • Seule une élite maîtrise la lecture et l'écriture : les scribes. Leur savoir leur donne un
      statut prestigieux auprès des temples et des palais.
    • Ils enregistrent les récoltes, les impôts, les échanges, les prières et les décisions
      politiques : sans eux, aucune archive durable ni contrôle des richesses.
    • Les représentations montrent souvent des scribes agenouillés, tablette ou rouleau sur les
      genoux, vérifiant et recopiant les colonnes de hiéroglyphes du haut vers le bas.
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
                question["prompt"], question["options"], question["answers"], question["explanation"],
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
        print("Courage ! Revois la carte, les fleuves et les différentes écritures.")

    log_result("histoire_premiers_etats_premieres_ecritures", percentage)


QUESTIONS: list[dict[str, object]] = [
    {
        "type": "tf",
        "prompt": "1. Les premiers États naissent vers le IVe-IIIe millénaire av. J.-C.",
        "answer": True,
        "explanation": "Les premières cités-États se structurent très tôt autour des grands fleuves.",
    },
    {
        "type": "single",
        "prompt": "Dans quelles deux régions se forment les premiers États ?",
        "options": ["En Mésopotamie et en Égypte", "En Grèce et en Gaule", "En Inde et en Chine"],
        "answer": 0,
        "explanation": "La carte montre la Mésopotamie et l'Égypte comme berceaux précoces.",
    },
    {
        "type": "single",
        "prompt": "Quels sont les deux fleuves principaux de Mésopotamie ?",
        "options": ["Le Tigre et l'Euphrate", "Le Nil et le Jourdain", "Le Danube et le Rhin"],
        "answer": 0,
        "explanation": "La Mésopotamie signifie littéralement 'le pays entre le Tigre et l'Euphrate'.",
    },
    {
        "type": "tf",
        "prompt": "4. 'Mésopotamie' veut dire 'pays entre deux fleuves'.",
        "answer": True,
        "explanation": "Le nom grec fait référence au Tigre et à l'Euphrate.",
    },
    {
        "type": "single",
        "prompt": "Quel fleuve structure l'Égypte antique ?",
        "options": ["Le Nil", "L'Amazone", "Le Yangzi"],
        "answer": 0,
        "explanation": "Le Nil et son delta rendent les terres cultivables au milieu du désert.",
    },
    {
        "type": "tf",
        "prompt": "6. Les premières villes se regroupent près des fleuves pour l'eau, les transports et l'irrigation.",
        "answer": True,
        "explanation": "Les cours d'eau fournissent ressources et voies de communication.",
    },
    {
        "type": "tf",
        "prompt": "7. Sans irrigation, les champs mésopotamiens se dessèchent rapidement.",
        "answer": True,
        "explanation": "Le contrôle de l'eau est vital dans ces régions à climat chaud.",
    },
    {
        "type": "single",
        "prompt": "Que déposent les crues du Nil chaque année ?",
        "options": ["Un limon fertile", "Du sable stérile", "Du sel marin"],
        "answer": 0,
        "explanation": "Le limon rend les sols propices aux récoltes en Égypte.",
    },
    {
        "type": "tf",
        "prompt": "9. Les pictogrammes mésopotamiens apparaissent vers 3500 av. J.-C.",
        "answer": True,
        "explanation": "Ce sont les plus anciennes écritures mentionnées dans la leçon.",
    },
    {
        "type": "tf",
        "prompt": "10. Un pictogramme est un dessin simple représentant un objet ou une action.",
        "answer": True,
        "explanation": "Les premiers signes reproduisent directement ce qu'ils évoquent.",
    },
    {
        "type": "tf",
        "prompt": "11. Les pictogrammes sont rangés dans des cases bien séparées.",
        "answer": False,
        "explanation": "Contrairement au cunéiforme, ils ne sont pas encore compartimentés.",
    },
    {
        "type": "single",
        "prompt": "Quel support est utilisé pour graver des pictogrammes ?",
        "options": ["Des tablettes d'argile", "Des feuilles de plastique", "Des rouleaux de soie"],
        "answer": 0,
        "explanation": "L'argile humide permet de tracer facilement puis de conserver la trace.",
    },
    {
        "type": "single",
        "prompt": "Avec quel instrument trace-t-on ces pictogrammes ?",
        "options": ["Un roseau taillé", "Une plume d'oie", "Un stylo bille"],
        "answer": 0,
        "explanation": "Les tiges de roseau servent de stylet pour graver l'argile.",
    },
    {
        "type": "tf",
        "prompt": "13. L'écriture cunéiforme transforme les dessins en clous en forme de coin.",
        "answer": True,
        "explanation": "D'un tracé courbe, on passe à des empreintes triangulaires.",
    },
    {
        "type": "tf",
        "prompt": "14. Le cunéiforme est inventé dans la même région que les pictogrammes.",
        "answer": True,
        "explanation": "Il s'agit toujours de la Mésopotamie.",
    },
    {
        "type": "single",
        "prompt": "Quel outil produit les coins caractéristiques du cunéiforme ?",
        "options": ["Un calame en tige de plante", "Un burin en métal", "Un pinceau large"],
        "answer": 0,
        "explanation": "Le calame est pressé dans l'argile pour laisser des empreintes en coin.",
    },
    {
        "type": "tf",
        "prompt": "16. Les signes cunéiformes sont souvent disposés dans de grands compartiments.",
        "answer": True,
        "explanation": "La leçon précise que les clous sont répartis dans des cases.",
    },
    {
        "type": "single",
        "prompt": "Dans quel pays antique utilise-t-on les hiéroglyphes ?",
        "options": ["En Égypte", "En Grèce", "En Chine"],
        "answer": 0,
        "explanation": "Les hiéroglyphes sont l'écriture sacrée des Égyptiens.",
    },
    {
        "type": "single",
        "prompt": "Quel support convient aux hiéroglyphes ?",
        "options": ["Pierre, bois ou papyrus", "Papier journal", "Parchemin médiéval"],
        "answer": 0,
        "explanation": "Les Égyptiens sculptent la pierre ou peignent sur papyrus et bois.",
    },
    {
        "type": "single",
        "prompt": "Avec quoi écrit-on les hiéroglyphes peints ?",
        "options": ["Un roseau taillé en pinceau", "Une craie", "Une plume de perroquet"],
        "answer": 0,
        "explanation": "Un roseau taillé sert de calame ou de pinceau pour appliquer les pigments.",
    },
    {
        "type": "tf",
        "prompt": "20. Les hiéroglyphes mélangent dessins et signes pour les sons.",
        "answer": True,
        "explanation": "On y trouve des idéogrammes mais aussi des symboles alphabétiques.",
    },
    {
        "type": "tf",
        "prompt": "21. Les scribes appartiennent à une élite très instruite.",
        "answer": True,
        "explanation": "La connaissance de l'écriture est rare et valorisée.",
    },
    {
        "type": "tf",
        "prompt": "22. Tout le monde sait lire et écrire dans ces sociétés.",
        "answer": False,
        "explanation": "La maîtrise de l'écrit est réservée à quelques spécialistes.",
    },
    {
        "type": "single",
        "prompt": "Quel est l'un des rôles principaux des scribes ?",
        "options": ["Compter récoltes et impôts", "Fabriquer des armes", "Tisser des vêtements"],
        "answer": 0,
        "explanation": "Ils enregistrent les richesses pour les temples et les palais.",
    },
    {
        "type": "tf",
        "prompt": "24. La compétence des scribes leur donne un statut prestigieux.",
        "answer": True,
        "explanation": "Ils travaillent auprès des autorités politiques et religieuses.",
    },
    {
        "type": "tf",
        "prompt": "25. Les scribes permettent de contrôler les échanges et les taxes.",
        "answer": True,
        "explanation": "Ils consignent contrats, marchandises et prélèvements.",
    },
    {
        "type": "single",
        "prompt": "Parmi ces écritures, laquelle est la plus ancienne ?",
        "options": ["Les pictogrammes", "Les hiéroglyphes", "L'alphabet grec"],
        "answer": 0,
        "explanation": "Les pictogrammes datent d'environ 3500 av. J.-C.",
    },
    {
        "type": "tf",
        "prompt": "27. Sans scribes, il serait difficile de conserver des archives durables.",
        "answer": True,
        "explanation": "Ils sont indispensables pour fixer et transmettre l'information écrite.",
    },
    {
        "type": "single",
        "prompt": "Qui dirige et protège les habitants en Égypte ?",
        "options": ["Le pharaon", "Le consul", "Le président"],
        "answer": 0,
        "explanation": "Le pharaon est le chef politique et religieux du pays.",
    },
    {
        "type": "tf",
        "prompt": "29. Le pharaon rend la justice et assure le bien-être de ses sujets.",
        "answer": True,
        "explanation": "Son pouvoir inclut la protection et l'arbitrage des conflits.",
    },
    {
        "type": "tf",
        "prompt": "30. Les premiers États se développent grâce aux ressources des fleuves.",
        "answer": True,
        "explanation": "L'eau, la fertilité et le transport fluvial favorisent leur essor.",
    },
    {
        "type": "single",
        "prompt": "Quelle mer borde l'ouest de la Mésopotamie sur la carte ?",
        "options": ["La mer Méditerranée", "La mer du Nord", "La mer Caspienne"],
        "answer": 0,
        "explanation": "La Méditerranée se situe à l'ouest du Croissant fertile.",
    },
    {
        "type": "tf",
        "prompt": "32. Les hiéroglyphes peuvent être gravés ou peints selon le support.",
        "answer": True,
        "explanation": "Pierre et bois sont gravés, le papyrus est plutôt peint.",
    },
    {
        "type": "multi",
        "prompt": "Quelles tâches les scribes accomplissent-ils ? (Plusieurs réponses possibles)",
        "options": [
            "Enregistrer les récoltes et les impôts",
            "Rédiger des prières et des décisions politiques",
            "Diriger les travaux d'irrigation",
            "Décorer les temples avec des couleurs",],
        "answers": {0, 1},
        "explanation": "Ils consignent les richesses et les textes officiels ; l'organisation des travaux relève du pouvoir royal.",
    },
    {
        "type": "tf",
        "prompt": "35. Les hiéroglyphes peuvent se lire en colonnes verticales du haut vers le bas.",
        "answer": True,
        "explanation": "La leçon mentionne cette disposition dans les représentations de scribes.",
    },
    {
        "type": "multi",
        "prompt": "Quels avantages l'écriture apporte-t-elle aux premiers États ?",
        "options": [
            "Collecter et vérifier les taxes",
            "Conserver les lois et décisions",
            "Remplacer totalement la parole orale",
            "Organiser les échanges commerciaux",],
        "answers": {0, 1, 3},
        "explanation": "L'écrit fixe les règles, suit les richesses et facilite les transactions sans supprimer la tradition orale.",
    },
    {
        "type": "single",
        "prompt": "Quel matériau naturel sert à fabriquer un calame ?",
        "options": ["Une tige de plante", "Un morceau de métal", "Un éclat de verre"],
        "answer": 0,
        "explanation": "Une tige de roseau ou de bambou taillée donne l'outil à enfoncer dans l'argile.",
    },
    {
        "type": "single",
        "prompt": "Quelle écriture combine des dessins et des symboles alphabétiques ?",
        "options": ["Les hiéroglyphes", "Le cunéiforme", "Les pictogrammes"],
        "answer": 0,
        "explanation": "Les hiéroglyphes possèdent des signes phonétiques en plus des images.",
    },
    {
        "type": "tf",
        "prompt": "39. Les premières écritures naissent dans des régions où s'organisent les premiers États.",
        "answer": True,
        "explanation": "La gestion des villes et des stocks crée le besoin d'écrire.",
    },
    {
        "type": "multi",
        "prompt": "Associe chaque écriture à son support privilégié (plusieurs bonnes réponses)",
        "options": [
            "Pictogrammes → tablettes d'argile",
            "Cunéiforme → argile comprimée au calame",
            "Hiéroglyphes → papyrus, bois ou pierre",
            "Hiéroglyphes → uniquement sur bronze"],
        "answers": {0, 1, 2},
        "explanation": "Les trois premières associations sont correctes ; le bronze n'est pas le support habituel des hiéroglyphes.",
    },
]

