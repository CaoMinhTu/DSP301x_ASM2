import enum
import re
import statistics

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
            valid_lines.append(line)

    if invalid_lines_no == 0:
        print('No errors found!')

    print('**** REPORT ****')
    print(f'Total valid lines of data: {len(file_lines) - invalid_lines_no}')
    print(f'Total invalid lines of data: {invalid_lines_no}')

    return valid_lines

def grade_one_student(line, answer_key):
    '''Chấm điểm 1 học sinh theo answer_key
    Trả về dictionary {'id': 'id of student', 'grade detail': ['right', 'wrong', 'no answer'...], 'grade total': 85}'''

    record = line.split(',')
    id = record[0]
    answer_detail = record[1:]
    grade_detail = list()

    for answer, key in zip(answer_detail, answer_key.split(',')):
        if not answer:
            grade_detail.append('no answer')
        elif answer == key:
            grade_detail.append('right')
        else:
            grade_detail.append('wrong')
    
    grade_total = 0
    for e in grade_detail:
        if e == 'right':
            grade_total += 4
        elif e == 'wrong':
            grade_total -= 1
    
    return {'id': id, 'grade detail': grade_detail, 'grade total': grade_total}

def grade_and_stats(lines, answer_key):
    '''Chấm điểm, in ra thống kê từ danh sách câu trả lời nhập vào, trả về danh sách điểm của các học sinh'''

    grades_detail = list()
    for line in lines:
        grades_detail.append(grade_one_student(line, answer_key))
    
    num_question = len(answer_key.split(','))

    grade_total = list() # list điểm tổng của tất cả các học sinh
    for e in grades_detail:
        grade_total.append(e['grade total'])
    
    # Đếm số lượng học sinh đạt điểm cao (>80)
    num_high_score = 0
    for e in grade_total:
        if e > 80:
            num_high_score += 1
    print(f'Total student of high scores: {num_high_score}')

    # Tìm điểm trung bình:
    print(f'Mean (average) score: {statistics.mean(grade_total)}')

    # Điểm cao nhất
    print(f'Highest score: {max(grade_total)}')

    # Điểm thấp nhất
    print(f'Lowest score: {min(grade_total)}')

    # Miền giá trị của điểm (cao nhất trừ thấp nhất)
    print(f'Range of scores: {max(grade_total) - min(grade_total)}')

    # Giá trị trung vị
    print(f'Median score: {statistics.median(grade_total)}')

    stats = list() # số lượng câu đúng/sai/không trả lời cho mỗi câu hỏi [{'right': 5', 'wrong': 7, 'no answer': 3}, {'right': 5', 'wrong': 7, 'no answer': 3}...]
    for i in range(num_question):
        stats.append({'right': 0, 'wrong': 0, 'no answer': 0})

    for student in grades_detail:
        for i in range(num_question):
            result = student['grade detail'][i]
            if result == 'right':
                stats[i]['right'] += 1
            elif result == 'wrong':
                stats[i]['wrong'] += 1
            else:
                stats[i]['no answer'] += 1

    # Trả về các câu hỏi bị học sinh bỏ qua nhiều nhất theo thứ tự: số thứ tự câu hỏi - số lượng học sinh bỏ qua -  tỉ lệ bị bỏ qua (nếu có cùng số lượng cho nhiều câu hỏi bị bỏ thì phải liệt kê ra đầy đủ)
    # Question that most people skip: 3 - 4 - 0.2 , 5 - 4 - 0.2 , 23 - 4 - 0.2
    num_skipped = list()
    for e in stats:
        num_skipped.append(e['no answer'])
    max_skipped = max(num_skipped)
    num_students = len(lines)
    s = ''
    for i in range(num_question):
        if num_skipped[i] == max_skipped:
            s += f' {i + 1} - {max_skipped} - {(max_skipped / num_students):.3f} ,'
    s = ('Question that most people skip:' + s)[:-2]
    print(s)
    
    # Trả về các câu hỏi bị học sinh sai qua nhiều nhất theo thứ tự: số thứ tự câu hỏi - số lượng học sinh trả lời sai - tỉ lệ bị sai (nếu có cùng số lượng cho nhiều câu hỏi bị sai thì phải liệt kê ra đầy đủ).
    # Question that most people answer incorrectly: 10 - 4 - 0.211, 14 - 4 - 0.211, 16 - 4 - 0.211, 19 - 4 - 0.222, 22 - 4 - 0.235
    num_wrong = list()
    for e in stats:
        num_wrong.append(e['wrong'])
    max_wrong = max(num_wrong)
    s = ''
    for i in range(num_question):
        if num_wrong[i] == max_wrong:
            s += f' {i + 1} - {max_wrong} - {(max_wrong / (max_wrong + stats[i]["right"])):.3f} ,'
    s = ('Question that most people answer incorrectly:' + s)[:-2]
    print(s)

    # Trả về danh sách điểm của học sinh
    id_grade_list = list()
    for e in grades_detail:
        id_grade_list.append(f"{e['id']},{e['grade total']}")
    return id_grade_list

# Task 1
filename = input('Enter a class file to grade (i.e. class1 or class1.txt):')
if not '.txt' in filename:
    filename += '.txt'

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
id_grade_list = grade_and_stats(valid_lines, answer_key)

# Task 4: Lưu kết quả vào tập tin
grades_file = filename[:-4] + '_grades.txt'
with open(grades_file, 'w') as write_file:
    for line in id_grade_list:
        write_file.write(line + '\n')
# print(f'Grades saved in {grades_file}')



