def count_lines(input_path):
    with open(input_path, "r") as f:
        return sum(1 for _ in f)


def extract_first_lines(input_path, n=2):
    lines = []

    with open(input_path, "r") as f:
        for i, line in enumerate(f):
            if i >= n:
                break
            lines.append(line)

    return lines


def write_lines(output_path, lines):
    with open(output_path, "w") as f:
        f.writelines(lines)


if __name__ == "__main__":

    input_path = "input.txt"
    output_path = "output_first_two_lines.txt"

    total_lines = count_lines(input_path)
    print("Total lines:", total_lines)

    first_two_lines = extract_first_lines(input_path, 2)

    print("First two lines:")
    for line in first_two_lines:
        print(line, end="")

    write_lines(output_path, first_two_lines)

    print("\nOutput file contents:")
    with open(output_path, "r") as f:
        print(f.read())
