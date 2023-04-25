import mxnet as mx
from mxnet import image
import gluoncv
from gluoncv.data.transforms.presets.segmentation import test_transform
from gluoncv.utils.viz import get_color_pallete
import decord as de
import numpy as np
import cv2
import os
ctx = mx.cpu(0)
model = gluoncv.model_zoo.get_model('deeplab_resnest269_ade', pretrained=True)
SKYcolor = [230, 230, 6]

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

# VideoToPic("test.mp4","OutputImage\\","SVFraw")
# Tomask("OutputImage\\","OutputImageMask\\")
#ClipToCircle("OutputImage\\","OutputImageRaw\\")
ElementOnly("OutputImageMask\\","SKY\\",SKYcolor)