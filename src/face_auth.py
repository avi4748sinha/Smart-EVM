import cv2

cam_port = 0
cam = cv2.VideoCapture(cam_port)

inp = input('Enter person name: ')

print("Press 's' to save the image, or 'q' to quit without saving.")

while True:
    result, image = cam.read()
    if result:
        cv2.imshow("Camera", image)

        key = cv2.waitKey(1) & 0xFF

        if key == ord('s'):
            filename = inp + ".png"
            cv2.imwrite(filename, image)
            print(f"Image saved as {filename}")
            break

        elif key == ord('q'):
            print("Quitting without saving.")
            break
    else:
        print("Failed to capture image.")
        break

cam.release()
cv2.destroyAllWindows()
