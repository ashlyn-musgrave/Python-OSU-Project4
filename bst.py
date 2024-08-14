# Name: Ashlyn Musgrave
# Course: CS261 - Data Structures
# Assignment: Assignment 4 BST/AVL Tree Implementation
# Due Date: November 20, 2023
# Description: This assignment implements a Binary Search Tree (BST)


import random
from queue_and_stack import Queue, Stack


class BSTNode:
    """
    Binary Search Tree Node class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """

    def __init__(self, value: object) -> None:
        """
        Initialize a new BST node
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.value = value   # to store node's data
        self.left = None     # pointer to root of left subtree
        self.right = None    # pointer to root of right subtree

    def __str__(self) -> str:
        """
        Override string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return 'BST Node: {}'.format(self.value)


class BST:
    """
    Binary Search Tree class
    """

    def __init__(self, start_tree=None) -> None:
        """
        Initialize new Binary Search Tree
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._root = None

        # populate BST with initial values (if provided)
        # before using this feature, implement add() method
        if start_tree is not None:
            for value in start_tree:
                self.add(value)

    def __str__(self) -> str:
        """
        Override string method; display in pre-order
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        values = []
        self._str_helper(self._root, values)
        return "BST pre-order { " + ", ".join(values) + " }"

    def _str_helper(self, node: BSTNode, values: []) -> None:
        """
        Helper method for __str__. Does pre-order tree traversal
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if not node:
            return
        values.append(str(node.value))
        self._str_helper(node.left, values)
        self._str_helper(node.right, values)

    def get_root(self) -> BSTNode:
        """
        Return root of tree, or None if empty
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._root

    def is_valid_bst(self) -> bool:
        """
        Perform pre-order traversal of the tree.
        Return False if nodes don't adhere to the bst ordering property.

        This is intended to be a troubleshooting method to help find any
        inconsistencies in the tree after the add() or remove() operations.
        A return of True from this method doesn't guarantee that your tree
        is the 'correct' result, just that it satisfies bst ordering.

        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        stack = Stack()
        stack.push(self._root)
        while not stack.is_empty():
            node = stack.pop()
            if node:
                if node.left and node.left.value >= node.value:
                    return False
                if node.right and node.right.value < node.value:
                    return False
                stack.push(node.right)
                stack.push(node.left)
        return True

    # ------------------------------------------------------------------ #

    def add(self, value: object) -> None:
        """
        This method adds a new value to the tree.

        Duplicates ARE allowed.

        Implemented with O(N) runtime complexity.
        """

        # If the tree is empty, create a new node as the root
        if self._root is None:
            self._root = BSTNode(value)
        else:
            # Otherwise, call the recursive helper method
            self._add_recursive(self._root, value)

    def _add_recursive(self, node: BSTNode, value: object) -> None:
        """
        Helper method for recursive addition of a value to the tree.
        """

        # If the value is less than or equal to the current node's value
        if value < node.value:
            # If the left subtree is empty, create a new node
            if node.left is None:
                node.left = BSTNode(value)
            else:
                # If the value is equal to the current node's value,
                # add the new value only to the right subtree of that node
                if value == node.value:
                    if node.right is None:
                        node.right = BSTNode(value)
                    else:
                        # Continue the recursion in the right subtree
                        self._add_recursive(node.right, value)
                else:
                    # Otherwise, continue the recursion in the left subtree
                    self._add_recursive(node.left, value)
        else:
            # If the right subtree is empty, create a new node
            if node.right is None:
                node.right = BSTNode(value)
            else:
                # Otherwise, continue the recursion in the right subtree
                self._add_recursive(node.right, value)

    def remove(self, value: object) -> bool:
        """
        This method removes a value from the tree.

        Implemented with O(N) runtime complexity.
        """
        # Initialize pointers for tracking the current node and its parent
        parent = None
        current = self._root

        # Search for the node with the given value
        while current is not None and current.value != value:
            parent = current
            if value < current.value:
                current = current.left
            else:
                current = current.right

        if current is None:
            # Value not found
            return False

        if current.left is None and current.right is None:
            # Case 1: Node with no children
            if parent is None:
                # Removing the root (the tree has only one node)
                self._root = None
            elif parent.left == current:
                parent.left = None
            else:
                parent.right = None

        elif current.left is not None and current.right is not None:
            # Case 3: Node with two children
            successor_parent = current
            successor = current.right

            # Find the leftmost child of the right subtree (inorder successor)
            while successor.left is not None:
                successor_parent = successor
                successor = successor.left

            # Replace the current node's value with the inorder successor's value
            current.value = successor.value

            # Remove the inorder successor (it has at most one right child)
            if successor_parent.left == successor:
                successor_parent.left = successor.right
            else:
                successor_parent.right = successor.right

        else:
            # Case 2: Node with one child
            if current.left is not None:
                child = current.left
            else:
                child = current.right

            if parent is None:
                # Removing the root
                self._root = child
            elif parent.left == current:
                parent.left = child
            else:
                parent.right = child

        # Successfully removed the node with the specified value
        return True

    def contains(self, value: object) -> bool:
        """
        This method verifies if the given value is within the tree.

        Implemented with O(N) runtime complexity.
        """
        # Start at the root of the tree
        current = self._root

        # Traverse the tree until a leaf node is reached
        while current is not None:
            # Check if the current node contains the target value
            if value == current.value:
                # The value is found in the tree
                return True
            elif value < current.value:
                # If the target value is less than the current node's value,
                # move to the left subtree
                current = current.left
            else:
                # If the target value is greater than the current node's value,
                # move to the right subtree
                current = current.right

        # If the loop completes without finding the value, it's not in the tree
        return False

    def inorder_traversal(self) -> Queue:
        """
        This method performs an inorder traversal of the tree and returns a Queue object that
        contains the values of the visited nodes, in the order they were visited

        Implemented with O(N) runtime complexity.
        """

        # Create a Queue to store the values in the order of traversal
        result_queue = Queue()

        # Start the inorder traversal from the root
        self._inorder_helper(self._root, result_queue)

        # Return the Queue containing the inorder traversal result
        return result_queue

    def _inorder_helper(self, node: BSTNode, result_queue: Queue) -> None:
        """
        Helper method for inorder traversal.
        Appends values to the result_queue in the order they are visited.
        """
        if node is not None:
            # Traverse the left subtree
            self._inorder_helper(node.left, result_queue)

            # Visit the current node and enqueue its value
            result_queue.enqueue(node.value)

            # Traverse the right subtree
            self._inorder_helper(node.right, result_queue)

    def find_min(self) -> object:
        """
        This method returns the lowest value in the tree.

        Implemented with O(N) runtime complexity.
        """

        # Start at the root of the tree
        current = self._root

        # Traverse to the leftmost node (node with the smallest value)
        while current is not None and current.left is not None:
            current = current.left

        # Return the value of the leftmost node (or None if the tree is empty)
        return current.value if current is not None else None

    def find_max(self) -> object:
        """
        This method returns the highest value in the tree.

        Implemented with O(N) runtime complexity.
        """

        # Start at the root of the tree
        current = self._root

        # Traverse to the rightmost node (node with the largest value)
        while current is not None and current.right is not None:
            current = current.right

        # Return the value of the rightmost node (or None if the tree is empty)
        return current.value if current is not None else None

    def is_empty(self) -> bool:
        """
        This method checks to see if the tree is empty.

        Implemented with O(1) runtime complexity.
        """
        return self._root is None

    def make_empty(self) -> None:
        """
        This method removes all of the nodes from the tree.

        Implemented with O(1) runtime complexity.
        """
        self._root = None


# ------------------- BASIC TESTING -----------------------------------------

if __name__ == '__main__':

    print("\nPDF - method add() example 1")
    print("----------------------------")
    test_cases = (
        (1, 2, 3),
        (3, 2, 1),
        (1, 3, 2),
        (3, 1, 2),
    )
    for case in test_cases:
        tree = BST(case)
        print(tree)

    print("\nPDF - method add() example 2")
    print("----------------------------")
    test_cases = (
        (10, 20, 30, 40, 50),
        (10, 20, 30, 50, 40),
        (30, 20, 10, 5, 1),
        (30, 20, 10, 1, 5),
        (5, 4, 6, 3, 7, 2, 8),
        (range(0, 30, 3)),
        (range(0, 31, 3)),
        (range(0, 34, 3)),
        (range(10, -10, -2)),
        ('A', 'B', 'C', 'D', 'E'),
        (1, 1, 1, 1),
    )
    for case in test_cases:
        tree = BST(case)
        print('INPUT  :', case)
        print('RESULT :', tree)

    print("\nPDF - method add() example 3")
    print("----------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        tree = BST()
        for value in case:
            tree.add(value)
        if not tree.is_valid_bst():
            raise Exception("PROBLEM WITH ADD OPERATION")
    print('add() stress test finished')

    print("\nPDF - method remove() example 1")
    print("-------------------------------")
    test_cases = (
        ((1, 2, 3), 1),
        ((1, 2, 3), 2),
        ((1, 2, 3), 3),
        ((50, 40, 60, 30, 70, 20, 80, 45), 0),
        ((50, 40, 60, 30, 70, 20, 80, 45), 45),
        ((50, 40, 60, 30, 70, 20, 80, 45), 40),
        ((50, 40, 60, 30, 70, 20, 80, 45), 30),
    )
    for case, del_value in test_cases:
        tree = BST(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 2")
    print("-------------------------------")
    test_cases = (
        ((50, 40, 60, 30, 70, 20, 80, 45), 20),
        ((50, 40, 60, 30, 70, 20, 80, 15), 40),
        ((50, 40, 60, 30, 70, 20, 80, 35), 20),
        ((50, 40, 60, 30, 70, 20, 80, 25), 40),
    )
    for case, del_value in test_cases:
        tree = BST(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 3")
    print("-------------------------------")
    case = range(-9, 16, 2)
    tree = BST(case)
    for del_value in case:
        print('INPUT  :', tree, del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 4")
    print("-------------------------------")
    case = range(0, 34, 3)
    tree = BST(case)
    for _ in case[:-2]:
        root_value = tree.get_root().value
        print('INPUT  :', tree, root_value)
        tree.remove(root_value)
        if not tree.is_valid_bst():
            raise Exception("PROBLEM WITH REMOVE OPERATION")
        print('RESULT :', tree)

    print("\nPDF - method contains() example 1")
    print("---------------------------------")
    tree = BST([10, 5, 15])
    print(tree.contains(15))
    print(tree.contains(-10))
    print(tree.contains(15))

    print("\nPDF - method contains() example 2")
    print("---------------------------------")
    tree = BST()
    print(tree.contains(0))

    print("\nPDF - method inorder_traversal() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree.inorder_traversal())

    print("\nPDF - method inorder_traversal() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree.inorder_traversal())

    print("\nPDF - method find_min() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_min() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_max() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method find_max() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method is_empty() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method is_empty() example 2")
    print("---------------------------------")
    tree = BST()
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method make_empty() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)

    print("\nPDF - method make_empty() example 2")
    print("---------------------------------")
    tree = BST()
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)
