import time
import os
import pickle
import xlsxwriter
from xlwt import Workbook
from transportationsimplex import transportation_simplex_method,get_total_cost,write_output
from alive_progress import alive_bar

def read_files(i):
    with open(f'{os.getcwd()}/or_instances/fact{i}.pkl', 'rb') as f:
        factory, warehouse,cost_matrix = pickle.load(f)
        return factory, warehouse,cost_matrix

def run_instance(i):
    factory, warehouse,cost_matrix = read_files(i)

    # print(f"Factories: \n {factory}")
    # print(f"Warehouses: {warehouse}")
    # print(f"Cost matrix: {cost_matrix}" )

    start_time = time.time()
    solution = transportation_simplex_method(factory, warehouse, cost_matrix)
    end_time = time.time()

    total_cost = get_total_cost(cost_matrix, solution)
    total_time = round((end_time - start_time)*1000,2)

    write_output(solution, total_cost, total_time, i)

    # excel(i,total_cost,total_time)

    # print(f"Solution: {solution}")
    # print(f"Total cost: {total_cost}")
    # print(f"Total runtime: {total_time}" )

# def excel(i,total_cost,total_time):

#     workbook = xlsxwriter.Workbook('output.xlsx')
#     worksheet = workbook.add_worksheet()

#     my_list = [i,total_cost,total_time]

#     for col_num, data in enumerate(my_list):
#         worksheet.write(i, col_num, data)

#     workbook.close()

with alive_bar(500) as bar:
    for i in range(0,500):
        run_instance(i)
        bar()

# def func1():
#     with alive_bar(120) as bar:
#         for i in range(0,120):
#             run_instance(i)
#             bar()

# def func2():
#     with alive_bar(40) as bar:
#         for i in range(120,160):
#             run_instance(i)
#             bar()

# def func3():
#     with alive_bar(20) as bar:
#         for i in range(160,180):
#             run_instance(i)
#             bar()
# def func4():
#     with alive_bar(20) as bar:
#         for i in range(180,200):
#             run_instance(i)
#             bar()

# t1 = threading.Thread(target=func1)
# t2 = threading.Thread(target=func2)
# t3 = threading.Thread(target=func3)
# t4 = threading.Thread(target=func4)

# t1.start()
# t2.start()
# t3.start()
# t4.start()

# t1.join()
# t2.join()
# t3.join()
# t4.join()