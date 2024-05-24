import random

# defining a class for convinience
class two_SAT:

    # constructor
    def __init__(self , num_clauses , num_variables , clause_list):
        
        # holds number of clauses
        self.num_clauses = num_clauses

        # holds number of variables
        self.num_variables = num_variables
        
        # holds the clause literals
        self.clauses = []

        # holds if any literal in any clause is negated
        self.negations = []

        # constructing clauses and negations
        for clause in clause_list:
            c = []
            n = []
            for literal in clause:
                c.append(abs(literal))
                n.append(literal > 0)

            self.clauses.append(c)
            self.negations.append(n)

        # holds the assignment of variables
        self.assignment = [True] * self.num_variables


    def is_satisfied_clause(self , clause_number):
        '''
        checks if the clause can be satisfied by the assignment held by self.assignment

        Parameters
            clause_number: the index for the clause to be checked for in self.clauses

        Returns
            True if the clause can be satisfied by the assignment else False
        '''
        clause = self.clauses[clause_number]
        negation = self.negations[clause_number]

        for literal_idx , literal in enumerate(clause):

            # if the assignment is equal to the negation bool,
            # the literal contributes a True
            if self.assignment[literal - 1] == negation[literal_idx]:
                return True
        return False
    

    def update (self , clause_number):
        '''
        Updates the assignment of truth values after we obtain a unsatisfied clause

        Parameters
            clause_number: the index for the clause to be checked for in self.clauses

        Returns
            None, updates self.assignment
        '''

        clause = self.clauses[clause_number]

        # choose a random literal to flip
        to_update_index = random.randint(0 , len(clause) - 1)
        to_update_literal = clause[to_update_index]
        self.assignment[to_update_literal - 1] = not self.assignment[to_update_literal - 1]


    def convert_to_string(self):
        '''
        Converts the assignment of variables to a string of 1s and 0s

        Parameters
            None,  works on self.assignment

        Returns
            assignment_string: a string of 1s and 0s representing the assignment of variables
        '''

        assignment_string = ""
        for a in self.assignment:
            assignment_string += '1' if a else '0'
        return assignment_string

    

    def find_satisfying_assignment(self):
        '''
        Main driver code for the class to obtain the satisfying assignment
        Assumes all clauses are satisfiable. In case that is not true,
        we can change the infinite loop to have bounded number of iterations

        Parameters
            None
        
        Returns
            assignment_string: a string of 1s and 0s representing the assignment of variables
        '''
        
        # since input is guaranteed to be satisfiable
        while 1:    

            found_false_clause = False

            for idx , clause in enumerate(self.clauses):

                # check if any clause cannot be satisfied with current assignment
                if not self.is_satisfied_clause(idx):

                    # update the assignment
                    self.update(idx)
                    found_false_clause = True
                    break
            
            # if none of the clauses were unsatisfied, we have found a satisfying assignment
            if not found_false_clause:
                return self.convert_to_string()

        # in case we have bounded iterations, return the assignment
        return self.convert_to_string()
        
def main():
    '''
    Main driver code for the file
    '''

    # REPLACE THE INPUT  AND OUTPUT FILE NAME --------------------
    input_file_name = "2-SAT-input5.txt"
    output_file_name = "output.txt"

    clause_list = []

    # parsing the input
    with open(input_file_name) as f:
        for idx , line in enumerate(f.readlines()):
            if idx == 0:
                num_variables = int(line.strip('\n'))
            elif idx == 1: 
                num_clauses = int(line.strip('\n'))
            else:
                clause_list.append([int(x) for x in line.strip('\n').split(',')])
                

    # creating an instance of the class and finding the satisfying assignment
    two_sat = two_SAT(num_clauses , num_variables , clause_list)
    answer = two_sat.find_satisfying_assignment()

    # writing the satisfying assignment to an output file
    with open(output_file_name , 'w') as f:
        f.write(answer)

if __name__ == "__main__":
    main()