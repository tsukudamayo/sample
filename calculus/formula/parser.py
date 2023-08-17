from typing import Union

from sympy import Rational, sqrt, Mul, Integer, Float


def parse(number: str) -> Union[float, Rational, Mul, Integer]:
    if "/" in number:
        _rational = number.split("/")
        return Rational(_rational[0], _rational[1])
    elif "√" in number:
        _roots = number.split("√")
        if "." in _roots[1]:
            return sqrt(Float(_roots[1]))
        return sqrt(Integer(_roots[1]))
    else:
        return float(number)


def main():
    print(parse("3"))
    print(parse("1/2"))
    print(parse("√4"))
    print(parse("√4.2"))
    print(parse("√8"))


if __name__ == "__main__":
    main()

