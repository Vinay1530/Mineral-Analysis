# import cv2
# import numpy as np
# import os

# def process_image(input_path, output_path):
#     image = cv2.imread(input_path)
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     _, thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)

#     contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#     for contour in contours:
#         moments = cv2.moments(contour)
        
#         if moments['m00'] == 0:
#             continue
        
#         cx = int(moments['m10'] / moments['m00'])
#         cy = int(moments['m01'] / moments['m00'])

#         radius = int(np.sqrt(moments['m00'] / np.pi))

#         # Draw the line through the center of the mineral particle
#         cv2.line(image, (0, cy), (image.shape[1] - 1, cy), (0, 255, 0), 2)

#         cv2.circle(image, (cx, cy), radius-25, (0, 0, 255), 2)  # Draw circle

#         perimeter = cv2.arcLength(contour, True)
#         surface_area = cv2.contourArea(contour)

#         cv2.circle(image, (cx, cy), 5, (0, 255, 0), -1)
#         cv2.putText(image, f"Perimeter: {perimeter:.2f} pixels", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
#         cv2.putText(image, f"Surface Area: {surface_area:.2f} pixels", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
#         cv2.putText(image, f"Centroid: ({cx},{cy})", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)


#     cv2.imwrite(output_path, image)

# def main():
#     input_folder = 'input/'
#     output_folder = 'output/'

#     os.makedirs(output_folder, exist_ok=True)

#     input_images = os.listdir(input_folder)
#     for image_name in input_images:
#         input_path = os.path.join(input_folder, image_name)
#         output_path = os.path.join(output_folder, image_name)
        
#         process_image(input_path, output_path)

# if __name__ == "__main__":
#     main()











import cv2
import numpy as np
import os

def process_image(input_path, output_path):
    image = cv2.imread(input_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if len(contour) >= 5:
            # Fit a line to the contour
            [vx, vy, x, y] = cv2.fitLine(contour, cv2.DIST_L2, 0, 0.01, 0.01)
            
            # Calculate the start and end points of the line
            start_x = int(x - 1000 * vx)
            start_y = int(y - 1000 * vy)
            end_x = int(x + 1000 * vx)
            end_y = int(y + 1000 * vy)

            # Draw the line on the image
            cv2.line(image, (start_x, start_y), (end_x, end_y), (0, 255, 0), 2)

        perimeter = cv2.arcLength(contour, True)
        surface_area = cv2.contourArea(contour)

        cv2.drawContours(image, [contour], 0, (0, 0, 255), 2)  # Draw contour
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
