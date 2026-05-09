# Optimisation de la Production d'une Pâtisserie
**Projet : Programmation Linéaire & Python**  
**3ème année – Ingénierie Informatique et Réseaux | Année universitaire 2025–2026**

---

## Membres du groupe
- Abdorrahman Douelkaoui
- Farouq Aouad
- Yassir Limni
- Youness Fetouaki
- Ammer Reffouch

**Encadré par :** Dr. Abdelati REHA & Dr. Yassine SAFSOUF

---

## Description du projet

Ce projet applique la **programmation linéaire** pour optimiser la production quotidienne d'une pâtisserie artisanale. L'objectif est de maximiser le profit journalier en respectant les contraintes de ressources (farine, four, main-d'œuvre, beurre).

---

## Structure du dépôt

```
patisserie-optimisation/
│
├── README.md                      ← Ce fichier
│
├── rapport/
│   └── Rapport_Projet_PL_Python_Patisserie.docx
│
└── code/
    ├── patisserie_2var.py          ← Modèle 2 variables + visualisation graphique
    ├── patisserie_3var_scipy.py    ← Modèle 3 variables avec SciPy
    ├── patisserie_3var_pulp.py     ← Modèle 3 variables avec PuLP
    └── patisserie_simplexe.py      ← Méthode Simplexe implémentée from scratch
```

---

## Description des fichiers Python

### `patisserie_2var.py`
- Résout le modèle à **2 variables** (croissants, pains au chocolat)
- Utilise `scipy.optimize.linprog`
- Génère une **visualisation graphique** de la région réalisable avec Matplotlib
- **Résultat** : x1=0, x2=150, Z*=1200 DH

### `patisserie_3var_scipy.py`
- Résout le modèle étendu à **3 variables** (+ tartes aux fruits)
- Utilise `scipy.optimize.linprog`
- Affiche les valeurs marginales (shadow prices)
- **Résultat** : x1=0, x2=200, x3=0, Z*=1600 DH

### `patisserie_3var_pulp.py`
- Résout le modèle à **3 variables** en variables entières (MIP)
- Utilise la bibliothèque `PuLP` (modélisation déclarative)
- Affiche les coûts réduits et valeurs marginales
- **Résultat** : x1=0, x2=200, x3=0, Z*=1600 DH

### `patisserie_simplexe.py`
- **Implémentation from scratch** de l'algorithme du Simplexe en Python/NumPy
- Affiche chaque itération du tableau Simplexe (pédagogique)
- Vérification croisée avec SciPy
- **Résultat** : Converge en 3 itérations, Z*=1600 DH

---

## Installation des dépendances

```bash
pip install numpy scipy matplotlib pulp
```

---

## Exécution

```bash
# Modèle 2 variables (génère aussi un graphique PNG)
python code/patisserie_2var.py

# Modèle 3 variables - SciPy
python code/patisserie_3var_scipy.py

# Modèle 3 variables - PuLP
python code/patisserie_3var_pulp.py

# Méthode Simplexe manuelle
python code/patisserie_simplexe.py
```

---

## Résultats principaux

| Modèle | x1 (Croissants) | x2 (Pains choc.) | x3 (Tartes) | Profit Z* |
|--------|:-:|:-:|:-:|:-:|
| 2 variables (graphique) | 0 | 150 | — | **1 200 DH** |
| 3 variables (SciPy/PuLP) | 0 | 200 | 0 | **1 600 DH** |
| Simplexe (from scratch) | 0 | 200 | 0 | **1 600 DH** |





