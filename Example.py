from SVF_img_calculator import SVF_img_cal as SVF
import cv2

print(cv2.imread("./ExampleImg/01.png").shape)

# Output from this function should be similar to Rayman's output
SVF.calVF_rayman("./ExampleImg/01.png", (512,512))

# Testing the calibrated Rayman algorithm and JW1984 algorithm
SVF.calVF_rayman_p("./ExampleImg/03.png", (512,512))
SVF.calVF_JW1984("./ExampleImg/03.png",(512,512), ring_no=10)
# Which would be quite different from Rayman's output
SVF.calVF_rayman("./ExampleImg/03.png", (512,512))