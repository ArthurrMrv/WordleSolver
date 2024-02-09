import pandas as pd
import string
import random

class WordleSolver:
    def __init__(self, dataPath="300kWords.txt", firstWord=None, recomanded = True, lenWords=5) -> None:
        """Initialize the WordleSolver object with the given parameters and set up the necessary attributes

        Args:
            dataPath (str, optional): _description_. Defaults to 'updated5letters.txt'.
            firstWord (_type_, optional): _description_. Defaults to None.
            lenWords (int, optional): _description_. Defaults to 5.

        Raises:
            ValueError: _description_
        """
        
        # countLetters is a dictionary that keeps track of the count, maximum tested index, and possible placements of each letter in the alphabet
        self.countLetters = dict([(i, {"nb": 0, 
                                       "maxtested": 0,
                                       "possPlacement": [None for _ in range(lenWords)]}) for i in string.ascii_lowercase])
        
        RECOMANDED_FIRST_WORDS = {5: "tares", 6: "stares", 7: "masters", 8: "smartest", 9: "smartness", 10: "smartasses"}
        
        if firstWord == None and recomanded:
            self.firstWord = RECOMANDED_FIRST_WORDS[lenWords] if lenWords in RECOMANDED_FIRST_WORDS.keys() else None
        
        # Check the file extension of the dataPath and load the data accordingly
        if dataPath.endswith('.csv'):
            self.dfPath = dataPath
            self.df = pd.read_csv(dataPath)
            self.df = pd.DataFrame(self.df)
            
            temp = self.df.iloc[:, 0].values
            
            for i in range(1, len(self.df.columns)):
                temp = temp + self.df.iloc[:, i].values
                
        elif dataPath.endswith('.txt'):
            with open(dataPath, 'r') as f:
                temp = [i.strip().lower() for i in f.readlines() if len(i.strip()) == lenWords]
            
        else:
            raise ValueError("The dataPath should be a .csv or .txt file")
            
        # Set the initial word, length of words, and other attributes
        self.firstWord = firstWord
        self.lenWords = lenWords
        
        self.words = set(temp)
        self.currentWord = None
        self.possibleWords = self.words.copy()
        self.possibleOuptus = dict()
        self.lastWord = None 
    
    def analyseResult(self, resultEval):
        """Analyze the result of the evaluation and update the possible words accordingly

        Args:
            resultEval (_type_): _description_

        Returns:
            _type_: _description_
        """
        
        if resultEval == tuple([1 for _ in range(self.lenWords)]):
            return None
        self.possibleWords = self.possibleOuptus[tuple(resultEval)]
        self.lastWord = self.currentWord
    
    def analyseResults(self, resultEvals, reinitialize=False):
        """Analyze the results of the evaluations and update the possible words accordingly

        Args:
            resultEvals (_type_): _description_

        Returns:
            _type_: _description_
        """
        resultEvals = dict(resultEvals) if type(resultEvals) != dict else resultEvals
        
        if reinitialize:
            self.possibleWords = self.words.copy()
            self.currentWord = self.firstWord
            self.possibleOuptus = self._getPossibilities(self.currentWord)
            
        for word in resultEvals.keys():
            
            #If the word os the one we are looking for, we set it as the current one and exit the loop
            if resultEvals[word] == tuple([1 for _ in range(len(word))]):
                self.currentWord = word
                return None

            self.lastWord = self.currentWord
            self.currentWord = word
            self.possibleOuptus = self._getPossibilities(self.currentWord)
            
            #Sometimes the eval output is not a possible key...
            if tuple(resultEvals[word]) in self.possibleOuptus:
                self.possibleWords = self.possibleOuptus[tuple(resultEvals[word])]
        
    def _eval(self, word_to_find, current_word):
        """Evaluate the similarity between the word to find and the current word

        Args:
            word_to_find (_type_): _description_
            current_word (_type_): _description_

        Returns:
            _type_: _description_
        """
        
        compo_word_to_find = list(word_to_find)
        sc = [0 for _ in range(len(word_to_find))]
        
        for i in range(len(current_word)):
            if current_word[i] == word_to_find[i]:
                compo_word_to_find.remove(current_word[i])
                sc[i] = 1
        
        for i in range(len(current_word)):
            if sc[i] == 0 and current_word[i] in compo_word_to_find:
                compo_word_to_find.remove(current_word[i])
                sc[i] = 0.5

        return tuple(sc)
    
    def _getPossibilities(self, pivot):
        """Get the possible words based on the pivot word

        Args:
            pivot (_type_): _description_

        Returns:
            _type_: _description_
        """
        
        possibilities = dict()
        for word in self.possibleWords:
            res = self._eval(word, pivot)
            if res in possibilities:
                possibilities[res].append(word)
            else:
                possibilities[res] = [word]
        return possibilities
        
    def getNextWord(self):
        """Get the next word to guess

        Returns:
            _type_: _description_
        """
        
        # For the first word
        if type(self.firstWord) == str and (len(self.words) == len(self.possibleWords)):
            possibilities = self._getPossibilities(self.firstWord)
            self.currentWord = self.firstWord if len(possibilities.keys()) > 1 else possibilities[list(possibilities.keys())[0]][0]
            self.possibleOuptus = possibilities
            return self.firstWord
        
        # For every other word
        ans = {
            "pivot": None,
            "possibilities": dict()
        }
        for pivot in self.words:
            possibilities = self._getPossibilities(pivot)
            if len(possibilities) > len(ans["possibilities"].keys()):
                ans["pivot"] = pivot
                ans["possibilities"] = possibilities

        self.currentWord = ans["pivot"] if len(ans["possibilities"].keys()) > 1 else ans["possibilities"][list(ans["possibilities"].keys())[0]][0]
        self.possibleOuptus = ans["possibilities"]
        
        #Set the ifrst word to itself if already entered, else set it to the current word
        if (len(self.possibleWords) == len(self.words)):
            self.firstWord = self.currentWord
        
        return self.currentWord
    
    def reset(self):
        """Reset the game (and keep the first word even if non provided)

        Returns:
            _type_: _description_
        """
        
        self.possibleWords = self.words.copy()
        self.possibleOuptus = dict()
        self.lastWord = None

