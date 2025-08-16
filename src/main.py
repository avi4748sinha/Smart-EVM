import face_recognition
import cv2
import numpy as np
import os
import serial
import time

# Set up serial connection
s = serial.Serial('COM1', 9600)

# Get the current folder path
CurrentFolder = os.getcwd()

# Load images for face recognition
image = CurrentFolder + '\\avinash.png'
image2 = CurrentFolder + '\\om.png'
image3 = CurrentFolder + '\\nishu.png'

# Initialize webcam
video_capture = cv2.VideoCapture(0)

# Load images and their encodings
person1_name = "avinash"
person1_image = face_recognition.load_image_file(image)
person1_face_encoding = face_recognition.face_encodings(person1_image)[0]

person2_name = "om"
person2_image = face_recognition.load_image_file(image2)
person2_face_encoding = face_recognition.face_encodings(person2_image)[0]

person3_name = "nishu"
person3_image = face_recognition.load_image_file(image3)
person3_face_encoding = face_recognition.face_encodings(person3_image)[0]

# Known faces
known_face_encodings = [
    person1_face_encoding,
    person2_face_encoding,
    person3_face_encoding,
]
known_face_names = [
    person1_name,
    person2_name,
    person3_name,
]

# Initialize variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
already_vote_taken = ""

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame for faster processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR to RGB
    rgb_small_frame = np.ascontiguousarray(small_frame[:, :, ::-1])

    # Only process every other frame to save time
    if process_this_frame:
        # Find all faces and face encodings in the current frame
        face_locations = face_recognition.face_locations(rgb_small_frame)
        
        if face_locations:
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # Compare the face with known faces
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                # Use the face with the smallest distance
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                face_names.append(name)
                
                if (already_vote_taken != name) and (name != "Unknown") and (name != "avinash"):
                    print("vote taken")
                    already_vote_taken = name
                    s.write(b'a')
                    time.sleep(1)
                elif name == "avinash":
                    print("Admin Access")
                    s.write(b'c')
                    time.sleep(1)
                else:
                    print("Invalid Voter")
                    s.write(b'b')
                    time.sleep(1)

    process_this_frame = not process_this_frame

    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with the name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the image with face recognition
    cv2.imshow('Video', frame)

    # Press 'q' to quit the program
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("data save")
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
