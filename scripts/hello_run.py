def main():
    with open("logs/hello_python.txt", "w") as f:
        f.write("hello from python\n")
    print("wrote hello file")


if __name__ == "__main__":
    main()
