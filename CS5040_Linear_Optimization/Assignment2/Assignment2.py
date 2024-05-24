'''
LINEAR OPTIMIZATION ASSIGNMENT 2

CODE BY:
Ansh Raninga: EE20BTECH11043
Tanay Yadav: AI20BTECH11026
Tanmay Goyal: AI20BTECH11021
Tanmay Shah: EE20BTECH11061
'''

import numpy as np

def read_input(file_name):
    '''
    function to read the input from the csv file
    '''
    input = []
    with open(file_name , 'r') as f:
        for line in f:
            split_strip_chars = [float(char.strip()) for char in line.split(',') if char != '\n']
            input.append(split_strip_chars)
    return input


class UnboundedLP:

    def __init__(self , input):
        '''
        constructer function for the class
        '''
        self.input = np.array(input , dtype = np.float64)
        self.A = self.input[2:,:-1]
        self.b = self.input[2:,-1]
        self.start = self.input[0][:-1]
        self.cost = self.input[1][:-1]
        self.optimum_point = None
        self.optimum_value = None
        self.num_iters = 0
        # assuming max number of extreme points can be n choose 2
        self.max_iters = self.A.shape[0] * (self.A.shape[0] - 1) / 2 

    def dot(self , x , y):
        '''
        an alias function to take the dot product between two vectors
        '''
        return np.dot(x,y)

    def check_inequality(self , LHS , RHS , lesser_than = True , equal_to = True):
        '''
        a function to check for inequalities for vectors
        '''
        if lesser_than and equal_to:
            for (x,y) in zip(LHS , RHS):
                if x > y:
                    return False
            return True
        elif lesser_than and not equal_to:
            for (x,y) in zip(LHS , RHS):
                if x >= y:
                    return False
            return True
        elif not lesser_than and equal_to:
            for (x,y) in zip(LHS , RHS):
                if x < y:
                    return False
            return True
        else:
            for (x,y) in zip(LHS , RHS):
                if x <= y:
                    return False
            return True


    def find_tight_untight(self , point):
        '''
        a function to find the tight and untight equations for a given extreme point
        Tight rows are those which satisfy strict equality
        Untight rows are those which satisfy strict inequality
        '''
        A_tight = []
        b_tight = []
        A_untight = []
        b_untight = []

        for (row,val) in zip(self.A , self.b):
            if self.dot(row , point) == val:
                A_tight.append(row)
                b_tight.append(val)
            else:
                A_untight.append(row)
                b_untight.append(val)
        
        return A_tight , b_tight , A_untight , b_untight

    def find_test_eps(self , point , dir):
        '''
        function to find a suitable epsilon to figure out if the direction we wish to test
        leads to an increase in the cost or not
        Any random epsilon would not work because we wish to also make sure that the 
        new test point satisfies all constraints.
        '''
        epsilon = 1
        p = point + epsilon * dir   # test point
        
        while epsilon > 1e-06:
            if self.check_inequality(self.A @ p , self.b):
                return epsilon
            else:
                epsilon /= 2
        
        return 1e-06    # we provide a lower bound of 1e-06 for epsilon

    def find_correct_direction(self , point, direction_vecs):
        '''
        function to find the correct direction to move in from a given point
        we say a direction is correct if the cost increases in that direction
        '''
        col_num = 0
        
        while col_num < direction_vecs.shape[1]:
            dir = direction_vecs[: , col_num] 
            eps = self.find_test_eps(point , dir)
            if self.dot(self.cost , point + eps * dir) > self.dot(self.cost , point):
                return dir
            
            col_num += 1
        
        return None     # cost does not increase in any direction    
            
    def find_correct_eps(self , A_untight , b_untight , point , dir):
        '''
        function to find the epsilon to reach a neighbouring extreme point
        given the correct direction (direction in which cost increases)

        Here, we assume the correct direction to move in is +dir, and thus, our
        epsilon should not be negative, since it would imply the extreme point is in -dir
        direction.

        Since this is unboundedLP, if all the epsilon are negative, this means that epsilon
        wishes for us to move in one direction to reach extreme point, while the direction
        in which cost increases is the other direction. This leads to a contradiction,
        and we would begin moving in infinite space, and thus, there is no solution.
        '''
        epsilon = 0
        all_negative = True
        for (row , val) in zip(A_untight , b_untight):
            e = (val - self.dot(row , point)) / self.dot(row , dir)
            if epsilon == 0 and e > epsilon:
                epsilon = e
                all_negative = False
            elif e > 0:
                epsilon = min(epsilon , e)
                all_negative = False

        return epsilon if not all_negative else None

    def print_soln(self):
        '''
        function to print the solution to console
        '''
        if self.optimum_point is None:
            print("\nNo solution was found since it is unbounded.")
        else:
            print("\nOptimal solution has been found...")
            print("The optimum point is: {}".format(self.optimum_point))
            print("The optimum value is: {}".format(self.optimum_value))


    def solve(self):
        '''
        main function to solve the unbounded Linear Programming problem
        '''

        print("Starting search for optimal point...\n")
        current_point = self.start

        while self.num_iters <= self.max_iters and self.optimum_point is None:           

            print("Iteration{}: Current Vertex = {} and Cost = {}".format(self.num_iters + 1 , current_point , self.dot(self.cost , current_point)))       
            self.num_iters += 1       

            # find the set of tight and untight rows for the current point     
            A_tight , b_tight , A_untight , b_untight = self.find_tight_untight(current_point)
            
            # direction vectors to neighbors are given by cols of -A_tight inverse
            direction_vecs = -np.linalg.inv(A_tight)
            cost_increasing_direction = self.find_correct_direction(current_point , direction_vecs)

            # if there is no direction of increase, we have found optimal point
            if cost_increasing_direction is None:
                self.optimum_point = current_point
                self.optimum_value = self.dot(self.cost , self.optimum_point)
                break
            
            # else update the current point using the direction of increase and epsilon
            eps = self.find_correct_eps(A_untight , b_untight , current_point , cost_increasing_direction)
            
            # if eps is None, this means we reached a contradiction where the epsilons 
            # show that extreme point is in -dir direction, but cost increases in opposite
            # direction, Thus, we have no solution.
            if eps is None:
                break
            
            current_point += eps * cost_increasing_direction
        
        # print the final solution
        self.print_soln()


if __name__ == "__main__":

    file_name = "input.csv"
    input = read_input(file_name)

    LP_Problem = UnboundedLP(input)
    LP_Problem.solve()