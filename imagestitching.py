# Three images are stitched together using OpenCV and NumPy libraries in Python.

import numpy as np  # Import NumPy library for numerical operations
import cv2  # Import OpenCV library for image processing
import glob  # Import glob for file pattern matching
import imutils  # Import imutils for image processing convenience functions

# Get all the images from the folder
image_paths = glob.glob('images/*.png')  # Get all image paths from the specified folder
images = []  # Initialize an empty list to store images

# Loop through each image path
for image in image_paths:
    img = cv2.imread(image)  # Read each image using OpenCV
    images.append(img)  # Append the read image to the images list
    cv2.imshow("Image", img)  # Display the image
    cv2.waitKey(0)  # Wait for a key press

# Create a Stitcher object using OpenCV
imageStitcher = cv2.Stitcher_create()

# Stitch the images together
error, stitched_img = imageStitcher.stitch(images)

# Check if stitching was successful
if not error:
    cv2.imwrite("stitchedOutput.png", stitched_img)  # Save the stitched image
    cv2.imshow("Stitched Img", stitched_img)  # Display the stitched image
    cv2.waitKey(0)  # Wait for a key press

    # Add a border to the stitched image
    stitched_img = cv2.copyMakeBorder(stitched_img, 10, 10, 10, 10, cv2.BORDER_CONSTANT, (0, 0, 0))

    # Convert the stitched image to grayscale
    gray = cv2.cvtColor(stitched_img, cv2.COLOR_BGR2GRAY)
    # Apply binary thresholding to the grayscale image
    thresh_img = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)[1]

    cv2.imshow("Threshold Image", thresh_img)  # Display the thresholded image
    cv2.waitKey(0)  # Wait for a key press

    # Find contours in the thresholded image
    contours = cv2.findContours(thresh_img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)  # Grab the contours
    areaOI = max(contours, key=cv2.contourArea)  # Find the largest contour

    # Create a mask for the largest contour
    mask = np.zeros(thresh_img.shape, dtype="uint8")
    x, y, w, h = cv2.boundingRect(areaOI)  # Get the bounding rectangle of the largest contour
    cv2.rectangle(mask, (x, y), (x + w, y + h), 255, -1)  # Draw the bounding rectangle on the mask

    minRectangle = mask.copy()  # Copy the mask
    sub = mask.copy()  # Copy the mask

    # Erode the mask until it matches the thresholded image
    while cv2.countNonZero(sub) > 0:
        minRectangle = cv2.erode(minRectangle, None)
        sub = cv2.subtract(minRectangle, thresh_img)

    # Find contours in the eroded mask
    contours = cv2.findContours(minRectangle.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)  # Grab the contours
    areaOI = max(contours, key=cv2.contourArea)  # Find the largest contour

    cv2.imshow("minRectangle Image", minRectangle)  # Display the eroded mask
    cv2.waitKey(0)  # Wait for a key press

    x, y, w, h = cv2.boundingRect(areaOI)  # Get the bounding rectangle of the largest contour

    # Crop the stitched image to the bounding rectangle
    stitched_img = stitched_img[y:y + h, x:x + w]

    cv2.imwrite("stitchedOutputProcessed.png", stitched_img)  # Save the cropped stitched image

    cv2.imshow("Stitched Image Processed", stitched_img)  # Display the cropped stitched image
    cv2.waitKey(0)  # Wait for a key press

else:
    print("Images could not be stitched!")  # Print error message if stitching failed
    print("Likely not enough keypoints being detected!")  # Print possible reason for failure