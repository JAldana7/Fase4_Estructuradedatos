"""
Author: Johan David Aldana Castillo
Date: 2026-11-20
Description: Main graphical user interface for the Binary Search Tree Explorer.
"""

import tkinter as tk
from tkinter import messagebox


class MainView:
    """Main window for interactive Binary Search Tree visualization."""

    # Color Palette
    BG_DARK = "#0b192c"
    BG_PANEL = "#0f233c"
    BG_HEADER = "#08121e"
    BORDER_CYAN = "#1e4976"
    ACCENT_CYAN = "#00b4d8"
    ACCENT_GREEN = "#10b981"
    ACCENT_ORANGE = "#f59e0b"
    ACCENT_RED = "#ef4444"
    TEXT_PRIMARY = "#f8fafc"
    TEXT_MUTED = "#94a3b8"

    # Node Colors
    NODE_REGULAR = "#00b4d8"
    NODE_FOUND = "#10b981"
    NODE_PATH = "#f59e0b"
    NODE_TRAVERSAL = "#f59e0b"

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Fase4JohanAldana — BST Explorer")
        self.root.geometry("1280x740")
        self.root.minsize(1100, 680)
        self.root.configure(bg=self.BG_DARK)

        self.controller = None
        self._build_ui()

    def set_controller(self, controller):
        """Binds the MainController instance to this view."""
        self.controller = controller
        self.refresh_all()

    def _build_ui(self):
        """Constructs the main window layout and widgets."""
        # Top Header Bar
        header = tk.Frame(
            self.root, bg=self.BG_HEADER, height=44,
            highlightbackground=self.BORDER_CYAN, highlightthickness=1
        )
        header.pack(fill=tk.X, side=tk.TOP)
        header.pack_propagate(False)

        tk.Label(
            header,
            text="🌲  BST Explorer  —  Binary Search Tree",
            font=("Segoe UI", 12, "bold"),
            fg=self.ACCENT_CYAN,
            bg=self.BG_HEADER
        ).pack(side=tk.LEFT, padx=16)

        tk.Label(
            header,
            text="Johan David Aldana Castillo  |  Data Structures 301305",
            font=("Segoe UI", 9),
            fg=self.TEXT_MUTED,
            bg=self.BG_HEADER
        ).pack(side=tk.RIGHT, padx=16)

        # Bottom Status Bar
        status_frame = tk.Frame(
            self.root, bg=self.BG_HEADER, height=28,
            highlightbackground=self.BORDER_CYAN, highlightthickness=1
        )
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        status_frame.pack_propagate(False)

        self.status_label = tk.Label(
            status_frame,
            text="Ready. Enter an integer value to build the Binary Search Tree.",
            font=("Segoe UI", 9),
            fg=self.ACCENT_GREEN,
            bg=self.BG_HEADER
        )
        self.status_label.pack(side=tk.LEFT, padx=14)

        # Main Body Container
        body = tk.Frame(self.root, bg=self.BG_DARK)
        body.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Left Sidebar (Controls, Statistics, Legend)
        sidebar = tk.Frame(
            body,
            bg=self.BG_PANEL,
            width=210,
            highlightbackground=self.BORDER_CYAN,
            highlightthickness=1
        )
        sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        sidebar.pack_propagate(False)

        self._build_sidebar(sidebar)

        # Right Workspace (Tree Canvas + 3 Traversal Canvases)
        workspace = tk.Frame(body, bg=self.BG_DARK)
        workspace.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self._build_workspace(workspace)

    def _build_sidebar(self, parent: tk.Frame):
        """Builds controls, tree statistics, and color legend inside the left panel."""
        tk.Label(
            parent,
            text="⚙  Controls",
            font=("Segoe UI", 12, "bold"),
            fg=self.ACCENT_CYAN,
            bg=self.BG_PANEL
        ).pack(anchor="w", padx=14, pady=(14, 8))

        tk.Frame(parent, bg=self.BORDER_CYAN, height=1).pack(fill=tk.X, padx=10, pady=(0, 10))

        tk.Label(
            parent,
            text="Node Value (Integer):",
            font=("Segoe UI", 9),
            fg=self.TEXT_MUTED,
            bg=self.BG_PANEL
        ).pack(anchor="w", padx=14, pady=(0, 4))

        self.value_entry = tk.Entry(
            parent,
            font=("Segoe UI", 12, "bold"),
            bg=self.BG_DARK,
            fg=self.TEXT_PRIMARY,
            insertbackground=self.ACCENT_CYAN,
            justify="center",
            relief=tk.FLAT,
            highlightbackground=self.BORDER_CYAN,
            highlightthickness=1
        )
        self.value_entry.pack(fill=tk.X, padx=14, pady=(0, 12), ipady=6)
        self.value_entry.bind("<Return>", lambda event: self._on_add_click())
        self.value_entry.focus_set()

        # Action Buttons
        btn_style = {"font": ("Segoe UI", 10, "bold"), "relief": tk.FLAT, "cursor": "hand2", "bd": 0}

        tk.Button(
            parent,
            text="+  Add Node",
            bg=self.ACCENT_CYAN,
            fg="#041524",
            activebackground="#0096c7",
            command=self._on_add_click,
            **btn_style
        ).pack(fill=tk.X, padx=14, pady=4, ipady=6)

        tk.Button(
            parent,
            text="🔍  Search Node",
            bg=self.ACCENT_GREEN,
            fg="#041524",
            activebackground="#059669",
            command=self._on_search_click,
            **btn_style
        ).pack(fill=tk.X, padx=14, pady=4, ipady=6)

        tk.Button(
            parent,
            text="🗑  Clear Tree",
            bg=self.ACCENT_ORANGE,
            fg="#041524",
            activebackground="#d97706",
            command=self._on_clear_click,
            **btn_style
        ).pack(fill=tk.X, padx=14, pady=4, ipady=6)

        tk.Button(
            parent,
            text="🚪  Exit",
            bg=self.ACCENT_RED,
            fg="#ffffff",
            activebackground="#dc2626",
            command=self._on_exit_click,
            **btn_style
        ).pack(fill=tk.X, padx=14, pady=4, ipady=6)

        tk.Frame(parent, bg=self.BORDER_CYAN, height=1).pack(fill=tk.X, padx=10, pady=14)

        # Tree Statistics
        tk.Label(
            parent,
            text="Tree Statistics",
            font=("Segoe UI", 10, "bold"),
            fg=self.TEXT_PRIMARY,
            bg=self.BG_PANEL
        ).pack(anchor="w", padx=14, pady=(0, 6))

        self.nodes_stat_label = tk.Label(
            parent, text="Nodes:   0", font=("Consolas", 10), fg=self.TEXT_MUTED, bg=self.BG_PANEL
        )
        self.nodes_stat_label.pack(anchor="w", padx=18, pady=2)

        self.height_stat_label = tk.Label(
            parent, text="Height:  0", font=("Consolas", 10), fg=self.TEXT_MUTED, bg=self.BG_PANEL
        )
        self.height_stat_label.pack(anchor="w", padx=18, pady=2)

        self.root_stat_label = tk.Label(
            parent, text="Root:    —", font=("Consolas", 10), fg=self.TEXT_MUTED, bg=self.BG_PANEL
        )
        self.root_stat_label.pack(anchor="w", padx=18, pady=2)

        tk.Frame(parent, bg=self.BORDER_CYAN, height=1).pack(fill=tk.X, padx=10, pady=14)

        # Legend
        tk.Label(
            parent,
            text="Legend",
            font=("Segoe UI", 10, "bold"),
            fg=self.TEXT_PRIMARY,
            bg=self.BG_PANEL
        ).pack(anchor="w", padx=14, pady=(0, 6))

        legend_items = [
            (self.NODE_REGULAR, "Regular node"),
            (self.NODE_FOUND, "Found node"),
            (self.NODE_PATH, "Search path"),
            (self.NODE_TRAVERSAL, "Traversal node"),
        ]
        for color, label_text in legend_items:
            row = tk.Frame(parent, bg=self.BG_PANEL)
            row.pack(anchor="w", padx=18, pady=3)
            dot = tk.Canvas(row, width=12, height=12, bg=self.BG_PANEL, highlightthickness=0)
            dot.create_oval(2, 2, 10, 10, fill=color, outline="")
            dot.pack(side=tk.LEFT, padx=(0, 8))
            tk.Label(row, text=label_text, font=("Segoe UI", 9), fg=self.TEXT_MUTED, bg=self.BG_PANEL).pack(side=tk.LEFT)

    def _build_workspace(self, parent: tk.Frame):
        """Builds the main tree panel and the three traversal panels."""
        # Panel 1: Main BST Canvas
        tree_container = tk.Frame(
            parent, bg=self.BG_PANEL, highlightbackground=self.BORDER_CYAN, highlightthickness=1
        )
        tree_container.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        tree_header = tk.Frame(tree_container, bg=self.BG_HEADER, height=30)
        tree_header.pack(fill=tk.X)
        tree_header.pack_propagate(False)
        tk.Label(
            tree_header,
            text="🌳  BST Tree  (max 4 levels)",
            font=("Segoe UI", 9, "bold"),
            fg=self.ACCENT_CYAN,
            bg=self.BG_HEADER
        ).pack(side=tk.LEFT, padx=10)

        self.tree_canvas = tk.Canvas(tree_container, bg=self.BG_DARK, highlightthickness=0)
        self.tree_canvas.pack(fill=tk.BOTH, expand=True)
        self.tree_canvas.bind("<Configure>", lambda event: self.refresh_all())

        # Bottom Row: 3 Traversal Canvases
        traversals_row = tk.Frame(parent, bg=self.BG_DARK, height=125)
        traversals_row.pack(fill=tk.X)
        traversals_row.pack_propagate(False)

        self.preorder_canvas = self._create_traversal_panel(traversals_row, "Pre-order", padx=(0, 5))
        self.inorder_canvas = self._create_traversal_panel(traversals_row, "In-order", padx=5)
        self.postorder_canvas = self._create_traversal_panel(traversals_row, "Post-order", padx=(5, 0))

    def _create_traversal_panel(self, parent: tk.Frame, title: str, padx) -> tk.Canvas:
        """Helper to construct each traversal panel (Pre-order, In-order, Post-order)."""
        panel = tk.Frame(parent, bg=self.BG_PANEL, highlightbackground=self.BORDER_CYAN, highlightthickness=1)
        panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=padx)

        header = tk.Frame(panel, bg=self.BG_HEADER, height=28)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        tk.Label(
            header,
            text=f"•  {title}",
            font=("Segoe UI", 9, "bold"),
            fg=self.ACCENT_CYAN,
            bg=self.BG_HEADER
        ).pack(side=tk.LEFT, padx=10)

        canvas = tk.Canvas(panel, bg=self.BG_DARK, highlightthickness=0)
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

    # --- UI State & Drawing Methods ---

    def destroy(self):
        """Closes the main window."""
        self.root.destroy()

    def clear_input(self):
        """Clears the text entry and focuses it."""
        self.value_entry.delete(0, tk.END)
        self.value_entry.focus_set()

    def set_status(self, message: str, is_error: bool = False):
        """Updates the bottom status bar text."""
        color = self.ACCENT_RED if is_error else self.ACCENT_GREEN
        self.status_label.config(text=message, fg=color)

    def show_error(self, title: str, message: str):
        """Displays an error popup dialog."""
        messagebox.showerror(title, message, parent=self.root)

    def show_info(self, title: str, message: str):
        """Displays an information popup dialog."""
        messagebox.showinfo(title, message, parent=self.root)

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
                fill=self.TEXT_MUTED,
                font=("Segoe UI", 12)
            )
            return

        start_y = 55
        vertical_gap = max(75, (height - 110) // 4)
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

        radius = 21
        child_y = y + y_gap
        next_offset = max(32, x_offset // 2)

        # Draw edges to children
        if node.left is not None:
            left_x = x - x_offset
            edge_color = self.NODE_PATH if (node.value in highlight_path and node.left.value in highlight_path) else "#cbd5e1"
            self.tree_canvas.create_line(x, y, left_x, child_y, fill=edge_color, width=2)
            self._draw_subtree(node.left, left_x, child_y, next_offset, y_gap, highlight_path, found_value)

        if node.right is not None:
            right_x = x + x_offset
            edge_color = self.NODE_PATH if (node.value in highlight_path and node.right.value in highlight_path) else "#cbd5e1"
            self.tree_canvas.create_line(x, y, right_x, child_y, fill=edge_color, width=2)
            self._draw_subtree(node.right, right_x, child_y, next_offset, y_gap, highlight_path, found_value)

        # Determine node fill color
        if found_value is not None and node.value == found_value:
            fill_color = self.NODE_FOUND
            outline_color = "#a7f3d0"
        elif node.value in highlight_path:
            fill_color = self.NODE_PATH
            outline_color = "#fde68a"
        else:
            fill_color = self.NODE_REGULAR
            outline_color = "#bae6fd"

        # Draw node circle and value
        self.tree_canvas.create_oval(
            x - radius, y - radius, x + radius, y + radius,
            fill=fill_color, outline=outline_color, width=2
        )
        self.tree_canvas.create_text(
            x, y,
            text=str(node.value),
            fill="#041524",
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
                fill=self.TEXT_MUTED,
                font=("Segoe UI", 9)
            )
            return

        count = len(values)
        margin_x = 22
        available_w = max(60, width - (margin_x * 2))
        step = available_w / max(1, count)
        radius = min(13, max(9, int(step * 0.36)))
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
                fill=self.TEXT_MUTED, width=1.5, arrow=tk.LAST, arrowshape=(6, 8, 3)
            )

        # Draw traversal circles
        for (cx, cy), val in zip(coords, values):
            canvas.create_oval(
                cx - radius, cy - radius, cx + radius, cy + radius,
                fill=self.NODE_TRAVERSAL, outline="#fef3c7", width=1.5
            )
            canvas.create_text(
                cx, cy,
                text=str(val),
                fill="#041524",
                font=("Segoe UI", 8, "bold")
            )