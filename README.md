To run the HSV inversion method.

```bash
$ python main.py \
    -v videos/sample.mp4 \
    -st 00:00:10 \
    -et 00:00:15 \
    -t "Ayman"  \
    -p false \
    -c false \
    -x 20 \
    -y 20 \
    -hsv true \
    -ff 3 \
    -fs 1
```

To run the Contrast Transformation method with a set contrast of 15.0.

```bash
$ python main.py \
    -v videos/sample.mp4 \
    -st 00:00:10 \
    -et 00:00:15 \
    -t "Christian"  \
    -p false \
    -c false \
    -x 20 \
    -y 20 \
    -hsv false \
    -ff 3 \
    -fs 1\
    -cl 15.0
```