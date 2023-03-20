import random
import colorama
import sys
import os

colorama.init()
folder_path = './or_instances_temp'
os.chdir(folder_path)

maxFactory = 2
maxWarehouse = 1
totalSupplyPerFactory = 150

if(maxWarehouse>10 or maxFactory>100):
    print(colorama.Fore.RED + "Max limit is exceeded")
    print(colorama.Style.RESET_ALL)
    sys.exit()

def separate_number(number, subvalues):
  subvalue_size = number // subvalues
  leftover = number % subvalues
  subvalues_list = [subvalue_size] * subvalues
  for i in range(leftover):
    subvalues_list[i] += 1
  return subvalues_list

def create_instance(i,j):
    totalSupply = random.randint(totalSupplyPerFactory-50,totalSupplyPerFactory+50)
    subFactorySupplies = []
    warehouseDemand = []
    
    if j==0:
        subFactorySupplies.append(totalSupply)
    elif j==1:
        temp = random.randint(1,int(totalSupply*2/3))
        subFactorySupplies.append(temp)
        temp = totalSupply-temp
        subFactorySupplies.append(temp)
    else:
        global tempSum

        tempX = random.randint(9,int(totalSupply/j))
        subFactorySupplies.append(tempX)

        tempSum = tempX

        for k in range(j-1):
            tempX = random.randint(10-k,int(totalSupply/j))
            if tempX>0:
                subFactorySupplies.append(tempX)
                tempSum=tempSum+tempX
            
        average = int(tempSum/(j-1))
        if totalSupply-tempSum>average:            
            subFactorySupplies.append(average)
        else:
            subFactorySupplies.append(totalSupply-tempSum)   
    
        subFactorySupplies = [x + y for x, y in zip(subFactorySupplies, separate_number(totalSupply-sum(subFactorySupplies),j+1))]

    # print(subFactorySupplies)
    # return sum(subFactorySupplies)
    return subFactorySupplies

def write_output(i,factory,warehouse):
    print(factory,warehouse)
    with open("fact"+str(i)+".txt", "w") as f:
        f.write("numsources numdestinations \n")
        f.write(str(len(factory)) + " " + str(len(warehouse)))
        f.write("\n")
        f.write("a")
        f.write("\n")

        for i in range(i+1):
            f.write(str(factory[i]) + " ")

        f.write("\n")
        f.write("b")
        f.write("\n")

        for i in range(i+1):
            demand = warehouse[i]
            f.write(str(demand) + " ")

        f.write("\n")
        f.write("c")
        f.write("\n")
        f.write("cost")

for i in range(maxWarehouse):
    print(f"Instance for 1 factories & {i+1} warehouses")
    arr = create_instance(1,i)
    write_output(i,arr,arr)