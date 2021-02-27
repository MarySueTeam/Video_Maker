import cv2
from PIL import Image
import numpy as np
from typing import Dict, Tuple


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


def get_img_feature(img_path: str, edge: int) -> dict:
    """
    获取图片的特征,并根据特征返回背景的生成模式和当前图片的摆放位置

    Args:
        img_path (str): 图片路径
        edge (int): 边缘大小

    Returns:
        dict : (背景的生成模式,边缘位置[上下左右],边缘距离)
    """
    origin_img = cv2.imread(img_path)
    tmp_img = cv2.imread(img_path)
    (w, h, z_index) = origin_img.shape
    top_edge = []
    bottom_edge = []
    left_edge = []
    right_edge = []

    RESULTS = {
        "mode": {
            "type": 0,
        },
        "edge": {
            "top": 0,
            "bottom": 0,
            "left": 0,
            "right": 0,
        },
    }

    # INFO 自外而内的遍历图像矩阵来检测边缘
    counter = 0
    cv2.imshow("2", tmp_img)
    cv2.waitKey(1000)
    first_point = origin_img[0, 0]
    while counter < (min(w, h) // 2):
        l, r, t, b = counter, w - counter - 1, counter, h - counter - 1
        for i in range(l, r):
            if (origin_img[i, t] != first_point).all():
                if RESULTS['edge']['top'] == 0:
                    RESULTS['edge']['top'] = counter
                else:
                    pass
            else:
                tmp_img[i, t] = [255, 0, 0]
            if (origin_img[i, b] != first_point).all():
                if RESULTS['edge']['bottom'] == 0:
                    RESULTS['edge']['bottom'] = counter
                else:
                    pass
            else:
                tmp_img[i, b] = [0, 255, 0]
            top_edge.append(origin_img[i, t])
            bottom_edge.append(origin_img[i, b])

        for i in range(t, b):
            if (origin_img[l, i] != first_point).all():
                if RESULTS['edge']['left'] == 0:
                    RESULTS['edge']['left'] = counter
                else:
                    pass
            else:
                tmp_img[l, i] = [0, 0, 255]
            if (origin_img[r, i] != first_point).all():
                if RESULTS['edge']['right'] == 0:
                    RESULTS['edge']['right'] = counter
                else:
                    pass
            else:
                tmp_img[r, i] = [255, 255, 0]

            left_edge.append(origin_img[l, i])
            right_edge.append(origin_img[r, i])

        cv2.imshow("2", tmp_img)
        cv2.waitKey(10)
        counter = counter + 1

    if counter == 0:
        RESULTS['mode']['type'] = 1
    else:
        RESULTS['mode']['type'] = 2

    return RESULTS


if __name__ == "__main__":
    img_path = "./src/images/87732624_p0.jpg"
    # img_path = "./src/images/⁄(⁄ ⁄•⁄ω⁄•⁄ ⁄)⁄_p0.jpg"
    res = get_img_feature(img_path=img_path, edge=10)
    print(res)
