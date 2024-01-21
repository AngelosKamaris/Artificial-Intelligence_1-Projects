import time
import csp
import csv


datafile = open('Στοιχεία Μαθημάτων.csv', 'r')
array = list(csv.reader(datafile))
array.pop(0)


domain=[(0,0)]*63

i=0
x=1
while i< 63:                            #a list from 1,1-21,3
    domain[i]=(x,1)
    domain[i+1]=(x,2)
    domain[i+2]=(x,3)
    i=i+3
    x=x+1

ldomain=[(0,0)]*42          
i=0
x=1
while i<42:                             #a list from 1,1-21,2, for the lessons with lab
    ldomain[i]=(x,1)
    ldomain[i+1]=(x,2)
    i=i+2
    x=x+1



def index_2d(myList, v):                    #program to find the position of a lesson in array
    for i, x in enumerate(myList):
        if v in x:
            return i, x.index(v)


variables=[row[1] for row in array]     #a list of all the lessons

i=0
dom={}

i=0
for les in variables:                       #a dict of all the lessons as keys and domain (or ldomain) as results
    position=index_2d(array, les)
    if(array[position[0]][4]=="TRUE"):
        dom[les]=ldomain
    else:
        dom[les]=domain
    

neighbours=dict()                           #a dict of all lessons as keys and each key has all the other lessons as results
for les in variables:
    n=[]
    for x in variables:
        if x!=les:
            n.append(x)
    neighbours[les]=n






def time_constraints(A,a,B,b):
    positionA=index_2d(array, A)
    positionB=index_2d(array, B)

    if(abs(a[0]-b[0])<2):
        if(array[positionA[0]][3]=="TRUE" and array[positionB[0]][3]=="TRUE"):               #if lesson is considered hard
            return False
        if(a[0]==b[0]):                            #if they are on the same day
            if(a[1]==b[1]):                                   #they can't be on the same hour
                return False

            if(array[positionA[0]][4]=="TRUE"):               #if A has a Lab, the Lab will go after the lesson 
                if(b[1]==a[1]+1 ):
                    return False

            if(array[positionB[0]][4]=="TRUE"):               #if B has a Lab, the Lab will go after the lesson 
                if(a[1]==b[1]+1 ):
                    return False

            if(array[positionA[0]][0]==array[positionB[0]][0]):                             #they can't be of same semester
                return False

            if(array[positionA[0]][2]==array[positionB[0]][2]):                             #the can't have the same teacher
                return False

        

    
    

    return True


class timetable(csp.CSP):

    def __init__(self):
        self.variables=variables
        self.domain=dom
        self.neighbours=neighbours
        csp.CSP.__init__(self, self.variables, self.domain, self.neighbours, time_constraints)
        


def program(tmtbl):                             #print timetable in order
    print("\n\n Timetable is: \n\n")
    print ("-" * 108)
    timelist=[ "9-12", "12-3", "3-6 "]

    for i in domain:
        lesson="-"*90
        for j in variables:
            if (tmtbl[j]==i):
                lesson=j
                position=index_2d(array, lesson)
                print("day:",i[0]," time:", timelist[i[1]-1]," | ",array[position[0]])
                break
        if (lesson=="-"*90):
            print("day:",i[0]," time:", timelist[i[1]-1]," | ",lesson)

    print ("-" * 108)
    print("\n\n")


if __name__ == '__main__':
    tmtbl=timetable()
    print("MAC\n\n")
    start = time.time()
    tmtbl.display(csp.backtracking_search( tmtbl, csp.mrv, csp.lcv, csp.mac))
    end = time.time()
    print("\n MAC finished after ", end-start, "seconds!")
    print("\n\n")
    program(tmtbl.infer_assignment())
    tmtbl=timetable()
    print("MinConflicts\n\n")
    start = time.time()
    mincon=csp.min_conflicts(tmtbl)
    tmtbl.display(mincon)
    end = time.time()
    print("\n MinConflicts finished after ", end-start, "seconds!")
    print("\n\n")
    program(mincon)
    tmtbl=timetable()
    print("Forward Checking\n\n")
    start = time.time()
    tmtbl.display(csp.backtracking_search(tmtbl, csp.mrv, csp.lcv, csp.forward_checking))
    end = time.time()
    print("\n FC finished after ", end-start, "seconds!")
    print("\n\n")
    program(tmtbl.infer_assignment())





