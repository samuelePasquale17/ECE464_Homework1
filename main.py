import re  # import library for regex


# matching patterns for detecting inputs, outputs, and gates using regex
input_output_pattern = r'^(input|output)\((.+)\)$'
input_pattern = r'^input\(.+\)$'
output_pattern = r'^output\(.+\)$'
gate_pattern = r'^\s*([^\s=]+)\s*=\s*([^\s(]+)\s*\(([^)]*)\)\s*$'


def get_gate(line):
    """
    get_gate is a function in charge of, given a string that describes a gate, extracting some information
    about the output pin name, the gate type and the input pin names that feed the gate.

    :param line: String that should have the following format: out_pin_name = GATE_TYPE(input_pin_name1, ...)
    :return get_gate returns three information about the gate with the following order: output pin name (str),
            gete type (str), input pin names (list). It the given line doesn't describe a gate, None is returned instead
    """

    # Regex match verification
    match = re.search(gate_pattern, line)

    # Check if match occurs
    if match:
        output_pin = match.group(1)  # getting the output pin name
        gate_name = match.group(2)  # getting the gate name
        list_inputs = match.group(3)  # getting the inputs string
        list_inputs = [element.strip() for element in list_inputs.split(',')] # generation of a list with all the inputs
        fanin = len(list_inputs)  # number of inputs
        if fanin > 1:
            gate_type = str(fanin) + "-input " + gate_name.upper()  # update the gate type with the number of inputs
        else:
            gate_type = gate_name.upper() # no changes

        # return the gate information
        return output_pin, gate_type, list_inputs
    else:
        # if NO match occurs
        return None, None, None


def get_input(line):
    """
    get_input is a function in charge of, given a line (str) as input, checking if it describes an either an input or an
    output, and return the pin name
    :param line: string with the following format: INPUT(pin_name) or OUTPUT(pin_name)
    :return: get_input returns the pin name if a match is found, None otherwise
    """

    # check if it is an INPUT or an OUTPUT (not Case Sensitive)
    match = re.search(input_output_pattern, line, re.IGNORECASE)

    # check is match occurs
    if match:
        return match.group(2)  # return the pin name
    else:
        return None  # None if no match


def get_output(line):
    """
    get_output is a wrapper that simply calls get_input. This is needed just for user interface purposes. In fact the
    user can call that function to get the output pin without know what's happening behind the scene. As we know the
    pattern for both inputs and outputs is almost the same, except for the word itself (either input or output)
    :param line:
    :return:
    """

    return get_input(line)  # return the output pin name


def circuit_parsing(file_name, list_input_node, list_output_node, list_gates):
    """
    circuit_parsing is a function in charge of, given a text file that describes a circuit benchmark, parsing the
    circuit, extracting some information
    :param file_name: name of the file that describes the circuit benchmark
    :param list_input_node: list with all the input nodes
    :param list_output_node: list with all the output nodes
    :param list_gates: list with all the gates, with their main characteristics (output pin, gate type, input pins)
    :return:
    """

    f = open(file_name, "r")  # open the file

    for line in f.readlines():  # read each line

        # check if it is an input
        if bool(re.match(input_pattern, line, re.IGNORECASE)):
            input = get_input(line)  # get the input pin name
            # adding the pin if not inserted yet
            list_input_node.append(input) if input not in list_input_node else None
        # check if it is an output
        elif bool(re.match(output_pattern, line, re.IGNORECASE)):
            output = get_output(line)  # get the output pin name
            # adding the pin if not inserted yet
            list_output_node.append(output) if output not in list_output_node else None
        # check if it not empty
        elif line.strip():
            # get the gate
            gate = get_gate(line)
            list_gates.append(gate) if gate not in list_gates else None


    f.close()  # close the file

def main():
    # file_name = "benchmark1.txt"
    # file_name = "benchmark2.txt"
    file_name = "benchmark3.txt"
    list_input_node = []
    list_output_node = []
    list_gates = []

    # parsing the circuit
    circuit_parsing(file_name, list_input_node, list_output_node, list_gates)

    # printing the parsing outcome
    print("List of inputs: ")
    for input in list_input_node:
        print(input)

    print("List of outputs: ")
    for output in list_output_node:
        print(output)

    print("List of gates: ")
    for gate in list_gates:
        print("Output pin: " + gate[0])
        print("Gate type: " + gate[1])
        print(f"Gate inputs: {', '.join(gate[2])}")
        print("-----------------------------")


main()
