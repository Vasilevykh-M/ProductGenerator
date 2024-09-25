#!/bin/sh

wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=1C1smXa0NJNYmg-guKOku6pwqEgMVGm3x' -o remover.onnx

wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=1Zj-NoVVt88kdiIPbeeaDkdZbUF4ilkjQ' -o clip.onnx


# Launch nginx
nginx &

# Launch app
fastapi run /code/app/main.py --port 8500