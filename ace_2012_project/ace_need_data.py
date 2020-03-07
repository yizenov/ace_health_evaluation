
import csv
from os.path import expanduser
home = expanduser("~")

vars = ["ACEDEPRS", "ACEDRINK", "ACEDRUGS", "ACEPRISN", "ACEDIVRC", "ACEPUNCH", "ACEHURT", "ACESWEAR", "ACETOUCH", "ACETTHEM", "ACEHVSEX"]

parsed_file_path = home + "/Downloads/ICGE_course/project/project_ace_python/ace_2012_project/"
parsed_info_file = "parsed_ace_data_2012.csv"
state_age_csv_file = "state_age_distribution_ace_data_2012.csv"
state_age_ace_csv_file = "state_age_ace_statistic_2012.csv"

variables_nbr = 359
fieldnames = [i for i in range(1, variables_nbr + 1)]

with open(state_age_csv_file, 'w') as csvfile1, open(state_age_ace_csv_file, 'w') as csvfile2:
    writer_age = csv.writer(csvfile1, delimiter=',')
    writer_ace = csv.writer(csvfile2, delimiter=',')

    age_categories = ["state_id", "people", "Don't know/Not sure", "Refused", "18-24", "25-34", "35-44", "45-54",
                      "55-64", "65-99"]
    writer_age.writerow(age_categories)

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
        age_distribution = {i: 0 for i in age_categories[2:]}

        # getting ace statistics by states and ages for 2012 dataset
        general_age_ace_data = {}

        for age_group_idx in age_distribution:
            general_ace_distributions = []

            # 22.1-4 and 22.5 -- combined with "Parents not married", idx = 8
            ace_answers1 = ["yes", "no", "Don’t know/Not Sure", "Parents not married", "Refused", "Not asked or Missing"]
            ace_answers_values1 = ["1", "2", "7", "8", "9", "nan"]
            for j in range(0, 5):
                ace_set1_distribution = {i: 0 for i in ace_answers_values1}
                general_ace_distributions.append(ace_set1_distribution)
                # writer_ace.writerow(age_categories)

            # 22.6-11
            ace_answers2 = ["Never", "Once", "More than once", "Don’t know/Not Sure", "Refused", "Not asked or Missing"]
            ace_answers_values2 = ["1", "2", "3", "7", "9", "nan"]
            for j in range(0, 6):
                ace_set2_distribution = {i: 0 for i in ace_answers_values2}
                general_ace_distributions.append(ace_set2_distribution)

            general_age_ace_data[age_group_idx] = general_ace_distributions

        ace_columns = ["state_id", "state sample population", "age category", "age category population",
                       "ace question", ""]
        for i in range(0, len(ace_answers1)):
            ace_columns.append(ace_answers1[i] + " / " + ace_answers2[i] + " -- number of responses")
        writer_ace.writerow(ace_columns)

        for idx, line in enumerate(state_content):
            if idx == 0:
                continue

            age_nbr = int(line[50])

            ace_values = [line[i] for i in range(229, 240)]
            # age_category = age_categories[2]
            # for var_idx in range(len(ace_values)):
            #     # age_ace_data = general_age_ace_data[age_category]
            #     # ace_data_distribution = age_ace_data[age_category][var_idx]
            #     # ace_data_distribution[ace_values[var_idx]] += 1
            #     general_age_ace_data[age_category][var_idx][ace_values[var_idx]] += 1

            if age_nbr == 7:
                age_distribution[age_categories[2]] += 1
                age_category = age_categories[2]
                for var_idx in range(len(ace_values)):
                    general_age_ace_data[age_category][var_idx][ace_values[var_idx]] += 1
            elif age_nbr == 9:
                age_distribution[age_categories[3]] += 1
                age_category = age_categories[3]
                for var_idx in range(len(ace_values)):
                    general_age_ace_data[age_category][var_idx][ace_values[var_idx]] += 1
            elif 25 > age_nbr > 17:
                age_distribution[age_categories[4]] += 1
                age_category = age_categories[4]
                for var_idx in range(len(ace_values)):
                    general_age_ace_data[age_category][var_idx][ace_values[var_idx]] += 1
            elif 35 > age_nbr > 24:
                age_distribution[age_categories[5]] += 1
                age_category = age_categories[5]
                for var_idx in range(len(ace_values)):
                    general_age_ace_data[age_category][var_idx][ace_values[var_idx]] += 1
            elif 45 > age_nbr > 34:
                age_distribution[age_categories[6]] += 1
                age_category = age_categories[6]
                for var_idx in range(len(ace_values)):
                    general_age_ace_data[age_category][var_idx][ace_values[var_idx]] += 1
            elif 55 > age_nbr > 44:
                age_distribution[age_categories[7]] += 1
                age_category = age_categories[7]
                for var_idx in range(len(ace_values)):
                    general_age_ace_data[age_category][var_idx][ace_values[var_idx]] += 1
            elif 65 > age_nbr > 54:
                age_distribution[age_categories[8]] += 1
                age_category = age_categories[8]
                for var_idx in range(len(ace_values)):
                    general_age_ace_data[age_category][var_idx][ace_values[var_idx]] += 1
            elif 100 > age_nbr > 64:
                age_distribution[age_categories[9]] += 1
                age_category = age_categories[9]
                for var_idx in range(len(ace_values)):
                    general_age_ace_data[age_category][var_idx][ace_values[var_idx]] += 1

#####################################################################################################
        # outputting rows into csv file

        print(state_id)
        age_data = [state_id, len(state_content)]
        [age_data.append(j) for i, j in age_distribution.items()]
        writer_age.writerow(age_data)

        no_ace_status = 0
        age_ace_line = [state_id, len(state_content)]
        writer_ace.writerow(age_ace_line)

        age_idx = 0
        for i, j in age_distribution.items():
            age_ace_line = ["\t", str(i), str(j)]
            writer_ace.writerow(age_ace_line)

            ace_data = general_age_ace_data[i]
            for var_id in range(11):
                age_ace_line = ["\t", "\t", vars[var_id]]
                writer_ace.writerow(age_ace_line)

                age_ace_line = ["\t", "\t", "\t"]
                responses = ace_data[var_id]
                [age_ace_line.append(str(k) + " -- " + str(l)) for k, l in responses.items()]
                writer_ace.writerow(age_ace_line)

                cc = 0
                for k, l in responses.items():
                    if cc == 5:
                        continue
                    no_ace_status += l
                    cc += 1

            age_idx += 1
        if no_ace_status != 0:
            print("Stat exists in :" + str(state_id))
    print("other states: ")
    print(other_states)


#####################################################################################################
