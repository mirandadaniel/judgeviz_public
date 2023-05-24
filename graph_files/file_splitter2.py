import csv

global matches
matches = ['0', '2', '3', '4', '5', '6', '7', '9', '11', '12', '13', '14', '15', '17', '18', '19', '20', '21', '22', '23', '24', '26', '29', '31', '32', '34', '35', '36', '38', '40', '42', '43', '45', '46', '47', '49', '52', '53', '55', '56', '57', '60', '62', '63', '66', '68', '69']

def get_case_num_list():
    global case_names 
    case_names = []
    global all_case_lines
    all_case_lines = []
    with open("as.tsv") as file:
        tsv_file = csv.reader(file, delimiter="\t") 
        all_numbers = []
        unique_numbers = []
        line = next(tsv_file)
        for line in tsv_file:
            curr_case = line[0]
            all_numbers.append(curr_case)
            all_case_lines.append(line)
        for x in all_numbers:
            if x not in unique_numbers:
                y = 'case' + x
                unique_numbers.append(x)
                case_names.append(y)

    return unique_numbers
    file.close()


def write_case_to_new_file(case_num, case_lines):
    with open('as_files/case{}.tsv'.format(case_num), 'w', encoding='utf8', newline='') as tsv_file:
        tsv_writer = csv.writer(tsv_file, delimiter='\t', lineterminator='\n')
        for x in case_lines:
            tsv_writer.writerow(x)

def get_all_lines_from_1_case(unique_numbers):
        cases_list = []
        global case_num 
        for x in unique_numbers:
            case_num = x
            if case_num in matches:
                case_lines = []
                for y in all_case_lines:
                    if(y[0] == x):
                        case_lines.append(y)
                    else:
                        write_case_to_new_file(x, case_lines)

            
i = get_case_num_list()
get_all_lines_from_1_case(i)
