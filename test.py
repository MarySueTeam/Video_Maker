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


def get_img_feature(img_path: str, edge: int) -> tuple(int, int, int):
    """
    获取图片的特征,并根据特征返回背景的生成模式和当前图片的摆放位置

    Args:
        img_path (str): 图片路径
        edge (int): 边缘大小

    Returns:
        tuple (int, int, int): (背景的生成模式,模式参数,图片摆放位置)
            FLAG: 1: TOP 2: BOTTOM 3: LEFT 4: RIGHT
    """
    origin_img = cv2.imread(img_path)
    tmp_img = origin_img
    (w, h, z_index) = origin_img.shape
    top_edge = []
    bottom_edge = []
    left_edge = []
    right_edge = []

    MODE = 0
    FLAG = 0
    POS = 0

    # INFO 自外而内的遍历图像矩阵来检测边缘
    counter = 0
    first_point = origin_img[0, 0]
    while counter < (min(w, h) // 2):
        l, r, t, b = counter, w - counter - 1, counter, h - counter - 1
        for i in range(l, r):
            if (origin_img[i, t] != first_point).all():
                FLAG = 1
                break
            if (origin_img[i, b] != first_point).all():
                FLAG = 2
                break
            top_edge.append(origin_img[i, t])
            bottom_edge.append(origin_img[i, b])
            tmp_img[i, t] = [255, 0, 0]
            tmp_img[i, b] = [255, 255, 0]

        for i in range(t, b):
            if (origin_img[l, i] != first_point).all():
                FLAG = 3
                break
            if (origin_img[r, i] != first_point).all():
                FLAG = 4
                break
            left_edge.append(origin_img[l, i])
            right_edge.append(origin_img[r, i])
            tmp_img[l, i] = [0, 255, 255]
            tmp_img[r, i] = [255, 0, 255]

        if FLAG != 0:
            break

        cv2.imshow("2", tmp_img)
        cv2.waitKey(10)
        counter = counter + 1

    print(top_edge)
    print(bottom_edge)
    print(left_edge)
    print(right_edge)
    if counter == 0:
        MODE = 1
        return (MODE, FLAG, POS)


if __name__ == "__main__":
    # img_path = "./src/images/⁄(⁄ ⁄•⁄ω⁄•⁄ ⁄)⁄_p0.jpg"
    img_path = "./src/images/風船を売るおじいちゃん_p7.jpg"
    (mode, flag, pos) = get_img_feature(img_path=img_path, edge=10)
    print(mode, flag, pos)
