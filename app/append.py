def stdin(content: str, filename: str):
    with open(filename, "a+") as file:
        file.write(content + "\n")


def stderr(content: str, filename: str):
    with open(filename, "a+") as file:
        file.write("")


def append(input: list[str], operator_found: list[bool]) -> str:
    operator_idx = operator_found.index(True)
    filename = input[operator_idx + 1]

    output = ""
    content = " ".join(input[0:operator_idx])

    match input[operator_idx]:
        case ">>" | "1>>":
            stdin(content, filename)
        case "2>>":
            stderr(content, filename)
            output = content

    return output
