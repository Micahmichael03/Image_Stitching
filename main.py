import cv2  # Import OpenCV library for image processing
import numpy as np  # Import NumPy library for numerical operations
import tkinter as tk  # Import Tkinter library for GUI
from tkinter import filedialog, messagebox  # Import filedialog and messagebox from Tkinter
from PIL import Image, ImageTk  # Import Image and ImageTk from PIL for image handling

def open_files():
    files = filedialog.askopenfilenames(title='Select Images')  # Open file dialog to select multiple images
    if len(files) < 3:  # Check if less than 3 images are selected
        messagebox.showerror("Error", "Please select at least three images.")  # Show error message
        return
    for file in files:  # Loop through selected files
        image_paths.append(file)  # Append each file path to image_paths list
    messagebox.showinfo("Success", "Selected {} images.".format(len(files)))  # Show success message with number of selected images

def stitch_images():
    paths = image_paths  # Get the list of image paths
    if len(paths) < 3:  # Check if less than 3 images are selected
        messagebox.showerror("Error", "Please select at least three images.")  # Show error message
        return
    
    images = []  # Initialize an empty list to store images
    for path in paths:  # Loop through image paths
        img = cv2.imread(path)  # Read each image using OpenCV
        if img is None:  # Check if image is not read properly
            messagebox.showerror("Error", "Could not read image {}".format(path))  # Show error message
            return
        images.append(img)  # Append the read image to images list

    stitcher = cv2.Stitcher_create()  # Create a Stitcher object using OpenCV
    status, pano = stitcher.stitch(images)  # Stitch the images together
    
    if status != cv2.Stitcher_OK:  # Check if stitching failed
        messagebox.showerror("Error", "Image stitching failed.")  # Show error message
        return
    
    display_image(pano)  # Display the stitched image
    messagebox.showinfo("Success", "Images stitched successfully.")  # Show success message

def display_image(cv_image):
    cv_image_rgb = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)  # Convert the image from BGR to RGB
    pil_image = Image.fromarray(cv_image_rgb)  # Convert the image to PIL format
    imgtk = ImageTk.PhotoImage(image=pil_image)  # Convert the PIL image to ImageTk format
    panel.config(image=imgtk)  # Update the panel with the new image
    panel.image = imgtk  # Keep a reference to the image to prevent garbage collection

root = tk.Tk()  # Create the main window
root.title("Image Stitching with OpenCV")  # Set the title of the window

# UI Variables
image_paths = []  # Initialize an empty list to store image paths

# UI Elements
open_button = tk.Button(root, text="Open Images", command=open_files)  # Create a button to open images
stitch_button = tk.Button(root, text="Stitch Images", command=stitch_images)  # Create a button to stitch images
panel = tk.Label(root)  # Create a label to display the stitched image

open_button.pack(pady=10)  # Pack the open button with padding
stitch_button.pack(pady=10)  # Pack the stitch button with padding
panel.pack(padx=10, pady=10)  # Pack the panel with padding

root.mainloop()  # Start the Tkinter event loop
