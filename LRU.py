from node import Node

class LRU:
    def __init__(self, n: int, m: int):
        self.head = None
        self.tail = None
        self.size = 0
        self.n = n
        self.m = m

    def create(self, value):
        """
        Add a node to the chained list
        """
        # First node
        if self.head == None:
            self.head = Node(None, None, value)
            self.tail = self.head
            # Increment list size
            self.size += 1
        # Second & more
        else:
            # Check if the value is already in the list
            if self.isInside(value):
                # Delete the node and make it the new head
                self.delete(value, makehead=True)
            else:
                node = Node(None, self.head, value)
                self.head.prev = node
                self.head = node
                # Increment list size
                self.size += 1
        # If list size exceeds <self.n>: remove last <self.m> nodes from the list
        if (self.size > self.n):
            for i in range(self.m):
                self.remove_tail()

    
    def delete(self, value, makehead: bool=False):
        """
        Remove node with given value from the chained list and from memory
        If @makehead is True the node containing the specified @value is set as the new head
        """
        node = self.head
        while node.value != value:
            node = node.next
        # If node is tail
        if node.next == None:
            node.prev.next = None
            self.tail = node.prev
        # If node is head
        elif node.prev == None:
            node.next.prev = None
            self.head = node.next
        # Any other node in the list
        else:
            # Branch next node to previous node
            node.next.prev = node.prev
            # Branch previous node to next node
            node.prev.next = node.next
        # If makehead: make it the new head
        if makehead:
            self.head.prev = node
            node.next = self.head
            node.prev = None
            self.head = node
        # Else: remove node from memory
        else:    
            del node

    def remove_tail(self):
        """
        Remove tail from the chained list and from memory
        """
        # Get former tail
        last_node = self.tail
        # Set new tail
        self.tail = self.tail.prev
        self.tail.next = None
        # Remove last node from memory
        del last_node

    def isInside(self, value) -> bool:
        """
        Check if the given value is inside the chained list
        """
        node = self.head
        while node:
            if node.value == value:
                return True
            node = node.next
        return False

    def show(self):
        """
        Show chained list
        """
        node = self.head
        while node:
            print(node)
            node = node.next

    
            


if __name__ == "__main__":
    lru = LRU(10, 1)
    lru.create(0)
    lru.create(1)
    lru.create(2)
    lru.create(3)
    lru.create(4)
    lru.show()
    lru.create(2)
    print("----------------")
    lru.show()