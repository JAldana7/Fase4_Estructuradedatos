"""
Author: Johan David Aldana Castillo
Date: 2026-11-20
Description: Binary Search Tree (BST) data structure model with max depth limit (4 levels).
"""


class TreeNode:
    """Represents a single node in the Binary Search Tree."""

    def __init__(self, value: int):
        self.value = value
        self.left = None
        self.right = None


class BinarySearchTree:
    """Binary Search Tree implementation with a maximum depth of 4 levels."""

    MAX_LEVEL = 4

    def __init__(self):
        self.root = None

    def clear(self):
        """Removes all nodes from the tree."""
        self.root = None

    def insert(self, value: int) -> tuple[bool, str]:
        """
        Inserts an integer value into the BST.
        Returns a tuple (success, error_type):
            - (True, "OK") if inserted
            - (False, "DUPLICATE") if value already exists
            - (False, "MAX_DEPTH") if inserting would exceed level 4
        """
        if self.root is None:
            self.root = TreeNode(value)
            return True, "OK"

        current = self.root
        level = 1

        while current is not None:
            if value == current.value:
                return False, "DUPLICATE"

            if level >= self.MAX_LEVEL:
                return False, "MAX_DEPTH"

            if value < current.value:
                if current.left is None:
                    current.left = TreeNode(value)
                    return True, "OK"
                current = current.left
            else:
                if current.right is None:
                    current.right = TreeNode(value)
                    return True, "OK"
                current = current.right

            level += 1

        return False, "MAX_DEPTH"

    def search(self, value: int) -> tuple[bool, list[int]]:
        """
        Searches for a value in the BST.
        Returns (found, path_values) where path_values lists visited nodes.
        """
        path = []
        current = self.root

        while current is not None:
            path.append(current.value)
            if value == current.value:
                return True, path
            elif value < current.value:
                current = current.left
            else:
                current = current.right

        return False, path

    def get_node_count(self) -> int:
        """Returns the total number of nodes in the tree."""
        return self._count_nodes(self.root)

    def _count_nodes(self, node: TreeNode | None) -> int:
        if node is None:
            return 0
        return 1 + self._count_nodes(node.left) + self._count_nodes(node.right)

    def get_height(self) -> int:
        """Returns the height (number of levels) of the tree."""
        return self._calculate_height(self.root)

    def _calculate_height(self, node: TreeNode | None) -> int:
        if node is None:
            return 0
        left_height = self._calculate_height(node.left)
        right_height = self._calculate_height(node.right)
        return 1 + max(left_height, right_height)

    def get_preorder(self) -> list[int]:
        """Returns a list of node values in Pre-order (Root, Left, Right)."""
        result = []
        self._preorder_recursive(self.root, result)
        return result

    def _preorder_recursive(self, node: TreeNode | None, result: list[int]):
        if node is not None:
            result.append(node.value)
            self._preorder_recursive(node.left, result)
            self._preorder_recursive(node.right, result)

    def get_inorder(self) -> list[int]:
        """Returns a list of node values in In-order (Left, Root, Right)."""
        result = []
        self._inorder_recursive(self.root, result)
        return result

    def _inorder_recursive(self, node: TreeNode | None, result: list[int]):
        if node is not None:
            self._inorder_recursive(node.left, result)
            result.append(node.value)
            self._inorder_recursive(node.right, result)

    def get_postorder(self) -> list[int]:
        """Returns a list of node values in Post-order (Left, Right, Root)."""
        result = []
        self._postorder_recursive(self.root, result)
        return result

    def _postorder_recursive(self, node: TreeNode | None, result: list[int]):
        if node is not None:
            self._postorder_recursive(node.left, result)
            self._postorder_recursive(node.right, result)
            result.append(node.value)