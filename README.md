# accumulativeSVF
These codes calculates SVF from Insta360 cameras.

[Functions in the file]
VideoToPic(filename,pic_folder,file_basename)
  Extracts images of a video (filename) by every second and output the images to a folder (pic_folder), named with a basename (file_basename).

Tomask(indir,pic_folder)
  To segment and classify images from a folder (indir), and put results in a folder (pic_folder).

ClipToCircle(indir,pic_folder)
  To visualize the SVF images from a folder (indir) by adding a mask of circle and output all images to a folder (pic_folder).
  REQUIREMENT: All input images must be 1:1 square.

ElementOnly(indir,pic_folder,color)
  Convert images in a folder (indir) to black and white mode by preserving pixels of one same color described in RGB (color), and output to a folder (pic_folder).

calVF_rayman(img_path,resize_scale)
  Calculate SVF based on a image (img_path) by using rayman method. The image is resized first (resize_scale, (1440,1440)).
  REQUIREMENT: Image is required to be (1) square, (2) black and white only. The image should be resized to a number which can be divided by 4.

calVF_JW1984(img_path,resize_scale,ring_no)
  Calculate SVF based on a image (img_path) by using JW1984 method. The image is resized first (resize_scale, (1440,1440)). The image is clipped into rings for   calculation of SVF (ring_no).
  REQUIREMENT: Image is required to be (1) square, (2) black and white only. The image should be resized to a number which can be divided by 4. It is suggested that the image pixel/ring_no >10.

calVFinFolder(indir,outdir,resize_scale,method,rings)
  It calculates SVF of images in a folder (indir) and output results to a .csv document (outdir, suggestted "test2.csv"). The resize scale will be transformed to calVF_rayman or calVF_JW1984. "method" should be either "rayman" or "JW1984". "rings" should be an integer, and when "rayman" method is used, any integar will make the runction run.
