"""Leçon et quiz sur Rome : du mythe à l'archéologie et à la République."""

from __future__ import annotations

import textwrap

from .histoire_prehistoire_neolithique import ask_multi_choice, ask_single_choice, ask_true_false
from .logger import log_result
from .utils import show_lesson

DISPLAY_NAME = "Histoire : Rome, du mythe à l'archéologie"

LESSON = textwrap.dedent(
    """
    🏛️ Rome : comparer mythe et histoire

    • Dans le mythe, Énée fuit Troie, arrive dans le Latium et ses descendants mènent à Romulus et Remus.
    • Les jumeaux, fils de Rhéa Silvia et du dieu Mars selon la légende, sont abandonnés près du Tibre,
      sauvés par une louve puis recueillis par des bergers.
    • Devenus adultes, Romulus et Remus veulent fonder une ville ; un augure (signe des dieux)
      départage les frères. Après leur conflit, Romulus fonde Rome sur le Palatin.
    • La date traditionnelle de fondation est 753 av. J.-C., soit le VIIIe siècle av. J.-C.

    📚 Les auteurs antiques et la prudence historique

    • Les récits de Virgile (Énéide) et Tite-Live (Histoire romaine) sont écrits au Ier siècle av. J.-C.
    • Ils racontent des faits censés se dérouler environ sept siècles plus tôt.
    • Ces textes sont précieux pour la culture romaine, mais ils mêlent mémoire, politique et légende.

    🧱 Ce que montre l'archéologie

    • Les plus anciennes traces d'occupation à Rome correspondent à des cabanes du VIIIe siècle av. J.-C.
      sur la colline du Palatin, occupées par des populations latines.
    • Rome se développe ensuite progressivement : d'habitats dispersés sur plusieurs collines,
      elle devient une ville structurée entre le VIIIe et le VIe siècle av. J.-C.
    • Le site est organisé autour du Tibre et de collines majeures : Palatin, Aventin, Capitole,
      Quirinal, Viminal, Esquilin et Caelius.

    ⚖️ La République romaine et la citoyenneté

    • En 509 av. J.-C., Rome devient une République.
    • Les citoyens romains ont des droits (voter, participer à la vie civique) et des devoirs
      (respecter les lois, servir Rome), et portent la toge comme vêtement civique symbolique.
    • Les citoyens sont répartis en groupes appelés centuries ; le vote s'arrête dès qu'une majorité
      est atteinte, ce qui favorise souvent les citoyens les plus riches.
    • La citoyenneté est limitée : elle est réservée aux hommes nés de parents citoyens ;
      les femmes et les esclaves en sont exclus.
    • Durant la République, Rome conquiert un vaste territoire méditerranéen et des hommes politiques
      utilisent le mythe des origines pour justifier leur pouvoir.
    • Les crises de la fin de la République renforcent des chefs comme Jules César, puis Auguste (son fils adoptif),
      qui inaugure le Principat en 27 av. J.-C., date retenue comme fin de la République.
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
    print(f"Résultat final : {score}/{len(QUESTIONS)} (soit {percentage:.1f} %)" )
    if percentage == 100:
        print("Bravo ! Tu maîtrises le chapitre sur Rome. 🥳")
    elif percentage >= 75:
        print("Très bien ! Encore un peu de révision pour être incollable.")
    elif percentage >= 50:
        print("Bon début, relis la leçon et réessaie.")
    else:
        print("Courage ! Revois le mythe, les dates, l'archéologie et la République romaine.")

    log_result("histoire_rome_du_mythe_a_larcheologie", percentage)


QUESTIONS: list[dict[str, object]] = [
    {
        "type": "single",
        "prompt": "Selon le mythe, de quelle ville Énée est-il originaire ?",
        "options": ["Troie", "Rome", "Athènes"],
        "answer": 0,
        "explanation": "Le récit présente Énée comme un héros troyen.",
    },
    {
        "type": "single",
        "prompt": "Dans quelle région d'Italie Énée s'installe-t-il ?",
        "options": ["Le Latium", "La Sicile", "La Gaule cisalpine"],
        "answer": 0,
        "explanation": "Les textes étudiés situent son installation dans le Latium.",
    },
    {
        "type": "tf",
        "prompt": "3. Romulus et Remus sont abandonnés près du Tibre dans la légende.",
        "answer": True,
        "explanation": "Le mythe place l'épisode sur les rives du fleuve.",
    },
    {
        "type": "single",
        "prompt": "Quel animal sauve d'abord Romulus et Remus selon le mythe ?",
        "options": ["Une louve", "Une ourse", "Une biche"],
        "answer": 0,
        "explanation": "La louve est une image emblématique des origines de Rome.",
    },
    {
        "type": "single",
        "prompt": "Qui est présenté comme le fondateur de Rome ?",
        "options": ["Romulus", "Remus", "Énée"],
        "answer": 0,
        "explanation": "Le récit se conclut par la fondation de Rome par Romulus.",
    },
    {
        "type": "single",
        "prompt": "Sur quelle colline Romulus fonde-t-il Rome ?",
        "options": ["Le Palatin", "L'Aventin", "Le Capitole"],
        "answer": 0,
        "explanation": "Le Palatin est explicitement associé à la fondation.",
    },
    {
        "type": "single",
        "prompt": "Quelle est la date traditionnelle de fondation de Rome ?",
        "options": ["753 av. J.-C.", "509 av. J.-C.", "44 av. J.-C."],
        "answer": 0,
        "explanation": "La tradition romaine retient 753 av. J.-C.",
    },
    {
        "type": "single",
        "prompt": "L'année 753 av. J.-C. appartient à quel siècle ?",
        "options": ["VIIIe siècle av. J.-C.", "VIIe siècle av. J.-C.", "Ier siècle av. J.-C."],
        "answer": 0,
        "explanation": "753 av. J.-C. se situe dans le VIIIe siècle av. J.-C.",
    },
    {
        "type": "single",
        "prompt": "Quel mot désigne un signe envoyé par les dieux ?",
        "options": ["Un augure", "Un sénat", "Un triomphe"],
        "answer": 0,
        "explanation": "Dans le récit, l'augure sert à départager les frères.",
    },
    {
        "type": "multi",
        "prompt": "Quels auteurs ont rédigé des récits célèbres sur les origines de Rome ?",
        "options": ["Virgile", "Tite-Live", "Jules César", "Homère"],
        "answers": {0, 1},
        "explanation": "La leçon mobilise l'Énéide de Virgile et l'Histoire romaine de Tite-Live.",
    },
    {
        "type": "single",
        "prompt": "À quelle époque écrivent Virgile et Tite-Live ?",
        "options": ["Au Ier siècle av. J.-C.", "Au VIIIe siècle av. J.-C.", "Au Ier siècle ap. J.-C."],
        "answer": 0,
        "explanation": "Leurs textes datent de la fin de la République romaine.",
    },
    {
        "type": "tf",
        "prompt": "12. Les récits de Virgile et Tite-Live sont contemporains de la fondation de Rome.",
        "answer": False,
        "explanation": "Ils écrivent environ sept siècles après la date traditionnelle de fondation.",
    },
    {
        "type": "tf",
        "prompt": "13. L'archéologie aide à vérifier et compléter les récits mythiques.",
        "answer": True,
        "explanation": "Elle apporte des traces matérielles indépendantes des légendes.",
    },
    {
        "type": "single",
        "prompt": "Quel type de vestiges anciens a été retrouvé sur le Palatin ?",
        "options": ["Des cabanes", "Des immeubles en béton", "Des cathédrales"],
        "answer": 0,
        "explanation": "Les traces les plus anciennes correspondent à des habitats simples.",
    },
    {
        "type": "single",
        "prompt": "Ces premières cabanes du Palatin datent surtout de quel siècle ?",
        "options": ["VIIIe siècle av. J.-C.", "IIIe siècle av. J.-C.", "Ve siècle ap. J.-C."],
        "answer": 0,
        "explanation": "Les fouilles renvoient aux débuts de l'occupation urbaine de Rome.",
    },
    {
        "type": "single",
        "prompt": "À quel peuple associe-t-on ces premières traces d'habitat ?",
        "options": ["Aux Latins", "Aux Vikings", "Aux Perses"],
        "answer": 0,
        "explanation": "La région du Latium est peuplée de communautés latines.",
    },
    {
        "type": "single",
        "prompt": "Quel fleuve traverse le site de Rome ?",
        "options": ["Le Tibre", "Le Nil", "Le Danube"],
        "answer": 0,
        "explanation": "Le Tibre structure l'espace de la ville antique.",
    },
    {
        "type": "multi",
        "prompt": "Quelles collines font partie du site de Rome antique ?",
        "options": ["Palatin", "Aventin", "Capitole", "Mont Blanc"],
        "answers": {0, 1, 2},
        "explanation": "Le Palatin, l'Aventin et le Capitole sont bien des collines romaines.",
    },
    {
        "type": "tf",
        "prompt": "19. L'archéologie montre une ville qui se construit progressivement entre le VIIIe et le VIe siècle av. J.-C.",
        "answer": True,
        "explanation": "On passe de traces d'habitats dispersés à une ville plus organisée.",
    },
    {
        "type": "tf",
        "prompt": "20. Mythe et archéologie racontent exactement la même chose, sans différence.",
        "answer": False,
        "explanation": "Le mythe donne un récit fondateur; l'archéologie reconstruit des faits matériels.",
    },
    {
        "type": "single",
        "prompt": "En quelle année Rome devient-elle une République ?",
        "options": ["509 av. J.-C.", "753 av. J.-C.", "27 av. J.-C."],
        "answer": 0,
        "explanation": "La date de 509 av. J.-C. marque le début de la République romaine.",
    },
    {
        "type": "single",
        "prompt": "Quel vêtement symbolique porte le citoyen romain ?",
        "options": ["La toge", "Le kimono", "La chlamyde spartiate"],
        "answer": 0,
        "explanation": "Dans la leçon, la toge est le vêtement civique du citoyen romain.",
    },
    {
        "type": "multi",
        "prompt": "Parmi ces propositions, lesquelles sont des droits du citoyen romain ?",
        "options": ["Voter", "Participer à la vie civique", "Être esclave", "Refuser toutes les lois"],
        "answers": {0, 1},
        "explanation": "Le citoyen dispose de droits politiques, mais aussi de devoirs.",
    },
    {
        "type": "multi",
        "prompt": "Parmi ces propositions, lesquelles sont des devoirs du citoyen romain ?",
        "options": ["Respecter les lois", "Servir Rome", "Ne jamais payer d'impôt", "Ignorer les magistrats"],
        "answers": {0, 1},
        "explanation": "Le statut civique implique des obligations envers la cité.",
    },
    {
        "type": "single",
        "prompt": "Comment s'appelle un groupe de citoyens romains dans l'organisation du vote ?",
        "options": ["Une centurie", "Une tribu gauloise", "Une phalange"],
        "answer": 0,
        "explanation": "Chaque groupe de citoyens est nommé 'centurie'.",
    },
    {
        "type": "tf",
        "prompt": "26. Dans le système des centuries, le vote peut s'arrêter dès qu'une majorité est atteinte.",
        "answer": True,
        "explanation": "L'ordre de vote favorise souvent les plus riches.",
    },
    {
        "type": "tf",
        "prompt": "27. Dans la République romaine, tous les citoyens ont exactement le même poids politique en pratique.",
        "answer": False,
        "explanation": "Le système des centuries avantage les citoyens les plus fortunés.",
    },
    {
        "type": "tf",
        "prompt": "28. La citoyenneté romaine est ouverte aux femmes selon la leçon étudiée.",
        "answer": False,
        "explanation": "La citoyenneté politique est réservée aux hommes dans ce cadre.",
    },
    {
        "type": "tf",
        "prompt": "29. Les esclaves sont exclus de la citoyenneté romaine.",
        "answer": True,
        "explanation": "La citoyenneté est limitée et ne les inclut pas.",
    },
    {
        "type": "single",
        "prompt": "Selon la fiche, à qui la citoyenneté est-elle réservée ?",
        "options": ["Aux hommes nés de parents citoyens", "À tous les habitants de l'Empire", "Aux seuls soldats étrangers"],
        "answer": 0,
        "explanation": "La définition donnée insiste sur une citoyenneté masculine et héréditaire.",
    },
    {
        "type": "single",
        "prompt": "Quel personnage est cité comme homme politique utilisant le mythe de Rome ?",
        "options": ["Jules César", "Périclès", "Hammourabi"],
        "answer": 0,
        "explanation": "La fiche mentionne Jules César puis Auguste.",
    },
    {
        "type": "single",
        "prompt": "Quel personnage inaugure le Principat en 27 av. J.-C., marquant la fin de la République ?",
        "options": ["Auguste", "Néron", "Romulus"],
        "answer": 0,
        "explanation": "Le cours associe 27 av. J.-C. à l'avènement d'Auguste.",
    },
    {
        "type": "tf",
        "prompt": "33. Pendant la République, Rome conquiert un vaste territoire autour de la Méditerranée.",
        "answer": True,
        "explanation": "La puissance romaine s'étend progressivement sur le bassin méditerranéen.",
    },
    {
        "type": "tf",
        "prompt": "34. Le mythe des origines est parfois utilisé pour justifier les conquêtes de Rome.",
        "answer": True,
        "explanation": "Le récit religieux et politique sert à légitimer la domination romaine.",
    },
    {
        "type": "single",
        "prompt": "La date 27 av. J.-C. se situe après 509 av. J.-C. dans la chronologie.",
        "options": ["Vrai, car elle est plus proche de l'an 0", "Faux, car 27 est plus grand que 509", "On ne peut pas comparer"],
        "answer": 0,
        "explanation": "En av. J.-C., plus le nombre diminue, plus on se rapproche de notre ère.",
    },
    {
        "type": "multi",
        "prompt": "Quelles collines appartiennent aux sept collines de Rome étudiées ici ?",
        "options": ["Quirinal", "Viminal", "Esquilin", "Olympe"],
        "answers": {0, 1, 2},
        "explanation": "Quirinal, Viminal et Esquilin font partie du relief de Rome antique.",
    },
    {
        "type": "tf",
        "prompt": "37. Le récit mythique donne une origine symbolique et religieuse à Rome.",
        "answer": True,
        "explanation": "Il explique le destin de Rome par l'action des héros et des dieux.",
    },
    {
        "type": "tf",
        "prompt": "38. L'archéologie repose sur des objets, des traces d'habitat et des vestiges matériels.",
        "answer": True,
        "explanation": "Elle s'appuie sur les preuves retrouvées dans les fouilles.",
    },
    {
        "type": "single",
        "prompt": "Pourquoi faut-il rester prudent face aux récits de fondation ?",
        "options": ["Ils sont écrits bien après les faits et peuvent mêler légende et politique", "Ils ont tous été dictés directement par Romulus", "Ils sont des textes scientifiques modernes"],
        "answer": 0,
        "explanation": "La distance temporelle invite à confronter les textes aux traces archéologiques.",
    },
    {
        "type": "single",
        "prompt": "Quel résumé est le plus juste ?",
        "options": ["Mythe et archéologie se complètent pour comprendre Rome", "Seul le mythe compte, les fouilles ne servent à rien", "Seules les fouilles comptent, les textes antiques sont inutiles"],
        "answer": 0,
        "explanation": "Le travail d'historien consiste à croiser les sources plutôt qu'à en choisir une seule.",
    },
]
