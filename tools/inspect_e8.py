from sage.all import RootSystem

ct = RootSystem(["E", 8]).cartan_type()
print(ct)
print(dir(ct)[:30])
print("has cartan_matrix", hasattr(ct, "cartan_matrix"))
if hasattr(ct, "cartan_matrix"):
    print(ct.cartan_matrix())
