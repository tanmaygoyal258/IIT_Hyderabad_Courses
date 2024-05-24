import numpy as np
import sys

# sys.argv[0] will be file name

threads = int(sys.argv[1])
size = int(sys.argv[2])

sudoku = [np.linspace(0 , size , size , endpoint = False , dtype = np.int64) for i in range(size)]
sudoku = np.array(sudoku)
sudoku += 1
sudoku = sudoku.reshape(-1,)
np.random.shuffle(sudoku)

str_sudoku = []

first_line = str(threads) + " " + str(size) + "\n"
str_sudoku.append(first_line)

for i in range(size):
    line = ""
    for j in range(size):
        line += str(sudoku[i * size + j])
        line += " "
    line += "\n"
    str_sudoku.append(line)

input_file = "input.txt"

with open(input_file , 'w') as f:
    f.writelines(str_sudoku)

