
import csv
from os.path import expanduser
home = expanduser("~")

parsed_file_path = home + "/Downloads/ICGE_course/project/project_ace_python/ace_2012_project/"
parsed_info_file = "parsed_ace_data_2012.csv"
output_csv_file = "state_age_distribution_ace_data_2012.csv"

variables_nbr = 359
fieldnames = [i for i in range(1, variables_nbr + 1)]

with open(output_csv_file, 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')

    column_names = ["state_id", "people", "Don't know/Not sure", "Refused", ">18", "18-24", "25-34", "35-44", "45-54",
                    "55-64", "65-99", "99<", "other"]
    writer.writerow(column_names)

    states = [i for i in range(1, 57)]  # no states: 52 43 14 7 3
    states.append(66)  # Guam
    states.append(72)  # Puerto Rico
    other_states = set()

    for state_id in states:

        state_content = []
        with open(parsed_file_path + parsed_info_file, "r") as content:

            for idx, line in enumerate(content):
                if idx == 0:
                    continue

                line = line.split(",")
                if line[358] != "nan":
                    line[358] = line[358][:len(line[358]) - 1]

                if int(line[0]) == state_id:  # state data
                    state_content.append(line)

                if 56 < int(line[0]) < 1:
                    other_states.add(int(line[0]))

#####################################################################################################
        # getting state and age based distribution for 2012 dataset

        age_distribution = {}
        age_categories = ["Don't know/Not sure", "Refused", ">18", "18-24", "25-34", "35-44", "45-54",
                          "55-64", "65-99", "99<", "other"]
        for i in age_categories:
            age_distribution[i] = 0

        for idx, line in enumerate(state_content):
            if idx == 0:
                continue

            age_nbr = int(line[50])

            if age_nbr == 7:
                age_distribution[age_categories[0]] += 1
            elif age_nbr == 9:
                age_distribution[age_categories[1]] += 1
            elif age_nbr < 18:
                age_distribution[age_categories[2]] += 1
            elif 25 > age_nbr > 17:
                age_distribution[age_categories[3]] += 1
            elif 35 > age_nbr > 24:
                age_distribution[age_categories[4]] += 1
            elif 45 > age_nbr > 34:
                age_distribution[age_categories[5]] += 1
            elif 55 > age_nbr > 44:
                age_distribution[age_categories[6]] += 1
            elif 65 > age_nbr > 54:
                age_distribution[age_categories[7]] += 1
            elif 100 > age_nbr > 64:
                age_distribution[age_categories[8]] += 1
            elif age_nbr > 98:
                age_distribution[age_categories[9]] += 1
            else:
                age_distribution[age_categories[10]] += 1

        print(state_id)
        age_data = [state_id, len(state_content)]
        [age_data.append(j) for i, j in age_distribution.items()]
        writer.writerow(age_data)

    print("other states: ")
    print(other_states)
#####################################################################################################
