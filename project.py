import tkinter as tk
from tkinter import filedialog
import threading
import queue
import cv2  # OpenCV for image processing

class WorkerThread(threading.Thread):
    def _init_(self, task_queue):
        super()._init_()
        self.task_queue = task_queue

    def run(self):
        while True:
            task = self.task_queue.get()
            if task is None:
                break
            image, operation, filter_type = task
            result = self.process_image(image, operation, filter_type)
            self.display_result(result)

    def process_image(self, image, operation, filter_type):
        # Load the image
        img = cv2.imread(image, cv2.IMREAD_COLOR)
        # Perform the specified operation
        if operation == 'edge_detection':
            result = cv2.Canny(img, 100, 200)
        elif operation == 'color_inversion':
            result = cv2.bitwise_not(img)
        # Apply the selected filter
        if filter_type == 'grayscale':
            result = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        elif filter_type == 'blur':
            result = cv2.GaussianBlur(img, (5, 5), 0)
        # Add more filters as needed...
        return result

    def display_result(self, result):
        # Display the processed image
        cv2.imshow('Processed Image', result)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

def select_image():
    file_path = filedialog.askopenfilename()
    entry.delete(0, tk.END)
    entry.insert(0, file_path)

def process_image():
    image_path = entry.get()
    operation = var.get()
    filter_type = filter_var.get()
    task_queue.put((image_path, operation, filter_type))
    start_worker_thread()

def start_worker_thread():
    WorkerThread(task_queue).start()

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

label3 = tk.Label(frame, text="Select Filter:")
label3.grid(row=3, column=0, sticky="w")

filter_var = tk.StringVar()
filter_var.set("grayscale")

filter_option1 = tk.Radiobutton(frame, text="Grayscale", variable=filter_var, value="grayscale")
filter_option1.grid(row=3, column=1, sticky="w")

filter_option2 = tk.Radiobutton(frame, text="Blur", variable=filter_var, value="blur")
filter_option2.grid(row=4, column=1, sticky="w")

process_button = tk.Button(frame, text="Process Image", command=process_image)
process_button.grid(row=5, column=1, padx=5, pady=10)

task_queue = queue.Queue()

root.mainloop()
