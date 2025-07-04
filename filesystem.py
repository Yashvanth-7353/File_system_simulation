import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

class FileNode:
    def __init__(self, name, size):
        self.name = name
        self.size = size
        self.next = None

class DirectoryNode:
    def __init__(self, name):
        self.name = name
        self.files = None  # Linked list of files
        self.parent = None
        self.children = None  # First child
        self.next_sibling = None  # Next sibling

class FileSystem:
    

    def __init__(self):
        self.root_directory = DirectoryNode("root")
        self.current_directory = self.root_directory
        self.version_history = []
        self.changes_history = []  # Track changes for each version

    def create_directory(self, name):
        new_dir = DirectoryNode(name)
        new_dir.parent = self.current_directory
        new_dir.next_sibling = self.current_directory.children
        self.current_directory.children = new_dir
        self.save_version(f"Created directory '{name}'")
        messagebox.showinfo("Success", f"Directory '{name}' created.")

    def create_file(self, name, size):
        new_file = FileNode(name, size)
        new_file.next = self.current_directory.files
        self.current_directory.files = new_file
        self.save_version(f"Created file '{name}' with size {size}")
        messagebox.showinfo("Success", f"File '{name}' created.")

    def delete_directory(self, name):
        prev = None
        child = self.current_directory.children
        while child is not None:
            if child.name == name:
                if prev is None:
                    self.current_directory.children = child.next_sibling
                else:
                    prev.next_sibling = child.next_sibling
                self.save_version(f"Deleted directory '{name}'")
                messagebox.showinfo("Success", f"Directory '{name}' deleted.")
                return
            prev = child
            child = child.next_sibling
        messagebox.showerror("Error", "Directory not found.")

    def delete_file(self, name):
        prev = None
        current_file = self.current_directory.files
        while current_file is not None:
            if current_file.name == name:
                if prev is None:
                    self.current_directory.files = current_file.next
                else:
                    prev.next = current_file.next
                self.save_version(f"Deleted file '{name}'")
                messagebox.showinfo("Success", f"File '{name}' deleted.")
                return
            prev = current_file
            current_file = current_file.next
        messagebox.showerror("Error", "File not found.")

    def change_directory(self, name):
        if name == ".." and self.current_directory.parent is not None:
            self.current_directory = self.current_directory.parent
        else:
            child = self.current_directory.children
            while child is not None:
                if child.name == name:
                    self.current_directory = child
                    return
                child = child.next_sibling
            messagebox.showerror("Error", "Directory not found.")

    def list_files_in_directory(self):
        files = []
        current_file = self.current_directory.files
        while current_file is not None:
            files.append(current_file.name)
            current_file = current_file.next
        return files

    def print_absolute_path(self):
        path = []
        directory = self.current_directory
        while directory is not None:
            path.append(directory.name)
            directory = directory.parent
        return "/".join(reversed(path))

    def save_version(self, change_description):
        # Save a snapshot of the current directory structure
        self.version_history.append(self.clone_directory(self.root_directory))
        self.changes_history.append(change_description)

    def clone_directory(self, directory):
        # Recursively clone the directory structure
        new_dir = DirectoryNode(directory.name)
        current_file = directory.files
        while current_file is not None:
            new_file = FileNode(current_file.name, current_file.size)
            new_file.next = new_dir.files
            new_dir.files = new_file
            current_file = current_file.next
        child = directory.children
        while child is not None:
            new_dir_child = self.clone_directory(child)
            new_dir_child.next_sibling = new_dir.children
            new_dir.children = new_dir_child
            child = child.next_sibling
        return new_dir

    def restore_version(self, version_index):
        if 0 <= version_index < len(self.version_history):
            self.root_directory = self.clone_directory(self.version_history[version_index])
            self.current_directory = self.root_directory
            messagebox.showinfo("Success", f"Restored to version {version_index}.")
        else:
            messagebox.showerror("Error", "Invalid version index.")

