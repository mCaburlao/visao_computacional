import cv2
import numpy as np

def nothing(x):
    pass

cap = cv2.VideoCapture(0)
cv2.namedWindow("Result Image")

cv2.createTrackbar("Line Rho", "Result Image", 1, 10, nothing)
cv2.createTrackbar("Line Threshold", "Result Image", 184, 200, nothing)

cv2.createTrackbar("Circle param1", "Result Image", 217, 500, nothing)
cv2.createTrackbar("Circle param2", "Result Image", 56, 100, nothing)
cv2.createTrackbar("Circle minRadius", "Result Image", 1, 100, nothing)
cv2.createTrackbar("Circle maxRadius", "Result Image", 196, 200, nothing)


while True:
    ret, img = cap.read()
    if not ret:
        break

    rho = cv2.getTrackbarPos("Line Rho", "Result Image")
    threshold = cv2.getTrackbarPos("Line Threshold", "Result Image")

    param1 = cv2.getTrackbarPos("Circle param1", "Result Image")
    param2 = cv2.getTrackbarPos("Circle param2", "Result Image")
    minRadius = cv2.getTrackbarPos("Circle minRadius", "Result Image")
    maxRadius = cv2.getTrackbarPos("Circle maxRadius", "Result Image")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 200)

    if rho < 1:
        rho = 1
    lines = cv2.HoughLinesP(edges, rho, np.pi/180, threshold, minLineLength=10, maxLineGap=250)

    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 3)

    # --- Circle detection ---
    img_blur = cv2.medianBlur(gray, 5)
    circles = cv2.HoughCircles(
        img_blur,
        cv2.HOUGH_GRADIENT,
        1,
        img.shape[0] / 64,
        param1=param1,
        param2=param2,
        minRadius=minRadius,
        maxRadius=maxRadius
    )
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            # Draw outer circle
            cv2.circle(img, (i[0], i[1]), i[2], (0, 255, 0), 2)
            # Draw center of the circle
            cv2.circle(img, (i[0], i[1]), 2, (0, 0, 255), 3)

    cv2.imshow("Result Image", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()