import ast
import itertools
import random
import matplotlib.pyplot as plt

#SUPPORTING PROGRAMMES

def feedback_finder(guess: str,
                    code: list,
                    mode: str = "automatic",
                    codelength = 4,
                    colouramount = 6,
                    zeros = "off"
                    ):
    """
    Finds the feedback for a certain guess.

    Inputs:
    - guess, can be list or string
    - code
    - mode
    - codelength: the length of the code
    - colouramount: the amount of colours allowed in a code
    - zeros: whether or not zeros are allowed in the code

    Modes:
    - Automatic mode: the programme computes the feedback itself, using the given code and guess.
    - Guided mode: the programme provides the user with the given guess, and prompts the user to input the feedback obtained.
    - Manual mode: the programme asks the user to provide their guess and prompts the user to input the feedback obtained.

    Returns:
    The feedback, as a tuple: (black, white)
    If the mode is manual, the programme also returns the guess
    """
    if mode == "automatic":

        guess_list = number_converter(guess, codelength)

        if type(code) is not list:
            code_list = number_converter(code, codelength)
        else:
            code_list = code
        
        length = 0
        black = 0
        white = 0
        if zeros == "on":
            begin = 0
            end = colouramount
        else:
            begin = 1
            end = colouramount+1
        for i in range(begin, end):
            count_i_guess = 0
            count_i_code = 0
            for j in range(codelength):
                if int(guess_list[j]) == i:
                    count_i_guess += 1
                if int(code_list[j]) == i:
                    count_i_code += 1
            length += min(count_i_guess, count_i_code)
        for i in range (codelength):
            if guess_list[i] == code_list[i]:
                black += 1
        white = length - black
        return (black,white)
    
    if mode == "guided":
        feedback = ast.literal_eval(input(("Your next guess should be", guess, ". What is the feedback for this?"))) 
        
        return feedback
    
    if mode == "manual":
        guess = str(input("What did you guess?"))
        feedback = ast.literal_eval(input("What was the feedback?"))
        return feedback, guess       

def number_converter(number: str,
                    codelength: int = None):
    """
    Inputs:
    - number: str
    - codelength: If it is not inputted, it is set to the len(number)

    Returns:
    - a list instead of an string. For example, 1234 will become [1,2,3,4]
    """
    list = []
    if codelength is None:
        codelength = len(number)

    for i in range(codelength):
        peg = number[i]
        list.append(peg)
    
    return list

def set_constrictor(set: list,
                    guess: str,
                    feedback: tuple,
                    n: int = 4,
                    k: int = 6,
                    zeros: str = "off"):
    """
    Takes a set of codes, a guess, and a feedback, and returns the set of all codes that would have given that feedback to that guess.

    Inputs:
    - set: list
    - guess: list (for example: [1,2,3,4])
    - feedback: tuple
    - n: length of codes
    - k: amount of available colours
    - zeros: whether or not zeros are allowed in the code

    Returns:
    A new set of all the codes in the list that would have given the provided feedback to the provided guess.
    """
    newset = []
    for element in set:
        result = feedback_finder(element, guess, "automatic", n, k, zeros)
        if result == feedback:
            newset.append(element)

    return newset

def nextguess(guess: list,
              info: list
              ):
    """
    Used within the function knuth(). Takes a guess, finds the feedback, and then adds that guess and feedback to a list of guesses and feedbacks.

    Inputs:
    - guess: a list, for example [1,2,3,4]
    - info: a list of lists, with information about the current process. The lists with indices 0 and 1 are the list with the guesses done up til now, and the list of all feedbacks received.
    The programme adds the current guess and feedback to these lists.

    Returns:
    - the feedback
    """
    guesslist = info[0]
    feedbacklist = info[1]
    code = info[2]
    mode = info[3]

    feedback = feedback_finder(str(guess), code, mode)
    
    guesslist.append(guess)
    feedbacklist.append(feedback)
        
    info[4] = set_constrictor(info[4], str(guess), feedback)
    
    return feedback

