"""Leçon et quiz interactif sur les tables de multiplication de 1 à 9."""

from __future__ import annotations

import random


def afficher_tables() -> None:
    """Affiche les tables de multiplication de 1 à 9."""

    print("Tables de multiplication de 1 à 9\n")
    for i in range(1, 10):
        print(f"Table de {i} :")
        for j in range(1, 10):
            print(f"  {i} x {j} = {i * j}")
        print()


def generer_propositions(resultat: int) -> list[int]:
    """Retourne trois propositions dont une correcte."""

    autres = [n for n in range(1, 82) if n != resultat]
    propositions = random.sample(autres, 2) + [resultat]
    random.shuffle(propositions)
    return propositions


def poser_question(table: int, multiplicateur: int) -> bool:
    """Pose une question et renvoie True si la réponse est correcte."""

    resultat = table * multiplicateur
    propositions = generer_propositions(resultat)
    print(f"\nCombien font {table} x {multiplicateur} ?")
    for i, choix in enumerate(propositions, start=1):
        print(f"  {i}. {choix}")
    reponse = input("Votre réponse : ")
    try:
        index = int(reponse) - 1
    except ValueError:
        index = -1
    if 0 <= index < 3 and propositions[index] == resultat:
        print("✔️ Bonne réponse !")
        return True
    print(f"❌ Mauvaise réponse. La bonne réponse était {resultat}.")
    return False


def entrainer_table(table: int) -> None:
    """Entraîne l'utilisateur sur la table donnée."""

    while True:
        mode = input(
            "Choisis le mode : 1. ordre séquentiel 2. ordre aléatoire\nVotre choix : "
        ).strip()
        if mode in {"1", "2"}:
            break
        print("Choix invalide.\n")

    multiplicateurs = list(range(1, 10))
    if mode == "2":
        random.shuffle(multiplicateurs)

    score = 0
    for m in multiplicateurs:
        if poser_question(table, m):
            score += 1

    print(f"\nScore final : {score}/9")


def main() -> None:
    """Présente les tables puis permet de s'entraîner."""

    afficher_tables()
    while True:
        choix = input("Quelle table veux-tu pratiquer ? (1-9) ").strip()
        try:
            table = int(choix)
        except ValueError:
            table = 0
        if 1 <= table <= 9:
            break
        print("Choix invalide.\n")

    entrainer_table(table)


if __name__ == "__main__":
    main()

