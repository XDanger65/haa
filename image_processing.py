import tkinter as tk
from tkinter import filedialog, messagebox, Canvas, Menu
import threading
import queue
import cv2  # OpenCV for image processing
from PIL import Image, ImageTk

class WorkerThread(threading.Thread):
    def _init_(self, task_queue):
        threading.Thread._init_(self)
        self.task_queue = task_queue
        self.processed_image = None  # Initialize processed_image attribute

    def run(self):
        while True:
            task = self.task_queue.get()
            if task is None:
                break
            image, operation = task
            result = self.process_image(image, operation)
            self.processed_image = result  # Set processed_image attribute
            show_image(result)

    def process_image(self, image, operation):
        # Load the image
        img = cv2.imread(image, cv2.IMREAD_COLOR)
        # Perform the specified operation
        if operation == 'edge_detection':
            result = cv2.Canny(img, 100, 200)
        elif operation == 'color_inversion':
            result = cv2.bitwise_not(img)
        # Add more operations as needed...
        return result

def select_image():
    file_path = filedialog.askopenfilename()
    entry.delete(0, tk.END)
    entry.insert(0, file_path)

def process_image():
    image_path = entry.get()
    operation = var.get()
    task_queue.put((image_path, operation))
    start_worker_thread()

def show_image(image):
    window = tk.Toplevel(root)
    window.title("Processed Image")
    window.geometry("500x500")

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(image)
    photo = ImageTk.PhotoImage(image)

    canvas = tk.Canvas(window, width=500, height=500)
    canvas.pack()
    canvas.create_image(0, 0, anchor=tk.NW, image=photo)
    canvas.image = photo

    # Create right-click menu for saving image
    menu = Menu(window, tearoff=0)
    menu.add_command(label="Save Image", command=lambda: save_image(image))
    canvas.bind("<Button-3>", lambda event: menu.post(event.x_root, event.y_root))

def save_image(image):
    file_path = filedialog.asksaveasfilename(defaultextension=".png")
    if file_path:
        image.save(file_path)
        messagebox.showinfo("Success", "Image saved successfully.")

def start_worker_thread():
    global worker_thread
    worker_thread = WorkerThread(task_queue)
    worker_thread.start()

root = tk.Tk()
root.title("Image Processing")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

label1 = tk.Label(frame, text="Select Image:")
label1.grid(row=0, column=0, sticky="w")

entry = tk.Entry(frame, width=50)
entry.grid(row=0, column=1, padx=5, pady=5)

button = tk.Button(frame, text="Browse", command=select_image)
button.grid(row=0, column=2, padx=5, pady=5)

label2 = tk.Label(frame, text="Select Operation:")
label2.grid(row=1, column=0, sticky="w")

var = tk.StringVar()
var.set("edge_detection")

option1 = tk.Radiobutton(frame, text="Edge Detection", variable=var, value="edge_detection")
option1.grid(row=1, column=1, sticky="w")

option2 = tk.Radiobutton(frame, text="Color Inversion", variable=var, value="color_inversion")
option2.grid(row=2, column=1, sticky="w")

process_button = tk.Button(frame, text="Process Image", command=process_image)
process_button.grid(row=3, column=1, padx=5, pady=10)

task_queue = queue.Queue()
worker_thread = None

root.mainloop()