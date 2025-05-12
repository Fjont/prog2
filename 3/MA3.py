""" MA3.py

Student:
Mail:
Reviewed by:
Date reviewed:

"""
import random
import matplotlib.pyplot as plt
import math as m
import concurrent.futures as future
from statistics import mean 
from time import perf_counter as pc
import multiprocessing as mp

def approximate_pi(n): # Ex1
    #n is the number of points
    # Write your code here
    x = [random.uniform(-1,1) for _ in range(n)]
    y = [random.uniform(-1,1) for _ in range(n)]
    nc=0
    blue_dot=[[],[]]
    red_dot=[[],[]]
    #blue_dot[0].append(3)
    #blue_dot[0].append(4)

    for i in range(n):
        if m.sqrt(y[i]**2+x[i]**2)<=1:
            nc+=1
            red_dot[0].append(x[i])
            red_dot[1].append(y[i])
        else:
            blue_dot[0].append(x[i])
            blue_dot[1].append(y[i])
        
    pi=4*nc/n
    print(pi)
    plt.plot(red_dot[0],red_dot[1],'.',color='red',)
    plt.plot(blue_dot[0],blue_dot[1],'.',color='blue',)
    plt.title(f"n: {n}, pi≈{pi}")
   
    fig = plt.gcf()
    fig.set_size_inches(12, 12)
    plt.savefig(f"n_{n}", dpi=300)
    plt.show()
    return pi

def sphere_volume(n, d): #Ex2, approximation
    #n is the number of points
    # d is the number of dimensions of the sphere

    c= lambda n : [random.uniform(-1,1) for _ in range(n)] #list of n random number
    coord=[c(n) for _ in range(d)] #makes d lists of lists

    square = lambda cor : [x**2 for x in cor]
    dists = [m.sqrt(sum(square(col))) for col in zip(*coord)] #zip(*coord), *: makes lists element wise

    def inside(num):
         if num<=1:
              return 1
         else:
              return 0
    inside_list=list(map(inside,dists))
    nc=sum(inside_list)
    area=2**d*nc/n
    print(area)#area*probability
    return area
def hypersphere_exact(d): #Ex2, real value
    # d is the number of dimensions of the sphere 
    return m.pi**(d/2)/(m.gamma(d/2+1))

def idk(lista):
    return sphere_volume(lista[0],lista[1])
#Ex3: parallel code - parallelize for loop
def sphere_volume_parallel1(n,d,np=10):
    start = pc()
    with future.ProcessPoolExecutor() as ex:
        #p=[(n,d) for _ in range(np)]
        #results = ex.map(idk, p)#submit list comp
        results = [ex.submit(sphere_volume,n,d) for _ in range(np)]
    end = pc()
    
    print(f"Process ex3, took {round(end-start, 4)}seconds")
    
    return mean([val.result() for val in results])
    #n is the number of points
    # d is the number of dimensions of the sphere
    #np is the number of processes

#Ex4: parallel code - parallelize actual computations by splitting data
def sphere_volume_parallel2(n,d,np=10):
    #n is the number of points
    #d is the number of dimensions of the sphere
    #np is the number of processes
    start = pc()
    with future.ProcessPoolExecutor() as ex:
        #p=[(n,d) for _ in range(np)]
        #results = ex.map(idk, p)#submit list comp
        results = [ex.submit(sphere_volume,int(n/10),d) for _ in range(np)]
    end = pc()
    
    #print(f"Process ex4, took {round(end-start, 4)}seconds")
    
    #return mean([val.result() for val in results])
    return round(end-start, 4)
    
def main():
    #Ex1
    #dots = [1000, 10000, 100000]
    #for n in dots:
    #    approximate_pi(n)
    #Ex2
    n = 100000
    d = 2
    sphere_volume(n,d)
    print(f"Actual volume of {d} dimentional sphere = {hypersphere_exact(d)}")
    n = 100000
    d = 11
    sphere_volume(n,d)
    print(f"Actual volume of {d} dimentional sphere = {hypersphere_exact(d)}")

    #Ex3
    n = 100000
    d = 11
    avg=0
    start = pc()
    for y in range (10):
        avg+=sphere_volume(n,d)
    stop = pc()
    print(f"average: {avg/10}")
    print(f"Ex3: Sequential time of {d} and {n}: {stop-start}")
    print("What is parallel time?")
    sphere_volume_parallel1(n,d)

    #Ex4
    n = 1000000
    d = 11
    start = pc()
    sphere_volume(n,d)
    stop = pc()
    print(f"Ex4: Sequential time of {d} and {n}: {stop-start}")
    tid=sphere_volume_parallel2(n,d)
    print("What is parallel time?",tid)

    
    

if __name__ == '__main__':
	main()
