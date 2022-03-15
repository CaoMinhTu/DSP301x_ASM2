import pandas as pd

# Task 1: đọc file
filename = input('Enter a class file to grade (i.e. class1 or class1.txt):')
if not '.txt' in filename:
    filename += '.txt'

