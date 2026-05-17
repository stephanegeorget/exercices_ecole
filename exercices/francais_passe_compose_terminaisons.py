from __future__ import annotations

"""Exercice complet sur le passé composé : participe, auxiliaire et accord."""

DISPLAY_NAME = "Français : Passé composé (complet)"

from collections import Counter, defaultdict
import random

from .logger import log_result
from .utils import show_lesson

LESSON = """
📚 **Passé composé — version complète**

Dans cette version, tu travailles 4 compétences :
1. trouver l'infinitif du verbe,
2. former le participe passé,
3. choisir l'auxiliaire (**avoir** / **être**),
4. accorder le participe passé quand il le faut.

🧠 **Méthode en 4 étapes**
- repérer le verbe à l'infinitif,
- former le participe,
- choisir l'auxiliaire,
- vérifier l'accord.
"""

SKILLS = ("infinitif", "participe", "auxiliaire", "accord")


def _item(
    fmt: str,
    skill: str,
    subskill: str,
    difficulty: int,
    lemma: str,
    prompt: str,
    explanation: str,
    expected: list[str] | None = None,
    choices: list[str] | None = None,
    answer: int | None = None,
) -> dict[str, object]:
    result: dict[str, object] = {
        "format": fmt,
        "skill": skill,
        "subskill": subskill,
        "difficulty": difficulty,
        "lemma": lemma,
        "prompt": prompt,
        "explanation": explanation,
    }
    if expected is not None:
        result["expected"] = expected
    if choices is not None:
        result["choices"] = choices
    if answer is not None:
        result["answer"] = answer
    return result


