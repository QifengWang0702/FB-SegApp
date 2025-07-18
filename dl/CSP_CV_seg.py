# -*- coding: UTF-8 -*-
import cv2
import numpy as np
import torch
from scipy.ndimage import zoom
from dl.models.unet import UNet, UNet_CCT, UNet_URPC, UNet_DS
from util.logger import logger

device = torch.device('cuda:0' if torch.cuda.is_available() else "cpu")


# UNet, UNet_CCT, UNet_URPC, UNet_DS
def net_factory(net_type="unet", in_chns=1, class_num=3):
    if net_type == "unet":
        net = UNet(in_chns=in_chns, class_num=class_num).to(device)
        return net
    if net_type == "unet_cct":
        net = UNet_CCT(in_chns=in_chns, class_num=class_num).to(device)
        return net
    if net_type == "unet_urpc":
        net = UNet_URPC(in_chns=in_chns, class_num=class_num).to(device)
        return net
    if net_type == "unet_ds":
        net = UNet_DS(in_chns=in_chns, class_num=class_num).to(device)
        return net


def mix(image_path, CCC, CV, size=256):
    try:
        logger.info(f'seg - mix - image_path: {image_path}')
        logger.info(f'seg - mix - size: {size}')
        original = cv2.imread(image_path)
        original = cv2.resize(original, (size, size))
        if len(CCC.shape) != 3:
            CCC = cv2.cvtColor(CCC, cv2.COLOR_GRAY2BGR)
        if len(CV.shape) != 3:
            CV = cv2.cvtColor(CV, cv2.COLOR_GRAY2BGR)
        CCC[np.all(CCC == [255, 255, 255], axis=-1)] = [0, 0, 255]
        CV[np.all(CV == [255, 255, 255], axis=-1)] = [0, 255, 0]
        result = cv2.add(CCC, CV)
        result = cv2.addWeighted(result, 0.2, original, 0.8, 0)
        logger.info(f'segment - mix - Mix successfully!')
        return result
    except Exception as e:
        logger.error(f'segment - mix - {e}')
        image = cv2.imread(image_path)
        return image


def compute(image, lengthScale, areaScale):
    try:
        logger.info(f'segment - compute - areaScale: {areaScale}, lengthScale: {lengthScale}')
        if len(image.shape) > 2:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image = image.astype(np.uint8)
        contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        areas = []
        for j in range(len(contours)):
            areas.append(cv2.contourArea(contours[j]))
        max_idx = np.argmax(areas)
        length = cv2.arcLength(contours[max_idx], True) * lengthScale
        area = cv2.contourArea(contours[max_idx]) * areaScale + length
        proccessImage = np.zeros_like(image)
        cv2.drawContours(proccessImage, [contours[max_idx]], -1, 255, cv2.FILLED)
        logger.info(f'segment - compute - area: {area}, length: {length}')
        return proccessImage, area, length
    except Exception as e:
        logger.error(f'segment - compute - {e}')
        return image, 0, 0


def inference(image_path, model_path, net_type, in_chns, class_num, size=256):
    try:
        logger.info(f'segment - inference - image_path: {image_path}')
        logger.info(f'segment - inference - model_path: {model_path}')
        logger.info(
            f'segment - inference - net_type: {net_type}, in_chns: {in_chns}, class_num: {class_num}, size: {size}')
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image = cv2.resize(image, (size, size))
        patch_size = [size, size]
        image = cv2.resize(image, (patch_size[0], patch_size[1]))
        x, y = image.shape[0], image.shape[1]
        input = torch.from_numpy(image).unsqueeze(0).unsqueeze(0).float().to(device)

        net = net_factory(net_type, in_chns, class_num)
        net.load_state_dict(torch.load(model_path, map_location=torch.device(device)))
        net.eval()
        with torch.no_grad():
            out_main, _, _, _ = net(input)
            out = torch.argmax(torch.softmax(out_main, dim=1), dim=1).squeeze(0)
            out = out.cpu().detach().numpy()
            pred = zoom(out, (x / patch_size[0], y / patch_size[0]), order=0)
        for x in range(pred.shape[0]):
            for y in range(pred.shape[1]):
                px = pred[x, y]
                if px == 0:
                    pred[x, y] = 0
                else:
                    pred[x, y] = 255
        logger.info(f'segment - inference - Predict successfully!')
        return pred
    except Exception as e:
        logger.error(f'segment - inference - {e}')
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return image
