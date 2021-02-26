import cv2
from PIL import Image
import numpy as np


def get_range(values: list) -> int:
    """
    获取一个列表在平均数周围的波动范围
    :param values: 需要分析的数据列表
    :return: 返回所有的值与平均数的差值总和
    """
    arr_mean = np.mean(values)
    arr_var = np.var(values)
    arr_std = np.std(values)
    print(arr_mean, arr_var, arr_std)


def get_img_feature(img_path: str, edge: int) -> tuple:
    """
    获取图片的特征,并根据特征返回背景的生成模式和当前图片的摆放位置

    Args:
        img_path (str): 图片路径
        edge (int): 边缘大小

    Returns:
        tuple: (背景的生成模式,图片摆放位置)
    """
    origin_img = cv2.imread(img_path)
    (w, h, z_index) = origin_img.shape
    _x = (0, edge, w - edge, w)
    _y = (0, edge, h - edge, h)
    top_edge = []
    bottom_edge = []
    left_edge = []
    right_edge = []

    for x in range(w):
        for y in range(h):
            if x >= _x[0] and x <= _x[1]:
                left_edge.append(origin_img[x, y])
                origin_img[x, y] = [0, 255, 255]
            if x >= _x[2] and x <= _x[3]:
                right_edge.append(origin_img[x, y])
                origin_img[x, y] = [0, 0, 255]
            if y >= _y[0] and y <= _y[1]:
                top_edge.append(origin_img[x, y])
                origin_img[x, y] = [255, 0, 0]
            if y >= _y[2] and y <= _y[3]:
                bottom_edge.append(origin_img[x, y])
                origin_img[x, y] = [255, 0, 255]
    get_range(top_edge)
    get_range(bottom_edge)
    get_range(left_edge)
    get_range(right_edge)

    cv2.imshow("2", origin_img)
    cv2.waitKey(delay=10000)


if __name__ == "__main__":
    # img_path = "./src/images/⁄(⁄ ⁄•⁄ω⁄•⁄ ⁄)⁄_p0.jpg"
    img_path = "./src/images/風船を売るおじいちゃん_p7.jpg"
    get_img_feature(img_path=img_path, edge=30)
