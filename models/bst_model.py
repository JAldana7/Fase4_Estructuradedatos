#clase tree node y arbol binario de busqueda
class TreeNode:
    # constructor de la clase TreeNode, que representa un nodo en el árbol binario de búsqueda.
    def __init__(self, value: int):
        self.value = value
        self.left = None
        self.right = None

# clase arbol binario de busqueda
class BinarySearchTree:
    MAX_LEVEL = 4 # nivel máximo permitido en el árbol, limitando la profundidad a 4 niveles.
    # constructor de la clase BinarySearchTree, que representa el árbol binario de búsqueda.
    def __init__(self):
        self.root = None

    # elimina todos los nodos del árbol, restableciendo la raíz a None.
    def clear(self):
        self.root = None

    # inserta un valor en el árbol binario de búsqueda, devolviendo una tupla que indica si la inserción fue exitosa y el motivo si no lo fue.
    def insert(self, value: int) -> tuple[bool, str]:
        if self.root is None:
            self.root = TreeNode(value)
            return True, "OK"

        current = self.root # inicia la búsqueda desde la raíz del árbol para encontrar la posición correcta para el nuevo nodo.
        level = 1

        # recorre el árbol para encontrar la posición correcta para el nuevo nodo, verificando duplicados y la profundidad máxima.
        while current is not None:
            if value == current.value:
                return False, "DUPLICATE" # si el valor ya existe en el árbol, devuelve False y la razón "DUPLICATE".

            if level >= self.MAX_LEVEL:
                return False, "MAX_DEPTH" # si se alcanza la profundidad máxima permitida, devuelve False y la razón "MAX_DEPTH".

            if value < current.value:
                if current.left is None:
                    current.left = TreeNode(value)
                    return True, "OK" # si el valor es menor que el nodo actual y el hijo izquierdo está vacío, inserta el nuevo nodo a la izquierda y devuelve True y "OK".
                current = current.left
            else:
                if current.right is None:
                    current.right = TreeNode(value)
                    return True, "OK" # si el valor es mayor que el nodo actual y el hijo derecho está vacío, inserta el nuevo nodo a la derecha y devuelve True y "OK".
                current = current.right

            level += 1 # incrementa el nivel actual a medida que se desciende en el árbol, para controlar la profundidad y evitar superar el límite máximo de niveles permitidos.

        return False, "MAX_DEPTH" # si se alcanza la profundidad máxima permitida, devuelve False y la razón "MAX_DEPTH".

    # busca un valor en el árbol binario de búsqueda, devolviendo una tupla que indica si el valor fue encontrado y la ruta de nodos visitados durante la búsqueda.
    def search(self, value: int) -> tuple[bool, list[int]]:
        path = [] # lista para almacenar la ruta de nodos visitados durante la búsqueda, útil para mostrar al usuario el camino recorrido en el árbol.
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

    # devuelve el número total de nodos en el árbol binario de búsqueda, utilizando un método recursivo para contar los nodos.
    def get_node_count(self) -> int:
        return self._count_nodes(self.root)

    # método recursivo auxiliar para contar los nodos en el árbol binario de búsqueda, recorriendo cada nodo y sumando 1 por cada nodo encontrado.
    def _count_nodes(self, node: TreeNode | None) -> int:
        if node is None:
            return 0
        return 1 + self._count_nodes(node.left) + self._count_nodes(node.right)

    # devuelve la altura (número de niveles) del árbol binario de búsqueda, utilizando un método recursivo para calcular la altura desde la raíz hasta las hojas.
    def get_height(self) -> int:
        return self._calculate_height(self.root)

    # método recursivo auxiliar para calcular la altura del árbol binario de búsqueda, comparando las alturas de los subárboles izquierdo y derecho y devolviendo la mayor altura más 1 para el nodo actual.
    def _calculate_height(self, node: TreeNode | None) -> int:
        if node is None:
            return 0
        left_height = self._calculate_height(node.left)
        right_height = self._calculate_height(node.right)
        return 1 + max(left_height, right_height)

    # devuelve una lista con los valores de los nodos en recorrido en preorden (Raíz, Izquierda, Derecha).
    def get_preorder(self) -> list[int]:
        result = []
        self._preorder_recursive(self.root, result)
        return result

    # método recursivo auxiliar para realizar el recorrido en preorden del árbol binario de búsqueda, agregando los valores de los nodos a la lista resultante en el orden correcto.
    def _preorder_recursive(self, node: TreeNode | None, result: list[int]):
        if node is not None:
            result.append(node.value)
            self._preorder_recursive(node.left, result)
            self._preorder_recursive(node.right, result)

    # devuelve una lista con los valores de los nodos en recorrido en inorden (Izquierda, Raíz, Derecha).
    def get_inorder(self) -> list[int]:
        result = []
        self._inorder_recursive(self.root, result)
        return result

    # método recursivo auxiliar para realizar el recorrido en inorden del árbol binario de búsqueda, agregando los valores de los nodos a la lista resultante en el orden correcto.
    def _inorder_recursive(self, node: TreeNode | None, result: list[int]):
        if node is not None:
            self._inorder_recursive(node.left, result)
            result.append(node.value)
            self._inorder_recursive(node.right, result)

    # devuelve una lista con los valores de los nodos en recorrido en postorden (Izquierda, Derecha, Raíz).
    def get_postorder(self) -> list[int]:
        result = []
        self._postorder_recursive(self.root, result)
        return result

    # método recursivo auxiliar para realizar el recorrido en postorden del árbol binario de búsqueda, agregando los valores de los nodos a la lista resultante en el orden correcto.
    def _postorder_recursive(self, node: TreeNode | None, result: list[int]):
        if node is not None:
            self._postorder_recursive(node.left, result)
            self._postorder_recursive(node.right, result)
            result.append(node.value)