import pandas as pd
import re

def check_file_line(line):
    '''Kiểm tra dòng dữ liệu nhập vào, trả về:
    0 nếu dòng không lỗi
    1 nếu dòng chứa không đúng 26 giá trị được phân tách bằng dấu phẩy
    2 nếu mã số học sinh không đúng "N" theo sau là 8 ký tự số
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

def record_valid_check(file_lines):
    '''Kiểm tra các dòng có valid và in ra thông tin tương ứng
    Trả về danh sách chỉ bao gồm các dòng valid
    '''

    print('**** ANALYZING ****')

    invalid_lines_no = 0
    valid_lines = list()

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
        else:
            valid_lines.append(line.split(','))

    if invalid_lines_no == 0:
        print('No errors found!')

    print('**** REPORT ****')
    print(f'Total valid lines of data: {len(file_lines) - invalid_lines_no}')
    print(f'Total invalid lines of data: {invalid_lines_no}')

    return valid_lines

# Task 1: đọc file - có thể đọc bằng pandas read_csv nhưng sẽ không thể lọc:
# - các dòng thiếu câu trả lời do pandas đã làm đầy bằng giá trị NaN
# - các dòng thừa câu trả lời nếu các giá trị từ cột 26 trở đi là giá trị NaN (thí sinh bỏ qua các câu này)
filename = input('Enter a class file to grade (i.e. class1 or class1.txt):')
if not filename:
    filename = 'class1.txt'
if not '.txt' in filename:
    filename += '.txt'

# # đọc bằng pandas
# try:
#     class_data = pd.read_csv(filename, names=list(range(30)), header=None)
# except FileNotFoundError:
#     print('File cannot be found.')
#     quit()
# else:
#     print(f'Successfully opened {filename}')
#
# for index, row in class_data.iterrows():
#     print(row.to_frame().T)

# đọc bằng open file thông thường để lọc các dòng thiếu, thừa giá trị
file_lines = list()
try:
    with open(filename, 'r') as read_file:
        for line in read_file:
            file_lines.append(line.rstrip())
except FileNotFoundError:
    print('File cannot be found.')
    quit()
else:
    print(f'Successfully opened {filename}')

# Task 2
valid_lines = record_valid_check(file_lines)

# Task 3
answer_key = "B,A,D,D,C,B,D,A,C,C,D,B,A,B,A,C,B,D,A,C,A,A,B,D,D"
answer_key = answer_key.split(',')
num_questions = 25

class_valid_lines = pd.DataFrame(valid_lines)
print('before transform:')
print(class_valid_lines)

# chấm điểm từng câu trả lời theo answer_key
for index, key in enumerate(answer_key):
    class_valid_lines[index + 1] = class_valid_lines[index + 1].apply(lambda answer: 0 if not answer else 4 if answer == key else -1)

class_valid_lines['sum'] = class_valid_lines.sum(axis=1)

print('after transform:')
print(class_valid_lines)

sum_student = class_valid_lines.loc[0, 'sum']

print(sum_student)

# đếm số câu đúng ứng với từng câu hỏi
for i in range(1, 26):
    class_valid_lines[i] = class_valid_lines[i].apply(lambda grade: pd.NA if grade != 4 else grade)

print(type(class_valid_lines.count()))

