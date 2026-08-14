def read_txt_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


if __name__ == "__main__":
    content = read_txt_file("data/sample.txt")
    print(content)