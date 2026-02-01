# Exercices pour l'école

Ce dépôt contient un programme `exercices` permettant d'exécuter différents exercices.

Le menu propose plusieurs exercices :
- `anglais_hello_world` affiche `hello world!`
- `anglais_jours_semaine` propose une leçon et un quiz pour apprendre les jours de la semaine en anglais et leurs origines mythologiques ou célestes.
- `anglais_alphabet_couleurs` propose une leçon et plusieurs exercices pour reconnaître l'alphabet à l'oral, écrire les couleurs et se présenter.
- `hist_test` affiche `La préhistoire c'est ce qu'il y a avant l'histoire.`
- `physique_changements_etats` propose une leçon et un quiz sur les changements d'état de la matière.
- `physique_proprietes_eau_liquide` propose une leçon et un quiz sur quelques propriétés de l'eau liquide.
- `math_tables_multiplication` propose une leçon et un quiz interactif pour pratiquer une table de multiplication.
- `geometrie_notation` propose une leçon et un quiz sur les segments, droites et demi-droites.
- `musique_cest_quoi` propose une leçon colorée et un quiz pour découvrir la portée, les notes et les rythmes.
- `sciences_vivant_non_vivant` propose une leçon et un quiz pour classer les éléments en vivant, naturel non vivant ou fabriqué par l'humain.
- `francais_cloze_dictations` fournit un atelier TUI pour créer et pratiquer des dictées à trous avec gestion des textes, des clozes et des tentatives élèves.
- `francais_present_imperatif` propose une leçon et un quiz sur le présent de l'impératif.

Le menu propose également une option pour mettre à jour le logiciel. Elle exécute `git pull`, met à jour les dépendances Python, puis redémarre le programme.

## Première installation

Avant la première exécution, installez les dépendances optionnelles décrites dans `requirements.txt` :

```bash
python -m pip install -r requirements.txt
```

Sur Windows cette commande installe automatiquement `windows-curses`, nécessaire pour l'exercice interactif de musique.

## Exécuter

```bash
python -m exercices
```
