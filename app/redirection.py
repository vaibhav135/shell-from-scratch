def stdin(content: str, filename: str):
    with open(filename, "w+") as file:
        file.write(content + "\n")


def stderr(content: str, filename: str):
    with open(filename, "w+") as file:
        file.write("")

    print(content)


def redirect(input: list[str], operator_found: list[bool]):
    operator_idx = operator_found.index(True)
    filename = input[operator_idx + 1]

    content = " ".join(input[0:operator_idx])

    match input[operator_idx]:
        case ">" | "1>":
            stdin(content, filename)
        case "2>":
            stderr(content, filename)
