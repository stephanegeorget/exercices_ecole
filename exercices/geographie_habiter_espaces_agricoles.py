"""Leçon et quiz sur les espaces agricoles à faible densité."""

from __future__ import annotations

import textwrap

from .histoire_prehistoire_neolithique import ask_single_choice, ask_true_false
from .logger import log_result
from .utils import show_lesson

DISPLAY_NAME = "Géographie : Habiter les espaces agricoles à faibles densités"

LESSON = textwrap.dedent(
    """
    🌍 Géographie – Chapitre 3 : Habiter les espaces agricoles à faibles densités

    1) Étude de cas n°1 : Les Grandes Plaines (États-Unis)
    • Localisation : au centre des États-Unis, en Amérique du Nord.
    • Climat continental : étés chauds, hivers froids, précipitations plutôt faibles.
    • Niveau de développement : très élevé.
    • Paysage d'openfield : très grands champs géométriques, ouverts, sans haies.
    • Agriculture intensive et moderne : forte mécanisation, rendements élevés.
    • Agriculture commerciale : les récoltes sont surtout destinées à la vente.
    • Habitat et population : fermes isolées, petite ville, faible densité de population.

    2) Étude de cas n°2 : Un front pionnier à Bornéo (Indonésie)
    • Localisation : île de Bornéo, en Indonésie, en Asie du Sud-Est.
    • Climat équatorial : chaleur et fortes précipitations toute l'année.
    • Niveau de développement de l'Indonésie : moyen.
    • Le paysage montre plusieurs plans : forêt, espace défriché, plantation de palmiers à huile,
      puis montagne recouverte de forêt à l'arrière-plan.
    • Le front pionnier correspond à la progression des activités humaines sur la forêt dense.

    3) Documents complémentaires (partie 2)
    • Dans de nombreux pays en développement, le travail agricole est souvent fait à la main,
      avec des rendements plus faibles.
    • L'agriculture y est souvent vivrière : les récoltes servent d'abord à nourrir les paysans.
    • La densité est faible : petits villages, pauvreté, exode rural vers les villes.
    • L'huile de palme a de multiples usages : produits alimentaires, agrocarburants,
      produits cosmétiques (hygiène, soins).
    • À Bornéo, la déforestation est importante et entraîne des conséquences négatives :
      menaces pour la biodiversité (espèces animales et végétales) et pour les populations locales.

    4) Mots-clés à retenir
    • Openfield : grands champs ouverts, sans haies ni clôtures.
    • Agriculture intensive : production importante grâce aux techniques et aux machines.
    • Agriculture commerciale : production vendue sur les marchés.
    • Agriculture vivrière : production destinée en priorité à nourrir la famille paysanne.
    • Front pionnier : espace de mise en valeur récent gagnant sur un milieu naturel.
    • Faible densité : peu d'habitants sur un vaste territoire.
    • Exode rural : départ des habitants des campagnes vers les villes.
    • Biodiversité : diversité des espèces vivantes (animales et végétales).

    5) Bilan
    • Les espaces agricoles à faibles densités sont variés :
      - dans un pays développé (États-Unis), ils peuvent être très productifs et très mécanisés ;
      - dans un pays en développement (exemple Bornéo/Indonésie), ils combinent faibles densités,
        fronts pionniers et fortes tensions environnementales.
    """
).strip()


def main() -> None:
    """Affiche la leçon puis lance le quiz de 40 questions."""

    show_lesson(LESSON)
    print("\nPlace au quiz ! Réponds en tapant le numéro ou 'v'/'f' selon les consignes.")

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
        else:  # pragma: no cover - defensive programming
            raise ValueError(f"Type de question inconnu: {q_type}")

    percentage = score / len(QUESTIONS) * 100
    print("\n" + "=" * 70)
    print(f"Résultat final : {score}/{len(QUESTIONS)} (soit {percentage:.1f} %)" )
    if percentage == 100:
        print("Bravo ! Tu maîtrises toute la leçon. 🥳")
    elif percentage >= 75:
        print("Très bien ! Encore un petit effort pour viser la perfection.")
    elif percentage >= 50:
        print("Bon début, relis la leçon et réessaie.")
    else:
        print("Courage ! Revois les deux études de cas et les mots-clés.")

    log_result("geographie_habiter_espaces_agricoles", percentage)


