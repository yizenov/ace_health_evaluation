
import PyPDF2
file_name = "CODEBOOK12_LLCP.pdf"
pdfFileObj = open(file_name, 'rb')
# keywords to parse: section, description, type, column, SAS Variable Name

pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
page_numbers = pdfReader.numPages
print("number of pages: " + str(page_numbers))

type_names, column_values, variable_values, questions = [], [], [], []

for page_idx in range(1, page_numbers):
    pageObj = pdfReader.getPage(page_idx)
    page_text = pageObj.extractText()
    page_text = page_text.split('\n')

    section_found, type_found, column_found, var_found = False, False, False, False
    description_found = False

    for line_idx, line in enumerate(page_text):
        if line == ' ':
            continue

        for element in ["Section:", "Module:", "Followup", "CellPhone:", "State:", "Weighting:", "ChildDemograp",
                        "ChildWeighting", "ChildLandandC", "LandandCellRa", "CalculatedVaria"]:
            if element in line:
                section_found = True
                break

        if section_found and "Type:" in line:
            type_found = True
            continue

        if type_found:
            type_name = line.strip()
            type_names.append(type_name)
            type_found = False
            continue

        if section_found and "Column:" in line:
            column_found = True
            continue

        if column_found:
            col_number = line.strip().split()[0]
            column_values.append(col_number)
            # var_field = line.strip().split()[1:]
            var_found = True
            column_found = False
            continue

        if var_found:
            var_name = line.strip()
            variable_values.append(var_name)
            var_found = False
            continue

        if section_found and "Description:" in line:
            description_found = True
            continue

        if description_found:
            question_name = line.strip()
            questions.append(question_name)
            description_found = False

            section_found = False
            continue

print(len(variable_values))
file1 = open("col_extract_info_2012.txt", "w")
questions_set = {}
print("var idx, column values, length, variable names, type, question:")
counter = 1
for idx in range(0, len(questions)):
    if questions[idx] not in questions_set:
        questions_set[questions[idx]] = column_values[idx]

        column_details = column_values[idx]
        if "-" in column_details:
            column_details = column_details.split("-")
            column_details = [int(column_details[0]), int(column_details[1])]
        else:
            column_details = [int(column_details)]

        if len(column_details) == 1:
            file1.write(str(counter) + ". " + column_values[idx] + " :: 1 :: " + variable_values[idx] + " :: "
                  + type_names[idx] + " :: " + questions[idx] + "\n")
        else:
            file1.write(str(counter) + ". " + column_values[idx] + " :: " + str(column_details[1] - column_details[0] + 1)
                  + " :: " + variable_values[idx] + " :: " + type_names[idx] + " :: " + questions[idx] + "\n")
        counter += 1
    else:
        if column_values[idx] != questions_set[questions[idx]]:

            column_details = column_values[idx]
            if "-" in column_details:
                column_details = column_details.split("-")
                column_details = [int(column_details[0]), int(column_details[1])]
            else:
                column_details = [int(column_details)]

            if len(column_details) == 1:
                file1.write("rep " + str(counter) + ". " + column_values[idx] + " :: 1 :: " + variable_values[idx] + " :: "
                  + type_names[idx] + " :: " + questions[idx] + "\n")
            else:
                file1.write("rep " + str(counter) + ". " + column_values[idx] + " :: "
                      + str(column_details[1] - column_details[0] + 1) + " :: " + variable_values[idx] + " :: "
                      + type_names[idx] + " :: " + questions[idx] + "\n")
            counter += 1

        # else:
        #
        #     column_details = column_values[idx]
        #     if "-" in column_details:
        #         column_details = column_details.split("-")
        #         column_details = [int(column_details[0]), int(column_details[1])]
        #     else:
        #         column_details = [int(column_details)]
        #
        #     if len(column_details) == 1:
        #         file1.write("aux " + str(counter) + ". " + column_values[idx] + " :: 1 :: " + variable_values[idx] + " :: "
        #           + type_names[idx] + " :: " + questions[idx] + "\n")
        #     else:
        #         file1.write("aux " + str(counter) + ". " + column_values[idx] + " :: "
        #               + str(column_details[1] - column_details[0] + 1) + " :: " + variable_values[idx] + " :: "
        #               + type_names[idx] + " :: " + questions[idx] + "\n")
        #     counter += 1

file1.close()
pdfFileObj.close()
