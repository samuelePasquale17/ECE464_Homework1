import re
import pprint

input_pattern = r'^input\(.+\)$'
output_pattern = r'^output\(.+\)$'


def get_gate(line):
    # Regex per estrarre la stringa prima di "=", la stringa tra "=" e "(", e quella tra "(" e ")"
    pattern = r'^\s*([^\s=]+)\s*=\s*([^\s(]+)\s*\(([^)]*)\)\s*$'

    # Utilizzo di re.search per trovare il match
    match = re.search(pattern, line)

    # Se il match esiste, estrai le parti corrispondenti
    if match:
        part_before_equal = match.group(1)  # Parte prima di "=" senza spazi
        part_between_equal_and_paren = match.group(2)  # Parte tra "=" e "("
        part_in_parentheses = match.group(3)  # Parte tra "(" e ")"
        inputs = [element.strip() for element in part_in_parentheses.split(',')]
        fanin = len(inputs)
        if fanin > 1:
            gate_type = str(fanin) + "-input " + part_between_equal_and_paren.upper()
        else:
            gate_type = part_between_equal_and_paren.upper()

        return part_before_equal, gate_type, inputs
    else:
        return None, None, None  # Se non c'è match, restituisci None


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
            gate = get_gate(line)
            list_gates.append(gate) if gate not in list_gates else None

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
        for parte in gate:
            if isinstance(parte, list):
                # Se la parte è una lista, unisci i suoi elementi con una virgola
                print(f"Inputs del Gate: {', '.join(parte)}")
            else:
                # Stampa le altre parti direttamente
                print(parte)
        print("-----------------------------")


main()
