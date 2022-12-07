import re
import os


def has_another_line(f):
    cur_pos = f.tell()
    has_line = bool(f.readline())
    f.seek(cur_pos)
    return has_line


def parse_next_country(infile, outfile, year):
    country_name = infile.readline().strip('\n').strip('\ufeff')
    lines = []
    next_line = infile.readline()
    while next_line != '\n' and next_line != '':
        lines.append(next_line)
        next_line = infile.readline()

    pattern = re.compile(r"\(\d+\)")
    new_lines = []
    for line in lines:
        age_pattern = pattern.findall(line)[0]
        age = age_pattern[1:-1]
        entries = line.strip('\n').split(',')
        entries[3] = entries[3].replace(f' {age_pattern}', '')
        new_lines.append(f"{entries[0]},{country_name},{entries[1]},{entries[2]},{entries[3]},{age},{entries[4]},{entries[5]},{entries[6]},{year}\n")
    outfile.writelines(new_lines)


def parse_year(file_name, outfile):
    print(f'processing {file_name}')
    infile = open(file_name, encoding="utf-8")
    year = file_name.replace(".csv", '')
    while has_another_line(infile):
        parse_next_country(infile, outfile, year)
    infile.close()


def execute():
    output_filename = "players.csv"
    if os.path.exists(output_filename):
        os.remove(output_filename)

    output_file = open("players.csv", "a", encoding="utf-8")
    parse_year("1991.csv", output_file)
    parse_year("1995.csv", output_file)
    parse_year("1999.csv", output_file)
    parse_year("2003.csv", output_file)
    parse_year("2007.csv", output_file)
    parse_year("2011.csv", output_file)
    parse_year("2015.csv", output_file)
    parse_year("2019.csv", output_file)
    output_file.close()
