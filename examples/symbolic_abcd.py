import sympy as sp

z, f = sp.symbols("z f", real=True, nonzero=True)
P = sp.Matrix([[1, z], [0, 1]])
L = sp.Matrix([[1, 0], [-1/f, 1]])
M = sp.simplify(P * L)
M_numeric = sp.lambdify((z, f), M, "numpy")
print(M_numeric(0.10, 0.05))  # z、f 均以 m 表示
