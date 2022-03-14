import re

def check_file_line(line):
    '''Kiểm tra dòng dữ liệu nhập vào, trả về:
    0 nếu dòng không lỗi
    1 nếu dòng chứa không đúng 26 giá trị được phân tách bằng dấu phẩy
    2 nếu mã số học sinh không đúng “N” theo sau là 8 ký tự số
    3 nếu chứa cả hai lỗi 1 và 2'''

    line_list = line.split(',')
    error = 0

    # check error 1
    if len(line_list) != 26:
        error = 1

    # check error 2, 3
    pattern = re.compile(r'N\d{8}')
    if not pattern.fullmatch(line_list[0]):
        error += 2

    return error

def anayze(file_lines):
    '''Analyze list of file lines and print out information accordingly'''

    print('**** ANALYZING ****')

    invalid_lines_no = 0

    for line in file_lines:
        test_result = check_file_line(line)
        if test_result == 1:
            print('Invalid line of data: does not contain exactly 26 values:')
            print(line)
            invalid_lines_no += 1
        elif test_result == 2:
            print('Invalid line of data: N# is invalid')
            print(line)
            invalid_lines_no += 1
        elif test_result == 3:
            print('Invalid line of data: does not contain exactly 26 values and N# is invalid')
            print(line)
            invalid_lines_no += 1

    if invalid_lines_no == 0:
        print('No errors found!')

    print('**** REPORT ****')
    print(f'Total valid lines of data: {len(file_lines) - invalid_lines_no}')
    print(f'Total invalid lines of data: {invalid_lines_no}')

# Task 1
filename = input('Enter a class file to grade (i.e. class1 or class1.txt):')
if not '.txt' in filename:
    filename += '.txt'

file_lines = list()
try:
    with open(filename, 'r') as f:
        for line in f:
            file_lines.append(line.rstrip())
except FileNotFoundError:
    print('File cannot be found.')
else:
    print(f'Successfully opened {filename}')

    # Task 2
    anayze(file_lines)

    

