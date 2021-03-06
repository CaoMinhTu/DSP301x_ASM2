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
class_valid_lines = class_valid_lines.rename(columns={0: 'id'})

# chấm điểm từng câu trả lời theo answer_key
for index, key in enumerate(answer_key):
    class_valid_lines[index + 1] = class_valid_lines[index + 1].apply(lambda answer: 0 if not answer else 4 if answer == key else -1)

col_list = list(class_valid_lines)
col_list.remove('id')

# tính tổng điểm cho từng học sinh
class_valid_lines['sum'] = class_valid_lines[col_list].sum(axis=1)

# 3.1. Đếm số lượng học sinh đạt điểm cao (>80).
num_high_score_students = sum(class_valid_lines['sum'] > 80)
print(f'Total student of high scores: {num_high_score_students}')

# 3.2. Điểm trung bình.
mean_grade = class_valid_lines['sum'].mean()
print(f'Mean (average) score: {mean_grade}')

# 3.3. Điểm cao nhất.
max_grade = class_valid_lines['sum'].max()
print(f'Highest score: {max_grade}')

# 3.4. Điểm thấp nhất.
min_grade = class_valid_lines['sum'].min()
print(f'Lowest score: {min_grade}')

# 3.5. Miền giá trị của điểm (cao nhất trừ thấp nhất).
print(f'Range of scores: {max_grade - min_grade}')

# 3.6. Giá trị trung vị
median_grade = class_valid_lines['sum'].median()
print(f'Median score: {median_grade}')

# 3.7. Trả về các câu hỏi bị học sinh bỏ qua nhiều nhất theo thứ tự: số thứ tự câu hỏi - số lượng học sinh bỏ qua -  tỉ lệ bị bỏ qua (nếu có cùng số lượng cho nhiều câu hỏi bị bỏ thì phải liệt kê ra đầy đủ).
num_right = class_valid_lines[class_valid_lines == 4].count()
num_wrong = class_valid_lines[class_valid_lines == -1].count()
num_skipped = class_valid_lines[class_valid_lines == 0].count()
num_students = class_valid_lines.shape[0]

max_skipped = num_skipped.max()
skipped_str = 'Question that most people skip:'
for col in col_list:
    if num_skipped[col] == max_skipped:
        skipped_str += f' {col} - {max_skipped} - {(max_skipped / num_students):.3f} ,'
skipped_str = skipped_str[:-2]
print(skipped_str)

max_wrong = num_wrong.max()
wrong_str = 'Question that most people answer incorrectly:'
for col in col_list:
    if num_wrong[col] == max_wrong:
        wrong_str += f' {col} - {max_wrong} - {(max_wrong / (max_wrong + num_right[col])):.3f} ,'
wrong_str = wrong_str[:-2]
print(wrong_str)

# Task 4: lưu danh sách điểm học sinh
sum_student = class_valid_lines[['id', 'sum']]
filename = filename[:-4] + '_grades.txt'
sum_student.to_csv(filename, header=False, index=False)
# print(f'Grades saved in {grades_file}')