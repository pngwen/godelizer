"""
MIT License

Copyright (c) 2025 Robert Lowe

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import math
primes = [2, 3, 5, 7, 11, 13, 17]

def is_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    for i in range(2, math.ceil(n**0.5)+1):
        if n % i == 0:
            return False
    return True

def update_prime_list(n):
    """
    Add primes until the primes list is at least n elements long.
    """
    global primes
    while len(primes) < n:
        i = primes[-1] + 2
        while True:
            if is_prime(i):
                primes.append(i)
                break
            i += 2


def symbols(formula):
    """
    Returns the formula as a senquence of symbols.
    """
    sym = []
    i = 0

    while i < len(formula):
        # skip whitespace
        if formula[i] == ' ':
            i += 1
            continue

        # check for basic signs 
        if formula[i] in ['0', 'f', '|', '^', '(', ')']:
            sym.append(formula[i])
            i += 1
            continue

        # check for variables
        if formula[i].isalpha():
            var = ""
            while i < len(formula) and formula[i].isalpha():
                var += formula[i]
                i += 1
            sym.append(var)
            continue
        
        # otherwise, ignore and warn
        print(f"WARNING: Ignoring character {formula[i]}")
        i+=1
    return sym

def var_type(s):
    """
    Returns the type of the variable
    """
    if s[0].islower():
        return 1
    if s[0].isupper() and s.isupper():
        return 3
    return 2

def gen_mappings(sym):
    """
    Returns a dictionary mapping all the symbols in the formaul
    """        

    # we start with godel's root mapping
    mappings = {
        '0': 1,
        'f': 3,
        '~': 5,
        '|': 7,
        '^': 9,
        '(': 11,
        ')': 13 
    }

    #variable indexes
    vidx = [len(primes)-1] * 3

    for s in sym:
        if s not in mappings:
            t = var_type(s)
            update_prime_list(vidx[t-1]+1)
            mappings[s] = f"{primes[vidx[t-1]]}**{t}"
            vidx[t-1] += 1
    return mappings

def gen_exp(formula):
    sym = symbols(formula)
    update_prime_list(len(sym))
    mappings = gen_mappings(sym)
    exp = ""
    for i in range(len(sym)):
        exp += f"{primes[i]}**({mappings[sym[i]]})*"
    return exp[:-1]


def main(argv):
    print("Welcome to Godelizer!")
    print("This program will convert PM formulae into Godel numbers.")
    print("Syntax: ")
    print("0 - Nought")
    print("f - Successor")
    print("~ - Not ")
    print("| - Disjunction")
    print("^ - Universal quantifier")
    print("() - Brackets")
    print("a - Variables of the first type begin with lower case letter")
    print("A - Variables of the second type begin with upper case letter")
    print("AA - Variables of the third type are completely upper case")

    while True:
        formula = input("Enter a PM formula: ")
        exp = gen_exp(formula)
        print(f"The arithmetic formula to generate the Godel number is: {exp}")
        print(f"The Godel number of the formula is: {eval(exp)}")
        
if __name__ == "__main__":
    import sys
    sys.set_int_max_str_digits(int(1e6))
    main(sys.argv)