# sort of like tensors
from textwrap import wrap
from typing import Sequence


def part1(layers: Sequence[str]) -> int:
    layer = min(layers, key=lambda l: l.count('0'))
    return layer.count('1') * layer.count('2')


def main(pixels: str, w: int, h: int):
    pixels_per_layer = w * h
    layers = tuple(wrap(pixels, width=pixels_per_layer))
    print(part1(layers))


with open('/home/dmb/aoc-2019/data/d08.txt') as f:
    pixels = f.read().strip()

main(pixels, w=25, h=6)
