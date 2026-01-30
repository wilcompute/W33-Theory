import sage.graphs.strongly_regular_db as srg


def main():
    print([n for n in dir(srg) if "graph" in n])
    print(dir(srg)[:200])


if __name__ == "__main__":
    main()
