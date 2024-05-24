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


class chineseRemainderTheorem:

    # defining the constructor
    # again, we define the environment only for m and n
    # the moduli for both m and n are kept flexible
    def __init__(self , m , n):
        self.m = m 
        self.n = n
        self.alg = ExtendedEuclidAlg(self.m , self.n)
        # we know if there is unique solution, it is unique mod mn
        self.unique_mod = self.m * self.n

    def solve(self , a , b):
        '''
        This will solve the two simultaneous congruences using the following method:
        If gcd(m,n) = 1, then we simply return -1
        Else,
            x = a + my = b + nz
            => my-nz = b - a
            => y = m^{-1} * (b-a)
            => x = a + my
        '''
        if self.alg.gcd() != 1:
            return -1

        res = a + self.m * ((b - a) * self.alg.find_coeff()[0])   
        
        # res should lie in Zmn
        while res < 0: res += self.unique_mod
        while res >= self.unique_mod: res -= self.unique_mod
        return res

if __name__ == "__main__":

    # input_file = "testinput-crt.txt"

    # with open(input_file , "r") as f:
    #     for line in f.readlines():
    #         l = line.strip('\n')
            
    #         # parsing the input based on if the delimiter is a space or a comma
    #         if ' ' in l:
    #             nums = [int(x) for x in l.split(' ')]
    #         elif ',' in l:
    #             nums = [int(x) for x in l.split(',')]

    #         CRT = chineseRemainderTheorem(nums[1] , nums[-1])

    #         print(CRT.solve(nums[0] , nums[-2]))

    m = int(input("Enter m: "))
    n = int(input("Enter n: "))
    a = int(input("Enter a: "))
    b = int(input("Enter b: "))
    CRT = chineseRemainderTheorem(m , n)
    print(CRT.solve(a , b))