# Questions classées par TYPE (demande utilisateur), puis distribuées par blocs.
FORMAT_ITEMS: dict[str, list[dict[str, object]]] = {
    "short_answer": [
        _item("short_answer", "participe", "regulier-er", 1, "chanter", "Complète : J'ai ____ une chanson.", "1er groupe en -er : chanté.", expected=["chanté"]),
        _item("short_answer", "participe", "regulier-er", 1, "jouer", "Complète : Nous avons ____ au ballon.", "1er groupe : joué.", expected=["joué"]),
        _item("short_answer", "participe", "regulier-er", 1, "nettoyer", "Complète : Tu as ____ ta chambre.", "Participe de nettoyer : nettoyé.", expected=["nettoyé"]),
        _item("short_answer", "participe", "regulier-ir", 1, "finir", "Complète : Ils ont ____ leurs devoirs.", "2e groupe : fini.", expected=["fini"]),
        _item("short_answer", "participe", "regulier-ir", 1, "grandir", "Complète : Elle a ____ vite.", "2e groupe : grandi.", expected=["grandi"]),
        _item("short_answer", "participe", "regulier-ir", 1, "réussir", "Complète : Vous avez ____ le test.", "2e groupe : réussi.", expected=["réussi", "reussi"]),
        _item("short_answer", "participe", "irregulier-u", 2, "voir", "Complète : J'ai ____ un film.", "Participe de voir : vu.", expected=["vu"]),
        _item("short_answer", "participe", "irregulier-is", 2, "prendre", "Complète : Nous avons ____ le train.", "Participe de prendre : pris.", expected=["pris"]),
        _item("short_answer", "participe", "irregulier-it", 2, "écrire", "Complète : Tu as ____ une lettre.", "Participe de écrire : écrit.", expected=["écrit", "ecrit"]),
        _item("short_answer", "participe", "irregulier-divers", 2, "mettre", "Complète : Elle a ____ sa veste.", "Participe de mettre : mis.", expected=["mis"]),
        _item("short_answer", "participe", "irregulier-divers", 2, "dire", "Complète : Vous avez ____ la vérité.", "Participe de dire : dit.", expected=["dit"]),
        _item("short_answer", "participe", "irregulier-divers", 2, "avoir", "Complète : Ils ont ____ de la chance.", "Participe de avoir : eu.", expected=["eu"]),
    ],
    "qcm": [
        _item("qcm", "participe", "regulier-er", 1, "regarder", "Choisis : Tu as ____ le match.", "Avec avoir : regardé.", choices=["regardé", "regarder", "regardais"], answer=1),
        _item("qcm", "participe", "irregulier", 2, "faire", "Choisis : Il a ____ ses exercices.", "Participe de faire : fait.", choices=["fait", "fais", "failli"], answer=1),
        _item("qcm", "participe", "irregulier", 2, "prendre", "Choisis : Nous avons ____ un taxi.", "On écrit pris (pas prix).", choices=["prix", "pris", "prend"], answer=2),
        _item("qcm", "auxiliaire", "avoir_etre", 3, "aller", "Choisis l'auxiliaire : Elles ____ allées au parc.", "Aller avec être : sont.", choices=["ont", "sont", "avaient"], answer=2),
        _item("qcm", "auxiliaire", "avoir_etre", 3, "manger", "Choisis l'auxiliaire : Nous ____ mangé tôt.", "Manger avec avoir : avons.", choices=["sommes", "avons", "étions"], answer=2),
        _item("qcm", "auxiliaire", "avoir_etre", 3, "venir", "Choisis l'auxiliaire : Ils ____ venus hier.", "Venir avec être : sont.", choices=["ont", "sont", "avaient"], answer=2),
        _item("qcm", "accord", "etre", 4, "partir", "Choisis la phrase correcte.", "Avec être et sujet pluriel : partis.", choices=["Ils sont partis tôt.", "Ils sont parti tôt.", "Ils ont partis tôt."], answer=1),
        _item("qcm", "accord", "etre", 4, "arriver", "Choisis la phrase correcte.", "Elles sont arrivées (accord au féminin pluriel).", choices=["Elles sont arrivées.", "Elles sont arrivé.", "Elles ont arrivées."], answer=1),
        _item("qcm", "accord", "avoir_cod_ant", 4, "écrire", "Choisis : Les lettres que j'ai ____ sont longues.", "COD antéposé avec avoir : écrites.", choices=["écrit", "écrites", "écrits"], answer=2),
        _item("qcm", "infinitif", "identification", 1, "grandir", "Infinitif de « ils ont grandi » ?", "Le participe grandi vient de grandir.", choices=["grandir", "grander", "grandi"], answer=1),
        _item("qcm", "infinitif", "identification", 1, "venu", "Infinitif de « elle est venue » ?", "Venue vient de venir.", choices=["venir", "venue", "vendre"], answer=1),
        _item("qcm", "infinitif", "identification", 1, "dit", "Infinitif de « nous avons dit » ?", "Dit vient de dire.", choices=["dire", "dit", "dîner"], answer=1),
    ],
    "rewrite": [
        _item("rewrite", "auxiliaire", "transformation", 3, "venir", "Réécris au passé composé : « Elles viennent tôt. »", "Venir avec être : elles sont venues.", expected=["elles sont venues tôt", "elles sont venues tot"]),
        _item("rewrite", "auxiliaire", "transformation", 3, "manger", "Réécris au passé composé : « Nous mangeons au restaurant. »", "Manger avec avoir : nous avons mangé.", expected=["nous avons mangé au restaurant", "nous avons mange au restaurant"]),
        _item("rewrite", "participe", "irregulier", 2, "prendre", "Réécris au passé composé : « Je prends le bus. »", "Prendre → j'ai pris.", expected=["j'ai pris le bus", "jai pris le bus"]),
        _item("rewrite", "participe", "irregulier", 2, "voir", "Réécris au passé composé : « Tu vois la mer. »", "Voir → tu as vu.", expected=["tu as vu la mer"]),
        _item("rewrite", "accord", "etre", 4, "aller", "Réécris au passé composé : « Elles vont à l'école. »", "Aller avec être + accord : elles sont allées.", expected=["elles sont allées à l'école", "elles sont allées a l'école", "elles sont allees a l'ecole", "elles sont allées à l'ecole"]),
        _item("rewrite", "accord", "etre", 4, "naître", "Réécris au passé composé : « Ils naissent en 2010. »", "Naître avec être : ils sont nés.", expected=["ils sont nés en 2010", "ils sont nes en 2010"]),
    ],
    "correction": [
        _item("correction", "accord", "etre", 4, "arriver", "Corrige : « Elles sont arrivé en avance. »", "Avec être : accord au féminin pluriel, arrivées.", expected=["elles sont arrivées en avance", "elles sont arrivees en avance"]),
        _item("correction", "accord", "avoir_cod_ant", 4, "écrire", "Corrige : « Les lettres que j'ai écrit sont longues. »", "Avec avoir + COD avant : écrites.", expected=["les lettres que j'ai écrites sont longues", "les lettres que j'ai ecrites sont longues"]),
        _item("correction", "accord", "etre", 4, "venir", "Corrige : « Ils sont venue hier. »", "Sujet masculin pluriel avec être : venus.", expected=["ils sont venus hier"]),
        _item("correction", "participe", "irregulier", 2, "mettre", "Corrige : « J'ai met mon manteau. »", "Participe de mettre : mis.", expected=["j'ai mis mon manteau", "jai mis mon manteau"]),
        _item("correction", "participe", "irregulier", 2, "faire", "Corrige : « Nous avons fais nos devoirs. »", "Participe de faire : fait.", expected=["nous avons fait nos devoirs"]),
        _item("correction", "auxiliaire", "avoir_etre", 3, "partir", "Corrige : « Elle a partie tôt. »", "Partir avec être : elle est partie.", expected=["elle est partie tôt", "elle est partie tot"]),
    ],
    "infinitif": [
        _item("infinitif", "infinitif", "identification", 1, "grandir", "Donne l'infinitif : « Elles ont grandi vite. »", "Grandi vient de grandir.", expected=["grandir"]),
        _item("infinitif", "infinitif", "identification", 1, "écrire", "Donne l'infinitif : « J'ai écrit une carte. »", "Écrit vient de écrire.", expected=["écrire", "ecrire"]),
        _item("infinitif", "infinitif", "identification", 1, "venir", "Donne l'infinitif : « Nous sommes venus hier. »", "Venus vient de venir.", expected=["venir"]),
        _item("infinitif", "infinitif", "identification", 1, "mettre", "Donne l'infinitif : « Tu as mis ta veste. »", "Mis vient de mettre.", expected=["mettre"]),
        _item("infinitif", "infinitif", "identification", 1, "voir", "Donne l'infinitif : « Ils ont vu ce musée. »", "Vu vient de voir.", expected=["voir"]),
        _item("infinitif", "infinitif", "identification", 1, "dire", "Donne l'infinitif : « Vous avez dit oui. »", "Dit vient de dire.", expected=["dire"]),
    ],
}

