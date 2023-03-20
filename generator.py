import random
import numpy as np
import sys
import os
import pickle
from alive_progress import alive_bar

maxFactory = 49
maxWarehouse = 9

def write_output(i,factory,warehouse,cost_matrix):
    with open(f"{os.getcwd()}/or_instances/fact{i}.txt", "w") as f:
        f.write("numsources numdestinations \n")
        f.write(str(len(factory)) + " " + str(len(warehouse)))
        f.write("\n")
        f.write("a")
        f.write("\n")

        for l in range(len(factory)):
            f.write(str(factory[l]))
            if l!=(len(factory)-1):
                f.write(" ")
        
        f.write("\n")
        f.write("b")
        f.write("\n")

        for m in range(len(warehouse)):
            demand = warehouse[m]
            f.write(str(demand))
            if m!=(len(warehouse)-1):
                f.write(" ")

        f.write("\n")
        f.write("c")
        f.write("\n")

        for n in range(len(cost_matrix)):
            cost = cost_matrix[n]
            f.write(str(str(str(cost).split("[")[1]).split("]")[0]))
            if n!=(len(cost_matrix)-1):
                f.write("\n")
    with open(f"{os.getcwd()}/or_instances/fact{i}.pkl", "wb") as f:
        pickle.dump((factory, warehouse,cost_matrix), f)

def create_instance(i,j):
    totalSupplyPerFactory = 15*(i+1)
    
    if j>totalSupplyPerFactory:
        sys.exit()
        
    warehouses = np.ones(j+1, dtype=np.int64)
    count = totalSupplyPerFactory - j - 1

    for k in range(1,count+1):
        # random.choice(warehouses)
        warehouseIndex = random.randint(0,len(warehouses)-1)
        warehouses[warehouseIndex] = warehouses[warehouseIndex] + 1

    return warehouses

def separate_number(number, subvalues):
  subvalue_size = number // subvalues
  leftover = number % subvalues
  subvalues_list = [subvalue_size] * subvalues
  for i in range(leftover):
    subvalues_list[i] += 1
  return subvalues_list

def subFactory(i,j):
    warehouses = create_instance(i,j)
    demandArray = []
    subFactories = []

    # for k in range(j+1):
    #     demand = separate_number(warehouses[k],(i+1)) # split the element into (i+1) parts
    #     demandArray.append(demand)
    # print(demandArray)

    for m in range(j+1):
        demand = np.ones(i+1, dtype=np.int64)
        count = warehouses[m] - i - 1

        for k in range(1,count+1):
            demandIndex = random.randint(0,len(demand)-1)
            demand[demandIndex] = demand[demandIndex] + 1
        demandArray.append(demand)

    for i in range(len(demandArray[0])):
        for j in range(len(demandArray)):
            subFactories.append(demandArray[j][i])
    # print(f"warehouses: {warehouses}")
    # print(f"demandArray: {demandArray}")
    # print(f"subFactories: {subFactories}")

    return warehouses,subFactories

def cost(subFactories, warehouses):
    # matrix = np.ones((subFactories, warehouses), dtype=np.int64)
    matrix = np.full((subFactories, warehouses), 5)
    for i in range(subFactories):
        matrix[i][i % warehouses]=1
    return matrix

def write_output_htn(packages,sources, warehouses,i):
    with open(f"{os.getcwd()}/htn_instances/fact{i}.hddl", "w") as f:
        f.write(f"(define\n\t(problem fact" + str(i) + ")\n\t(:domain  domain_htn)\n\t(:objects\n")
        
        for p in range(0,packages):
            f.write(f"\t\tpackage_{p} - package\n")

        for q in range(len(sources)):
            f.write(f"\t\tfactory_{q} - location\n")

        for r in range(len(warehouses)):
            f.write(f"\t\twarehouse_{r} - location\n")

        for s in range(len(warehouses)):
            f.write(f"\t\ttruck_{s} - vehicle\n")

        f.write(f"\t)\n\t(:htn\n\t\t:parameters ()\n\t\t:subtasks (and\n")

        task_count = 0
        packagesPerFactory = 0
        packagesPrevious = 0
        for v in range(len(sources)):
            packagesPerFactory = sources[v]+packagesPerFactory
            for w in range(packagesPrevious,packagesPerFactory):
                f.write(f"\t\t(task{task_count} (deliver package_{w} warehouse_{v%len(warehouses)}))\n")
                task_count = task_count+1

            packagesPrevious = sum(sources[:v+1])
        
        f.write(f"\t\t)\n\t)\n\t(:init\n")
        
        for t in range(len(sources)):
            for u in range(len(warehouses)):
                f.write(f"\t\t(road factory_{t} warehouse_{u})\n")
                f.write(f"\t\t(road warehouse_{u} factory_{t})\n")

        packagesPerFactory = 0
        packagesPrevious = 0
        for v in range(len(subFactories)):
            packagesPerFactory = subFactories[v]+packagesPerFactory
            for w in range(packagesPrevious,packagesPerFactory):
                f.write(f"\t\t(at package_{w} factory_{v})\n")
            packagesPrevious = sum(subFactories[:v+1])

        for x in range(len(warehouses)):
            f.write(f"\t\t(at truck_{x} factory_0)\n")
        
        f.write(f"\t)\n)")


factCount = 0
with alive_bar((maxFactory+1)*(maxWarehouse+1)) as bar:
    for i in range(maxFactory+1):
        for j in range(maxWarehouse+1):
            warehouses,subFactories = subFactory(i,j)
            if(sum(warehouses)!=sum(subFactories)):
                print(f"Fact {factCount}: sources: {i+1} warehouses: {j+1} - Regenerating fact file...")
                while True:
                    warehouses,subFactories = subFactory(i,j)
                    if(sum(warehouses)==sum(subFactories)):
                        cost_matrix = cost(len(subFactories),len(warehouses))
                        write_output_htn(15*(i+1),subFactories,warehouses,factCount) # HTN
                        write_output(factCount,subFactories,warehouses,cost_matrix)
                        break
                    
            else:
                cost_matrix = cost(len(subFactories),len(warehouses))
                write_output_htn(15*(i+1),subFactories,warehouses,factCount) # HTN
                write_output(factCount,subFactories,warehouses,cost_matrix)
            factCount = factCount + 1
            bar()