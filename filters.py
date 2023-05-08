import cv2
import numpy as np
import streamlit as st

@st.cache_data
def color_dodge(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_inverted = cv2.bitwise_not(img_gray)
    img_blurred = cv2.GaussianBlur(img_inverted, (13, 13), 0)
    img_color_dodge = cv2.divide(img_gray, 255 - img_blurred, scale=256)
    return img_color_dodge

@st.cache_data
def emboss(img, ksize=3):
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    height, width = gray_img.shape
    y = np.ones((height, width), np.uint8) * 128
    emboss_kernel = np.array([[-2, -1, 0],
                              [-1, 1, 1],
                              [0, 1, 2]], dtype=np.float32)
    emboss_img = cv2.filter2D(gray_img, -1, emboss_kernel) + 128
    return emboss_img

@st.cache_data
def watercolor(img, ksize=5, sigmaColor=50, sigmaSpace=15):
    img_filtered = cv2.bilateralFilter(img, ksize, sigmaColor, sigmaSpace)
    img_filtered = cv2.medianBlur(img_filtered, 7)
    return img_filtered

@st.cache_data
def cartoon(img, ksize=5, sigmaColor=50, sigmaSpace=15):
    img_cartoon = cv2.bilateralFilter(img, ksize, sigmaColor, sigmaSpace)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_edges = cv2.adaptiveThreshold(img_gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
    img_edges = cv2.cvtColor(img_edges, cv2.COLOR_GRAY2BGR)
    img_cartoon = cv2.bitwise_and(img_cartoon, img_edges)
    return img_cartoon
    