BLOCK_SPECS: dict[str, tuple[tuple[str, int], ...]] = {
    "A": (("short_answer", 6), ("qcm", 2), ("infinitif", 2)),
    "B": (("short_answer", 4), ("qcm", 4), ("rewrite", 2)),
    "C": (("qcm", 4), ("rewrite", 2), ("correction", 2)),
    "D": (("correction", 4), ("qcm", 3), ("rewrite", 2), ("infinitif", 1)),
}

BLOCK_ORDER = ["A", "B", "C", "D"]


def _normalize(text: str) -> str:
    cleaned = text.strip().lower().replace("’", "'")
    return " ".join(cleaned.split())


def _pick_items(fmt: str, count: int) -> list[dict[str, object]]:
    pool = list(FORMAT_ITEMS[fmt])
    if count >= len(pool):
        return pool
    return random.sample(pool, count)


def _build_block_items(block_name: str) -> list[dict[str, object]]:
    result: list[dict[str, object]] = []
    for fmt, count in BLOCK_SPECS[block_name]:
        result.extend(_pick_items(fmt, count))
    random.shuffle(result)
    return result


def _ask_item(item: dict[str, object]) -> bool:
    print(f"\n➡️ {item['prompt']}")
    fmt = item["format"]

    if fmt == "qcm":
        choices: list[str] = item["choices"]  # type: ignore[assignment]
        for i, choice in enumerate(choices, start=1):
            print(f"  {i}. {choice}")
        raw = input("Ton choix (1/2/3) : ").strip()
        if raw not in {"1", "2", "3"}:
            print("❌ Réponse invalide (1, 2 ou 3 attendus).")
            print(f"ℹ️ {item['explanation']}")
            return False
        success = int(raw) == item["answer"]
    else:
        answer = _normalize(input("Ta réponse : "))
        expected = [_normalize(x) for x in item["expected"]]  # type: ignore[index]
        success = answer in expected

    if success:
        print("✅ Correct !")
    else:
        print("❌ Incorrect.")
        print(f"ℹ️ {item['explanation']}")
    return success


