# SVFcalculator
The code provided here may assist calculation of sky view factor by using fisheye images. It offers an alterative to using Rayman.
The input image, as shown in the example folder, should be a square image that only contains black or white pixels.

Currently, two algorithms are included.

calVF_rayman(img_path,resize_scale)
This algorithm should be identical to Rayman software.

calVF_rayman_p(img_path,resize_scale)
This algorithm is an update to Rayman software, which incorporates a calibration of zenith angle. Output of this function should be similar to the below algorithm.

calVF_JW1984(img_path,resize_scale,ring_no)
This function follows algorithm of JW1984.

[Required environment]
Python 3.7
Packages used: cv2
