"""
Author: Johan David Aldana Castillo
Date: 2026-11-20
Description: Controller managing user interactions between MainView and BinarySearchTree.
"""

from models.bst_model import BinarySearchTree
from views.main_view import MainView


class MainController:
    """Coordinates tree operations, validations, and view updates."""

    def __init__(self, view: MainView):
        self.view = view
        self.bst = BinarySearchTree()
        self.view.set_controller(self)

    def _parse_integer(self, raw_text: str) -> int | None:
        """Validates that the input string is a valid integer."""
        cleaned = raw_text.strip()
        if not cleaned:
            self.view.show_error(
                "Invalid Input",
                "Input cannot be empty.\nOnly whole numbers are accepted (e.g. 50, -8, 42)."
            )
            self.view.set_status("Error: Empty input.", is_error=True)
            return None

        try:
            return int(cleaned)
        except ValueError:
            self.view.show_error(
                "Invalid Input",
                f"'{cleaned}' is not a valid integer.\nOnly whole numbers are accepted (e.g. 50, -8, 42)."
            )
            self.view.set_status(f"Error: '{cleaned}' is not a valid integer.", is_error=True)
            return None

    def handle_add_node(self, raw_value: str):
        """Validates input and inserts a new node into the BST."""
        value = self._parse_integer(raw_value)
        if value is None:
            return

        inserted, reason = self.bst.insert(value)

        if inserted:
            self.view.clear_input()
            self.view.refresh_all()
            self.view.set_status(f"Node {value} added successfully.")
        elif reason == "DUPLICATE":
            self.view.show_error(
                "Duplicate Node",
                f"Node {value} already exists in the tree.\nDuplicate values are not allowed in a BST."
            )
            self.view.set_status(f"Error: Node {value} already exists.", is_error=True)
        elif reason == "MAX_DEPTH":
            self.view.show_error(
                "Maximum Depth Reached",
                f"Cannot insert node {value}.\n\n"
                "This tree is limited to 4 levels.\n"
                "Adding this node would create a level 5.\n\n"
                "Clear the tree or choose a different value."
            )
            self.view.set_status(f"Error: Maximum depth (4 levels) reached for node {value}.", is_error=True)

    def handle_search_node(self, raw_value: str):
        """Searches for a node and highlights the search path on the canvas."""
        if self.bst.root is None:
            self.view.show_error(
                "Empty Tree",
                "The Binary Search Tree is currently empty.\nAdd at least one node before searching."
            )
            self.view.set_status("Error: Cannot search in an empty tree.", is_error=True)
            return

        value = self._parse_integer(raw_value)
        if value is None:
            return

        found, path = self.bst.search(value)
        path_str = " -> ".join(str(v) for v in path)

        if found:
            self.view.refresh_all(highlight_path=path, found_value=value)
            self.view.set_status(f"Node {value} found in the tree!")
            self.view.show_info(
                "Node Found",
                f"Node {value} was found in the tree!\n\nSearch path: {path_str}"
            )
        else:
            self.view.refresh_all(highlight_path=path, found_value=None)
            self.view.set_status(f"Node {value} does not exist in the tree.", is_error=True)
            self.view.show_error(
                "Node Not Found",
                f"Node {value} does not exist in the tree.\n\nVisited path: {path_str}"
            )

    def handle_clear_tree(self):
        """Clears the entire tree and resets all panels."""
        self.bst.clear()
        self.view.clear_input()
        self.view.refresh_all()
        self.view.set_status("Tree cleared successfully.")

    def handle_exit(self):
        """Closes the application."""
        self.view.destroy()