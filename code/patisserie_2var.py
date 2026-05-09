import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linprog

# =============================================================================
# OPTIMISATION DE LA PRODUCTION D'UNE PATISSERIE - MODELE A 2 VARIABLES
# =============================================================================
# Probleme : Maximiser le profit journalier
# Variables : x1 = croissants, x2 = pains au chocolat
# Profit unitaire : Croissant = 5 DH, Pain au chocolat = 8 DH

print("=" * 60)
print("MODELE A 2 VARIABLES - RESOLUTION PAR SCIPY.OPTIMIZE.LINPROG")
print("=" * 60)

# Coefficients de la fonction objectif (negatifs car linprog minimise)
c = [-5, -8]

# Matrice des contraintes (A_ub @ x <= b_ub)
# Ordre des contraintes : Farine, Four, Main-d'oeuvre, Beurre
A = [
    [0.15, 0.20],   # Farine (kg)
    [10, 12],       # Four (minutes)
    [5, 8],         # Main-d'oeuvre (minutes)
    [50, 80]        # Beurre (grammes)
]

# Membres droits (ressources disponibles journalierement)
b = [30, 1800, 1200, 12000]

# Bornes des variables (non-negativite)
x_bounds = [(0, None), (0, None)]

# Resolution avec la methode highs (algorithme du simplexe moderne)
result = linprog(c, A_ub=A, b_ub=b, bounds=x_bounds, method='highs')

# Affichage des resultats
print()
print(">>> SOLUTION OPTIMALE <<<")
print("Nombre de croissants (x1)       : %.0f" % result.x[0])
print("Nombre de pains au chocolat (x2): %.0f" % result.x[1])
print("Profit maximum (Z)              : %.2f DH" % (-result.fun))
print("Statut de la resolution         : %s" % ("Optimal" if result.success else "Echec"))

# Verification des contraintes
print()
print(">>> VERIFICATION DES CONTRAINTES <<<")
labels = ["Farine (kg)", "Four (min)", "Main-d'oeuvre (min)", "Beurre (g)"]
for i, (label, ai, bi) in enumerate(zip(labels, A, b)):
    used = ai[0]*result.x[0] + ai[1]*result.x[1]
    print("%-20s : utilise = %8.2f / disponible = %8.0f | Ecart = %8.2f" % (label, used, bi, bi-used))

# =============================================================================
# VISUALISATION GRAPHIQUE DE LA REGION REALISABLE
# =============================================================================
x1 = np.linspace(0, 250, 500)

# Equations des droites frontieres (en posant l'egalite)
x2_farine = (30 - 0.15*x1) / 0.20
x2_four = (1800 - 10*x1) / 12
x2_main = (1200 - 5*x1) / 8
x2_beurre = (12000 - 50*x1) / 80

plt.figure(figsize=(11, 8))

# Trace des droites de contrainte
plt.plot(x1, x2_farine, 'b-', linewidth=2, label='Farine : 0.15x1 + 0.20x2 <= 30')
plt.plot(x1, x2_four, 'g-', linewidth=2, label='Four : 10x1 + 12x2 <= 1800')
plt.plot(x1, x2_main, 'r-', linewidth=2, label="Main-d'oeuvre : 5x1 + 8x2 <= 1200")
plt.plot(x1, x2_beurre, 'orange', linewidth=2, label='Beurre : 50x1 + 80x2 <= 12000')

# Remplissage de la region realisable (intersection des demi-plans)
x2_limit = np.minimum(np.minimum(x2_farine, x2_four), np.minimum(x2_main, x2_beurre))
x2_limit = np.maximum(x2_limit, 0)
plt.fill_between(x1, 0, x2_limit, where=(x2_limit >= 0),
                  alpha=0.25, color='purple', label='Region realisable')

# Trace du point optimal
plt.scatter(result.x[0], result.x[1], color='black', s=200, zorder=5,
             marker='*', label='Optimum A(%.0f, %.0f)' % (result.x[0], result.x[1]))

# Annotation du point optimal
annotation_text = "Z* = %.0f DH\n(%.0f, %.0f)" % (-result.fun, result.x[0], result.x[1])
plt.annotate(annotation_text,
              xy=(result.x[0], result.x[1]), xytext=(result.x[0]+15, result.x[1]-20),
             fontsize=11, fontweight='bold',
             arrowprops=dict(arrowstyle='->', color='black'))

# Trace des droites d'isoprofit (Z = 5x1 + 8x2 = constante)
for z_val in [400, 800, 1200]:
    x2_iso = (z_val - 5*x1) / 8
    plt.plot(x1, x2_iso, '--', color='gray', alpha=0.6, linewidth=1)
    x_text = 220
    y_text = (z_val - 5*x_text) / 8
    if 0 <= y_text <= 180:
        plt.text(x_text, y_text, 'Z=%d' % z_val, fontsize=9, color='dimgray')

plt.xlim(0, 250)
plt.ylim(0, 180)
plt.xlabel('x1 : Nombre de croissants', fontsize=12)
plt.ylabel('x2 : Nombre de pains au chocolat', fontsize=12)
plt.title("Optimisation de la Production d'une Patisserie - Methode Graphique (Matplotlib)",
           fontsize=14, fontweight='bold')
plt.legend(loc='upper right', fontsize=9)
plt.grid(True, alpha=0.3)
plt.axhline(0, color='black', linewidth=0.5)
plt.axvline(0, color='black', linewidth=0.5)
plt.tight_layout()
plt.savefig('graphique_2var.png', dpi=200, bbox_inches='tight')
plt.show()

print()
print(">>> Graphique sauvegarde sous graphique_2var.png")
