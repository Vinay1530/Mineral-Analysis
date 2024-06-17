import cv2
import numpy as np
import os

def process_image(input_path, output_path):
    image = cv2.imread(input_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        moments = cv2.moments(largest_contour)
        
        cx = int(moments['m10'] / moments['m00'])
        cy = int(moments['m01'] / moments['m00'])

        radius = int(np.sqrt(moments['m00'] / np.pi))

        cv2.circle(image, (cx, cy), radius-30, (0, 0, 255), 2)

        perimeter = cv2.arcLength(largest_contour, True)
        surface_area = cv2.contourArea(largest_contour)

        cv2.circle(image, (cx, cy), 5, (0, 255, 0), -1)
        cv2.putText(image, f"Perimeter: {perimeter:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        cv2.putText(image, f"Surface Area: {surface_area:.2f}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    cv2.imwrite(output_path, image)

def main():
    input_folder = 'input/'
    output_folder = 'output/'

    os.makedirs(output_folder, exist_ok=True)

    input_images = os.listdir(input_folder)
    for image_name in input_images:
        input_path = os.path.join(input_folder, image_name)
        output_path = os.path.join(output_folder, image_name)
        
        process_image(input_path, output_path)

if __name__ == "__main__":
    main()
