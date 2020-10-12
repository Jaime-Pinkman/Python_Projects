from superpixel.Slic import Slic


if __name__ == '__main__':
    p = Slic('images/Lenna.png', 500, 30)
    p.iterate_10times()