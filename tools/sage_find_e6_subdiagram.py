#!/usr/bin/env python3
from itertools import combinations

from sage.all import WeylGroup

wanted = 51840
found = []


if not found:
    print("No subset found")


def main():
    W8 = WeylGroup(["E", 8])
    refs = W8.simple_reflections()
    indices = list(refs.keys())
    for subset in combinations(indices, 6):
        gens = [refs[i] for i in subset]
        H = W8.subgroup(gens)
        order = H.order()
        if order == wanted:
            found.append(subset)
            print(f"Found subset {subset} order {order}")
            break


if __name__ == "__main__":
    main()