QUESTIONS: list[dict[str, object]] = [
    {
        "type": "tf",
        "prompt": "1. Le chapitre porte sur des espaces agricoles à faibles densités.",
        "answer": True,
        "explanation": "C'est le thème central de la leçon.",
    },
    {
        "type": "single",
        "prompt": "Où se situent les Grandes Plaines étudiées ?",
        "options": ["Au centre des États-Unis", "Au nord du Canada", "Au sud de l'Argentine"],
        "answer": 0,
        "explanation": "L'étude de cas n°1 concerne le centre des États-Unis.",
    },
    {
        "type": "tf",
        "prompt": "3. Les Grandes Plaines se trouvent en Amérique du Nord.",
        "answer": True,
        "explanation": "Les États-Unis font partie de l'Amérique du Nord.",
    },
    {
        "type": "single",
        "prompt": "Quel climat caractérise surtout les Grandes Plaines ?",
        "options": ["Continental", "Équatorial", "Polaire"],
        "answer": 0,
        "explanation": "Le climat indiqué est continental.",
    },
    {
        "type": "single",
        "prompt": "Dans ce climat continental, les étés sont plutôt…",
        "options": ["Chauds", "Très froids", "Toujours neigeux"],
        "answer": 0,
        "explanation": "La leçon indique des étés chauds.",
    },
    {
        "type": "single",
        "prompt": "Dans ce même climat, les hivers sont…",
        "options": ["Froids", "Tropicaux", "Caniculaires"],
        "answer": 0,
        "explanation": "La leçon indique des hivers froids.",
    },
    {
        "type": "tf",
        "prompt": "7. Dans l'étude de cas n°1, les précipitations sont plutôt faibles.",
        "answer": True,
        "explanation": "C'est un élément du tableau climatique.",
    },
    {
        "type": "single",
        "prompt": "Niveau de développement des États-Unis (dans le document) :",
        "options": ["Très élevé", "Moyen", "Faible"],
        "answer": 0,
        "explanation": "La case cochée est 'très élevé'.",
    },
    {
        "type": "single",
        "prompt": "Le terme openfield désigne surtout…",
        "options": ["De grands champs ouverts sans haies", "Une forêt tropicale dense", "Un quartier industriel"],
        "answer": 0,
        "explanation": "Openfield = champs ouverts, sans clôtures bocagères.",
    },
    {
        "type": "tf",
        "prompt": "10. Dans un paysage d'openfield, les parcelles sont souvent géométriques.",
        "answer": True,
        "explanation": "Le document décrit des formes rectangulaires/carrées.",
    },
    {
        "type": "single",
        "prompt": "Quel type d'agriculture est associé aux Grandes Plaines ?",
        "options": ["Intensive et moderne", "Vivrière traditionnelle", "Pastorale nomade"],
        "answer": 0,
        "explanation": "La mécanisation et les rendements élevés sont mis en avant.",
    },
    {
        "type": "tf",
        "prompt": "12. L'agriculture des Grandes Plaines utilise beaucoup de machines.",
        "answer": True,
        "explanation": "La forte mécanisation est une caractéristique du cas étudié.",
    },
    {
        "type": "single",
        "prompt": "Que devient principalement la récolte dans ce système ?",
        "options": ["Elle est vendue", "Elle est détruite", "Elle est réservée uniquement à la famille"],
        "answer": 0,
        "explanation": "Il s'agit d'une agriculture commerciale.",
    },
    {
        "type": "tf",
        "prompt": "14. 'Agriculture commerciale' signifie que la production est destinée à la vente.",
        "answer": True,
        "explanation": "C'est la définition donnée dans la leçon.",
    },
    {
        "type": "single",
        "prompt": "Comment est décrite la densité de population dans les Grandes Plaines ?",
        "options": ["Faible", "Très forte", "Uniformément élevée"],
        "answer": 0,
        "explanation": "Le document coche la faible densité.",
    },
    {
        "type": "tf",
        "prompt": "16. L'habitat observé comprend des fermes isolées et une petite ville.",
        "answer": True,
        "explanation": "Le paysage est peu peuplé et dispersé.",
    },
    {
        "type": "single",
        "prompt": "Dans ces espaces peu denses, on se déplace surtout…",
        "options": ["En voiture", "En métro", "En tramway"],
        "answer": 0,
        "explanation": "Le bilan insiste sur la place de la voiture.",
    },
    {
        "type": "single",
        "prompt": "Où se situe l'étude de cas n°2 ?",
        "options": ["À Bornéo en Indonésie", "Au Japon", "En Égypte"],
        "answer": 0,
        "explanation": "Le second cas porte sur l'île de Bornéo (Indonésie).",
    },
    {
        "type": "tf",
        "prompt": "19. Bornéo se trouve en Asie du Sud-Est.",
        "answer": True,
        "explanation": "C'est la localisation indiquée.",
    },
    {
        "type": "single",
        "prompt": "Quel est le climat de l'Indonésie dans la leçon ?",
        "options": ["Équatorial", "Méditerranéen", "Polaire"],
        "answer": 0,
        "explanation": "Le tableau mentionne un climat équatorial.",
    },
    {
        "type": "tf",
        "prompt": "21. Le climat équatorial se caractérise par la chaleur toute l'année.",
        "answer": True,
        "explanation": "Températures élevées constantes.",
    },
    {
        "type": "tf",
        "prompt": "22. En climat équatorial, les précipitations sont fortes toute l'année.",
        "answer": True,
        "explanation": "Le document le précise explicitement.",
    },
    {
        "type": "single",
        "prompt": "Niveau de développement de l'Indonésie (dans le document) :",
        "options": ["Moyen", "Très élevé", "Faible"],
        "answer": 0,
        "explanation": "La case cochée est 'moyen'.",
    },
    {
        "type": "single",
        "prompt": "Dans la photo de Bornéo, quelle culture est visible ?",
        "options": ["Plantation de palmiers à huile", "Vignes", "Rizières de montagne"],
        "answer": 0,
        "explanation": "Le croquis légendé mentionne les palmiers à huile.",
    },
    {
        "type": "tf",
        "prompt": "25. Le paysage de Bornéo montre aussi un espace défriché.",
        "answer": True,
        "explanation": "Le croquis distingue une zone défrichée.",
    },
    {
        "type": "single",
        "prompt": "Quel élément apparaît à l'arrière-plan du croquis de Bornéo ?",
        "options": ["Une montagne recouverte de forêt", "Un centre-ville dense", "Un glacier"],
        "answer": 0,
        "explanation": "La légende indique une montagne recouverte de forêt.",
    },
    {
        "type": "tf",
        "prompt": "27. Dans la scène étudiée à Bornéo, on observe beaucoup de bâtiments.",
        "answer": False,
        "explanation": "Au contraire, l'absence d'habitat est soulignée.",
    },
    {
        "type": "single",
        "prompt": "L'absence d'habitation visible indique plutôt…",
        "options": ["Une faible densité", "Une forte densité", "Une mégalopole"],
        "answer": 0,
        "explanation": "Peu d'habitants visibles sur un grand espace = faible densité.",
    },
    {
        "type": "single",
        "prompt": "Un front pionnier correspond à…",
        "options": [
            "Une progression des activités humaines sur un milieu naturel",
            "Une frontière politique historique",
            "Une zone de montagne enneigée",
        ],
        "answer": 0,
        "explanation": "Ici, la forêt dense est transformée par les activités agricoles.",
    },
    {
        "type": "tf",
        "prompt": "30. Le front pionnier de Bornéo illustre une transformation rapide des paysages.",
        "answer": True,
        "explanation": "Le passage forêt/défrichement/plantation montre cette dynamique.",
    },
    {
        "type": "single",
        "prompt": "Dans un pays en développement, l'agriculture est souvent…",
        "options": ["Vivrière", "Entièrement robotisée", "Toujours exportatrice"],
        "answer": 0,
        "explanation": "Les récoltes servent d'abord à nourrir les paysans eux-mêmes.",
    },
    {
        "type": "tf",
        "prompt": "32. L'agriculture vivrière a pour but principal de nourrir la famille paysanne.",
        "answer": True,
        "explanation": "C'est la définition de l'agriculture vivrière.",
    },
    {
        "type": "single",
        "prompt": "Le travail agricole dans ces espaces est souvent…",
        "options": ["Fait à la main", "Réalisé uniquement par drones", "Sans main-d'œuvre"],
        "answer": 0,
        "explanation": "Le bilan de la partie 2 insiste sur le travail manuel.",
    },
    {
        "type": "tf",
        "prompt": "34. L'exode rural correspond au départ des campagnes vers les villes.",
        "answer": True,
        "explanation": "Les habitants espèrent de meilleures conditions de vie en ville.",
    },
    {
        "type": "single",
        "prompt": "Parmi ces propositions, laquelle est un usage de l'huile de palme ?",
        "options": ["Produits alimentaires", "Carburant nucléaire", "Fabrication de rails"],
        "answer": 0,
        "explanation": "Le document mentionne les produits alimentaires.",
    },
    {
        "type": "single",
        "prompt": "Un autre usage cité de l'huile de palme est…",
        "options": ["Les cosmétiques", "Les pneus d'avion uniquement", "Les panneaux solaires"],
        "answer": 0,
        "explanation": "Le document cite aussi les produits cosmétiques.",
    },
    {
        "type": "tf",
        "prompt": "37. La déforestation à Bornéo est présentée comme importante.",
        "answer": True,
        "explanation": "La forêt n'occupe plus qu'une partie réduite de l'île.",
    },
    {
        "type": "single",
        "prompt": "Quelle conséquence est directement citée ?",
        "options": ["Menace sur les espèces animales", "Augmentation des glaciers", "Disparition des océans"],
        "answer": 0,
        "explanation": "La déforestation menace la biodiversité.",
    },
    {
        "type": "tf",
        "prompt": "39. Les populations locales vivant dans la forêt peuvent être menacées.",
        "answer": True,
        "explanation": "Le document parle explicitement de menaces pour les populations locales.",
    },
    {
        "type": "single",
        "prompt": "Quelle phrase résume le mieux le chapitre ?",
        "options": [
            "Des espaces peu peuplés peuvent être très productifs ou fragilisés par la déforestation.",
            "Tous les espaces agricoles ont le même climat et les mêmes techniques.",
            "La faible densité empêche toute activité économique.",
        ],
        "answer": 0,
        "explanation": "Le bilan compare productivité (USA) et enjeux sociaux/environnementaux (Bornéo).",
    },
]
