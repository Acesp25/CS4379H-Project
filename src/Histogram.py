import cv2
from matplotlib import pyplot as plt
<<<<<<< Updated upstream
img1 = cv2.imread('images/Historgrams/out.png', 1)
=======
img1 = cv2.imread('images/Histograms/out.png', 1)
>>>>>>> Stashed changes
plt.hist(img1.ravel(),256,[0,256])
plt.show()
