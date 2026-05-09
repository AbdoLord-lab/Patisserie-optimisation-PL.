from pulp import *

# =============================================================================
# OPTIMISATION DE LA PRODUCTION D'UNE PATISSERIE - MODELE A 3 VARIABLES (PULP)
# =============================================================================
# Extension du modele avec un 3eme produit : Tarte aux fruits (x3)
# Profit unitaire : Croissant = 5 DH, Pain au chocolat = 8 DH, Tarte = 13 DH
# Installation requise : pip install pulp

print("=" * 60)
print("MODELE A 3 VARIABLES - RESOLUTION AVEC PULP (COIN-OR CBC)")
print("=" * 60)

# Creation du modele de maximisation
modele = LpProblem("Patisserie_Optimisation_3Produits", LpMaximize)

# Variables de decision
# cat=Integer pour des quantites entieres (plus realiste pour des patisseries)
x1 = LpVariable("Croissants", lowBound=0, cat='Integer')
x2 = LpVariable("Pains_au_chocolat", lowBound=0, cat='Integer')
x3 = LpVariable("Tartes_aux_fruits", lowBound=0, cat='Integer')

# Fonction objectif
modele += 5*x1 + 8*x2 + 13*x3, "Profit_Total_Journalier"

# Contraintes de ressources
modele += 0.15*x1 + 0.20*x2 + 0.30*x3 <= 45, "Contrainte_Farine"
modele += 10*x1 + 12*x2 + 20*x3 <= 2400, "Contrainte_Four"
modele += 5*x1 + 8*x2 + 15*x3 <= 1800, "Contrainte_Main_d_oeuvre"
modele += 50*x1 + 80*x2 + 120*x3 <= 18000, "Contrainte_Beurre"

# Resolution avec le solveur CBC
modele.solve(PULP_CBC_CMD(msg=1, timeLimit=30))

# Affichage des resultats
print()
print(">>> STATUT DE LA RESOLUTION : %s <<<" % LpStatus[modele.status])
print("-" * 60)
print("%-25s %10s %12s %12s" % ("Produit", "Quantite", "Profit unit.", "Profit total"))
print("-" * 60)

profit_x1 = 5 * value(x1)
profit_x2 = 8 * value(x2)
profit_x3 = 13 * value(x3)

print("%-25s %10.0f %12s %11.0f DH" % ("Croissants (x1)", value(x1), "5 DH", profit_x1))
print("%-25s %10.0f %12s %11.0f DH" % ("Pains au chocolat (x2)", value(x2), "8 DH", profit_x2))
print("%-25s %10.0f %12s %11.0f DH" % ("Tartes aux fruits (x3)", value(x3), "13 DH", profit_x3))
print("-" * 60)
print("%-25s %10s %12s %11.0f DH" % ("PROFIT MAXIMUM JOURNALIER", "", "", value(modele.objective)))
print("=" * 60)

# Analyse des contraintes
print()
print(">>> ANALYSE DES CONTRAINTES (Ecarts et Valeurs marginales) <<<")
print("%-25s %10s %10s %10s %16s" % ("Contrainte", "Utilise", "Dispo.", "Ecart", "Valeur marginale"))
print("-" * 75)

contraintes_info = [
    ("Farine (kg)", 45),
    ("Four (min)", 2400),
    ("Main-d'oeuvre (min)", 1800),
    ("Beurre (g)", 18000)
]

for (nom, dispo), (nom_contrainte, contrainte) in zip(contraintes_info, modele.constraints.items()):
    utilise = value(contrainte)
    ecart = dispo - utilise
    shadow_price = "%.4f" % contrainte.pi if hasattr(contrainte, 'pi') and contrainte.pi is not None else "N/A"
    print("%-25s %10.2f %10.0f %10.2f %16s" % (nom, utilise, dispo, ecart, shadow_price))

# Couts reduits
print()
print(">>> COUTS REDUITS (Reduced Costs) <<<")
print("%-25s %15s %12s" % ("Variable", "Valeur optimale", "Cout reduit"))
print("-" * 55)
for v in [x1, x2, x3]:
    rc = v.dj if hasattr(v, 'dj') and v.dj is not None else "N/A"
    print("%-25s %15.0f %12s" % (v.name, value(v), rc))

print()
print(">>> INTERPRETATION ECONOMIQUE <<<")
print("- Le cout reduit indique de combien diminuerait le profit si on etait")
print("  contraint de produire une unite d'un produit non present dans la")
print("  solution optimale (ou de combien il faudrait augmenter son profit")
print("  unitaire pour le rendre attractif).")
