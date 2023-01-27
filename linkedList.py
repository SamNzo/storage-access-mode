from node import Node

class LinkedList:
    """
    Represents a linked list.
    If the list size exceeds <n>; <m> nodes are removed starting from the tail
    """
    def __init__(self, n: int, m: int):
        self.head = None
        self.tail = None
        self.size = 0
        self.n = n
        self.m = m

    def create(self, value) -> None | list:
        """
        Add a node to the linked list
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
            deleted_values = []
            for i in range(self.m):
                deleted_values.append(self.tail.value)
                self.remove_tail()
            # Return list of deleted values
            return deleted_values

    
    def delete(self, value, makehead: bool=False) -> None:
        """
        Remove node with given value from the linked list.
        If @makehead is True the node containing the specified @value is set as the new head.
        Otherwise it is removed from memory.
        """
        node = self.head
        while node.value != value:
            node = node.next
        # If node is tail
        if node.next == None and node.prev != None:
            node.prev.next = None
            self.tail = node.prev
        # If node is head
        elif node.prev == None and node.next != None:
            node.next.prev = None
            self.head = node.next
        # If node is both head and tail
        elif node.prev == None and node.next == None:
            if makehead:
                return
            else:
                self.head = None
                self.tail = None
                del node
                return
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
        Remove tail from the linked list and from memory
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
        Check if the given value is inside the linked list
        """
        node = self.head
        while node:
            if node.value == value:
                return True
            node = node.next
        return False

    def show(self):
        """
        Show linked list
        """
        node = self.head
        while node:
            print(node)
            node = node.next


if __name__ == "__main__":
    list = LinkedList(4, 1)
    # Add nodes to the linked list
    list.create(0)
    list.create(1)
    list.create(2)
    list.create(3)
    # Next line should remove node with value 0 from the list
    list.create(4)
    list.show()
    # Since node with value 2 is already in the list; the node should be moved to head
    list.create(2)
    print("----------------")
    list.show()