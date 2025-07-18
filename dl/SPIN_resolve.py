# -*- coding: UTF-8 -*-
import argparse
import os
import cv2
import yaml
import numpy as np
import torch
import torch.nn as nn
import imageio.v2 as imageio
import skimage.color as sc
from cv2 import dnn_superres
import importlib
from util.logger import logger

print('SPIN model train and test code URL: https://github.com/ArcticHare105/SPIN')
parser = argparse.ArgumentParser(description='SPIN')


def import_module(name):
    return importlib.import_module(name)


def ndarray2tensor(ndarray_hwc):
    ndarray_chw = np.ascontiguousarray(ndarray_hwc.transpose((2, 0, 1)))
    tensor = torch.from_numpy(ndarray_chw).float()
    return tensor


def SPIN_resolve(image_path, model_paths: list, configs_path):
    try:
        lr_image = imageio.imread(image_path, pilmode="RGB")
        lr_image = sc.rgb2ycbcr(lr_image)[:, :, 0:1]
        image = ndarray2tensor(lr_image)

        args = parser.parse_args()
        opt = vars(args)
        yaml_args = yaml.load(open(configs_path), Loader=yaml.FullLoader)
        opt.update(yaml_args)

        gpu_ids_str = str(args.gpu_ids).replace('[', '').replace(']', '')
        os.environ['CUDA_DEVICE_ORDER'] = 'PCI_BUS_ID'
        os.environ['CUDA_VISIBLE_DEVICES'] = '{}'.format(gpu_ids_str)

        # select active gpu devices
        device = None
        if args.gpu_ids is not None and torch.cuda.is_available():
            logger.info('resolve - SPIN_resolve - use cuda & cudnn for acceleration!')
            logger.info('resolve - SPIN_resolve - the gpu id is: {}'.format(args.gpu_ids))
            device = torch.device('cuda')
            torch.backends.cudnn.benchmark = True
        else:
            logger.info('resolve - SPIN_resolve - use cpu for training!')
            device = torch.device('cpu')
        torch.set_num_threads(args.threads)

        # try:
        model = import_module('dl.models.{}'.format(args.model)).create_model(args)
        # except Exception:
        #     raise ValueError('not supported model type! or something')
        model = nn.DataParallel(model).to(device)

        ckpt = torch.load(model_paths[0], map_location=torch.device(device))
        model.load_state_dict(ckpt['model_state_dict'])

        torch.set_grad_enabled(False)
        model = model.eval()

        image = image.to(device)
        torch.cuda.empty_cache()
        srImage = model(image)
        out_img = srImage.detach()[0].float().cpu().numpy()
        out_img = np.transpose(out_img, (1, 2, 0))
        dst = out_img[:, :, [2, 1, 0]]
        return dst
    except Exception:
        logger.error('resolve - SPIN_resolve - not supported model type! or something')
        image = cv2.imread(image_path)
        sr = dnn_superres.DnnSuperResImpl_create()
        sr.readModel(model_paths[1])
        sr.setModel("fsrcnn", 2)
        dst = sr.upsample(image)
        # cv2.imwrite(r"D:\F\prenatal_py38\upscaled.png", dst)
        return dst


# if __name__ == '__main__':
#     imageName = r'E:\biye\SR_FBUS\benchmarks\B100\LR_bicubic\X2\0001x2.png'
#     modelName = r'E:\biye\SPIN-main\experiments\FBUS-spin-fp32-x2-2024-0303-1444\models\model_x2_59.pt'
#     configsName = r'E:\biye\SPIN-main\configs\spin_light_x2.yml'
#     SPIN_resolve(imageName, modelName, configsName)
