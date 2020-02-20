
"""
    Converting original ASCII file into txt file for better readability.
    Combined landline and cell phone data set
    275 variables in total
    It has a fixed record length of 2033 positions (starts 0 and ends 2033), zero idx is empty
    2018 Combined Landline and Telephone Multiple Data Variable Layout
"""

# TODO: find older/newer data sets

import csv
from os.path import expanduser
home = expanduser("~")

col_info_file_path = home + "/Downloads/ICGE_course/project/project_ace_python/"
col_info_file = "col_extract_info_2018.txt"

column_values, column_lengths = [], []

with open(col_info_file_path + col_info_file, "r") as content:

    for line_idx, line in enumerate(content):
        if "::" in line:
            line = line.split("::")
            columns, length = line[0], int(line[1])
            columns = columns.split(".")[1]

            if "-" in columns:
                columns = columns.split("-")
                columns = [int(columns[0]), int(columns[1])]

                column_values.append((columns[0], columns[1]))
            else:
                columns = [int(columns)]
                column_values.append((columns[0], columns[0]))

            column_lengths.append(length)

#####################################################################

file_path = home + "/Downloads/ICGE_course/project/LLCP2018ASC/"
file_name = "LLCP2018.ASC"

output_csv_file = "montana_parsed_ace_data_2018.csv"
fieldnames = [i for i in range(1, len(column_values) + 1)]

# cc = 0
with open(output_csv_file, 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(fieldnames)

    dist_val_last_question = set()

    with open(file_path + file_name, "r") as content:
        line_counter = 0
        line_len = set()
        for line in content:
            line_len.add(len(line))
            line_counter += 1

            # if cc == 100:
            #     break
            # cc += 1

            is_montana_state = True
            new_line = ""
            for col_idx, col_vals in enumerate(column_values):
                next_value = line[col_vals[0] - 1:col_vals[1]]
                next_value = next_value.strip()
                if len(next_value.split()) == 0:  # next_value.isspace():
                    # print(str(col_idx) + " " + line)
                    next_value = "nan"

                if col_idx == 273:
                    dist_val_last_question.add(next_value)

                # if col_idx == 0 and next_value != "30":
                #     is_montana_state = False
                #     break

                new_line = new_line + "," + next_value

            new_line = new_line[1:].split(',')

            if is_montana_state:
                writer.writerow(new_line)

        print(dist_val_last_question)

        print("number of lines: " + str(line_counter))  # 437436 lines
        print("lines: " + str(line_len))  # 2034

#####################################################################
