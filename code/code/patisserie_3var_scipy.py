import numpy as np
from scipy.optimize import linprog

# =============================================================================
# OPTIMISATION DE LA PRODUCTION D'UNE PATISSERIE - MODELE A 3 VARIABLES
# =============================================================================
# Extension du modele avec un 3eme produit : Tarte aux fruits (x3)
# Profit unitaire : Croissant = 5 DH, Pain au chocolat = 8 DH, Tarte = 13 DH

print("=" * 60)
print("MODELE A 3 VARIABLES - RESOLUTION AVEC SCIPY.OPTIMIZE.LINPROG")
print("=" * 60)

# Coefficients de la fonction objectif (negatifs car linprog minimise)
c = [-5, -8, -13]

# Matrice des contraintes (A_ub @ x <= b_ub)
A = [
    [0.15, 0.20, 0.30],   # Farine (kg)
    [10.0, 12.0, 20.0],   # Four (minutes)
    [5.0,  8.0,  15.0],   # Main-d'oeuvre (minutes)
    [50.0, 80.0, 120.0]   # Beurre (grammes)
]

# Membres droits (ressources disponibles journalierement)
b = [45, 2400, 1800, 18000]

# Bornes des variables (non-negativite)
x_bounds = [(0, None), (0, None), (0, None)]

# Resolution avec la methode highs
result = linprog(c, A_ub=A, b_ub=b, bounds=x_bounds, method='highs')

# Affichage des resultats
print()
print(">>> SOLUTION OPTIMALE <<<")
print("-" * 60)
print("%-25s %10s %12s %12s" % ("Produit", "Quantite", "Profit unit.", "Profit total"))
print("-" * 60)

profit_x1 = 5 * result.x[0]
profit_x2 = 8 * result.x[1]
profit_x3 = 13 * result.x[2]

print("%-25s %10.0f %12s %11.0f DH" % ("Croissants (x1)", result.x[0], "5 DH", profit_x1))
print("%-25s %10.0f %12s %11.0f DH" % ("Pains au chocolat (x2)", result.x[1], "8 DH", profit_x2))
print("%-25s %10.0f %12s %11.0f DH" % ("Tartes aux fruits (x3)", result.x[2], "13 DH", profit_x3))
print("-" * 60)
print("%-25s %10s %12s %11.0f DH" % ("PROFIT MAXIMUM JOURNALIER", "", "", -result.fun))
print("=" * 60)

# Verification des contraintes
print()
print(">>> VERIFICATION DES CONTRAINTES <<<")
print("%-25s %10s %10s %10s" % ("Contrainte", "Utilise", "Dispo.", "Ecart"))
print("-" * 60)

labels = ["Farine (kg)", "Four (min)", "Main-d'oeuvre (min)", "Beurre (g)"]
for i, (label, ai, bi) in enumerate(zip(labels, A, b)):
    used = ai[0]*result.x[0] + ai[1]*result.x[1] + ai[2]*result.x[2]
    print("%-25s %10.2f %10.0f %10.2f" % (label, used, bi, bi-used))

# Analyse des valeurs marginales (shadow prices)
print()
print(">>> VALEURS MARGINALES (Shadow Prices) <<<")
print("Ces valeurs indiquent de combien augmenterait le profit optimal")
print("si l'on disposait d'une unite supplementaire de chaque ressource.")
print()

if hasattr(result, 'ineqlin') and hasattr(result.ineqlin, 'marginals'):
    for i, label in enumerate(labels):
        print("%-25s : %.4f DH/%s" % (label, result.ineqlin.marginals[i], label.split()[-1].strip('()')))
else:
    print("Valeurs marginales non disponibles avec ce solveur.")

print()
print(">>> INTERPRETATION ECONOMIQUE <<<")
print("- Le modele a 3 variables confirme l'efficacite de la programmation lineaire")
print("  pour resoudre des problemes de production multi-produits.")
print("- La solution optimale indique la repartition ideale des ressources")
print("  entre les trois produits pour maximiser le profit.")
