import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
 
ret, sol = cv2.solve(coeff,z,flags=cv2.DECOMP_QR)