import sys


MAX_LINES = 1000000


def main():
    if len(sys.argv) < 2:
        print "Invalid args"
        return
    main_file_name = sys.argv[1]
    lines = []
    with open(main_file_name) as f:
        lines_count = 0
        files_count = 0
        for line in f:
            lines.append(line)
            lines_count += 1
            if lines_count == MAX_LINES:
                files_count += 1
                temp_file = open(main_file_name + str(files_count), 'w')
                temp_file.writelines(lines)
                temp_file.close()
                lines = []
                lines_count = 0
    if len(lines) > 0:
        temp_file = open(main_file_name + str(files_count), 'w')
        temp_file.writelines(lines)
        temp_file.close()


if __name__ == "__main__":
    main()