def finalstretch(guess: list,
                 info: list
                 ):
    """
    Used in the function knuth().
    Narrows down the code when there are only a few possible codes left.

    Inputs:
    - guess: a list, for example [1,2,3,4]
    - info: a list with information about the current process

    Prints:
    - if printing is set to "on" in the function knuth(), this function prints the message "The code is..." with the code at the end

    Returns:
    - the amount of guesses it took to find the code
    - the code
    - a list of guesses made
    - a list of feedbacks received
    """
    if not guess == "done":
        feedback = nextguess(guess, info)

    codesleft = info[4]
    guesslist = info[0]
    feedbacklist = info[1]
    printing = info[5]
    codefound = False

    if len(codesleft) == 0:
        print("There seems to be an issue, returning the previous guesses and feedbacks.")
        return guesslist, feedbacklist

    if len(codesleft) == 1:
        code = codesleft[0]
    
    else:
        feedback = nextguess(codesleft[0], info)

        for i in range(len(codesleft)):
            if feedback == feedback_finder(codesleft[0], codesleft[i]):
                code = codesleft[i]
                codefound = True
                break
        
        if not codefound:
            print("There seems to be an issue, returning the previous guesses and feedbacks.")
            return guesslist, feedbacklist
        
    if guesslist[-1] != code:
        guesslist.append(code)
    if feedbacklist[-1] != (4,0):
        feedbacklist.append((4,0))
    
    if printing == "on":
        print("The code is", code)

    return len(guesslist), code, guesslist, feedbacklist

def set_creator(n: int,
                k: int,
                repeating: str = "on",
                zeros: str = "off"
                ):
    """
    Creates a list of all possible codes, given the length of the codes, the amount of colours allowed, whether or not repetition of colours is allowed, and whether or not we allow zeros.

    Inputs:
    - n: the length of the code
    - k: the amount of colours allowed
    - repeating: whether or not we allow repetition in the code
    - zeros: whether or not zeros are allowed in the code

    Returns:
    - the set of all possible codes, taking the given parameters into account
    """
    if repeating == "on":
        if zeros == "on":
            tupleset = list(itertools.product(list(range(0,k)), repeat = n))
        else:
            tupleset = list(itertools.product(list(range(1,k+1)), repeat = n))
    elif repeating == "off":
        if zeros == "on":
            tupleset = list(itertools.permutations(range(0, k), n))
        else:
            tupleset = list(itertools.permutations(range(1, k+1), n))

    set = []
    for element in tupleset:
        newelement = "".join(str(i) for i in element)
        set.append(newelement)
    return set

# INTELLIGENT FUNCTIONS
def best_guess_finder(possible_codes: list,
                      all_guesses: list,
                      n: int = 4,
                      k: int = 6,
                      zeros: str = "off",
                      printing:str = "off"):
    """
    Finds the next best guess for narrowing down the amount of possible codes.

    Inputs:
    - possible_codes: a list of all possible codes
    - all_guesses: a list of all possible guesses the codebreaker could make
    - n: the length of the codes
    - k: the amount of allowed colours
    - zeros: indicates whether we are allowed to include zeros in the code
    - printing: If set to "on", the code will print "Examining element..." with the number of the guess being examined. This gives an indication for how far along the process is.

    Returns:
    - previous_best_guesses[0]: A list with information about the best guess. The 0th element is the guess, the 1th is the sorted list of the number of codes left after each feedback, the 2nd is that same list, but now sorted by feedback. 
    - best_guess: the guess that has the lowest maximum amount of codes left after making that guess (if there are multiple, the programme chooses the guess that is lowest numerically)
    """

    guess_information = []
    elements = len(all_guesses)

    if len(possible_codes) == 0:
        print("The feedback you got was impossible.")
        raise ValueError("The previous feedback was impossible")

    # Iteration over all possible guesses

    if printing == "on":
        counter = 0
    for guess in all_guesses:
        if printing == "on":
            counter += 1
            print("Examining element ", counter, " of ", elements)
        groupkeys = {}    
        groups = []
        group_lengths = []


        for black in range (n+1):
            for white in reversed(range(n - black + 1)):
                groupkeys[(black,white)] = []
                groups.append(groupkeys[(black,white)])
                
    
        # Iteration over all possible codes
        for code in possible_codes:
            feedback = feedback_finder(guess, code, "automatic", n, k, zeros)
        
            black = feedback[0]
            white = feedback[1]

            groupkeys[(black,white)].append(code)

        for group in groups:
            group_lengths.append(len(group))
    
        sorted_lengths = sorted(group_lengths, reverse=True)

        guess_information.append([guess, sorted_lengths, group_lengths])
  
    if len(possible_codes) ==1:
        print(f"There is only one possible code, namely {possible_codes[0]}")
        previous_best_guesses = "found"
        best_guess = "found"
    else:
        previous_best_guesses = guess_information
        best_guesses = []
        iteration = 0
        while True: # Repeat until found best guess 
            # Check if group sizes are all already equal
            done = True
            for guess in previous_best_guesses:
                if guess[1] != previous_best_guesses[0][1]:
                    done = False
                    break 
            # If group sizes are not equal, look at next group size
            if not done:            
                for element in previous_best_guesses:
                    if best_guesses == []:
                        best_guesses.append(element)
                    elif element[1][iteration] < best_guesses[0][1][iteration]:
                        best_guesses = [element]
                    elif element[1][iteration] == best_guesses[0][1][iteration]:
                        best_guesses.append(element)
                iteration+=1
                previous_best_guesses = best_guesses
                best_guesses = []
            # If they are equal, do this:
            else: 
                found_best_guess = False
                for guess in previous_best_guesses:
                    if not found_best_guess and guess[0] in possible_codes:
                        best_guess = guess[0]
                        found_best_guess = True   
                if not found_best_guess:     
                    best_guess = previous_best_guesses[0][0]
                break

    return previous_best_guesses[0], best_guess

