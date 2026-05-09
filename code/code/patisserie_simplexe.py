import numpy as np

# =============================================================================
# METHODE SIMPLEXE - IMPLEMENTATION PYTHON FROM SCRATCH
# =============================================================================
# Resout un probleme de maximisation sous forme canonique :
#   Max Z = c^T * x
#   s.c.  A * x <= b
#         x >= 0
#
# L'algorithme transforme le probleme en forme standard par l'ajout de
# variables d'ecart, puis itere sur les tableaux jusqu'a l'optimalite.


class SimplexSolver:
    """
    Solveur Simplexe pour probleme de maximisation.

    Parametres :
    -----------
    A : ndarray de shape (m, n)
        Matrice des coefficients techniques des contraintes
    b : ndarray de shape (m,)
        Vecteur des ressources disponibles (membres droits)
    c : ndarray de shape (n,)
        Vecteur des profits unitaires (coefficients de la fonction objectif)
    """

    def __init__(self, A, b, c):
        self.m, self.n = A.shape

        # Construction du tableau initial (forme standard)
        # [ A | I_m | b ]
        # [ -c^T | 0_m | 0 ]
        tableau_width = self.n + self.m + 1  # vars de decision + vars d'ecart + RHS
        self.tableau = np.zeros((self.m + 1, tableau_width))

        # Partie contraintes
        self.tableau[:self.m, :self.n] = A
        self.tableau[:self.m, self.n:self.n + self.m] = np.eye(self.m)
        self.tableau[:self.m, -1] = b

        # Ligne objectif (derniere ligne)
        self.tableau[self.m, :self.n] = -c

        # Variables en base (initialement les variables d'ecart s1, s2, ...)
        self.basic_vars = list(range(self.n, self.n + self.m))
        # Variables hors base (initialement les variables de decision x1, x2, ...)
        self.non_basic_vars = list(range(self.n))

        self.iteration = 0

    def solve(self, verbose=True):
        """Execute l'algorithme du Simplexe et retourne la solution optimale."""
        if verbose:
            print("=" * 70)
            print("         ALGORITHME DU SIMPLEXE - RESOLUTION PAS A PAS")
            print("=" * 70)
            c_vals = -self.tableau[self.m, :self.n]
            print("\nProbleme : Max Z = " + " + ".join([f"{ci}x{i+1}" for i, ci in enumerate(c_vals)]))
            print(f"Contraintes : {self.m} contraintes, {self.n} variables de decision")

        while True:
            self.iteration += 1
            if verbose:
                self._print_iteration()

            # --- TEST D'OPTIMALITE ---
            # Tous les coefficients de la ligne objectif doivent etre >= 0
            z_row = self.tableau[self.m, :-1]  # Exclut le membre droit

            if np.all(z_row >= -1e-9):
                if verbose:
                    print("\n" + "=" * 70)
                    print(">> OPTIMALITE ATTEINTE : Tous les couts reduits sont positifs ou nuls.")
                    print("=" * 70)
                break

            # --- CHOIX DE LA VARIABLE ENTRANTE ---
            # Regle de Dantzig : variable avec le coefficient le plus negatif
            entering_col = np.argmin(z_row)
            entering_val = z_row[entering_col]

            if verbose:
                var_name = f"x{entering_col + 1}" if entering_col < self.n else f"s{entering_col - self.n + 1}"
                print(f"\n1) VARIABLE ENTRANTE : {var_name}")
                print(f"   Coefficient dans la ligne Z : {entering_val:.4f} (le plus negatif)")

            # --- CHOIX DE LA VARIABLE SORTANTE (Regle du ratio minimum) ---
            col = self.tableau[:self.m, entering_col]
            rhs = self.tableau[:self.m, -1]

            ratios = []
            for i in range(self.m):
                if col[i] > 1e-9:
                    ratios.append(rhs[i] / col[i])
                else:
                    ratios.append(np.inf)  # Coefficient nul ou negatif -> ratio infini

            leaving_row = np.argmin(ratios)

            if ratios[leaving_row] == np.inf:
                print("\n[!] PROBLEME NON BORNE - La solution est infinie.")
                return None

            if verbose:
                leaving_name = self._var_name(self.basic_vars[leaving_row])
                print(f"\n2) VARIABLE SORTANTE : {leaving_name}")
                print(f"   Ratios calcules : {[f'{r:.2f}' if r != np.inf else 'inf' for r in ratios]}")
                print(f"   Ratio minimum   : {ratios[leaving_row]:.4f} (ligne {leaving_row + 1})")

            # --- OPERATION DE PIVOT ---
            pivot = self.tableau[leaving_row, entering_col]
            if verbose:
                print(f"\n3) PIVOT : Element ({leaving_row + 1}, {entering_col + 1}) = {pivot:.4f}")
                print("   Operations : Normalisation de la ligne pivot, puis elimination de Gauss-Jordan")

            # Normaliser la ligne pivot
            self.tableau[leaving_row, :] /= pivot

            # Eliminer la variable entrante des autres lignes
            for i in range(self.m + 1):
                if i != leaving_row:
                    factor = self.tableau[i, entering_col]
                    if abs(factor) > 1e-12:
                        self.tableau[i, :] -= factor * self.tableau[leaving_row, :]

            # Mise a jour des variables de base
            self.basic_vars[leaving_row] = entering_col

        # --- EXTRACTION DE LA SOLUTION FINALE ---
        solution = np.zeros(self.n + self.m)
        for i, var_idx in enumerate(self.basic_vars):
            solution[var_idx] = self.tableau[i, -1]

        x_opt = solution[:self.n]      # Variables de decision
        s_opt = solution[self.n:]      # Variables d'ecart
        z_opt = self.tableau[self.m, -1]  # Valeur optimale de Z

        if verbose:
            self._print_solution(x_opt, s_opt, z_opt)

        return x_opt, s_opt, z_opt

    def _var_name(self, idx):
        """Retourne le nom lisible d'une variable."""
        if idx < self.n:
            return f"x{idx + 1}"
        else:
            return f"s{idx - self.n + 1}"

    def _print_iteration(self):
        """Affiche le tableau courant de maniere formatee."""
        print(f"\n{'─' * 70}")
        print(f"ITERATION {self.iteration}")
        print(f"{'─' * 70}")

        # En-tete
        headers = [f"x{i+1}" for i in range(self.n)] + [f"s{i+1}" for i in range(self.m)] + ["b"]
        print(f"{'Base':>6} | " + " | ".join(f"{h:>10}" for h in headers))
        print("-" * 70)

        # Lignes des contraintes
        for i in range(self.m):
            base_name = self._var_name(self.basic_vars[i])
            row_vals = self.tableau[i]
            print(f"{base_name:>6} | " + " | ".join(f"{v:>10.3f}" for v in row_vals))

        # Ligne objectif
        z_vals = self.tableau[self.m]
        print(f"{'Z':>6} | " + " | ".join(f"{v:>10.3f}" for v in z_vals))

    def _print_solution(self, x, s, z):
        """Affiche la solution finale de maniere detaillee."""
        print("\n" + "=" * 70)
        print("                    SOLUTION OPTIMALE FINALE")
        print("=" * 70)
        print(f"\n{'Variables de decision :':<30}")
        for i in range(self.n):
            status = " (en base)" if i in self.basic_vars else " (hors base)"
            print(f"   x{i+1} = {x[i]:10.4f}{status}")

        print("\nVariables d'ecart :")
        for i in range(self.m):
            print(f"   s{i+1} = {s[i]:10.4f}")

        print(f"\n{'─' * 70}")
        print(f"   PROFIT MAXIMUM Z* = {z:.4f} DH")
        print(f"{'─' * 70}")

        print("\n>>> INTERPRETATION ECONOMIQUE <<<")
        for i in range(self.n):
            if x[i] > 1e-6:
                print(f"   - Produire {x[i]:.0f} unite(s) du produit x{i+1}")
            else:
                print(f"   - Ne pas produire le produit x{i+1} (cout reduit non nul)")

        for i in range(self.m):
            if s[i] < 1e-6:
                print(f"   - La contrainte {i+1} est SATUREE (ressource epuisee)")
            else:
                print(f"   - La contrainte {i+1} a un excedent de {s[i]:.2f} unites")