def playOnce(display=True, recommanded=True, lenWords=5, wordToFind=None, wordToStart=None):
    """Play the game once

    Args:
        display (bool, optional): _description_. Defaults to True.
        recommanded (bool, optional): Use recomanded first word (if exists). Defaults to True.
        wordToFind (_type_, optional): _description_. Defaults to None.
        wordToStart (_type_, optional): _description_. Defaults to None.
    """
    
    bob = WordleSolver(firstWord=wordToStart, recommanded=recommanded, lenWords=lenWords)
    to_find = wordToFind if wordToFind != None else random.choice(tuple(bob.words))
    if display:
        print(f"-> to find: {to_find}")
    for i in range(20):
        resultEval = eval(to_find, bob.getNextWord())
        if display:
            print(f"Guess {i+1} ; word: {bob.currentWord} | eval : {resultEval}")
        if resultEval == tuple([1 for _ in range(len(to_find))]):
            if display:
                print(f"Found in {i+1} guesses")
            break
        bob.analyseResult(resultEval)
        
def evaluateModel(iters=100, recommanded = True, lenWords=5, wordToFind=None, wordToStart=None):
    """Evaluate the model by playing the game multiple times

    Args:
        iters (int, optional): _description_. Defaults to 100.
        recommanded (bool, optional): Use the recommanded first word (If exists). Defaults to True.
        lenWords (int, optional): _description_. Defaults to 5.
        wordToFind (str, optional): _description_. Defaults to "".
        wordToStart (str, optional): _description_. Defaults to "".

    Returns:
        _type_: _description_
    """
    
    score = 0
    bob = WordleSolver(firstWord=wordToStart, recommanded=recommanded, lenWords=lenWords)
    for _ in range(iters):
        to_find = random.choice(tuple(bob.words)) if wordToFind == None else wordToFind
        for i in range(1, 7):
            resultEval = eval(to_find, bob.getNextWord())
            if resultEval == tuple([1 for _ in range(lenWords)]):
                score += i 
                break
            bob.analyseResult(resultEval)
        if i == 6:
            pass
        bob.reset()
        
    return score/iters