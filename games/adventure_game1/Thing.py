import random

class Thing:

    def __init__(self, description):
        """
            Constructor method
        :param description: text description for this room
        """
        # Type [0: normal, 1: key, 2: final thing]
        self.description = description
        self.type = 0
        self.id = 0
        self.location = [random.randint(80, 750), random.randint(80, 420)]  #随机生成地址

    def setType(self, _type):
    	self.type = _type

    def getType(self):
    	return self.type

    def setId(self, _id):
    	self.id = _id

    def getId(self):
    	return self.id

    def getShortDescription(self):
        """
            Fetch a short text description
        :return: text description
        """
        return self.description

    def getLongDescription(self):
        """
            Fetch a longer description including available exits
        :return: text description
        """
        if (1 == self.type):
        	return f'this is a key, can unlock room:{self.type}'
        elif (2 == self.type):
        	return f'this is a final thing.'
        else:
        	return f'this is a normal thing'
