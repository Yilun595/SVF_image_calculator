import cv2
import math
import numpy as np

def calVF_rayman(img_path,resize_scale):
    img = cv2.imread(img_path)
    img = cv2.resize(img, resize_scale)
    img_bg = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    d = float(img.shape[1])
    r = d/2
    sum_i = 0.0
    sum_j = 0.0
    for y in range(img.shape[1]):
        for x in range(img.shape[0]):
            a = float(x)
            b = float(y)
            degree = (((a - r) ** 2.0 + (b - r) ** 2.0) ** 0.5) * math.pi / d
            if degree > 0 and degree <= math.pi/2:
                fac = math.sin(degree) / degree
                sum_j = sum_j + fac
                if img_bg[x, y] == 0:
                    pass
                else:
                    sum_i = sum_i + fac
            else:
                pass
    SVF = sum_i/sum_j
    note = "Input image size {}, rescale size {}.".format(img.shape[0],resize_scale[0])
    return((SVF,img_path,note))

def calVF_rayman_p(img_path,resize_scale):
    img = cv2.imread(img_path)
    img = cv2.resize(img, resize_scale)
    img_bg = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    d = float(img.shape[1])
    r = d/2
    sum_i = 0.0
    sum_j = 0.0
    for y in range(img.shape[1]):
        for x in range(img.shape[0]):
            a = float(x)
            b = float(y)
            degree = (((a - r) ** 2.0 + (b - r) ** 2.0) ** 0.5) * math.pi / d
            if degree > 0 and degree <= math.pi/2:
                fac = math.sin(degree) * math.cos(degree)/ degree
                sum_j = sum_j + fac
                if img_bg[x, y] == 0:
                    pass
                else:
                    sum_i = sum_i + fac
            else:
                pass
    SVF = sum_i/sum_j
    note = "Input image size {}, rescale size {}.".format(img.shape[0],resize_scale[0])
    return((SVF,img_path,note))

def calVF_JW1984(img_path,resize_scale,ring_no):
    img = cv2.imread(img_path)
    img = cv2.resize(img, resize_scale)
    n = ring_no
    r = int (img.shape[0] / 2)
    r_width = int(r/n)
    cen = int (r_width / 2)

    mask_0 = np.zeros(img.shape, np.uint8)
    sum_i = 0.0
    img_bg = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)

    for i in range(1,n+1):
        mask = np.zeros(img.shape, np.uint8)
        cv2.circle(mask,(r,r),r_width * i - cen,(255,255,255),r_width, lineType = 8)
        mask = cv2.bitwise_and(mask, cv2.bitwise_not(mask_0))
        sky_in_ring = cv2.bitwise_and(mask,img)

        mask_0=mask.copy()
        mask_bw = cv2.cvtColor(mask,cv2.COLOR_RGB2GRAY)
        sky_in_ring_bw = cv2.cvtColor(sky_in_ring, cv2.COLOR_RGB2GRAY)

        pixel_ring_all = cv2.countNonZero(mask_bw)
        pixel_ring_sky = cv2.countNonZero(sky_in_ring_bw)

        sum_i = sum_i + (math.sin((math.pi * (2.0 * i - 1.0)) / (2.0 * n)) * ((float(pixel_ring_sky) / float(pixel_ring_all)) * 2.0 * math.pi))

    SVF = ((1.0 / (2.0 * math.pi)) * math.sin(math.pi / (2.0 * n))) * sum_i
    note = "Input image size {}, rescale size {}. {} rings , {} pixels in each ring .".format(img.shape[0],resize_scale[0],ring_no,r_width)
    return((SVF,img_path,note))