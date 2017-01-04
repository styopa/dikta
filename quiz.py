#!/usr/bin/python3
import argparse

ap = argparse.ArgumentParser(description =
    'Interactive Do I Know It Already quiz')
ap.add_argument('json_file', type = argparse.FileType('r'))

args = ap.parse_args()
