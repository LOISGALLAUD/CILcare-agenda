import tkinter as tk

def update_dimensions():
    frame.update_idletasks()
    width = frame.winfo_width()
    height = frame.winfo_height()
    print(f"width: {width}, height: {height}")

root = tk.Tk()
root.title("Frame Dimensions")
root.attributes("-fullscreen", True)

# Créer une frame
frame = tk.Frame(root, bg="lightgray")
frame.pack(expand=True, fill="both")

update_dimensions()

root.mainloop()