def group_finder(guess: list,
                 possible_codes: list,
                 k: int,
                 repeating: str = "on",
                 zeros:str = "off",
                 printing: str = "off"
                 ):
    """CHANGE
    Sorts codes based on what feedback they would give to the given guess.

    Inputs:
    - guess
    - n: length of code
    - k: amount of colours in code
    - repeating: whether or not repetition is allowed
    - zeros: whether or not zeros are allowed in the code
    - printing: if set to "on", the programme prints "Examining code..." for each code, giving an indication of the progress made

    Returns:
    - groups: a list of lists, each inner list corresponding to a feedback
    - group_lengths: a list of the number of codes left after each feedback
    - keys: a list of the feedbacks considered
    """

    groupkeys = {}    
    groups = []
    keys = []
    group_lengths = []

    n = len(guess)

    for black in range (n+1):
        for white in reversed(range(n - black + 1)):
            groupkeys[(black,white)] = []
            groups.append(groupkeys[(black,white)])
            keys.append((black,white))

    
    # Iteration over all possible codes
    counter = 0
    for code in possible_codes:
        counter += 1
        if printing == "on":
            print(counter)
        feedback = feedback_finder(guess, code, "automatic", n, k, zeros)
        
        black = feedback[0]
        white = feedback[1]

        groupkeys[(black,white)].append(code)

    for group in groups:
        group_lengths.append(len(group))

    return groups, group_lengths, keys

#PLAYING THE GAME

def play_mastermind(code:list = [random.randint(1,6),random.randint(1,6), random.randint(1,6), random.randint(1,6)]):
    """
    A programme in which a player is the codebreaker and the computer is the codemaker.

    Input:
    - code (set to a random code by default)
    """
    feedback = None
    while feedback != (4,0):
        guess = str(input("What is your guess?"))
        if guess == "help":
            print("The code is", code)
            break
        
        feedback = feedback_finder(guess, code, "automatic")
        if feedback == (4,0):
            break
        print("Your guess", guess, "resulted in feedback", feedback)
    
    print("Well done, you have cracked the code!")
    return code

