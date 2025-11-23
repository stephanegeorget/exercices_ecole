from __future__ import annotations

"""Leçon et quiz sur le présent de l'indicatif."""

DISPLAY_NAME = "Français : Présent de l'indicatif"

from .logger import log_result
from .utils import show_lesson

LESSON = """
📚 **Le présent de l'indicatif : exprimer ce qui se passe maintenant**

- **1er groupe (-er)** : terminaisons régulières `-e`, `-es`, `-e`, `-ons`, `-ez`, `-ent`.
  > je regarde, nous parlons, ils jouent
- **2ᵉ groupe (-ir régulier)** : terminaisons `-is`, `-is`, `-it`, `-issons`, `-issez`, `-issent`.
  > tu finis, nous choisissons, elles grandissent
- **3ᵉ groupe** : formes variées, il faut les connaître au cas par cas.
  > il prend, nous faisons, vous pouvez, ils vont

Lis chaque phrase, repère le verbe entre parenthèses et saisis **la forme conjuguée**
au présent de l'indicatif pour compléter le blanc.
"""

QUESTIONS = [
    {
        "prompt": "1. (parler) — Je ___ doucement avec ma sœur.",
        "answers": ["parle"],
        "verb": "parler",
        "group": "1er groupe",
        "explanation": "Au présent, je + parler → je parle (-e).",
    },
    {
        "prompt": "2. (chanter) — Tu ___ sous la douche très fort !",
        "answers": ["chantes"],
        "verb": "chanter",
        "group": "1er groupe",
        "explanation": "Tu + 1er groupe → terminaison -es : tu chantes.",
    },
    {
        "prompt": "3. (aimer) — Il ___ les expériences de sciences.",
        "answers": ["aime"],
        "verb": "aimer",
        "group": "1er groupe",
        "explanation": "Il aime : forme en -e pour la 3ᵉ personne du singulier.",
    },
    {
        "prompt": "4. (jouer) — Nous ___ au basket chaque mercredi.",
        "answers": ["jouons"],
        "verb": "jouer",
        "group": "1er groupe",
        "explanation": "Nous + -er → terminaison -ons : nous jouons.",
    },
    {
        "prompt": "5. (regarder) — Vous ___ les étoiles dans le ciel.",
        "answers": ["regardez"],
        "verb": "regarder",
        "group": "1er groupe",
        "explanation": "Vous + 1er groupe → terminaison -ez : vous regardez.",
    },
    {
        "prompt": "6. (arriver) — Elles ___ au parc en avance.",
        "answers": ["arrivent"],
        "verb": "arriver",
        "group": "1er groupe",
        "explanation": "Elles + -er → terminaison -ent : elles arrivent.",
    },
    {
        "prompt": "7. (finir) — Je ___ les détails de mon dessin.",
        "answers": ["finis"],
        "verb": "finir",
        "group": "2ᵉ groupe",
        "explanation": "2ᵉ groupe : je finis (terminaison -is).",
    },
    {
        "prompt": "8. (choisir) — Tu ___ ce roman à la bibliothèque.",
        "answers": ["choisis"],
        "verb": "choisir",
        "group": "2ᵉ groupe",
        "explanation": "Tu + 2ᵉ groupe → tu choisis (-is).",
    },
    {
        "prompt": "9. (grandir) — Il ___ de plusieurs centimètres.",
        "answers": ["grandit"],
        "verb": "grandir",
        "group": "2ᵉ groupe",
        "explanation": "Il grandit : terminaison -it au présent pour il/elle des verbes en -ir réguliers.",
    },
    {
        "prompt": "10. (réussir) — Nous ___ ce problème ensemble.",
        "answers": ["réussissons", "reussissons"],
        "verb": "réussir",
        "group": "2ᵉ groupe",
        "explanation": "Nous réussissons : terminaison -issons pour nous.",
    },
    {
        "prompt": "11. (rougir) — Vous ___ facilement.",
        "answers": ["rougissez"],
        "verb": "rougir",
        "group": "2ᵉ groupe",
        "explanation": "Vous rougissez : terminaison -issez au présent.",
    },
    {
        "prompt": "12. (obéir) — Elles ___ toujours aux règles.",
        "answers": ["obéissent", "obeissent"],
        "verb": "obéir",
        "group": "2ᵉ groupe",
        "explanation": "Elles obéissent : terminaison -issent pour ils/elles.",
    },
    {
        "prompt": "13. (être) — Je ___ à l'heure, prête.",
        "answers": ["suis"],
        "verb": "être",
        "group": "3ᵉ groupe",
        "explanation": "Être est irrégulier : je suis.",
    },
    {
        "prompt": "14. (avoir) — Tu ___ deux chats à la maison.",
        "answers": ["as"],
        "verb": "avoir",
        "group": "3ᵉ groupe",
        "explanation": "Avoir : tu as (sans s à la fin).",
    },
    {
        "prompt": "15. (aller) — Il ___ à l'école en bus chaque matin.",
        "answers": ["va"],
        "verb": "aller",
        "group": "3ᵉ groupe",
        "explanation": "Aller : il va est la forme au présent.",
    },
    {
        "prompt": "16. (faire) — Nous ___ un gâteau avec une recette simple.",
        "answers": ["faisons"],
        "verb": "faire",
        "group": "3ᵉ groupe",
        "explanation": "Faire : nous faisons (terminaison -ons mais radical fais-).",
    },
    {
        "prompt": "17. (prendre) — Vous ___ le train puis le métro.",
        "answers": ["prenez"],
        "verb": "prendre",
        "group": "3ᵉ groupe",
        "explanation": "Prendre : vous prenez (radical pren-).",
    },
    {
        "prompt": "18. (venir) — Ils ___ avec nous à la fête.",
        "answers": ["viennent"],
        "verb": "venir",
        "group": "3ᵉ groupe",
        "explanation": "Venir : ils viennent (double n + ent).",
    },
    {
        "prompt": "19. (pouvoir) — Je ___ t'aider demain.",
        "answers": ["peux"],
        "verb": "pouvoir",
        "group": "3ᵉ groupe",
        "explanation": "Pouvoir : je peux (x final).",
    },
    {
        "prompt": "20. (vouloir) — Tu ___ un chocolat chaud.",
        "answers": ["veux"],
        "verb": "vouloir",
        "group": "3ᵉ groupe",
        "explanation": "Vouloir : tu veux (x final).",
    },
    {
        "prompt": "21. (devoir) — Il ___ ranger sa chambre.",
        "answers": ["doit"],
        "verb": "devoir",
        "group": "3ᵉ groupe",
        "explanation": "Devoir : il doit (t final).",
    },
    {
        "prompt": "22. (dire) — Nous ___ bonjour aux voisins chaque matin.",
        "answers": ["disons"],
        "verb": "dire",
        "group": "3ᵉ groupe",
        "explanation": "Dire : nous disons (sans e après s).",
    },
    {
        "prompt": "23. (voir) — Vous ___ ce film et ses acteurs.",
        "answers": ["voyez"],
        "verb": "voir",
        "group": "3ᵉ groupe",
        "explanation": "Voir : vous voyez (y + ez).",
    },
    {
        "prompt": "24. (mettre) — Elles ___ la table avec les assiettes.",
        "answers": ["mettent"],
        "verb": "mettre",
        "group": "3ᵉ groupe",
        "explanation": "Mettre : elles mettent (deux t).",
    },
    {
        "prompt": "25. (savoir) — Je ___ déjà la réponse.",
        "answers": ["sais"],
        "verb": "savoir",
        "group": "3ᵉ groupe",
        "explanation": "Savoir : je sais (terminaison -s).",
    },
    {
        "prompt": "26. (partir) — Tu ___ ce soir pour le voyage.",
        "answers": ["pars"],
        "verb": "partir",
        "group": "3ᵉ groupe",
        "explanation": "Partir : tu pars (radical par- + s).",
    },
    {
        "prompt": "27. (sortir) — Il ___ du cinéma avec ses amis.",
        "answers": ["sort"],
        "verb": "sortir",
        "group": "3ᵉ groupe",
        "explanation": "Sortir : il sort (radical sort-).",
    },
    {
        "prompt": "28. (dormir) — Nous ___ tôt, vers dix heures.",
        "answers": ["dormons"],
        "verb": "dormir",
        "group": "3ᵉ groupe",
        "explanation": "Dormir : nous dormons (on garde m).",
    },
    {
        "prompt": "29. (lire) — Vous ___ chaque soir.",
        "answers": ["lisez"],
        "verb": "lire",
        "group": "3ᵉ groupe",
        "explanation": "Lire : vous lisez (terminaison -ez).",
    },
    {
        "prompt": "30. (écrire) — Ils ___ des cartes postales à leurs amis.",
        "answers": ["écrivent", "ecrivent"],
        "verb": "écrire",
        "group": "3ᵉ groupe",
        "explanation": "Écrire : ils écrivent (terminaison -ivent).",
    },
    {
        "prompt": "31. (croire) — Je ___ à ton projet.",
        "answers": ["crois"],
        "verb": "croire",
        "group": "3ᵉ groupe",
        "explanation": "Croire : je crois (s final).",
    },
    {
        "prompt": "32. (boire) — Tu ___ de l'eau après le sport.",
        "answers": ["bois"],
        "verb": "boire",
        "group": "3ᵉ groupe",
        "explanation": "Boire : tu bois (terminaison -is).",
    },
    {
        "prompt": "33. (ouvrir) — Il ___ la fenêtre pour aérer.",
        "answers": ["ouvre"],
        "verb": "ouvrir",
        "group": "3ᵉ groupe",
        "explanation": "Ouvrir se conjugue comme un verbe du 1er groupe : il ouvre.",
    },
    {
        "prompt": "34. (offrir) — Nous ___ des fleurs en bouquet.",
        "answers": ["offrons"],
        "verb": "offrir",
        "group": "3ᵉ groupe",
        "explanation": "Offrir : nous offrons (terminaison -ons).",
    },
    {
        "prompt": "35. (courir) — Vous ___ très rapidement.",
        "answers": ["courez"],
        "verb": "courir",
        "group": "3ᵉ groupe",
        "explanation": "Courir : vous courez (u dans le radical).",
    },
    {
        "prompt": "36. (vivre) — Elles ___ à la campagne, près de la forêt.",
        "answers": ["vivent"],
        "verb": "vivre",
        "group": "3ᵉ groupe",
        "explanation": "Vivre : elles vivent (terminaison -vent).",
    },
    {
        "prompt": "37. (connaître) — Je ___ bien cette histoire.",
        "answers": ["connais"],
        "verb": "connaître",
        "group": "3ᵉ groupe",
        "explanation": "Connaître : je connais (deux n, s final).",
    },
    {
        "prompt": "38. (servir) — Tu ___ le jus de fruit aux invités.",
        "answers": ["sers"],
        "verb": "servir",
        "group": "3ᵉ groupe",
        "explanation": "Servir : tu sers (radical ser-).",
    },
    {
        "prompt": "39. (tenir) — Il ___ la porte pour tout le monde.",
        "answers": ["tient"],
        "verb": "tenir",
        "group": "3ᵉ groupe",
        "explanation": "Tenir : il tient (radical tien-).",
    },
    {
        "prompt": "40. (recevoir) — Nous ___ de bonnes nouvelles dans une lettre.",
        "answers": ["recevons"],
        "verb": "recevoir",
        "group": "3ᵉ groupe",
        "explanation": "Recevoir : nous recevons (radical recev- + -ons).",
    },
]


def main() -> None:
    """Affiche la leçon puis lance le quiz sur le présent de l'indicatif."""

    show_lesson(LESSON)
    print("Tape la forme conjuguée du verbe entre parenthèses (accents acceptés ou non).")
    score = 0
    total = len(QUESTIONS)
    for question in QUESTIONS:
        print(f"\n{question['prompt']}")
        answer = input("Forme conjuguée : ").strip().lower()
        valid_answers = [option.lower() for option in question["answers"]]
        if answer in valid_answers:
            print("✅ Bravo !")
            score += 1
        else:
            correct = question["answers"][0]
            print(
                "❌ Ce n'est pas la bonne forme. "
                f"Le verbe '{question['verb']}' au présent ici est : {correct}."
            )
            print(f"ℹ️ {question['explanation']}")
    print(f"\nScore final : {score}/{total}")
    percentage = score / total * 100 if total else 0.0
    log_result("francais_present_indicatif", percentage)


if __name__ == "__main__":
    main()
