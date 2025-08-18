from SVF_img_calculator import SVF_img_cal as SVF
import cv2

print(cv2.imread("./ExampleImg/01.png").shape)

SVF.calVF_rayman("./Example_Img/01.png", (512, 512))
SVF.calVF_rayman_p("./ExampleImg/02.png", (512, 512))
SVF.calVF_JW1984("./ExampleImg/03.png", (512, 512), ring_no=10)