class FileSystemApp:
    def __init__(self, root):
        self.fs = FileSystem()
        self.root = root
        self.root.title("File System Simulation")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")

        style = ttk.Style()
        style.configure("Treeview", font=("Helvetica", 10), background="#e6e6e6", foreground="#333")
        style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"), background="#d9d9d9", foreground="#333")

        self.tree = ttk.Treeview(root)
        self.tree.heading("#0", text="File System", anchor='w')
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.path_label = tk.Label(root, text="Current Path: /root", font=("Helvetica", 10), bg="#f0f0f0")
        self.path_label.pack(pady=5)

        button_frame = tk.Frame(root, bg="#f0f0f0")
        button_frame.pack(pady=10)

        self.create_dir_button = tk.Button(button_frame, text="Create Directory", command=self.create_directory, bg="#4CAF50", fg="white", font=("Helvetica", 10), width=15)
        self.create_dir_button.grid(row=0, column=0, padx=5)

        self.create_file_button = tk.Button(button_frame, text="Create File", command=self.create_file, bg="#2196F3", fg="white", font=("Helvetica", 10), width=15)
        self.create_file_button.grid(row=0, column=1, padx=5)

        self.delete_dir_button = tk.Button(button_frame, text="Delete Directory", command=self.delete_directory, bg="#F44336", fg="white", font=("Helvetica", 10), width=15)
        self.delete_dir_button.grid(row=0, column=2, padx=5)

        self.delete_file_button = tk.Button(button_frame, text="Delete File", command=self.delete_file, bg="#E91E63", fg="white", font=("Helvetica", 10), width=15)
        self.delete_file_button.grid(row=0, column=3, padx=5)

        self.change_dir_button = tk.Button(button_frame, text="Change Directory", command=self.change_directory, bg="#FF9800", fg="white", font=("Helvetica", 10), width=15)
        self.change_dir_button.grid(row=1, column=0, padx=5, pady=5)

        self.list_files_button = tk.Button(button_frame, text="List Files", command=self.list_files, bg="#9C27B0", fg="white", font=("Helvetica", 10), width=15)
        self.list_files_button.grid(row=1, column=1, padx=5, pady=5)

        self.restore_version_button = tk.Button(button_frame, text="Restore Version", command=self.restore_version, bg="#607D8B", fg="white", font=("Helvetica", 10), width=15)
        self.restore_version_button.grid(row=1, column=2, padx=5, pady=5)

        self.show_versions_button = tk.Button(button_frame, text="Show Versions", command=self.show_versions, bg="#3F51B5", fg="white", font=("Helvetica", 10), width=15)
        self.show_versions_button.grid(row=1, column=3, padx=5, pady=5)

        self.draw_tree_button = tk.Button(button_frame, text="Draw Tree", command=self.open_tree_window, bg="#8BC34A", fg="white", font=("Helvetica", 10), width=15)
        self.draw_tree_button.grid(row=2, column=1, padx=5, pady=5)

        self.update_tree_view(self.fs.root_directory, "")

    def update_tree_view(self, directory, parent_id):
        dir_id = self.tree.insert(parent_id, 'end', text=directory.name, open=True)
        current_file = directory.files
        while current_file is not None:
            self.tree.insert(dir_id, 'end', text=current_file.name)
            current_file = current_file.next
        child = directory.children
        while child is not None:
            self.update_tree_view(child, dir_id)
            child = child.next_sibling

    def refresh_tree_view(self):
        self.tree.delete(*self.tree.get_children())
        self.update_tree_view(self.fs.root_directory, "")

    def update_path_label(self):
        self.path_label.config(text=f"Current Path: {self.fs.print_absolute_path()}")

    def create_directory(self):
        name = simpledialog.askstring("Input", "Enter directory name:")
        if name:
            self.fs.create_directory(name)
            self.refresh_tree_view()
            self.update_path_label()

    def create_file(self):
        name = simpledialog.askstring("Input", "Enter file name:")
        if name:
            default_size = 0  # Set a default size for the file
            self.fs.create_file(name, default_size)
            self.refresh_tree_view()

    def delete_directory(self):
        name = simpledialog.askstring("Input", "Enter directory name to delete:")
        if name:
            self.fs.delete_directory(name)
            self.refresh_tree_view()
            self.update_path_label()

    def delete_file(self):
        name = simpledialog.askstring("Input", "Enter file name to delete:")
        if name:
            self.fs.delete_file(name)
            self.refresh_tree_view()

    def change_directory(self):
        name = simpledialog.askstring("Input", "Enter directory name (use '..' to go back):")
        if name:
            self.fs.change_directory(name)
            self.update_path_label()

    def list_files(self):
        files = self.fs.list_files_in_directory()
        messagebox.showinfo("Files", "\n".join(files) if files else "No files found.")

    def restore_version(self):
        version_index = simpledialog.askinteger("Input", "Enter version index to restore:")
        if version_index is not None:
            self.fs.restore_version(version_index)
            self.refresh_tree_view()
            self.update_path_label()

    def show_versions(self):
        versions = [f"Version {i}: {change}" for i, change in enumerate(self.fs.changes_history)]
        messagebox.showinfo("Versions", "\n".join(versions) if versions else "No versions saved.")

    def open_tree_window(self):
        tree_window = tk.Toplevel(self.root)
        tree_window.title("Directory Tree")
        tree_window.geometry("600x400")
        canvas = tk.Canvas(tree_window, bg="white")
        canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.draw_directory(self.fs.root_directory, 20, 20, 20, canvas)

    def draw_directory(self, directory, x, y, offset, canvas):
        canvas.create_text(x, y, anchor="nw", text=directory.name, font=("Helvetica", 10, "bold"))
        current_file = directory.files
        file_y = y + 20
        while current_file is not None:
            canvas.create_text(x + offset, file_y, anchor="nw", text=current_file.name, font=("Helvetica", 10))
            file_y += 20
            current_file = current_file.next
        child = directory.children
        child_x = x + 100
        child_y = y + 40
        while child is not None:
            canvas.create_line(x + 20, y + 10, child_x, child_y, fill="black")
            self.draw_directory(child, child_x, child_y, offset, canvas)
            child_y += 60
            child = child.next_sibling

if __name__ == "__main__":
    root = tk.Tk()
    app = FileSystemApp(root)
    root.mainloop()
