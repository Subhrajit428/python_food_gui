import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

DB_NAME = "food_delivery.db"


class FoodDeliveryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Food Delivery Management System")
        self.root.geometry("1120x700")
        self.root.minsize(950, 600)
        self.conn = sqlite3.connect(DB_NAME)
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.create_tables()
        self.seed_menu()
        self.setup_style()
        self.build_ui()
        self.refresh_all()

    def create_tables(self):
        cur = self.conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                address TEXT NOT NULL
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS menu_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                category TEXT NOT NULL,
                price REAL NOT NULL CHECK(price >= 0),
                available INTEGER NOT NULL DEFAULT 1
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER NOT NULL,
                order_date TEXT NOT NULL,
                total REAL NOT NULL,
                status TEXT NOT NULL DEFAULT 'Pending',
                FOREIGN KEY(customer_id) REFERENCES customers(id)
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS order_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER NOT NULL,
                menu_item_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL CHECK(quantity > 0),
                unit_price REAL NOT NULL,
                FOREIGN KEY(order_id) REFERENCES orders(id) ON DELETE CASCADE,
                FOREIGN KEY(menu_item_id) REFERENCES menu_items(id)
            )
        """)
        self.conn.commit()

    def seed_menu(self):
        items = [
            ("Veg Burger", "Fast Food", 90),
            ("Cheese Pizza", "Fast Food", 220),
            ("Paneer Roll", "Indian", 130),
            ("Veg Biryani", "Indian", 160),
            ("Masala Dosa", "South Indian", 100),
            ("Cold Coffee", "Beverage", 80),
            ("Chocolate Brownie", "Dessert", 110),
        ]
        self.conn.executemany(
            "INSERT OR IGNORE INTO menu_items(name, category, price) VALUES (?, ?, ?)",
            items
        )
        self.conn.commit()

    def setup_style(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("Header.TLabel", font=("Segoe UI", 19, "bold"), foreground="#17324d")
        style.configure("Sub.TLabel", font=("Segoe UI", 10), foreground="#536575")
        style.configure("Treeview", rowheight=27, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
        style.configure("Accent.TButton", font=("Segoe UI", 10, "bold"))

    def build_ui(self):
        outer = ttk.Frame(self.root, padding=16)
        outer.pack(fill="both", expand=True)

        header = ttk.Frame(outer)
        header.pack(fill="x", pady=(0, 12))
        ttk.Label(header, text="Food Delivery Management System",
                  style="Header.TLabel").pack(anchor="w")
        ttk.Label(header, text="Manage customers, food menu and orders",
                  style="Sub.TLabel").pack(anchor="w", pady=(3, 0))

        self.tabs = ttk.Notebook(outer)
        self.tabs.pack(fill="both", expand=True)
        self.customer_tab = ttk.Frame(self.tabs, padding=12)
        self.menu_tab = ttk.Frame(self.tabs, padding=12)
        self.order_tab = ttk.Frame(self.tabs, padding=12)
        self.history_tab = ttk.Frame(self.tabs, padding=12)
        self.tabs.add(self.customer_tab, text="Customers")
        self.tabs.add(self.menu_tab, text="Food Menu")
        self.tabs.add(self.order_tab, text="Place Order")
        self.tabs.add(self.history_tab, text="Order History")
        self.build_customer_tab()
        self.build_menu_tab()
        self.build_order_tab()
        self.build_history_tab()

    def build_customer_tab(self):
        form = ttk.LabelFrame(self.customer_tab, text="Customer Details", padding=12)
        form.pack(fill="x", pady=(0, 12))
        self.c_name = tk.StringVar()
        self.c_phone = tk.StringVar()
        self.c_address = tk.StringVar()
        for col, label, var, width in [
            (0, "Name", self.c_name, 22),
            (1, "Phone", self.c_phone, 18),
            (2, "Address", self.c_address, 42),
        ]:
            ttk.Label(form, text=label).grid(row=0, column=col, sticky="w", padx=5)
            ttk.Entry(form, textvariable=var, width=width).grid(row=1, column=col, padx=5, pady=5, sticky="ew")
            form.columnconfigure(col, weight=1)
        ttk.Button(form, text="Add Customer", style="Accent.TButton",
                   command=self.add_customer).grid(row=1, column=3, padx=8)
        ttk.Button(form, text="Clear", command=self.clear_customer).grid(row=1, column=4, padx=4)

        self.customer_tree = self.make_tree(
            self.customer_tab, ("id", "name", "phone", "address"),
            ("ID", "Name", "Phone", "Address"), (60, 220, 170, 500)
        )
        ttk.Button(self.customer_tab, text="Delete Selected Customer",
                   command=self.delete_customer).pack(anchor="e", pady=8)

    def build_menu_tab(self):
        form = ttk.LabelFrame(self.menu_tab, text="Food Item Details", padding=12)
        form.pack(fill="x", pady=(0, 12))
        self.m_name = tk.StringVar()
        self.m_category = tk.StringVar()
        self.m_price = tk.StringVar()
        fields = [("Food name", self.m_name), ("Category", self.m_category), ("Price (₹)", self.m_price)]
        for i, (label, var) in enumerate(fields):
            ttk.Label(form, text=label).grid(row=0, column=i, sticky="w", padx=5)
            ttk.Entry(form, textvariable=var, width=24).grid(row=1, column=i, padx=5, pady=5, sticky="ew")
            form.columnconfigure(i, weight=1)
        ttk.Button(form, text="Add Food Item", style="Accent.TButton",
                   command=self.add_menu_item).grid(row=1, column=3, padx=8)
        self.menu_tree = self.make_tree(
            self.menu_tab, ("id", "name", "category", "price", "available"),
            ("ID", "Food Item", "Category", "Price (₹)", "Available"),
            (60, 300, 200, 130, 120)
        )
        actions = ttk.Frame(self.menu_tab)
        actions.pack(fill="x", pady=8)
        ttk.Button(actions, text="Toggle Availability",
                   command=self.toggle_menu_item).pack(side="right", padx=4)
        ttk.Button(actions, text="Delete Selected Item",
                   command=self.delete_menu_item).pack(side="right", padx=4)

    def build_order_tab(self):
        customer_box = ttk.LabelFrame(self.order_tab, text="Select Customer", padding=10)
        customer_box.pack(fill="x", pady=(0, 10))
        self.order_customer = tk.StringVar()
        self.customer_combo = ttk.Combobox(customer_box, textvariable=self.order_customer,
                                           state="readonly", width=65)
        self.customer_combo.pack(side="left", padx=5)
        ttk.Label(customer_box, text="Add customers in the Customers tab first.").pack(side="left", padx=10)

        body = ttk.Frame(self.order_tab)
        body.pack(fill="both", expand=True)
        left = ttk.LabelFrame(body, text="Available Food", padding=8)
        left.pack(side="left", fill="both", expand=True, padx=(0, 8))
        right = ttk.LabelFrame(body, text="Current Order", padding=8)
        right.pack(side="left", fill="both", expand=True, padx=(8, 0))

        self.available_tree = self.make_tree(left, ("id", "name", "price"),
                                             ("ID", "Food Item", "Price (₹)"), (55, 230, 100),
                                             height=11, pack=False)
        addrow = ttk.Frame(left)
        addrow.pack(fill="x", pady=8)
        self.quantity = tk.StringVar(value="1")
        ttk.Label(addrow, text="Quantity").pack(side="left")
        ttk.Entry(addrow, textvariable=self.quantity, width=7).pack(side="left", padx=6)
        ttk.Button(addrow, text="Add Selected", command=self.add_to_cart).pack(side="left")

        self.cart_tree = self.make_tree(right, ("id", "name", "qty", "subtotal"),
                                        ("ID", "Food Item", "Qty", "Subtotal (₹)"),
                                        (45, 180, 60, 120), height=11, pack=False)
        ttk.Button(right, text="Remove Selected", command=self.remove_from_cart).pack(anchor="e", pady=8)
        bottom = ttk.Frame(self.order_tab)
        bottom.pack(fill="x", pady=10)
        self.total_label = ttk.Label(bottom, text="Total: ₹0.00", font=("Segoe UI", 14, "bold"))
        self.total_label.pack(side="left")
        ttk.Button(bottom, text="Place Order", style="Accent.TButton",
                   command=self.place_order).pack(side="right")
        self.cart = {}

    def build_history_tab(self):
        filters = ttk.Frame(self.history_tab)
        filters.pack(fill="x", pady=(0, 8))
        ttk.Button(filters, text="Refresh", command=self.refresh_orders).pack(side="left")
        ttk.Label(filters, text="Update selected order status:").pack(side="left", padx=(20, 6))
        self.status_var = tk.StringVar(value="Preparing")
        ttk.Combobox(filters, textvariable=self.status_var, state="readonly",
                     values=["Pending", "Preparing", "Out for Delivery", "Delivered", "Cancelled"],
                     width=20).pack(side="left")
        ttk.Button(filters, text="Update Status", command=self.update_order_status).pack(side="left", padx=6)
        self.order_tree = self.make_tree(
            self.history_tab, ("id", "customer", "phone", "date", "total", "status"),
            ("Order ID", "Customer", "Phone", "Date", "Total (₹)", "Status"),
            (75, 190, 130, 180, 120, 170)
        )
        ttk.Button(self.history_tab, text="View Order Items",
                   command=self.view_order_items).pack(anchor="e", pady=8)

    def make_tree(self, parent, columns, headings, widths, height=15, pack=True):
        frame = ttk.Frame(parent)
        if pack:
            frame.pack(fill="both", expand=True)
        tree = ttk.Treeview(frame, columns=columns, show="headings", height=height)
        for col, heading, width in zip(columns, headings, widths):
            tree.heading(col, text=heading)
            tree.column(col, width=width, minwidth=45, anchor="w")
        yscroll = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=yscroll.set)
        tree.pack(side="left", fill="both", expand=True)
        yscroll.pack(side="right", fill="y")
        return tree

    def add_customer(self):
        name, phone, address = self.c_name.get().strip(), self.c_phone.get().strip(), self.c_address.get().strip()
        if not all((name, phone, address)):
            messagebox.showwarning("Missing details", "Please enter the customer's name, phone and address.")
            return
        self.conn.execute("INSERT INTO customers(name, phone, address) VALUES (?, ?, ?)",
                          (name, phone, address))
        self.conn.commit()
        self.clear_customer()
        self.refresh_all()

    def clear_customer(self):
        self.c_name.set("")
        self.c_phone.set("")
        self.c_address.set("")

    def delete_customer(self):
        selected = self.customer_tree.selection()
        if not selected:
            messagebox.showinfo("Select customer", "Select a customer to delete.")
            return
        customer_id = self.customer_tree.item(selected[0], "values")[0]
        used = self.conn.execute("SELECT COUNT(*) FROM orders WHERE customer_id=?", (customer_id,)).fetchone()[0]
        if used:
            messagebox.showwarning("Cannot delete", "This customer has order history and cannot be deleted.")
            return
        if messagebox.askyesno("Confirm", "Delete this customer?"):
            self.conn.execute("DELETE FROM customers WHERE id=?", (customer_id,))
            self.conn.commit()
            self.refresh_all()

    def add_menu_item(self):
        name, category, price_text = self.m_name.get().strip(), self.m_category.get().strip(), self.m_price.get().strip()
        if not name or not category or not price_text:
            messagebox.showwarning("Missing details", "Enter food name, category and price.")
            return
        try:
            price = float(price_text)
            if price < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid price", "Price must be a non-negative number.")
            return
        try:
            self.conn.execute("INSERT INTO menu_items(name, category, price) VALUES (?, ?, ?)",
                              (name, category, price))
            self.conn.commit()
        except sqlite3.IntegrityError:
            messagebox.showerror("Duplicate item", "A food item with this name already exists.")
            return
        self.m_name.set("")
        self.m_category.set("")
        self.m_price.set("")
        self.refresh_all()

    def selected_id(self, tree, title):
        selected = tree.selection()
        if not selected:
            messagebox.showinfo("Select item", f"Select {title} first.")
            return None
        return tree.item(selected[0], "values")[0]

    def delete_menu_item(self):
        item_id = self.selected_id(self.menu_tree, "a food item")
        if item_id is None:
            return
        used = self.conn.execute("SELECT COUNT(*) FROM order_items WHERE menu_item_id=?", (item_id,)).fetchone()[0]
        if used:
            messagebox.showwarning("Cannot delete", "This item appears in past orders. Toggle its availability instead.")
            return
        if messagebox.askyesno("Confirm", "Delete this food item?"):
            self.conn.execute("DELETE FROM menu_items WHERE id=?", (item_id,))
            self.conn.commit()
            self.refresh_all()

    def toggle_menu_item(self):
        item_id = self.selected_id(self.menu_tree, "a food item")
        if item_id is None:
            return
        self.conn.execute("UPDATE menu_items SET available=1-available WHERE id=?", (item_id,))
        self.conn.commit()
        self.refresh_all()

    def add_to_cart(self):
        item_id = self.selected_id(self.available_tree, "a food item")
        if item_id is None:
            return
        try:
            qty = int(self.quantity.get())
            if qty <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid quantity", "Quantity must be a positive whole number.")
            return
        row = self.conn.execute("SELECT name, price FROM menu_items WHERE id=? AND available=1",
                                (item_id,)).fetchone()
        if not row:
            messagebox.showerror("Unavailable", "This item is no longer available.")
            return
        name, price = row
        if item_id in self.cart:
            self.cart[item_id]["qty"] += qty
        else:
            self.cart[item_id] = {"name": name, "price": price, "qty": qty}
        self.refresh_cart()

    def remove_from_cart(self):
        item_id = self.selected_id(self.cart_tree, "a cart item")
        if item_id is not None:
            self.cart.pop(item_id, None)
            self.refresh_cart()

    def refresh_cart(self):
        self.cart_tree.delete(*self.cart_tree.get_children())
        total = 0
        for item_id, item in self.cart.items():
            subtotal = item["price"] * item["qty"]
            total += subtotal
            self.cart_tree.insert("", "end", values=(item_id, item["name"], item["qty"], f"{subtotal:.2f}"))
        self.total_label.config(text=f"Total: ₹{total:.2f}")

    def place_order(self):
        customer_text = self.order_customer.get()
        if not customer_text:
            messagebox.showwarning("Select customer", "Please add and select a customer.")
            return
        if not self.cart:
            messagebox.showwarning("Empty order", "Add at least one food item to the order.")
            return
        customer_id = int(customer_text.split(" - ", 1)[0])
        total = sum(x["price"] * x["qty"] for x in self.cart.values())
        try:
            cur = self.conn.cursor()
            cur.execute("INSERT INTO orders(customer_id, order_date, total, status) VALUES (?, ?, ?, 'Pending')",
                        (customer_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), total))
            order_id = cur.lastrowid
            for item_id, item in self.cart.items():
                cur.execute("""INSERT INTO order_items(order_id, menu_item_id, quantity, unit_price)
                               VALUES (?, ?, ?, ?)""",
                            (order_id, int(item_id), item["qty"], item["price"]))
            self.conn.commit()
        except sqlite3.Error as exc:
            self.conn.rollback()
            messagebox.showerror("Database error", str(exc))
            return
        self.cart.clear()
        self.refresh_cart()
        self.refresh_orders()
        messagebox.showinfo("Order placed", f"Order #{order_id} placed successfully!\nTotal: ₹{total:.2f}")

    def update_order_status(self):
        order_id = self.selected_id(self.order_tree, "an order")
        if order_id is None:
            return
        status = self.status_var.get()
        self.conn.execute("UPDATE orders SET status=? WHERE id=?", (status, order_id))
        self.conn.commit()
        self.refresh_orders()

    def view_order_items(self):
        order_id = self.selected_id(self.order_tree, "an order")
        if order_id is None:
            return
        rows = self.conn.execute("""
            SELECT m.name, oi.quantity, oi.unit_price, oi.quantity * oi.unit_price
            FROM order_items oi JOIN menu_items m ON m.id=oi.menu_item_id
            WHERE oi.order_id=?
        """, (order_id,)).fetchall()
        win = tk.Toplevel(self.root)
        win.title(f"Order #{order_id} Details")
        win.geometry("520x350")
        ttk.Label(win, text=f"Items in Order #{order_id}",
                  font=("Segoe UI", 14, "bold")).pack(anchor="w", padx=12, pady=12)
        tree = ttk.Treeview(win, columns=("name", "qty", "price", "subtotal"), show="headings")
        for col, heading, width in [
            ("name", "Food Item", 190), ("qty", "Quantity", 80),
            ("price", "Unit Price (₹)", 110), ("subtotal", "Subtotal (₹)", 110)
        ]:
            tree.heading(col, text=heading)
            tree.column(col, width=width)
        tree.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        for row in rows:
            tree.insert("", "end", values=(row[0], row[1], f"{row[2]:.2f}", f"{row[3]:.2f}"))

    def refresh_all(self):
        self.refresh_customers()
        self.refresh_menu()
        self.refresh_available_items()
        self.refresh_orders()

    def refresh_customers(self):
        self.customer_tree.delete(*self.customer_tree.get_children())
        rows = self.conn.execute("SELECT id, name, phone, address FROM customers ORDER BY id DESC").fetchall()
        for row in rows:
            self.customer_tree.insert("", "end", values=row)
        current = self.order_customer.get()
        options = [f"{r[0]} - {r[1]} ({r[2]})" for r in rows]
        self.customer_combo["values"] = options
        if current in options:
            self.order_customer.set(current)
        elif options:
            self.order_customer.set(options[0])
        else:
            self.order_customer.set("")

    def refresh_menu(self):
        self.menu_tree.delete(*self.menu_tree.get_children())
        rows = self.conn.execute("SELECT id, name, category, price, available FROM menu_items ORDER BY name").fetchall()
        for row in rows:
            self.menu_tree.insert("", "end", values=(row[0], row[1], row[2], f"{row[3]:.2f}",
                                                     "Yes" if row[4] else "No"))

    def refresh_available_items(self):
        self.available_tree.delete(*self.available_tree.get_children())
        rows = self.conn.execute("SELECT id, name, price FROM menu_items WHERE available=1 ORDER BY name").fetchall()
        for row in rows:
            self.available_tree.insert("", "end", values=(row[0], row[1], f"{row[2]:.2f}"))

    def refresh_orders(self):
        if not hasattr(self, "order_tree"):
            return
        self.order_tree.delete(*self.order_tree.get_children())
        rows = self.conn.execute("""
            SELECT o.id, c.name, c.phone, o.order_date, o.total, o.status
            FROM orders o JOIN customers c ON c.id=o.customer_id
            ORDER BY o.id DESC
        """).fetchall()
        for row in rows:
            self.order_tree.insert("", "end", values=(row[0], row[1], row[2], row[3],
                                                      f"{row[4]:.2f}", row[5]))

    def close(self):
        self.conn.close()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = FoodDeliveryApp(root)
    root.protocol("WM_DELETE_WINDOW", app.close)
    root.mainloop()
