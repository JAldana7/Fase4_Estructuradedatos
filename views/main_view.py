"""
Author: Johan David Aldana Castillo
Date: 2026-11-20
Description: Main graphical user interface for the Binary Search Tree Explorer.
"""

import tkinter as tk
from tkinter import messagebox


class MainView:
    """Main window for interactive Binary Search Tree visualization."""

    # Exact Color Palette from LoginView
    COLOR_AZUL = "#00B4D8"
    COLOR_AZUL_HOVER = "#0284C7"
    COLOR_ROJO = "#DC2626"
    COLOR_ROJO_HOVER = "#B91C1C"
    COLOR_FONDO = "#F4F6F8"
    COLOR_CARD = "#FFFFFF"
    COLOR_INPUT_BG = "#F8FAFC"
    COLOR_BORDER = "#CBD5E1"
    COLOR_TEXT_DARK = "#0F172A"
    COLOR_TEXT_MUTED = "#64748B"
    COLOR_VERDE = "#10B981"
    COLOR_VERDE_HOVER = "#059669"
    COLOR_NARANJA = "#F59E0B"
    COLOR_NARANJA_HOVER = "#D97706"

    # Node Colors
    NODE_REGULAR = "#00B4D8"
    NODE_FOUND = "#10B981"
    NODE_PATH = "#F59E0B"
    NODE_TRAVERSAL = "#F59E0B"

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Fase4JohanAldana — BST Explorer")
        self.root.geometry("1280x740")
        self.root.minsize(1100, 680)
        self.root.configure(bg=self.COLOR_FONDO)

        # Maximize window upon startup
        try:
            self.root.state("zoomed")
        except tk.TclError:
            self.root.attributes("-zoomed", True)

        # Intercept window close button (X) to ask confirmation
        self.root.protocol("WM_DELETE_WINDOW", self._on_exit_click)

        self.controller = None
        self._build_ui()

    def set_controller(self, controller):
        """Binds the MainController instance to this view."""
        self.controller = controller
        self.refresh_all()

    def _build_ui(self):
        """Constructs the main window layout and widgets."""
        # Top Header Bar (matches LoginView banner)
        header = tk.Frame(self.root, bg=self.COLOR_AZUL, height=52)
        header.pack(fill=tk.X, side=tk.TOP)
        header.pack_propagate(False)

        tk.Label(
            header,
            text="🌲  BST Explorer  —  Binary Search Tree",
            font=("Segoe UI", 14, "bold"),
            fg="#FFFFFF",
            bg=self.COLOR_AZUL
        ).pack(side=tk.LEFT, padx=20)

        tk.Label(
            header,
            text="Johan David Aldana Castillo  |  Data Structures · Code: 301305 · ECBTI",
            font=("Segoe UI", 9, "bold"),
            fg="#FFFFFF",
            bg=self.COLOR_AZUL
        ).pack(side=tk.RIGHT, padx=20)

        # Bottom Status Bar
        status_frame = tk.Frame(
            self.root, bg=self.COLOR_CARD, height=30,
            highlightbackground=self.COLOR_BORDER, highlightthickness=1
        )
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        status_frame.pack_propagate(False)

        self.status_label = tk.Label(
            status_frame,
            text="Ready. Enter an integer value to build the Binary Search Tree.",
            font=("Segoe UI", 9, "bold"),
            fg=self.COLOR_VERDE,
            bg=self.COLOR_CARD
        )
        self.status_label.pack(side=tk.LEFT, padx=16)

        # Main Body Container
        body = tk.Frame(self.root, bg=self.COLOR_FONDO)
        body.pack(fill=tk.BOTH, expand=True, padx=14, pady=14)

        # Left Sidebar (Controls, Statistics, Legend)
        sidebar = tk.Frame(
            body,
            bg=self.COLOR_CARD,
            width=225,
            highlightbackground=self.COLOR_BORDER,
            highlightthickness=1
        )
        sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 14))
        sidebar.pack_propagate(False)

        self._build_sidebar(sidebar)

        # Right Workspace (Tree Canvas + 3 Traversal Canvases)
        workspace = tk.Frame(body, bg=self.COLOR_FONDO)
        workspace.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self._build_workspace(workspace)

    def _build_sidebar(self, parent: tk.Frame):
        """Builds controls, tree statistics, and color legend inside the left panel."""
        tk.Label(
            parent,
            text="⚙  Controls",
            font=("Segoe UI", 12, "bold"),
            fg=self.COLOR_TEXT_DARK,
            bg=self.COLOR_CARD
        ).pack(anchor="w", padx=16, pady=(16, 8))

        tk.Frame(parent, bg=self.COLOR_BORDER, height=1).pack(fill=tk.X, padx=14, pady=(0, 12))

        tk.Label(
            parent,
            text="Node Value (Integer):",
            font=("Segoe UI", 9, "bold"),
            fg=self.COLOR_TEXT_MUTED,
            bg=self.COLOR_CARD
        ).pack(anchor="w", padx=16, pady=(0, 4))

        self.value_entry = tk.Entry(
            parent,
            font=("Segoe UI", 12, "bold"),
            bg=self.COLOR_INPUT_BG,
            fg=self.COLOR_TEXT_DARK,
            insertbackground=self.COLOR_AZUL,
            justify="center",
            relief=tk.FLAT,
            highlightbackground=self.COLOR_BORDER,
            highlightthickness=1
        )
        self.value_entry.pack(fill=tk.X, padx=16, pady=(0, 12), ipady=6)
        self.value_entry.bind("<Return>", lambda event: self._on_add_click())
        self.value_entry.focus_set()

        # Action Buttons
        btn_style = {"font": ("Segoe UI", 10, "bold"), "relief": tk.FLAT, "cursor": "hand2", "bd": 0}

        tk.Button(
            parent,
            text="+  Add Node",
            bg=self.COLOR_AZUL,
            fg="#FFFFFF",
            activebackground=self.COLOR_AZUL_HOVER,
            activeforeground="#FFFFFF",
            command=self._on_add_click,
            **btn_style
        ).pack(fill=tk.X, padx=16, pady=4, ipady=6)

        tk.Button(
            parent,
            text="🔍  Search Node",
            bg=self.COLOR_VERDE,
            fg="#FFFFFF",
            activebackground=self.COLOR_VERDE_HOVER,
            activeforeground="#FFFFFF",
            command=self._on_search_click,
            **btn_style
        ).pack(fill=tk.X, padx=16, pady=4, ipady=6)

        tk.Button(
            parent,
            text="🗑  Clear Tree",
            bg=self.COLOR_NARANJA,
            fg="#FFFFFF",
            activebackground=self.COLOR_NARANJA_HOVER,
            activeforeground="#FFFFFF",
            command=self._on_clear_click,
            **btn_style
        ).pack(fill=tk.X, padx=16, pady=4, ipady=6)

        tk.Button(
            parent,
            text="🚪  Exit",
            bg=self.COLOR_ROJO,
            fg="#FFFFFF",
            activebackground=self.COLOR_ROJO_HOVER,
            activeforeground="#FFFFFF",
            command=self._on_exit_click,
            **btn_style
        ).pack(fill=tk.X, padx=16, pady=4, ipady=6)

        tk.Frame(parent, bg=self.COLOR_BORDER, height=1).pack(fill=tk.X, padx=14, pady=14)

        # Tree Statistics
        tk.Label(
            parent,
            text="Tree Statistics",
            font=("Segoe UI", 10, "bold"),
            fg=self.COLOR_TEXT_DARK,
            bg=self.COLOR_CARD
        ).pack(anchor="w", padx=16, pady=(0, 6))

        self.nodes_stat_label = tk.Label(
            parent, text="Nodes:   0", font=("Consolas", 10, "bold"), fg=self.COLOR_TEXT_MUTED, bg=self.COLOR_CARD
        )
        self.nodes_stat_label.pack(anchor="w", padx=20, pady=2)

        self.height_stat_label = tk.Label(
            parent, text="Height:  0", font=("Consolas", 10, "bold"), fg=self.COLOR_TEXT_MUTED, bg=self.COLOR_CARD
        )
        self.height_stat_label.pack(anchor="w", padx=20, pady=2)

        self.root_stat_label = tk.Label(
            parent, text="Root:    —", font=("Consolas", 10, "bold"), fg=self.COLOR_TEXT_MUTED, bg=self.COLOR_CARD
        )
        self.root_stat_label.pack(anchor="w", padx=20, pady=2)

        tk.Frame(parent, bg=self.COLOR_BORDER, height=1).pack(fill=tk.X, padx=14, pady=14)

        # Legend
        tk.Label(
            parent,
            text="Legend",
            font=("Segoe UI", 10, "bold"),
            fg=self.COLOR_TEXT_DARK,
            bg=self.COLOR_CARD
        ).pack(anchor="w", padx=16, pady=(0, 6))

        legend_items = [
            (self.NODE_REGULAR, "Regular node"),
            (self.NODE_FOUND, "Found node"),
            (self.NODE_PATH, "Search path"),
            (self.NODE_TRAVERSAL, "Traversal node"),
        ]
        for color, label_text in legend_items:
            row = tk.Frame(parent, bg=self.COLOR_CARD)
            row.pack(anchor="w", padx=20, pady=3)
            dot = tk.Canvas(row, width=12, height=12, bg=self.COLOR_CARD, highlightthickness=0)
            dot.create_oval(2, 2, 10, 10, fill=color, outline="")
            dot.pack(side=tk.LEFT, padx=(0, 8))
            tk.Label(row, text=label_text, font=("Segoe UI", 9), fg=self.COLOR_TEXT_MUTED, bg=self.COLOR_CARD).pack(side=tk.LEFT)

    def _build_workspace(self, parent: tk.Frame):
        """Builds the main tree panel and the three traversal panels."""
        # Panel 1: Main BST Canvas
        tree_container = tk.Frame(
            parent, bg=self.COLOR_CARD, highlightbackground=self.COLOR_BORDER, highlightthickness=1
        )
        tree_container.pack(fill=tk.BOTH, expand=True, pady=(0, 14))

        tree_header = tk.Frame(tree_container, bg=self.COLOR_TEXT_DARK, height=34)
        tree_header.pack(fill=tk.X)
        tree_header.pack_propagate(False)
        tk.Label(
            tree_header,
            text="🌳  BST Tree  (max 4 levels)",
            font=("Segoe UI", 9, "bold"),
            fg="#FFFFFF",
            bg=self.COLOR_TEXT_DARK
        ).pack(side=tk.LEFT, padx=14)

        self.tree_canvas = tk.Canvas(tree_container, bg=self.COLOR_INPUT_BG, highlightthickness=0)
        self.tree_canvas.pack(fill=tk.BOTH, expand=True)
        self.tree_canvas.bind("<Configure>", lambda event: self.refresh_all())

        # Bottom Row: 3 Traversal Canvases
        traversals_row = tk.Frame(parent, bg=self.COLOR_FONDO, height=135)
        traversals_row.pack(fill=tk.X)
        traversals_row.pack_propagate(False)

        self.preorder_canvas = self._create_traversal_panel(traversals_row, "Pre-order", padx=(0, 7))
        self.inorder_canvas = self._create_traversal_panel(traversals_row, "In-order", padx=7)
        self.postorder_canvas = self._create_traversal_panel(traversals_row, "Post-order", padx=(7, 0))

    def _create_traversal_panel(self, parent: tk.Frame, title: str, padx) -> tk.Canvas:
        """Helper to construct each traversal panel (Pre-order, In-order, Post-order)."""
        panel = tk.Frame(parent, bg=self.COLOR_CARD, highlightbackground=self.COLOR_BORDER, highlightthickness=1)
        panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=padx)

        header = tk.Frame(panel, bg=self.COLOR_TEXT_DARK, height=30)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        tk.Label(
            header,
            text=f"•  {title}",
            font=("Segoe UI", 9, "bold"),
            fg="#FFFFFF",
            bg=self.COLOR_TEXT_DARK
        ).pack(side=tk.LEFT, padx=12)

        canvas = tk.Canvas(panel, bg=self.COLOR_INPUT_BG, highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True)
        return canvas

    # --- Button Handlers ---

    def _on_add_click(self):
        if self.controller:
            self.controller.handle_add_node(self.value_entry.get())

    def _on_search_click(self):
        if self.controller:
            self.controller.handle_search_node(self.value_entry.get())

    def _on_clear_click(self):
        if self.controller:
            self.controller.handle_clear_tree()

    def _on_exit_click(self):
        if self.controller:
            self.controller.handle_exit()

    # --- UI State & Dialog Methods ---

    def destroy(self):
        """Closes the main window."""
        self.root.destroy()

    def clear_input(self):
        """Clears the text entry and focuses it."""
        self.value_entry.delete(0, tk.END)
        self.value_entry.focus_set()

    def set_status(self, message: str, is_error: bool = False):
        """Updates the bottom status bar text."""
        color = self.COLOR_ROJO if is_error else self.COLOR_VERDE
        self.status_label.config(text=message, fg=color)

    def show_error(self, title: str, message: str):
        """Displays an error popup dialog."""
        messagebox.showerror(title, message, parent=self.root)

    def show_info(self, title: str, message: str):
        """Displays an information popup dialog."""
        messagebox.showinfo(title, message, parent=self.root)

    def ask_confirmation(self, title: str, message: str) -> bool:
        """Displays a Yes/No confirmation dialog."""
        return messagebox.askyesno(title, message, parent=self.root)

    def update_statistics(self, count: int, height: int, root_val: int | None):
        """Updates the Tree Statistics labels in the sidebar."""
        self.nodes_stat_label.config(text=f"Nodes:   {count}")
        self.height_stat_label.config(text=f"Height:  {height}")
        self.root_stat_label.config(text=f"Root:    {root_val if root_val is not None else '—'}")

    def refresh_all(self, highlight_path: list[int] | None = None, found_value: int | None = None):
        """Redraws the tree, traversals, and statistics."""
        if not self.controller:
            return

        bst = self.controller.bst
        root_val = bst.root.value if bst.root else None
        self.update_statistics(bst.get_node_count(), bst.get_height(), root_val)

        self.draw_tree(bst.root, highlight_path or [], found_value)
        self.draw_traversal(self.preorder_canvas, bst.get_preorder(), "No Pre-order data")
        self.draw_traversal(self.inorder_canvas, bst.get_inorder(), "No In-order data")
        self.draw_traversal(self.postorder_canvas, bst.get_postorder(), "No Post-order data")

    def draw_tree(self, root, highlight_path: list[int], found_value: int | None):
        """Renders the BST graphically on the main canvas."""
        self.tree_canvas.delete("all")
        self.tree_canvas.update_idletasks()

        width = self.tree_canvas.winfo_width()
        height = self.tree_canvas.winfo_height()

        if width <= 1 or height <= 1:
            return

        if root is None:
            self.tree_canvas.create_text(
                width // 2,
                height // 2,
                text="Empty tree",
                fill=self.COLOR_TEXT_MUTED,
                font=("Segoe UI", 12)
            )
            return

        start_y = 55
        vertical_gap = max(80, (height - 110) // 4)
        initial_offset = width // 4

        self._draw_subtree(
            node=root,
            x=width // 2,
            y=start_y,
            x_offset=initial_offset,
            y_gap=vertical_gap,
            highlight_path=highlight_path,
            found_value=found_value
        )

    def _draw_subtree(self, node, x: int, y: int, x_offset: int, y_gap: int, highlight_path: list[int], found_value: int | None):
        """Recursively draws edges first and nodes on top."""
        if node is None:
            return

        radius = 22
        child_y = y + y_gap
        next_offset = max(36, x_offset // 2)

        # Draw edges to children
        if node.left is not None:
            left_x = x - x_offset
            edge_color = self.NODE_PATH if (node.value in highlight_path and node.left.value in highlight_path) else self.COLOR_TEXT_MUTED
            self.tree_canvas.create_line(x, y, left_x, child_y, fill=edge_color, width=2.2)
            self._draw_subtree(node.left, left_x, child_y, next_offset, y_gap, highlight_path, found_value)

        if node.right is not None:
            right_x = x + x_offset
            edge_color = self.NODE_PATH if (node.value in highlight_path and node.right.value in highlight_path) else self.COLOR_TEXT_MUTED
            self.tree_canvas.create_line(x, y, right_x, child_y, fill=edge_color, width=2.2)
            self._draw_subtree(node.right, right_x, child_y, next_offset, y_gap, highlight_path, found_value)

        # Determine node fill color
        if found_value is not None and node.value == found_value:
            fill_color = self.NODE_FOUND
            outline_color = "#047857"
        elif node.value in highlight_path:
            fill_color = self.NODE_PATH
            outline_color = "#B45309"
        else:
            fill_color = self.NODE_REGULAR
            outline_color = self.COLOR_AZUL_HOVER

        # Draw node circle and value
        self.tree_canvas.create_oval(
            x - radius, y - radius, x + radius, y + radius,
            fill=fill_color, outline=outline_color, width=2
        )
        self.tree_canvas.create_text(
            x, y,
            text=str(node.value),
            fill="#FFFFFF",
            font=("Segoe UI", 10, "bold")
        )

    def draw_traversal(self, canvas: tk.Canvas, values: list[int], empty_text: str):
        """Renders horizontal sequence of traversal nodes connected by arrows."""
        canvas.delete("all")
        canvas.update_idletasks()

        width = canvas.winfo_width()
        height = canvas.winfo_height()

        if width <= 1 or height <= 1:
            return

        if not values:
            canvas.create_text(
                width // 2,
                height // 2,
                text=empty_text,
                fill=self.COLOR_TEXT_MUTED,
                font=("Segoe UI", 9)
            )
            return

        count = len(values)
        margin_x = 24
        available_w = max(60, width - (margin_x * 2))
        step = available_w / max(1, count)
        radius = min(14, max(10, int(step * 0.36)))
        center_y = height // 2

        coords = []
        for idx in range(count):
            cx = int(margin_x + step * (idx + 0.5))
            coords.append((cx, center_y))

        # Draw connecting arrows
        for i in range(len(coords) - 1):
            x1, y1 = coords[i]
            x2, y2 = coords[i + 1]
            canvas.create_line(
                x1 + radius, y1, x2 - radius, y2,
                fill=self.COLOR_TEXT_MUTED, width=1.6, arrow=tk.LAST, arrowshape=(6, 8, 3)
            )

        # Draw traversal circles
        for (cx, cy), val in zip(coords, values):
            canvas.create_oval(
                cx - radius, cy - radius, cx + radius, cy + radius,
                fill=self.NODE_TRAVERSAL, outline="#B45309", width=1.5
            )
            canvas.create_text(
                cx, cy,
                text=str(val),
                fill="#FFFFFF",
                font=("Segoe UI", 8, "bold")
            )