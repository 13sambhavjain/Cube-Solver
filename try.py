from enum import StrEnum, global_enum, auto
# import c

@global_enum
class Color(StrEnum):
    RED = auto()
    BLUE = auto()
    GREEN = auto()
    YELLOW = auto()
    WHITE = auto()
    ORANGE = auto()
class Cube():
    """Keeping it real -->
    Defination which includes mirror cube --
    1. A cube is a cube of mathematics just the unit of lenght is the number of pieces. A piece is counted as one when its directly connected (by the edge of the pieces) vertexes are being used for measure. Not when 
    A cube is a  object with equal number of pieces in its each dimension. And these pieces are moving with some rules.
    Every piece which is at some specific depth in the cube will always be at same depth, and can only change positions with other pieces on the same depth.
      Depth can be the distance from center of the face or the nearest edge of the face. 
      On a single face of the cude there can be either 1, 4, or 8 pieces at the same depth. (intersection of a circle and a square with same center)
    """
    def __init__(self, size=3):
        self.size = size




# for c in Color:
#     print(c)

class Custom_list():
    def __init__(self):
        self._collection = [1,2,3,4,5,6,7,8,9]
        self._index = 0
    
    def __str__(self):
        return str(self._collection)
    
    def __getitem__(self, index: int):
        return self._collection[index]
    
    def __setitem__(self, index: int, item) -> None:
        self._collection[index] = item

def main():
    c = Custom_list()
    c[3:40] = [1,2]
    print(c)
    pass

if __name__ == "__main__":
    for _ in range(10):
        print("sdgssdfsf")



























# dd = {
#     'a': 1,
#     'b': 2,
#     'c': 3
# }
# ss = {1, 2, 3}
# ll = [1, 2, 3]
# tt = (1, 2, 3)

# filte
# print(ss, ll, dd, tt, sep='\n')


# n = int(input())
# ll = [13, 20, 14, 10, 34, 12]
# print(list(filter(lambda x: x%n == 0, ll)))




# ss = input().lower()
# vow = {'a': 0, 'e': 0, 'i': 0, 'o': 0, 'u': 0}
# for c in ss:
#     if c in vow:
#         vow[c] += 1
# print(vow)

# def factorial(n):
#     if n < 0:
#         raise ValueError
#     if n <= 1:
#         return 1
#     else:
#         return factorial(n-1)*n
    
# n = int(input())
# print(factorial(n))

# class Rect():
#     def __init__(self, l = 10, b = 10):
#         self .l = l
#         self. b = b

#     @staticmethod
#     def area(l , b):
#         a = l * b
#         print(a)
#         return a
    
#     @classmethod
#     def className(cls):
#         print("Rectangle")

#     def perimeter(self):
#         p = 2*(self.l + self.b)
#         print(p)
#         return p
#     def diagonal(self):
#         d = self.l**2 + self.b**2
#         d = d**0.5
#         print(d)
#         return d
    
# A = Rect.

    
# r1 = Rect(5, 12)
# Rect.className()


# r1.area()
# r1.perimeter()
# r1.diagonal()


# ss = input().lower()
# ss1 = ss[::-1]
# if ss1 == ss:
#     print("Its a plaindrome")
# else:
#     print("not a palindrome")

# n = input()
# sum1 = 0
# for c in n:
#     sum1 += int(c)
# print(sum1)


# hardware in loop
# ECU -- electronic control unit


def isPrime(n) -> bool:
    return 