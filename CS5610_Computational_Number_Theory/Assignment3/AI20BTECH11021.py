import random

class ExtendedEuclidAlg:

    # defining the constructor
    def __init__(self , a , b):
        self.num1 = a
        self.num2 = b

        # we assume m < n
        self.m = a if a < b else b      
        self.n = b if self.m == a else a
        
        # to print the output in the correct order
        self.swap = (self.num1 != self.m)

        # setting up the matrix elements
        self.M11 = 1
        self.M12 = 0
        self.M21 = 0 
        self.M22 = 1
    
    def calculate(self):
        '''
        Runs Extended Euclid's Algorithm which is:
        (a_i , b_i) = (b_i % a_i , a_i)
        while a_i != 0

        When a_i = 0, b_i = gcd(a,b)
        '''
        while self.m != 0:

            # finding the new m and n
            q = self.n // self.m
            m_new = self.n - q * self.m
            n_new = self.m

            # setting up the matrix multiplication in equation form
            M11_new = -q * self.M11 + self.M21
            M12_new = -q * self.M12 + self.M22
            M21_new = self.M11
            M22_new = self.M12

            # updating the values
            self.m , self.n , self.M11 , self.M12 , self.M21 , self.M22 = m_new , n_new , M11_new , M12_new , M21_new , M22_new


    def gcd(self):
        '''
        returns the gcd of two numbers
        '''
        # run Euclid's algorithm
        self.calculate()
        
        # the gcd is then given by self.n
        return self.n

    def find_coeff(self):
        '''
        Using Bezout's Lemma, we can write 
        ax + by = gcd(a,b)
        Returns the values of x and y
        '''
        # run Euclid's algorithm
        self.calculate()

        # if the numbers were swapped initially, return the swapped values
        if self.swap:
            return self.M22 , self.M21
        return self.M21 , self.M22

        
class Arithmetic_Zn:
    
    # defining the constructor
    # for the environment Zn, we only take input as n
    # we keep the inputs flexible
    def __init__(self , n):
        self.n = n

    def exponentiation(self , element , power):
        '''
        Returns (element ^ power) in Zn
        '''
        
        # we perform the exponentiation using repeated squaring
        a = element % self.n
        # contains a^{POWERS OF 2}
        a_power = a     
        result = 1

        while power >= 1:
            if power & 1:
                result = (result * a_power) % self.n
            power >>= 1
            a_power = (a_power * a_power) % self.n
        
        return result

    def Zn_star(self , element):
        '''
        Returns if the element is in Zn_star
        i.e if it is coprime to n
        '''
        # running Euclid's Algorithm to calculate the gcd
        if ExtendedEuclidAlg(self.n , element).gcd() == 1:
            return True
        return False

    def inverse(self , element):
        '''
        Returns the inverse of the element in Zn
        Will return None if the inverse does not exist
        '''
        
        # running Euclid's extended Algorithm
        alg = ExtendedEuclidAlg(self.n , element)
        
        if alg.gcd() != 1:
            return 0 # since element is not in Zn_star
        else:
            inverse = alg.find_coeff()[1]
            
            # the inverse should lie in Zn
            while inverse < 0: inverse += self.n
            while inverse >= self.n: inverse -= self.n
            return inverse

    def square_root(self , a):
        '''
        returns the smallest sqaure root of a in Zn
        returns 0 if square root does not exist
        '''

        # for square root to exist a^{(p-1)/2} = 1
        if self.exponentiation(a , (self.n-1)//2) != 1:
            return 0

        # find a non-quadratic residue, i.e r^{(p-1)/2} = p-1
        # we can do this randomly, with probability of success = 1/2
        while True:
            r = random.choice(range(1 , self.n))
            if self.exponentiation(r , (self.n - 1)//2) == self.n-1:
                break
        
        # find the greatest odd factor of p-1
        odd_factor = self.n-1
        while odd_factor % 2 == 0:
            odd_factor >>= 1

        # initializing the variables
        r_exp = [0]
        current = a

        while True:
            
            # if current ^ odd_factor is 1, then we have found the exponent
            # solution is a^{-(odd_factor-1)/2} x r^{-(odd_factor * sum(r_exp))/2}
            if self.exponentiation(current , odd_factor) == 1:
                a_inverse = self.inverse(a)
                r_inverse = self.inverse(r)
                a_power = self.exponentiation(a_inverse , (odd_factor - 1)//2)
                r_power = self.exponentiation(r_inverse , odd_factor * sum(r_exp) //2)
                root = (a_power * r_power) % self.n

                # we wish to find minimum root
                # if x is a root, so is -x, i.e p-x
                return min(root , self.n - root) 
            
            # find the exponent of current such that current^exponent=-1
            # and exponent is of the form 2^k * odd_factor
            else:
                exponent = odd_factor
                while True:
                    if self.exponentiation(current , exponent) == self.n-1:
                        break
                    exponent *= 2

            # else update the values
            current *= self.exponentiation(r , (self.n-1) // (2*exponent))
            current %= self.n
            r_exp.append((self.n-1) // (2*exponent))
            
        return 0


if __name__ == "__main__":
    
    input_file = "inputSquareRoots.csv"

    with open(input_file , "r") as f:
        for line in f.readlines():
            l = line.strip('\n')
            
            items = l.split(',')
            a = int(items[0])
            p = int(items[1])

            arithmetic_env = Arithmetic_Zn(p)
            print(arithmetic_env.square_root(a))
        