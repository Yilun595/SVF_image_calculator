#Python version: 3.7
import mxnet as mx
from mxnet import image
import gluoncv
from gluoncv.data.transforms.presets.segmentation import test_transform
from gluoncv.utils.viz import get_color_pallete
import decord as de
import numpy as np
import cv2
import os
import math
import pandas as pa
ctx = mx.cpu(0)
model = gluoncv.model_zoo.get_model('deeplab_resnest269_ade', pretrained=True)
SKYcolor = [230, 230, 6]
GREENcolor = [230, 230, 6]

def VideoToPic(filename,pic_folder,file_basename):
    #extract frames
    vr = de.VideoReader(filename)
    fps = round(vr.get_avg_fps())
    fra_num = len(vr)
    print('The video contains %d frames' % fra_num)
    print("FPS %d frames per sec" % fps)

    frame_id_list = range(0,fra_num,fps)
    frames = vr.get_batch(frame_id_list).asnumpy()

    count = 1

    for frame in frames:
        image_name = file_basename + '-' + str(count) + ".jpg"
        cv2.imwrite(os.path.join(pic_folder, image_name), frame)
        count = count + 1
        print('{} done!'.format(image_name))
def Tomask(indir,pic_folder):
    print("starting segmentation")
    for i in os.listdir(indir):
        img = image.imread(os.path.join(indir, i))
        img = test_transform(img,ctx)
        #make prediction using single scale
        output = model.predict(img)
        predict = mx.nd.squeeze(mx.nd.argmax(output, 1)).asnumpy()
        #add color pallete for visualization
        mask = get_color_pallete(predict, 'ade20k')
        output_name = "mask-" + i.split(".")[0] + ".png"
        mask.save(os.path.join(pic_folder, output_name))
        print('{} done!'.format(output_name))
def ClipToCircle(indir,pic_folder):
    print("starting mask with circle")
    for i in os.listdir(indir):
        img = cv2.imread(os.path.join(indir, i))
        mask_cir = np.zeros(img.shape[:2], dtype="uint8")
        mask_cir = cv2.circle(mask_cir, (round(img.shape[1] / 2), round(img.shape[0] / 2)), round(img.shape[1] / 2),
                   (255, 255, 255),
                   -1)
        masked = cv2.bitwise_and(img, img, mask=mask_cir)
        output_name = "mask-circle-" + i.split(".")[0] + ".png"
        cv2.imwrite(os.path.join(pic_folder, output_name),masked)
        print('{} done!'.format(output_name))
def ElementOnly(indir,pic_folder,color):
    print("starting picking out element")
    for i in os.listdir(indir):
        img = cv2.imread(os.path.join(indir, i))
        for y in range(img.shape[1]):
            for x in range(img.shape[0]):
                if img[x, y][0] == color[0] and img[x, y][1] == color[1] and img[x, y][2] == color[2]:
                    img[x, y] = [255,255,255]
                else:
                    img[x, y] = [0, 0, 0]
        output_name = "Element-" + i.split(".")[0] + ".png"
        cv2.imwrite(os.path.join(pic_folder, output_name),img)
        print('{} done!'.format(output_name))
def calVF_rayman(img_path,resize_scale):
    img = cv2.imread(img_path)
    img = cv2.resize(img, resize_scale)
    img_bg = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    sum_i = 0.0
    sum_j = 0.0

    for y in range(img.shape[1]):
        for x in range(img.shape[0]):
            degree = (1.0 - (
                        ((float(x) - float(img.shape[1])) ** 2.0 + (float(y) - float(img.shape[1])) ** 2.0) ** 0.5) / float(
                img.shape[1])) * (math.pi / 2.0)
            if degree > 0:
                fac = float(math.pi * math.sin(degree) / float(2.0 * degree))
                sum_j = sum_j + fac
                if img_bg[x, y] == 0:
                    pass
                else:
                    img_bg[x, y] =255
                    sum_i = sum_i + fac * float(img_bg[x, y])/255
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
def calVFinFolder(indir,outdir,resize_scale,method,rings):
    print("Starting calculating SVF in the given folder.")
    Results=[]
    if method == "rayman":
        for i in os.listdir(indir):
            img_0 = os.path.join(indir, i)
            VF = calVF_rayman(img_0,resize_scale)
            Results.append(VF)
        Res = pa.DataFrame(Results)
        Res.to_csv(outdir)
        print("File saved as {}.".format(outdir))
    else:
        if method == "JW1984":
            for i in os.listdir(indir):
                img_0 = os.path.join(indir, i)
                VF = calVF_JW1984(img_0, resize_scale,rings)
                Results.append(VF)
            Res = pa.DataFrame(Results)
            Res.to_csv(outdir)
            print("File saved as {}.".format(outdir))
        else:
            print("Wrong method input.")


# VideoToPic("test.mp4","OutputImage\\","SVFraw")
# Tomask("OutputImage\\","OutputImageMask\\")
#ClipToCircle("OutputImage\\","OutputImageRaw\\")
#ElementOnly("OutputImageMask\\","SKY\\",SKYcolor)
# calVF_rayman("SKY\\Element-mask-SVFraw-1.png",(1440,1440))
# calVF_JW1984("SKY\\Element-mask-SVFraw-1.png",(1440,1440),60)

calVFinFolder("SKY\\","test.csv",(1440,1440),"rayman",0) #when rayman is used, the last parameter can be anything
calVFinFolder("SKY\\","test2.csv",(1440,1440),"JW1984",60)
