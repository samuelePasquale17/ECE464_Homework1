import re

input_pattern = r'^input\(.+\)$'
output_pattern = r'^output\(.+\)$'


def get_input(line):
    pattern = r'^(input|output)\((.+)\)$'
    match = re.search(pattern, line, re.IGNORECASE)

    if match:
        return match.group(2)
    else:
        return None


def get_output(line):
    return get_input(line)


def circuit_parsing(file_name, list_input_node, list_output_node, list_gates):
    f = open(file_name, "r")

    for line in f.readlines():
        if bool(re.match(input_pattern, line, re.IGNORECASE)):
            # get input
            input = get_input(line)
            list_input_node.append(input) if input not in list_input_node else None

        elif bool(re.match(output_pattern, line, re.IGNORECASE)):
            # get output
            output = get_output(line)
            list_output_node.append(output) if output not in list_output_node else None
        else:
            # gate
            a = 1
    f.close()

def main():
    file_name = "benchmark1.txt"
    list_input_node = []
    list_output_node = []
    list_gates = []

    circuit_parsing(file_name, list_input_node, list_output_node, list_gates)

    print("List of inputs: ")
    for input in list_input_node:
        print(input)

    print("List of outputs: ")
    for output in list_output_node:
        print(output)

    print("List of gates: ")
    for gate in list_gates:
        print(gate)

main()
