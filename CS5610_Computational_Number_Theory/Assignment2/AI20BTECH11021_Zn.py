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

if __name__ == "__main__":

    # input_file = "testinput-Zn.txt"

    # with open(input_file , "r") as f:
    #     for line in f.readlines():
    #         l = line.strip('\n')
            
    #         # parsing the input based on if the delimiter is a space or a comma
    #         if ' ' in l:
    #             nums = [int(x) for x in l.split(' ')]
    #         elif ',' in l:
    #             nums = [int(x) for x in l.split(',')]

    #         Zn = Arithmetic_Zn(nums[0])

    #         print("{} , {} {} {}".format(Zn.exponentiation(nums[1] , nums[-1]), "true" if Zn.Zn_star(nums[1]) \
    #             else "false" , "," if Zn.inverse(nums[1]) else "" , Zn.inverse(nums[1]) if Zn.inverse(nums[1]) else ""))

    # n = int(input("Enter n: "))
    # a = int(input("Enter a: "))
    # b = int(input("Enter b: "))

    # Zn = Arithmetic_Zn(n)
    # print("{} , {} {} {}".format(Zn.exponentiation(a , b), "true" if Zn.Zn_star(a) \
    #     else "false" , "," if Zn.inverse(a) else "" , Zn.inverse(a) if Zn.inverse(a) else ""))

    n = 1117
    d = 93
    print((n-1)/d)
    Zn = Arithmetic_Zn(n)
    LHS = [i for i in range(1,n) if Zn.exponentiation(i,d)==1]

    RHS = []
    for i in range(1,n):
        if Zn.exponentiation(i , (n-1)//d) not in RHS:
            RHS.append(Zn.exponentiation(i , (n-1)//d))

    print(LHS)
    print(RHS)
    