"""
    A simple text based User Interface (UI) for the
    Adventure World game
"""

class TextUI:

    def __init__(self):
        # Nothing to do ...
        pass

    def getCommand(self):
        """
            Fetches a command from the console
        :return: a 2-tuple of the form (commandWord, secondWord)
        """
        word1 = None
        word2 = None
        print('> ', end='')
        inputLine = input()
        if inputLine != "":
            allWords = inputLine.split()
            word1 = allWords[0]
            if len(allWords) > 1:
                word2 = allWords[1]
            else:
                word2 = None
            # Just ignore any other words
        return (word1, word2)

    def printtoTextUI(self, text):
        """
            Displays text to the console
        :param text: Text to be displayed
        :return: None
        """
        print(text)