#GUIDED GAME
def knuth(code: str = None,
          mode: str = "guided",
          printing: str = "on"):
    """
    Helps the user find the codemaker's code using Knuth's algorithm.

    Inputs:
    - code. The default is None, since the user does not know the code. The code can be input as a string when testing the programme.
    - mode: can be either guided (the default mode), or testing
    - printing: whether or not the programme prints the message "The code is..." at the end. Can be turned off for testing.

    Returns:
    Returns:
    - the amount of guesses it took to find the code
    - the code
    - a list of guesses made
    - a list of feedbacks received
    """


    guess_list = []
    feedback_list = []
    info = [guess_list, feedback_list, code, mode, set_creator(4,6), printing]

    feedback = nextguess(1122, info)

    if feedback == (0, 3):
        feedback = nextguess(1213, info)
        
        if feedback == (1,2):
            return finalstretch(1415, info)
        
        elif feedback == (1,1):
            return finalstretch(1145, info)
        
        elif feedback == (2,1):
            return finalstretch(4115,info)

        elif feedback == (2,0):
            return finalstretch(1145, info)

        else:
            return finalstretch("done", info)

    elif feedback == (0,2):   #SITUATION A
        feedback = nextguess(2344, info)

        if feedback == (0,2):    
            feedback = nextguess(3215, info)

            if feedback == (2,1):
                return finalstretch(3231, info)

            elif feedback == (3,0):
                return finalstretch(3213, info)
            
            else:
                return finalstretch("done",info)

        elif feedback == (0,1):      
            feedback = nextguess(5215, info)

            if feedback == (1,1):
                return finalstretch(3511, info)

            elif feedback == (1,0):
                return finalstretch(3611, info)

            else:
                return finalstretch("done", info)

        elif feedback == (0,0):
            return finalstretch(1515, info)
        
        elif feedback == (1,2):
            return finalstretch(2413, info)

        elif feedback == (1,1):
            feedback = nextguess(2415, info)

            if feedback == (1,1):
                return finalstretch(2253, info)

            elif feedback == (1,0):
                return finalstretch(2236, info) 

            else:
                return finalstretch("done", info)
        
        elif feedback == (1,0):
            return finalstretch(2256,info)

        elif feedback == (2,1):
            return finalstretch(2234, info)

        elif feedback == (2,0):   
            return finalstretch(3315, info)

        elif feedback == (3,0):   
            return finalstretch(2314, info)

        else:
            return finalstretch("done", info)

    elif feedback == (0,1):   #SITUATION B
        feedback = nextguess(2344, info)

        if feedback == (0,3):
            return finalstretch(2335, info)
    
        elif feedback == (0,2):
            feedback = nextguess(3235, info)
                            
            if feedback == (0,1):
                return finalstretch(4613, info)

            elif feedback == (1,2):
                return finalstretch(5263, info)
            
            elif feedback == (1,1):
                return finalstretch(3413, info)
            
            elif feedback == (1,0):
                return finalstretch(3416, info)

            elif feedback == (2,1):
                return finalstretch(3256, info)     

            elif feedback == (2,0):
                return finalstretch(1336, info)
                
            elif feedback == (3,0):
                return finalstretch(1536, info)
            
            else:
                return finalstretch("done", info)

        elif feedback == (0,1):
            feedback = nextguess(3516, info)

            if feedback == (0,3):
                return finalstretch(4651, info)
            
            elif feedback == (0,2):
                return finalstretch(6255, info)
            
            elif feedback == (1,3):
                return finalstretch(5613, info)
            
            elif feedback == (1,2):
                return finalstretch(1461, info)
            
            elif feedback == (1,1):
                return finalstretch(4551, info)
            
            elif feedback == (2,2):
                return finalstretch(1113, info)
            
            elif feedback == (2,1):
                return finalstretch(3551, info)
            
            elif feedback == (2,0):
                return finalstretch(4515, info)
            
            elif feedback == (3,0):
                return finalstretch(1145, info)
            
            else:
                return finalstretch("done", info)

        elif feedback == (0,0):
            feedback = nextguess(5515, info)

            if feedback == (2,0):
                return finalstretch(1516, info)
            
            elif feedback == (3,0):
                return finalstretch(1516, info)
            
            else:
                return finalstretch("done", info)
    
        elif feedback == (1,2):
            feedback = nextguess(3245, info)

            if feedback == (0,3):
                return finalstretch(2436, info)
            
            elif feedback == (2,1):
                return finalstretch(3234, info)
            
            elif feedback == (3,0):
                return finalstretch(3243, info)
            
            else:
                return finalstretch("done", info)

        elif feedback == (1,1):
            feedback = nextguess(4514, info)

            if feedback == (0,2):
                return finalstretch(2456, info)
            
            elif feedback == (0,1):
                return finalstretch(2635, info)
            
            elif feedback == (0,0):
                return finalstretch(2636, info)
            
            elif feedback == (1,2):
                return finalstretch(1356, info)
            
            elif feedback == (1,1):
                return finalstretch(4361, info)
            
            elif feedback == (1,0):
                return finalstretch(1635, info)
            
            elif feedback == (2,0):
                return finalstretch(3614, info)
            
            elif feedback == (3,0):
                return finalstretch(4414, info)
            
            else:
                return finalstretch("done", info)

        elif feedback == (1,0):
            feedback = nextguess(3315, info)

            if feedback == (0,2):
                return finalstretch(5641, info)
            
            elif feedback == (0,1):
                return finalstretch(2566, info)
            
            elif feedback == (1,2):
                return finalstretch(5361, info)
            
            elif feedback == (1,1):
                return finalstretch(5614, info)

            elif feedback == (1,0):
                return finalstretch(6614, info)

            elif feedback == (2,1):
                return finalstretch(3331, info)

            elif feedback == (3,0):
                return finalstretch(3316, info)

            else:
                return finalstretch("done", info) 

        elif feedback == (2,2):
            return finalstretch(2434, info)

        elif feedback == (2,1):
            return finalstretch(2425, info)

        elif feedback == (2,0):
            feedback = nextguess(1545, info)

            if feedback == (0,2):
                return finalstretch(2654, info)
            
            elif feedback == (0,1):
                return finalstretch(2353, info)
            
            elif feedback == (0,0):
                return finalstretch(1136, info)
            
            elif feedback == (1,1):
                return finalstretch(2564, info)
            
            elif feedback == (1,0):
                return finalstretch(2335, info)
            
            else:
                return finalstretch("done", info)

        elif feedback == (3,0):
            return finalstretch(1335, info)

        else:
            return finalstretch("done", info)

    elif feedback == (0,0):    #SITUATION C
        feedback = nextguess(3345, info)
        
        if feedback == (0,3):
            feedback = nextguess(4653, info)

            if feedback == (1,3):
                return finalstretch(4536, info)
            
            elif feedback == (1,2):
                return finalstretch(4534, info)
            
            elif feedback == (3,0):
                return finalstretch(4453, info)
            
            else:
                return finalstretch("done", info)
            
        elif feedback == (0,2):
            feedback = nextguess(6634, info)

            if feedback == (0,3):
                return finalstretch(4566, info)
            
            elif feedback == (0,2):
                return finalstretch(4556, info)
            
            elif feedback == (1,2):
                return finalstretch(4656, info)
            
            elif feedback == (1,1):
                return finalstretch(5653, info)
            
            elif feedback == (1,0):
                return finalstretch(1444, info)
            
            elif feedback == (2,1):
                return finalstretch(5636, info)
            
            elif feedback == (2,0):
                return finalstretch(4654, info)
            
            elif feedback == (3,0):
                return finalstretch(1413, info)
            
            else:
                return finalstretch("done", info)
   
        elif feedback == (0,1):
            feedback = nextguess(6646, info)

            if feedback == (1,2):
                return finalstretch(1416, info)
            
            elif feedback == (2,2):
                return finalstretch(1416, info)
            
            elif feedback == (2,1):
                return finalstretch(5666, info)
            
            else:
                return finalstretch("done", info)

        elif feedback == (1,3):
            return finalstretch(3453, info)
        
        elif feedback == (1,2):
            feedback = nextguess(3454, info)

            if feedback == (0,3):
                return finalstretch(4535, info)
            
            elif feedback == (0,2):
                return finalstretch(1436, info)
            
            elif feedback == (1,2):
                return finalstretch(4356, info)
            
            elif feedback == (1,1):
                return finalstretch(3536, info)
            
            elif feedback == (2,1):
                return finalstretch(3564, info)
            
            elif feedback == (2,0):
                return finalstretch(3463, info)
            
            elif feedback == (3,0):
                return finalstretch(3456, info)
            
            else:
                return finalstretch("done", info)

        elif feedback == (1,1):
            feedback = nextguess(3636, info)

            if feedback == (0,2):
                return finalstretch(4364, info)
            
            elif feedback == (0,1):
                return finalstretch(4565, info)
            
            elif feedback == (0,0):
                return finalstretch(4544, info)
            
            elif feedback == (1,2):
                return finalstretch(4366, info)
            
            elif feedback == (1,1):
                return finalstretch(1565, info)
            
            elif feedback == (1,0):
                return finalstretch(4546, info)
            
            elif feedback == (2,1):
                return finalstretch(3466, info)
            
            elif feedback == (2,0):
                return finalstretch(3556, info)
            
            else:
                return finalstretch("done", info)

        elif feedback == (1,0):
            feedback = nextguess(3656, info)

            if feedback == (1,2):
                return finalstretch(5665, info)
            
            elif feedback == (1,1):
                return finalstretch(6446, info)
            
            elif feedback == (1,0):
                return finalstretch(4446, info)
            
            elif feedback == (2,0):
                return finalstretch(4646, info)
            
            else:
                return finalstretch("done", info)

        elif feedback == (2,2):
            return finalstretch(3435, info)
        
        elif feedback == (2,1):
            feedback = nextguess(3443, info)

            if feedback == (0,2):
                return finalstretch(4355, info)
            
            elif feedback == (1,2):
                return finalstretch(3334, info)
            
            elif feedback == (1,1):
                return finalstretch(3356, info)
            
            elif feedback == (2,0):
                return finalstretch(3455, info)
            
            else:
                return finalstretch("done", info)

        elif feedback == (2,0):
            feedback = nextguess(3636, info)

            if feedback == (0,2):
                return finalstretch(5365, info)
            
            elif feedback == (0,1):
                return finalstretch(6445, info)
            
            elif feedback == (0,0):
                return finalstretch(1444, info)
            
            elif feedback == (1,1):
                return finalstretch(3565, info)
            
            elif feedback == (1,0):
                return finalstretch(4645, info)
            
            elif feedback == (2,0):
                return finalstretch(3446, info)
            
            else:
                return finalstretch("done", info)

        elif feedback == (3,0):
            return finalstretch(3446, info)
        
        else:
            return finalstretch("done", info)

    elif feedback == (1,2):    #SITUATION D
        feedback = nextguess(1213, info)       

        if feedback == (0,3):
            return finalstretch(1145, info)

        elif feedback == (0,2):
            return finalstretch(1415, info)
        
        elif feedback == (1,2):
            feedback = nextguess(1114, info)

            if feedback == (2,0):
                return finalstretch(2115, info)
                
            else:
                return finalstretch("done", info)             

        elif feedback == (1,1):
            return finalstretch(2412, info) 
                
        elif feedback == (2,1):
            return finalstretch(1145, info)                                 

        elif feedback == (2,0):
            return finalstretch(1145, info)

        elif feedback == (3,0):
            return finalstretch(1114, info)

        else:
            return finalstretch("done", info)
    
    elif feedback == (1,1):     #SITUATION E
        feedback = nextguess(1134, info)

        if feedback == (0,3):
            return finalstretch(1312, info)
        
        elif feedback == (0,2):
            feedback = nextguess(3521, info)

            if feedback == (0,2):
                return finalstretch(4612, info)
            
            elif feedback == (1,2):
                return finalstretch(3312, info)
            
            elif feedback == (1,1):
                return finalstretch(2423, info)
            
            elif feedback == (2,0):
                return finalstretch(4621, info)
            
            elif feedback == (3,0):
                return finalstretch(3321, info)
            
            else:
                return finalstretch("done", info)
    
        elif feedback == (0,1):
            feedback = nextguess(2352, info)

            if feedback == (0,3):
                return finalstretch(3226, info)

            elif feedback == (0,2):
                return finalstretch(5621, info)
            
            elif feedback == (1,2):
                return finalstretch(2223, info)
            
            elif feedback == (1,1):
                return finalstretch(6242, info)
            
            elif feedback == (2,1):
                return finalstretch(2323, info)
            
            elif feedback == (2,0):
                return finalstretch(2462, info)
            
            else:
                return finalstretch("done", info)

        elif feedback == (0,0):
            feedback = nextguess(2525, info)

            if feedback == (1,2):
                return finalstretch(2252, info)
            
            elif feedback == (1,1):
                return finalstretch(2262, info)
            
            elif feedback == (3,0):
                return finalstretch(2225, info)
            
            else:
                return finalstretch("done", info)
            
        elif feedback == (1,3):
            return finalstretch(1341, info)

        elif feedback == (1,2):
            feedback = nextguess(1315, info)

            if feedback == (0,3):
                return finalstretch(4151, info)
            
            elif feedback == (0,2):
                return finalstretch(4161, info)
            
            elif feedback == (1,2):
                return finalstretch(6451, info)
            
            elif feedback == (1,1):
                return finalstretch(1461, info)
            
            elif feedback == (2,2):
                return finalstretch(1351, info)
            
            elif feedback == (2,1):
                return finalstretch(1361, info)
            
            elif feedback == (3,0):
                return finalstretch(1113, info)
            
            else:
                return finalstretch("done", info)

        elif feedback == (1,1):
            feedback = nextguess(1516, info)

            if feedback == (0,2):
                return finalstretch(2145, info)
            
            elif feedback == (0,0):
                return finalstretch(2324, info)
            
            elif feedback == (1,2):
                return finalstretch(1661, info)
            
            elif feedback == (1,1):
                return finalstretch(1245, info)
            
            elif feedback == (2,2):
                return finalstretch(1561, info)
            
            elif feedback == (2,1):
                return finalstretch(1551, info)
            
            elif feedback == (3,0):
                return finalstretch(1511, info)
            
            else:
                return finalstretch("done", info)

        elif feedback == (1,0):
            feedback = nextguess(1256, info)

            if feedback == (0,2):
                return finalstretch(2524, info)
            
            elif feedback == (1,1):
                return finalstretch(5224, info)
            
            elif feedback == (1,0):
                return finalstretch(2224, info)
            
            else:
                return finalstretch("done", info)
            
        elif feedback == (2,2):
            return finalstretch(1314, info)
        
        elif feedback == (2,1):
            return finalstretch(1315, info)
        
        elif feedback == (2,0):
            return finalstretch(1235, info)
        
        else:
            return finalstretch("done", info)

    elif feedback == (1,0):     #SITUATION F
        feedback = nextguess(1344, info)

        if feedback == (0,3):
            return finalstretch(1335, info)
        
        elif feedback == (0,2):
            feedback = nextguess(3135, info)

            if feedback == (0,1):
                return finalstretch(4623, info)
            
            elif feedback == (1,2):
                return finalstretch(5163, info)
            
            elif feedback == (1,1):
                return finalstretch(3423, info)
            
            elif feedback == (1,0):
                return finalstretch(3426, info)
            
            elif feedback == (2,1):
                return finalstretch(3156, info)
            
            elif feedback == (2,0):
                return finalstretch(1436, info)
            
            elif feedback == (3,0):
                return finalstretch(1536, info)
            
            else:
                return finalstretch("done", info)
    
        elif feedback == (0,1):
            feedback = nextguess(3526, info)

            if feedback == (0,3):
                return finalstretch(4652, info)
            
            elif feedback == (0,2):
                return finalstretch(6155, info)
            
            elif feedback == (1,3):
                return finalstretch(5623, info)
            
            elif feedback == (1,2):
                return finalstretch(1462, info)
            
            elif feedback == (1,1):
                return finalstretch(4552, info)
            
            elif feedback == (2,2):
                return finalstretch(1123, info)
            
            elif feedback == (2,1):
                return finalstretch(3552, info)
            
            elif feedback == (2,0):
                return finalstretch(4525, info)
            
            elif feedback == (3,0):
                return finalstretch(1145, info)
            
            else:
                return finalstretch("done", info)
    
        elif feedback == (0,0):
            feedback = nextguess(5525, info)

            if feedback == (2,0) or feedback == (3,0):
                return finalstretch(1516, info)
            
            else:
                return finalstretch("done", info)

        elif feedback == (1,2):
            feedback = nextguess(3145, info)

            if feedback == (0,3):
                return finalstretch(1436, info)
            
            elif feedback == (2,1):
                return finalstretch(3134, info)
            
            elif feedback == (3,0):
                return finalstretch(3143, info)
            
            else:
                return finalstretch("done", info)

        elif feedback == (1,1):
            feedback = nextguess(4524, info)

            if feedback == (0,2):
                return finalstretch(1456, info)
            
            elif feedback == (0,1):
                return finalstretch(1635, info)
            
            elif feedback == (0,0):
                return finalstretch(1636, info)
            
            elif feedback == (1,2):
                return finalstretch(1356, info)
            
            elif feedback == (1,1):
                return finalstretch(4362, info)
            
            elif feedback == (1,0):
                return finalstretch(1336, info)
            
            elif feedback == (2,0):
                return finalstretch(3624, info)
            
            elif feedback == (3,0):
                return finalstretch(4424, info)
            
            else:
                return finalstretch("done", info)

        elif feedback == (1,0):
            feedback = nextguess(3325, info)

            if feedback == (0,2):
                return finalstretch(5642, info)
            
            elif feedback == (0,1):
                return finalstretch(1566, info)
            
            elif feedback == (1,2):
                return finalstretch(5362, info)
            
            elif feedback == (1,1):
                return finalstretch(5624, info)
            
            elif feedback == (1,0):
                return finalstretch(6624, info)
            
            elif feedback == (2,1):
                return finalstretch(3332, info)
            
            elif feedback == (3,0):
                return finalstretch(3326, info)
            
            else:
                return finalstretch("done", info)

        elif feedback == (2,2):
            return finalstretch(1434, info)
        
        elif feedback == (2,1):
            return finalstretch(1415, info)
        
        elif feedback == (2,0):
            feedback = nextguess(1415, info)

            if feedback == (0,1):
                return finalstretch(3324, info)
            
            elif feedback == (1,2):
                return finalstretch(1546, info)
            
            elif feedback == (1,1):
                return finalstretch(1356, info)
            
            elif feedback == (1,0) or feedback == (2,0):
                return finalstretch(1136, info)
            
            else:
                return finalstretch("done", info)

        elif feedback == (3,0):
            return finalstretch(1335, info)
        
        else:
            return finalstretch("done", info)

    elif feedback == (2,2):     #DONE
        return finalstretch(1213, info)
    
    elif feedback == (2,1):     #situation G, DONE
        feedback = nextguess(1223, info)

        if feedback == (0,3):
            return finalstretch(2145, info)
        
        elif feedback == (0,2):
            return finalstretch(4115, info)
        
        elif feedback == (1,2):
            return finalstretch(2145, info)
        
        elif feedback == (1,1):
            return finalstretch(4512, info)
        
        elif feedback == (2,1):
            return finalstretch(1245, info)
        
        elif feedback == (2,0):
            return finalstretch(1415, info)
        
        elif feedback == (3,0):
            return finalstretch(1145, info)
        
        else:
            return finalstretch("done", info)
    
    elif feedback == (2,0):     #situation H, DONE
        feedback = nextguess(1234, info)

        if feedback == (0,3):
            feedback = nextguess(1325, info)

            if feedback == (0,3):
                return finalstretch(4152, info)
            
            elif feedback == (0,2):
                return finalstretch(4162, info)
            
            elif feedback == (1,2):
                return finalstretch(3126, info)
            
            else:
                return finalstretch("done", info)

        elif feedback == (0,2):
            feedback = nextguess(1325, info)

            if feedback == (0,3):
                return finalstretch(5162, info)
            
            elif feedback == (1,1):
                return finalstretch(4522, info)
            
            elif feedback == (1,0):
                return finalstretch(4622, info)
            
            elif feedback == (2,1):
                return finalstretch(5125, info)
            
            elif feedback == (2,0):
                return finalstretch(2116, info)
            
            else:
                return finalstretch("done", info)
    
        elif feedback == (0,1):
            return finalstretch(2515, info)
        
        elif feedback == (1,3):
            return finalstretch(1323, info)
        
        elif feedback == (1,2):
            feedback = nextguess(1352, info)

            if feedback == (1,2):
                return finalstretch(1623, info)
            
            elif feedback == (2,1):
                return finalstretch(1323, info)
            
            elif feedback == (2,0):
                return finalstretch(1462, info)
            
            else:
                return finalstretch("done", info)

        elif feedback == (1,1):
            return finalstretch(2156, info)
        
        elif feedback == (1,0):
            return finalstretch(1315, info)
        
        elif feedback == (2,1):
            return finalstretch(3526, info)
        
        elif feedback == (2,0):
            return finalstretch(1536, info)
        
        else:
            return finalstretch("done", info)

    elif feedback == (3,0):     #situation I, DONE
        feedback = nextguess(1223, info)

        if feedback == (1,2):
            return finalstretch(1145, info)
        
        elif feedback == (1,1):
            return finalstretch(1114, info)
        
        elif feedback == (2,1):
            return finalstretch(1415, info)
        
        elif feedback == (2,0):
            return finalstretch(1114, info)
        
        else:
            return finalstretch("done", info)

    else:
        return finalstretch("done", info)

