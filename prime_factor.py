
# 06.07.2013 Arto Mujunen
# Tool to get Prime Factor values out from given number
# Results hve been saved to text file prime_factors.txt, so calculating same number again it will be picked from file.
# More info: http://en.wikipedia.org/wiki/Prime_factor

import sys
import time
import os

def doWeHaveTheNumInFile(num):
    if not os.path.exists('prime_factors.txt'):
        db_file = open(os.getcwd() + '/' + "prime_factors.txt", "w")
    # Open a file
    db_file = open(os.getcwd() + '/' + "prime_factors.txt", "r")
    found = False
    for line in db_file:
        if str(num) in line:
            found = True
            # Debug:
            print "Line: ", line
            break
    
    # Close opened file
    db_file.close()    
    return found

def all_prime_factors(n):
    """Returns all prime factors of a given integer"""
    animation = "|/-\\"
    
    old_value = 0
    factors = []
    d = 2
    animation_idx = 0
    animation_counter = 0
    while n > 1:
        if (animation_counter / 10000 == 1): # TODO change animation_counter to d
            print animation[animation_idx % len(animation)] + "\r",
            animation_idx += 1
            animation_counter = 0
        while n % d == 0:
            # Amu: fix for avoiding same numbers
            # Amu: TODO BUG e.g. with number 23452667799 - eternal loop. Is there some logical error in "while n % d == 0"??
            if (old_value is not d):
                factors.append(d)
                old_value = d
                n /= d
            else:
                n /= d
        # DEBUG
    #    if (d / 10000 == 1):
    #        print "N VALUE: ", n, "D value: ", d
        d = d + 1
        animation_counter = animation_counter + 1
    return factors
    
def main():
    number = int(raw_input("\nGive the number:\n"))
    
    num_available = doWeHaveTheNumInFile(number)
    
    # Start the timer
    start = time.clock()
    # If prime factors not in file yet - write it to there
    if not(num_available):
        print "Prime factors for: ", number
        
        factors = all_prime_factors(number)
        db_file = open("prime_factors.txt", "a")
        db_file.write("Prime factors for: " + str(number))
        db_file.write('\n')
        for item in factors:
            print str(item)
            db_file.write( str(item) )
            db_file.write('\n')
        # '---' indicate the end of prime factor info section
        db_file.write('-----------------\n')
        elapsed = (time.clock() - start)
        elapsed = elapsed * 1000.0
        print "It took ",'%.6f' % elapsed, " mill - seconds to run the script"
        
    # If prime factors already in file read from there
    else:
        print "\nRead from db - file!"
        print "Prime factors for: ", number, " are:"
        db_file = open("prime_factors.txt", "r")
        lines = db_file.read()
        len_of_num = len(str(number))
        start_pos = lines.find(str(number)) + len_of_num

        str_tarting_from_number = lines[start_pos:] # End part of string after "number"
        end_pos = str_tarting_from_number.find('--')
        
        # Final needed string
        wanted_str = str_tarting_from_number[:end_pos]
        print wanted_str.lstrip() #  '\n'

        db_file.close()
     
# boiler plate
if __name__ == '__main__':
    main()