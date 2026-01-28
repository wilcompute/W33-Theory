from sage.all import RootSystem

if hasattr(ct, "cartan_matrix"):
    print(ct.cartan_matrix())


def main():
    ct = RootSystem(["E", 8]).cartan_type()
    print(ct)
    print(dir(ct)[:30])
    print("has cartan_matrix", hasattr(ct, "cartan_matrix"))


if __name__ == "__main__":
    main()
