import threading

# Define a generator function to read lines from a file
def read_file(filename):
    """
    Generator function to read lines from a file.
    Args:
        filename (str): The name of the file to read.
    Yields:
        str: The next line from the file.
    """
    with open(filename, "r") as f:
        for line in f:
            yield line.strip()

def findleftdigits(found):
    """
    Find the leftmost digits in a file.

    The digits can either be numeric {1,2,3,...,9} or named i.e. one, two, three, etc.

    Args:
        found (list): A list to store the found digits.

    Returns:
        None
    """
    generator = read_file(FILENAME)
    for line in generator:
        broke = False

        for i in range(len(line)):

             # Check if the line contains any named digits
            for named_digit, digit in named_digits.items():
                if line[i:i+len(named_digit)] == named_digit:
                    found.append(digit)
                    broke = True
                    break
            
            # If the line does not contain a named digit, check for a numeric digit
            else:
                character = line[i]
                if (ord(character) - 48) in digits: #Convert ASCII character to integer and check if it is a valid digit.
                    found.append(character)
                    break
            if (broke):
                break

def findrightdigits(found):
    """
    Find the rightmost digits in a file.

    The digits can either be numeric {1,2,3,...,9} or named i.e. one, two, three, etc.

    Args:
        found (list): A list to store the found digits.

    Returns:
        None
    """
    generator = read_file(FILENAME)
    for line in generator:
        broke = False
        
        #Iterate the line backwards.
        for i in range(len(line)-1, -1, -1):
            for named_digit, digit in named_digits.items():
                # Check if the line contains any named digits
                if line[i-len(named_digit)+1: i+1] == named_digit:
                    found.append(digit)
                    broke = True
                    break

            # If the line does not contain a named digit, check for a numeric digit
            else:
                character = line[i]
                if (ord(character) - 48) in digits:
                    found.append(character)
                    break
            if (broke):
                break



if __name__ == "__main__":
    FILENAME = "input.txt"
    digits = set(i for i in range(10)) # All integer digits from 0 to 9
    named_digits = {"one": "1", "two": "2", "three": "3", "four" : "4", 
    "five" : "5", "six": "6", "seven": "7", "eight": "8", "nine": "9"} # Named digits

    leftdigits = []
    rightdigits = []

    #Spin up a seperate thread to handle the rightmost digits.
    right_thread = threading.Thread(target=findrightdigits, args=(rightdigits,))
    right_thread.start()

    #Find the left digits in main thread.
    findleftdigits(leftdigits)

    #Wait for the right thread to finish
    right_thread.join()
    
    #Calculate the sum of the left and right digits
    # ex: zip(["1","2"], ["3", "4"]) = [('1', '3'), ('2', '4')]
    # "".join will transform it to ["13", "23"]
    # int will cast it to integer.
    # and finally we get the sum.
    calced_sum = sum(map(lambda l: int("".join(l)), zip(leftdigits, rightdigits)))
    print(calced_sum)