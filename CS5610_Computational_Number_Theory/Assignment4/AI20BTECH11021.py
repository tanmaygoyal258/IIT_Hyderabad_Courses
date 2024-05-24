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
                r_power = self.exponentiation(r_inverse , odd_factor * sum(r_exp)//2)
                root = (a_power * r_power) % self.n

                # we wish to find minimum root
                # if x is a root, so is -x, i.e p-x
                return min(root , self.n - root) 
            
            else:
                # find the exponent of current such that current^exponent=-1
                # and exponent is of the form 2^k * odd_factor
                exponent = odd_factor
                while True:
                    if self.exponentiation(current , exponent) == self.n-1:
                        break
                    exponent *= 2

                # update the values
                current *= self.exponentiation(r , (self.n-1) // (2*exponent))
                current %= self.n
                r_exp.append((self.n-1) // (2*exponent))
            
        return 0


class Polynomial:
    def __init__(self , coefficients = None , p = None):
        '''
        Initializes the polynomial

        Parameters:
            coefficients: if float or int, initializes a constant poly
                        else, list of coefficients
            p : if the polynomial exists in Z_p, default value is None
            integer : converts coefficients to integers, default value is True
        '''
        self.coefficents = None
        if type(coefficients) in [int , float]:
            self.coefficients = [coefficients]
        elif type(coefficients) == list and len(coefficients) > 0:
            self.coefficients = coefficients
        if p is not None:
            self.coefficients = [int(i % p) for i in self.coefficients]
        
        self.p = p
        self.degree = self.get_degree()
        

    def get_degree(self):
        '''
        Returns the degree of the polynomial.
        Adjusts if the leading coefficients are 0.
        [0] is trated as a polynomial of degree 0 with value 0
        '''
        if self.coefficients is None:
            return None
        
        while self.coefficients[-1] == 0:
            self.coefficients = self.coefficients[:-1]
            if len(self.coefficients) == 0:
                self.coefficients = [0]
                return 0

        return max(0 , len(self.coefficients)-1)


    def string_polynomial(self):
        '''
        Returns the string of the polynomial
        '''

        if self.coefficients is None:
            return "Undefined Polynomial"

        if self.degree == 0:
            return str(self.coefficients[0])

        coefficients = self.coefficients.copy()[::-1]
        str_polynomial = ""

        for idx , coeff in enumerate(coefficients):
            
            deg = len(coefficients) - 1 - idx
            if coeff == 0:
                continue

            elif coeff == 1:
                term = ""
                if deg == 0:
                    term = " + 1"
                elif deg == 1:
                    term = " + x"
                else:
                    term = " + x^{}".format(deg)
                # we remove the operator in the beginning
                if deg == self.degree:
                    term = term[3:]
                str_polynomial += term

            elif coeff == -1:
                term = ""
                if deg == 0:
                    term = " - 1"
                elif deg == 1:
                    term = " - x"
                else:
                    term = " -x^{}".format(deg)
                str_polynomial += term

            elif coeff > 0:
                term = ""
                if deg == 0:
                    term = " + {}".format(coeff)
                elif deg == 1:
                    term = " + {}x".format(coeff)
                else:
                    term = " + {}*x^{}".format(coeff , deg)
                # we remove the operator in the beginning
                if deg == self.degree:
                    term = term[3:]
                str_polynomial += term

            elif coeff < 0:
                term = ""
                if deg == 0:
                    term = " - {}".format(abs(coeff))
                elif deg == 1:
                    term = " - {}x".format(abs(coeff))
                else:
                    term = " -{}*x^{}".format(abs(coeff) , deg)
                str_polynomial += term
        return str_polynomial.strip()

    def add(self , other):
        '''
        Adds two given polynomials
        '''
        if self.p != other.p:
            print("Inconsistent fields for operations")
            return None

        small_poly = self if self.degree < other.degree else other
        large_poly = self if small_poly == other else other 

        new_poly_coeff = large_poly.coefficients.copy()
        for idx , coeff in enumerate(small_poly.coefficients):
            new_poly_coeff[idx] += coeff    
        return Polynomial(new_poly_coeff , self.p)

    def multiply(self , other):
        ''' 
        multiplies two given polynomials : could be scalar multiplication
        ''' 
        if self.p != other.p:
            print("Inconsistent fields for operations")
            return None

        # scalar multiplication
        if self.degree == 0:
            new_poly_coeff = [i * self.coefficients[0] for i in other.coefficients]
            return Polynomial(new_poly_coeff , self.p)
        elif other.degree == 0:
            new_poly_coeff = [i * other.coefficients[0] for i in self.coefficients]
            return Polynomial(new_poly_coeff , self.p)

        # polynomial multiplication
        else:
            new_poly_coeff = [0]*(self.degree + other.degree + 1)  
            for deg1 , coeff1 in enumerate(self.coefficients):
                for deg2 , coeff2 in enumerate(other.coefficients):
                    new_poly_coeff[deg1+deg2] += (coeff1 * coeff2) % self.p if self.p is not None \
                                                else (coeff1 * coeff2)
            return Polynomial(new_poly_coeff , self.p)  


    def subtract(self , other):
        '''
        subtracts two polynomials
        ''' 
        if self.p != other.p:
            print("Inconsistent fields for operations")
            return None
        negative_other = other.multiply(Polynomial(-1 , self.p))
        return self.add(negative_other)

    def division(self , other):
        '''
        divides polynomial self by polynomial other
        returns quotient and remainder
        '''
        if self.p != other.p:
            print("Inconsistent fields for operations")
            return None

        # if degree of other > degree of self, then quotient is 0
        if other.degree > self.degree:
            return Polynomial(0 , self.p) , self

        # if we divide by a scalar, we assume there is zero remainder
        if other.degree == 0:
            scalar = 1 / other.coefficients[0] if self.p is None else \
                    Arithmetic_Zn(self.p).inverse(other.coefficients[0])
            return self.multiply(Polynomial(scalar , self.p)) , Polynomial(0 , self.p)
            
        # we implement division for integers here
        # we continue till degree of remainder is less than that of divisor
        quotient_coefficients = [0] * (self.degree - other.degree + 1)
        dividend_coeff = self.coefficients.copy()
        divisor_coeff = other.coefficients.copy()
        divisor_deg = other.degree
        if self.p is not None: 
            zp_env = Arithmetic_Zn(self.p)

        while True:
            # creating the dividend for this iteration of the loop
            dividend = Polynomial(dividend_coeff , self.p)

            # creating the quotient for this iteration of the loop
            current_q_term = [0]*(dividend.degree - other.degree + 1)
            if self.p is None:
                current_q_term[-1] = dividend_coeff[-1]/divisor_coeff[-1]
            else:
                current_q_term[-1] = dividend_coeff[-1] * zp_env.inverse(divisor_coeff[-1])

            # updating the overall quotient
            quotient_coefficients[dividend.degree - other.degree] = current_q_term[-1]

            # updating the dividend
            current_q_poly = Polynomial(current_q_term , self.p)
            remainder = dividend.subtract(other.multiply(current_q_poly))

            # checking for the breaking condition
            if (remainder.degree < divisor_deg):
                quotient = Polynomial(quotient_coefficients , self.p)
                return quotient , remainder
            dividend_coeff = remainder.coefficients.copy()    
        
        return quotient , remainder

class Euclid_Polynomials:

    # defining the constructur class
    def __init__(self , poly1 , poly2 , p = None):
        self.p1 = poly1
        self.p2 = poly2
        self.p = p

        # we assume poly2 has higher degree
        self.poly1 = self.p1 if self.p1.degree < self.p2.degree else self.p2
        self.poly2 = self.p1 if self.poly1 == self.p2 else self.p2
    
        # to check if our polynomials are in the correct order:
        self.swap = (self.poly1 != self.p1)

        # setting up our matrix elements
        self.M11 = Polynomial(1 , self.p)
        self.M12 = Polynomial(0 , self.p)
        self.M21 = Polynomial(0 , self.p) 
        self.M22 = Polynomial(1 , self.p)

        # Scaling factor for the gcd since gcd is unique upto a scalar
        self.scale = None

    def calculate(self):
        '''
        Runs Extended Euclid's Algorithm for polynomials:
        '''
        while self.poly1.coefficients != [0]:

            # finding the new polynomials
            quotient , remainder = self.poly2.division(self.poly1)
            poly1_new = remainder
            poly2_new = self.poly1

            # setting up the matrix multiplication in equation form
            M11_new = quotient.multiply(Polynomial(-1 , self.p)).multiply(self.M11).add(self.M21)
            M12_new = quotient.multiply(Polynomial(-1 , self.p)).multiply(self.M12).add(self.M22)
            M21_new = self.M11
            M22_new = self.M12

            # updating the values
            self.poly1 , self.poly2 , self.M11 , self.M12 , self.M21 , self.M22 = poly1_new , poly2_new , M11_new , M12_new , M21_new , M22_new

    def gcd(self):
        '''
        returns the gcd of two polynomials
        '''
        # run Euclid's algorithm
        self.calculate()
        
        # the gcd is given by poly2
        # we will ensure the highest coefficient is 1, i.e gcd is monic
        self.scale = self.poly2.coefficients[-1]
        return self.poly2.division(Polynomial(self.scale , self.p))[0]

    def find_coeff(self):
        '''
        Using Bezout's Lemma, we can write 
        ax + by = gcd(a,b)
        Returns the values of x and y
        '''
        # run Euclid's algorithm
        self.calculate()
        # find the scaling factor
        self.gcd()

        # divide the coefficients by the scaling factor
        self.M22 = self.M22.division(Polynomial(self.scale , self.p))[0]
        self.M21 = self.M21.division(Polynomial(self.scale , self.p))[0]
        
        # if the numbers were swapped initially, return the swapped values
        if self.swap:
            return self.M22, self.M21
        return self.M21 , self.M22



if __name__ == "__main__":

    # Change input file name here
    input_file = "input-polygcd2.csv"
    
    with open(input_file , "r") as f:
        data = f.readlines()
        if len(data) != 3:
            print("Invalid Output")

        # picking out p
        p = int(data[0].split(",")[0])

        # picking out the polynomials
        poly1 = data[1].strip("\n").split(",")
        poly2 = data[2].strip("\n").split(",")
        poly1_deg = int(poly1[0])
        poly2_deg = int(poly2[0])
        
        poly1_coeff = [int(i) for i in poly1[1:poly1_deg+2]][::-1]
        poly2_coeff = [int(i) for i in poly2[1:poly2_deg+2]][::-1]

        # creating the polynomials
        poly1 = Polynomial(poly1_coeff , p)
        poly2 = Polynomial(poly2_coeff , p)

        # creating the environment
        env = Euclid_Polynomials(poly1 , poly2 , p)
        gcd = env.gcd()
        u,v = env.find_coeff()
        print("GCD: ", gcd.string_polynomial())
        print("u: ", u.string_polynomial())
        print("v: ", v.string_polynomial())