def _run_block(block_name: str, questions: list[dict[str, object]], stats: dict[str, Counter]) -> tuple[int, int]:
    print(f"\n===== Bloc {block_name} ({len(questions)} questions) =====")
    score = 0
    for item in questions:
        ok = _ask_item(item)
        skill = str(item["skill"])
        subskill = str(item["subskill"])
        stats[skill]["total"] += 1
        stats[skill]["success"] += int(ok)
        stats[skill][f"subskill:{subskill}"] += int(not ok)
        if ok:
            score += 1
    print(f"Bloc {block_name} : {score}/{len(questions)}")
    return score, len(questions)


def _print_diagnostic(stats: dict[str, Counter]) -> None:
    print("\n📊 Diagnostic par compétence")
    for skill in SKILLS:
        total = stats[skill]["total"]
        success = stats[skill]["success"]
        pct = (success / total * 100) if total else 0.0
        print(f"- {skill.capitalize():<10}: {success}/{total} ({pct:.1f} %) ")

    errors: list[tuple[int, str, str]] = []
    for skill in SKILLS:
        for key, value in stats[skill].items():
            if key.startswith("subskill:") and value > 0:
                errors.append((value, skill, key.removeprefix("subskill:")))
    errors.sort(reverse=True)

    print("\n🔎 Top erreurs")
    if not errors:
        print("- Aucune erreur récurrente : excellent travail !")
    else:
        for count, skill, subskill in errors[:3]:
            print(f"- {skill}/{subskill} : {count} erreur(s)")


def main() -> None:
    show_lesson(LESSON)
    mode = input("Choisis le mode : (E)ntraînement ou É(v)aluation : ").strip().lower()

    total_score = 0
    total_questions = 0
    stats: dict[str, Counter] = defaultdict(Counter)

    for block in BLOCK_ORDER:
        questions = _build_block_items(block)
        score, block_total = _run_block(block, questions, stats)
        total_score += score
        total_questions += block_total

        pct = score / block_total * 100 if block_total else 0
        if pct < 75:
            print("🛠️ Remédiation : 4 questions ciblées supplémentaires.")
            remedial = questions[:4]
            r_score, r_total = _run_block(f"{block} (remédiation)", remedial, stats)
            total_score += r_score
            total_questions += r_total

    percentage = total_score / total_questions * 100 if total_questions else 0.0
    print(f"\n🎯 Score global : {total_score}/{total_questions} ({percentage:.1f} %) ")
    if mode == "v":
        print("\nℹ️ Mode évaluation : diagnostic en fin de session.")
    else:
        print("\nℹ️ Mode entraînement : feedback immédiat activé.")

    _print_diagnostic(stats)
    log_result("francais_passe_compose_terminaisons", percentage)


if __name__ == "__main__":
    main()
