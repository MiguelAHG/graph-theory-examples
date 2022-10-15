"""
Miguel Antonio H. Germar, 2022
"""

import streamlit as st

def format_line(seq, cell_length):
    line_parts = []
    for x in seq:
        x_str = str(x).rjust(cell_length, " ")
        line_parts.append(x_str)
    line = " ".join(line_parts)
    return line
    
def compile_lines(output_lines):
    return "\n".join(output_lines)

def havel_hakimi(deg_seq):
    """Take a degree sequence and use the Havel-Hakimi technique to determine whether or not the degree sequence is graphic. If it is graphic, show how to construct a simple graph from it."""

    # List of lines of text to display to the user.
    output_lines = []

    # This is the number of characters in the largest "vertex label." Each vertex label is a string that starts with the letter v, which is followed by an integer representing the position of the vertex from left to right in the degree sequence. For example, the first vertex is v1, the second vertex is v2, and so on.
    num_chars_largest_vertex_label = len(str(len(deg_seq))) + 1

    # This is the number of digits in the largest value in the degree sequence.
    num_digits_largest_degree = len(str(max(deg_seq)))

    # A "cell" is a set of consecutive characters in the text output that contains a number. There will be multiple cells in each line. Each cell will have one space after it to separate it from the next cell.
    # Cell length has to be at least 2 to accommodate the number -1.
    cell_length = max(
        num_chars_largest_vertex_label,
        num_digits_largest_degree,
        2
    )

    # This line shows the vertex labels. These will serve as column headers; they will be aligned with the rest of the output.
    label_numbers = range(1, len(deg_seq) + 1)
    vertex_label_line = format_line(
        [f"v{num}" for num in label_numbers],
        cell_length
    )
    horiz_line = "-" * (cell_length + 1) * len(deg_seq)

    output_lines.append("")
    output_lines.append(vertex_label_line)
    output_lines.append(horiz_line)

    # This line displays the inputted degree sequence.
    deg_seq_line = format_line(deg_seq, cell_length)

    output_lines.append(deg_seq_line)
    output_lines.append("")

    # Check whether the first value is greater than or equal to the number of vertices.
    num_vertices = len(deg_seq)
    first_value = deg_seq[0]
    if first_value >= num_vertices:
        output_lines.append(f"The degree sequence is not graphic.\nThe first vertex is adjacent to {first_value} vertices other than itself. However, there are only {num_vertices - 1} other vertices in the graph. Therefore, a simple graph that follows this degree sequence cannot be constructed.\n")
        
        output_str = compile_lines(output_lines)
        return output_str

    # Check whether the sum of degrees is odd.
    sum_degrees = sum(deg_seq)
    if sum_degrees % 2 == 1:
        output_lines.append(f"The degree sequence is not graphic.\nThe sum of the degrees of the vertices, {sum_degrees}, is odd. However, to be able to construct a graph, it is necessary that the sum of degrees is even. The First Theorem of graph theory states that the sum of the degrees of the vertices of a graph is equal to 2 times the number of edges in the graph.\n")
        
        output_str = compile_lines(output_lines)
        return output_str

    # In the while loop, this variable is assigned the "latest" sequence in the solution, i.e., the most recent sequence obtained directly after the step of rearranging the sequence in non-ascending order.
    # This is a list of lists. In the while loop, after the step where the sequence is rearranged in non-ascending order, it is appended to this list. The list is named `graph_construction_steps` because the sequences stored in it will be used in constructing a graph after we have confirmed that the sequence is graphic.
    graph_construction_steps = []
    graph_construction_steps.append([x for x in deg_seq])

    # The "latest sequence" refers to the most recent sequence obtained directly after the step (in the while loop) of rearranging the sequence to be non-ascending.
    latest_seq = graph_construction_steps[0]

    # Number of cells to indent on the left
    indent_number = 0
    # String with whitespace, to be used to indent lines.
    indent_str = " " * (cell_length + 1) * indent_number

    # The loop will end if the sum of the latest sequence is zero.
    while sum(latest_seq) > 0:

        if indent_number == 0:
            v1 = latest_seq[0]
            explanation1 = f"(Copy the sequence. The first number is {v1}.\nStarting from the second number, underline {v1} numbers.)"
            output_lines.append(explanation1)

        # Copy the sequence to the next line and underline the 2nd to the (n+1)th items, where n is the value of the first item.
        # Carets were used to serve as underline symbols.
        initial_seq_list = [indent_str, format_line(latest_seq, cell_length)]
        initial_seq_line = "".join(initial_seq_list)

        indent_number += 1
        indent_str = " " * (cell_length + 1) * indent_number
        n = latest_seq[0]
        caret_str = "^" * (cell_length + 1) * n
        underline_line = indent_str + caret_str

        output_lines.append(initial_seq_line)
        output_lines.append(underline_line)

        # Copy to the next line, delete the first item in the sequence, and subtract 1 from each of the underlined numbers.

        if indent_number == 1:
            explanation2 = "(Delete the first number. Subtract 1 from each of the underlined numbers.)"
            output_lines.append(explanation2)

        seq_after_subtracting = [x - 1 for x in latest_seq[1 : n + 1]] + latest_seq[n + 1 :]
        list_after_subtracting = [indent_str, format_line(seq_after_subtracting, cell_length)]
        line_after_subtracting = "".join(list_after_subtracting)

        output_lines.append(line_after_subtracting)
        output_lines.append(underline_line)

        # If any item becomes -1, the degree sequence is not graphic, so the function will return.
        for item in seq_after_subtracting:
            if item == -1:
                error_line = "The degree sequence is not graphic.\n"
                output_lines.append(error_line)

                output_str = compile_lines(output_lines)
                return output_str

        # On the next line, rearrange the numbers in non-increasing order. Do not underline anything.

        if indent_number == 1:
            explanation3 = "(Rearrange the numbers in non-increasing order.)"
            output_lines.append(explanation3)

        seq_rearranged = list(sorted(seq_after_subtracting, reverse = True))
        list_rearranged = [indent_str, format_line(seq_rearranged, cell_length)]
        line_rearranged = "".join(list_rearranged)

        output_lines.append(line_rearranged)
        output_lines.append("") # Append a blank line

        # Append the rearranged sequence to graph_construction_steps.
        graph_construction_steps.append(seq_rearranged)
        # Update this variable so it is assigned the rearranged sequence
        latest_seq = seq_rearranged

    output_lines.append("The degree sequence is graphic.")

    # Explain how to construct a simple graph based on the degree sequence.
    output_lines.append("\nGraph construction:\n1. Start by drawing a graph based on the first degree sequence listed below.\n2. Add one vertex.\n3. Add edges so that the graph follows the next sequence.\n4. Repeat steps 2 and 3 until the graph follows the last sequence.\n")

    # Go backwards from the second-to-last sequence to the very first sequence (the sequence that was inputted).
    # We don't start at the last sequence because this is the one where all of the vertices have degree 0.
    final_steps = graph_construction_steps[-2::-1]
    
    for step_seq in final_steps:
        step_str_values = [str(x) for x in step_seq]
        step_comma_separated = ", ".join(step_str_values)
        step_line = f"({step_comma_separated})"

        output_lines.append(step_line)

    output_lines.append("")

    output_str = compile_lines(output_lines)
    return output_str

def feature_havel_hakimi():
    st.markdown("## Havel-Hakimi Technique")
    st.markdown("Input a degree sequence in the text box below by typing integers greater than or equal to 0 in descending order, separated by commas. Do not put spaces. For example: `4,3,2,2,1`")
    st.markdown("Then, press the button. The app will show whether the sequence is graphic. If it is, the Havel-Hakimi technique will be used to show how to construct a simple graph from the sequence.")

    input_str = st.text_input(label = "Degree Sequence", value = "")

    if not st.button("Go"):
        st.stop()
    
    try:
        deg_seq_str = input_str.split(",")
        deg_seq_int = [int(x) for x in deg_seq_str]
    except:
        st.warning("The input is invalid. Ensure that all of the values in the sequence are integers, and that they are separated only by commas.")
        st.stop()

    prev_value = deg_seq_int[0]

    # If values are inappropriate, show a warning.
    for item in deg_seq_int[1:]:
        if item < 0:
            st.warning("The degree sequence contains a value less than 0.")
            st.stop()
        elif item > prev_value:
            st.warning("The degree sequence is not arranged in non-ascending order.")
            st.stop()
        else:
            prev_value = item

    result = havel_hakimi(deg_seq_int)
    st.markdown(f"```\n{result}\n```")
