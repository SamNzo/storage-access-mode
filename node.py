class Node:
    """
    Instances of this class represent nodes for a linked list
    """
    
    def __init__(self, prev, next, value):
        self.prev = prev
        self.next = next
        self.value = value

    def __str__(self):
        if (self.prev == None and self.next == None):
            return "prev: [None] curr: [{}] next: [None]".format(self.value)
        elif (self.prev == None):
            return "prev: [None] curr: [{}] next: [{}]".format(self.value, self.next.value)
        elif (self.next == None):
            return "prev: [{}] curr: [{}] next: [None]".format(self.prev.value, self.value)

        else:
            return "prev: [{}] curr: [{}] next: [{}]".format(self.prev.value, self.value, self.next.value)