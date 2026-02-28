import pygame
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)
BASE_IMG_PATH = os.path.join(ROOT_DIR, "data", "sprites")

def load_img(path):
    img_path = os.path.join(BASE_IMG_PATH, path)
    img = pygame.image.load(img_path).convert()
    img.set_colorkey((0, 0, 0))
    return img

def load_img_2x(path):
    img = load_img(path)
    w, h = img.get_size()
    return pygame.transform.scale(img, (w*2, h*2))