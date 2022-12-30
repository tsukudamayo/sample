from dezero.core import Variable
from dezero.functions import Square, Exp, square, exp, Add

import numpy as np


def numerical_diff(f, x, eps=1e-4):
    x0 = Variable(x.data - eps)
    x1 = Variable(x.data + eps)
    y0 = f(x0)
    y1 = f(x1)

    return (y1.data - y0.data) / (2 * eps)


def f(x):
    A = Square()
    B = Exp()
    C = Square()
    return C(B(A(x)))


def main():
    # step11
    x0 = Variable(np.array(2))
    x1 = Variable(np.array(3))
    f = Add()
    y = f(x0, x1)
    print(y.data)
        


if __name__ == "__main__":
    main()
