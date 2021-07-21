"""
    Create a room described "description". Initially, it has
    no exits. 'description' is something like 'kitchen' or
    'an open court yard'
"""
from Thing import Thing

class Room:

    #加一个房间名
    def __init__(self, roomname, description):
        """
            Constructor method
        :param description: text description for this room
        """
        self.description = description
        self.exits = {}     # Dictionary
        self.key = 0 # Key id[int] big then 0
        self.things = []
        #加一个房间名
        self.roomname = roomname

    def setExit(self, direction, neighbour):
        """
            Adds an exit for a room. The exit is stored as a dictionary
            entry of the (key, value) pair (direction, room)
        :param direction: The direction leading out of this room
        :param neighbour: The room that this direction takes you to
        :return: None
        """
        self.exits[direction] = neighbour

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
        return f'Location: {self.description}, Exits: {self.getExits()} '

    def getLongDescription2(self):
        """
            Fetch a longer description for bedroom.
        :return: text description
        """
        return f'Location: {self.description} '

    def getLongDescription3(self):
        """
            Fetch a longer description including available exits
        :return: text description
        """
        return f'Location: {self.description}, Exits: {self.getExits()} '


    def getExits(self):
        """
            Fetch all available exits as a list
        :return: list of all available exits
        """
        allExits = self.exits.keys()
        return list(allExits)

    def getExit(self, direction):
        """
            Fetch an exit in a specified direction
        :param direction: The direction that the player wishes to travel
        :return: Room object that this direction leads to, None if one does not exist
        """
        if direction in self.exits:
            return self.exits[direction]
        else:
            return None

    def createThing(self, _desc, _id, _type = 0):
        """
            Create a item or key in your package.
        :param _desc, _id, _type: The attribute of these item.
        :return: None
        """
        t = Thing(_desc)
        t.setType(_type)
        t.setId(_id)
        self.pushThing(t)

    def pushThing(self, _thing):
        """
            add item/key
        :param _thing: The object item/key.
        :return: None
        """
        self.things.append(_thing)

    def popThing(self):
        """
            delete item/key from the list
        :return: delete the object from the list
        """
        return self.things.pop()

    def isEmpty(self):
        """
            Whether it is empty
        :return: return 0 if the it is empty
        """
        return len(self.things) == 0

    def listThing(self):
        """
            list all the item/key in there.
        :return: return all the element in the list
        """
        return ", ".join([t.description for t in self.things])

    def checkThingType(self):
        """
            check the item, and print the detail of it.
        :return: return details
        """
        for t in self.things:
            if t.type == 1:
                return f'Detail: You are getting closer and closer to success.'
            elif t.type == 2:
                return f'Detail: This is a very important item.'
            elif t.type == 66:
                return f'Detail: These are the weapens which can be used to defeat Dr. Evil.'
            else:
                return f'Detail: This is just a normal item.'

    def pickupThing(self):
        """
            After picking up the item/key, the place(room) where it was stored loses this item/key.
        :return: Remove the item in the place, None otherwise
        """
        if len(self.things) > 0:
            return self.things.pop(0)
        else:
            return None

    def setLock(self, lockid):
        """
            set the lock in the door of the room
        :param lockid: The id of the door.
        :return: None
        """
        self.key = lockid

    def needKey(self):
        """
            check whether it need a key or not.
        :return: key > 0
        """
        return self.key > 0

    def getLockId(self):
        """
            The lock.
        :return: key
        """
        return self.key
