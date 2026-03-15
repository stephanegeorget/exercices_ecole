# Exercices pour l'école

Ce dépôt contient un programme `exercices` permettant d'exécuter différents exercices.

Le menu propose plusieurs exercices :
- `anglais_hello_world` affiche `hello world!`
- `anglais_jours_semaine` propose une leçon et un quiz pour apprendre les jours de la semaine en anglais et leurs origines mythologiques ou célestes.
- `anglais_alphabet_couleurs` propose une leçon et plusieurs exercices pour reconnaître l'alphabet à l'oral, écrire les couleurs et se présenter.
- `anglais_school_uniform` propose 30 fiches de vocabulaire sur l'uniforme scolaire avec descriptions en français, deux quiz à choix multiples avec flèches, puis une recopie guidée avec tirets bas.
- `hist_test` affiche `La préhistoire c'est ce qu'il y a avant l'histoire.`
- `physique_changements_etats` propose une leçon et un quiz sur les changements d'état de la matière.
- `physique_proprietes_eau_liquide` propose une leçon et un quiz sur quelques propriétés de l'eau liquide.
- `math_tables_multiplication` propose une leçon et un quiz interactif pour pratiquer une table de multiplication.
- `math_association_facteurs_images` propose un quiz guidé inspiré d'une fiche en photo, avec associations astucieuses, flèches et parenthèses mises en évidence (3 questions par calcul).
- `geometrie_notation` propose une leçon et un quiz sur les segments, droites et demi-droites.
- `musique_cest_quoi` propose une leçon colorée et un quiz pour découvrir la portée, les notes et les rythmes.
- `sciences_vivant_non_vivant` propose une leçon et un quiz pour classer les éléments en vivant, naturel non vivant ou fabriqué par l'humain.
- `geographie_habiter_espaces_agricoles` propose une leçon et un quiz de 40 questions sur les espaces agricoles à faibles densités (Grandes Plaines et Bornéo).
- `francais_cloze_dictations` fournit un atelier TUI pour créer et pratiquer des dictées à trous avec gestion des textes, des clozes et des tentatives élèves.
- `francais_present_imperatif` propose une leçon et un quiz sur le présent de l'impératif.
- `francais_imparfait_indicatif` propose une leçon sur l'imparfait et un quiz à trous où l'élève complète les terminaisons, avec sélection des groupes de verbes à inclure.
- `francais_homophones_ai_es_est_et_son_sont` propose une leçon et deux quiz de 15 questions chacun sur les homophones grammaticaux `ai/es/est/et` et `son/sont`.

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