def intelligent_mastermind_guide(n:int = 4,
                                 k: int = 6,
                                 repeating:str = "on",
                                 zeros:str = "off",
                                 printing:str = "off"):
    
    """
    
    """

    turn = 1
    possible_codes = set_creator(n,k, repeating, zeros)
    all_guesses = possible_codes.copy()
    while True:
        print(f"Turn {turn}:")
        print("Computing next best guess...")
        best_guesses, best_guess = best_guess_finder(possible_codes, all_guesses, n, k, zeros, printing)
        if best_guess == "found":
            print(f"Congrats, you've found the code in {turn} turns!")
            break
        else:
            all_guesses.remove(best_guess)
        print(f"The guess {best_guess} is (one of) the best guesses, with a feedback group sizes of {best_guesses[2]} codes.")
        feedback = ast.literal_eval(input(("What feedback did you get?")))
        print(f"You get the feedback {feedback} after guessing {best_guess}")
        if feedback == (4,0):
            print(f"Congrats, you've found the code in {turn} turns!")
            break
        possible_codes = set_constrictor(possible_codes, best_guess, feedback, n, k, zeros)
        turn += 1
        print()

set = set_creator(4,8,repeating = "on", zeros = "off")

# counter = 0
# checking = []
# for guess in set:
#     counter += 1
#     print(counter)
#     sizes = group_finder(guess, newset, 10, "off", "on")[1]
#     if sizes not in checking:
#         checking.append(sizes)

# print(checking)

maxsizes = []
maxmax = 10
counter = 0
for guess in set:
    counter += 1
    print(counter)
    sizes = group_finder(guess, set, 8, "on", "off")[1]
    maxsize = max(sizes)
    maxsizes.append([guess])

sizes_examined = []
information = []
for size in maxsizes:
    if size not in sizes_examined:
        info = []
        sizes_examined.append(size)
        info.append(size)
        info.append(maxsizes.count(size))
        information.append(info)

print(information)
