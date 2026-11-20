# importaciones necesarias
from models.bst_model import BinarySearchTree
from views.main_view import MainView

# Controlador principal que coordina las operaciones del árbol, validaciones y actualizaciones de la vista.
class MainController:
    # Inicializa el controlador con la vista y el modelo del árbol binario de búsqueda.
    def __init__(self, view: MainView):
        self.view = view # Instancia de la vista principal
        self.bst = BinarySearchTree() # Instancia del modelo del árbol binario de búsqueda
        self.view.set_controller(self) # Asocia el controlador a la vista para manejar eventos y actualizaciones

    # valida y convierte la entrada del usuario en un número entero, mostrando errores si es inválida.
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

    # valida la entrada del usuario y agrega un nuevo nodo al ABB
    def handle_add_node(self, raw_value: str):
        value = self._parse_integer(raw_value)
        if value is None:
            return

        inserted, reason = self.bst.insert(value) # Intenta insertar el nodo en el árbol y obtiene el resultado y la razón si falla.

        # Actualiza la vista y muestra mensajes según el resultado de la inserción.
        if inserted:
            self.view.clear_input()
            self.view.refresh_all()
            self.view.set_status(f"Node {value} added successfully.")
        elif reason == "DUPLICATE":
            self.view.show_error(
                "Duplicate Node",
                f"Node {value} already exists in the tree.\nDuplicate values are not allowed in a BST." # describe el duplicado
            )
            self.view.set_status(f"Error: Node {value} already exists.", is_error=True)
        elif reason == "MAX_DEPTH": # maximo del nivel del arbol
            self.view.show_error(
                "Maximum Depth Reached",
                f"Cannot insert node {value}.\n\n"
                "This tree is limited to 4 levels.\n"
                "Adding this node would create a level 5.\n\n"
                "Clear the tree or choose a different value."
            )
            self.view.set_status(f"Error: Maximum depth (4 levels) reached for node {value}.", is_error=True)

    # valida la entrada del usuario y busca un nodo en el ABB
    def handle_search_node(self, raw_value: str):
        # valida si el árbol está vacío antes de intentar buscar un nodo, mostrando un error si es así.
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

    # valida la entrada del usuario y elimina un nodo del ABB
    def handle_clear_tree(self):
        if self.bst.root is None:
            self.view.set_status("Tree is already empty.")
            return

        # solicita confirmación antes de eliminar todos los nodos del árbol, mostrando un mensaje de advertencia.
        confirmed = self.view.ask_confirmation(
            "Confirm Clear Tree",
            "Are you sure you want to clear the entire Binary Search Tree?\nThis action cannot be undone."
        )
        if confirmed:
            self.bst.clear()
            self.view.clear_input()
            self.view.refresh_all()
            self.view.set_status("Tree cleared successfully.")

    # valida la confirmación del usuario antes de cerrar la aplicación, mostrando un mensaje de advertencia.
    def handle_exit(self):
        confirmed = self.view.ask_confirmation(
            "Confirm Exit",
            "Are you sure you want to exit the BST Explorer application?"
        )
        if confirmed:
            self.view.destroy() # cierra la ventana principal y termina la aplicación.