# =============================================================================
# APPLICATION AU PROBLEME DE LA PATISSERIE (3 VARIABLES)
# =============================================================================

print("\n" + "#" * 70)
print("# PROJET : OPTIMISATION DE LA PRODUCTION D'UNE PATISSERIE")
print("# METHODE SIMPLEXE IMPLEMENTEE EN PYTHON")
print("#" * 70)

# Donnees du probleme
# Variables : x1=Croissants, x2=Pains au chocolat, x3=Tartes aux fruits
A = np.array([
    [0.15, 0.20, 0.30],   # Farine
    [10.0, 12.0, 20.0],   # Four
    [5.0,  8.0,  15.0],   # Main-d'oeuvre
    [50.0, 80.0, 120.0]   # Beurre
], dtype=float)

b = np.array([45, 2400, 1800, 18000], dtype=float)
c = np.array([5, 8, 13], dtype=float)

print("\n>>> DONNEES DU PROBLEME <<<")
print("Fonction objectif : Max Z = 5x1 + 8x2 + 13x3")
print("\nContraintes :")
print("  C1 (Farine)        : 0.15x1 + 0.20x2 + 0.30x3 <= 45")
print("  C2 (Four)          : 10x1 + 12x2 + 20x3 <= 2400")
print("  C3 (Main-d'oeuvre) : 5x1 + 8x2 + 15x3 <= 1800")
print("  C4 (Beurre)        : 50x1 + 80x2 + 120x3 <= 18000")
print("\nForme standard (ajout des variables d'ecart s1, s2, s3, s4) :")
print("  0.15x1 + 0.20x2 + 0.30x3 + s1 = 45")
print("  10x1 + 12x2 + 20x3 + s2 = 2400")
print("  5x1 + 8x2 + 15x3 + s3 = 1800")
print("  50x1 + 80x2 + 120x3 + s4 = 18000")

# Resolution
solver = SimplexSolver(A, b, c)
x_opt, s_opt, z_opt = solver.solve(verbose=True)

# Verification avec scipy (optionnel)
print("\n" + "=" * 70)
print("VERIFICATION NUMERIQUE AVEC SCIPY.OPTIMIZE.LINPROG")
print("=" * 70)
from scipy.optimize import linprog
res = linprog(-c, A_ub=A, b_ub=b, bounds=[(0, None)]*3, method='highs')
print(f"Scipy    -> x = {res.x}, Z = {-res.fun:.4f}")
print(f"Simplexe -> x = {x_opt}, Z = {z_opt:.4f}")
print(f"\nDifference maximale : {np.max(np.abs(x_opt - res.x)):.2e} (erreur numerique negligeable)")
