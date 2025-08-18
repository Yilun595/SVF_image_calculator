# View Factor Calculator Using Fisheye Images

This repository assists in calculating view factors from fisheye images. It offers an alternative to using Rayman software.

---

## Required Environment

- **Python version:** 3.7
- **Packages:** `cv2`, `numpy`

```bash
pip install opencv-python
pip install numpy
```

## Usage

### Input image

Square, black and white image, only containing black or white pixels. The image will be resized, see below, in case the calculation runs too slow.

### Functions

Currently, three functions are included.

- calVF_rayman(img_path,resize_scale)

This algorithm should give a similar output as Rayman software. It follows the algorithm described in `Rayman manual` p44.

- calVF_rayman_p(img_path,resize_scale)

As discussed by `Hämmerle et al. (2011)` and described in `Rayman manual` p44-45, incorporating a calibration of zenith angle will be necessary in some occasions. This function implements the algorithm with a zenith angle calibration. The output from this function should be similar to the below JW1984 algorithm.

- calVF_JW1984(img_path,resize_scale,ring_no)

This function follows algorithm by `Johnson and Watson (1984)`. When using an image, this algorithm uses rings from the image center to calculate the view factor, and is therefore sensitive to the image size and ring_no parameter.

## Example

Clone this repository and run the following code in Python.

```python
from SVF_img_calculator import SVF_img_cal as SVF
import cv2

print(cv2.imread("./ExampleImg/01.png").shape)

SVF.calVF_rayman("./ExampleImg/01.png", (512, 512))
SVF.calVF_rayman_p("./ExampleImg/02.png", (512, 512))
SVF.calVF_JW1984("./ExampleImg/03.png", (512, 512), ring_no=10)
```

## References

Hämmerle, M., Gál, T., Unger, J., & Matzarakis, A. (2011). Comparison of models calculating the sky view factor used for urban climate investigations. Theoretical and Applied Climatology, 105(3–4), 521–527.

Johnson GT, Watson ID. 1984. The determination of view factors in urban canyons. Journal of Climate and Applied Meteorology 2: 329–335.

Matzarakis, A., Rutz, F., & Mayer, H. (2007). Modelling radiation fluxes in simple and complex environments—Application of the RayMan model. International Journal of Biometeorology, 51(4), 323–334.

Matzarakis, A., Rutz, F., & Mayer, H. (2010). Modelling radiation fluxes in simple and complex environments: Basics of the RayMan model. International Journal of Biometeorology, 54(2), 131–139.

## Usage

This implementation was first used in this below work, calculating SVF profile from panoramic videos.

Li, Y., Li, Z., & Ren, C. (2025). Diversity of summertime thermal and environmental perceptions in residential public spaces: A walking-based assessment in Hong Kong’s Public Housing Estates. Building and Environment, 112594.

Please consider the below description when using this package in a publication.

"View factor is calculated following the algorithm of Rayman (Matzarakis et al., 2007, 2010), implemented in Python (Li et al., 2025)."
