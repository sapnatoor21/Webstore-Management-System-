import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class WebStoreManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Webstore Manager")
        self.root.geometry("600x400")

        # Initialize database
        self.conn = sqlite3.connect("webstore.db")
        self.cursor = self.conn.cursor()
        self.setup_database()

        # UI components
        self.create_ui()

    def setup_database(self):
        """Create the products table if it doesn't exist."""
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            stock INTEGER NOT NULL
        )''')
        self.conn.commit()

    def create_ui(self):
        """Set up the user interface."""
        # Labels and Entry Widgets
        ttk.Label(self.root, text="Product Name").grid(row=0, column=0, padx=10, pady=10)
        self.name_var = tk.StringVar()
        ttk.Entry(self.root, textvariable=self.name_var).grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(self.root, text="Price").grid(row=1, column=0, padx=10, pady=10)
        self.price_var = tk.DoubleVar()
        ttk.Entry(self.root, textvariable=self.price_var).grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(self.root, text="Stock").grid(row=2, column=0, padx=10, pady=10)
        self.stock_var = tk.IntVar()
        ttk.Entry(self.root, textvariable=self.stock_var).grid(row=2, column=1, padx=10, pady=10)

        # Buttons
        ttk.Button(self.root, text="Add Product", command=self.add_product).grid(row=3, column=0, padx=10, pady=10)
        ttk.Button(self.root, text="View Products", command=self.view_products).grid(row=3, column=1, padx=10, pady=10)
        ttk.Button(self.root, text="Delete Product", command=self.delete_product).grid(row=5, column=0, padx=10, pady=10)
        ttk.Button(self.root, text="Update Product", command=self.update_product).grid(row=5, column=1, padx=10, pady=10)

        # Treeview for Product List
        self.tree = ttk.Treeview(self.root, columns=("ID", "Name", "Price", "Stock"), show="headings", height=10)
        self.tree.grid(row=4, column=0, columnspan=2, padx=10, pady=10)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Price", text="Price")
        self.tree.heading("Stock", text="Stock")

        # Bind selection event for Treeview
        self.tree.bind("<ButtonRelease-1>", self.on_tree_select)

    def add_product(self):
        """Add a new product to the database."""
        name = self.name_var.get()
        price = self.price_var.get()
        stock = self.stock_var.get()

        if name and price > 0 and stock > 0:
            self.cursor.execute("INSERT INTO products (name, price, stock) VALUES (?, ?, ?)", (name, price, stock))
            self.conn.commit()
            messagebox.showinfo("Success", "Product added successfully!")
            self.clear_fields()
            self.view_products()
        else:
            messagebox.showerror("Error", "Please enter valid product details.")

    def view_products(self):
        """Display all products in the Treeview."""
        for row in self.tree.get_children():
            self.tree.delete(row)

        self.cursor.execute("SELECT * FROM products")
        for product in self.cursor.fetchall():
            self.tree.insert("", tk.END, values=product)

    def delete_product(self):
        """Delete the selected product from the database."""
        selected_item = self.tree.selection()
        if selected_item:
            product_id = self.tree.item(selected_item)["values"][0]
            self.cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
            self.conn.commit()
            messagebox.showinfo("Success", "Product deleted successfully!")
            self.view_products()
        else:
            messagebox.showerror("Error", "Please select a product to delete.")

    def update_product(self):
        """Update the selected product's details."""
        selected_item = self.tree.selection()
        if selected_item:
            product_id = self.tree.item(selected_item)["values"][0]
            name = self.name_var.get()
            price = self.price_var.get()
            stock = self.stock_var.get()

            if name and price > 0 and stock > 0:
                self.cursor.execute(
                    "UPDATE products SET name = ?, price = ?, stock = ? WHERE id = ?",
                    (name, price, stock, product_id)
                )
                self.conn.commit()
                messagebox.showinfo("Success", "Product updated successfully!")
                self.view_products()
            else:
                messagebox.showerror("Error", "Please enter valid product details.")
        else:
            messagebox.showerror("Error", "Please select a product to update.")

    def on_tree_select(self, event):
        """Populate the input fields with selected product's details."""
        selected_item = self.tree.selection()
        if selected_item:
            product = self.tree.item(selected_item)["values"]
            self.name_var.set(product[1])
            self.price_var.set(product[2])
            self.stock_var.set(product[3])

    def clear_fields(self):
        """Clear input fields."""
        self.name_var.set("")
        self.price_var.set(0)
        self.stock_var.set(0)

if __name__ == "__main__":
    root = tk.Tk()
    app = WebStoreManager(root)
    root.mainloop()

