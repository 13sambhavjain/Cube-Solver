from enum import StrEnum
class Algo():
    class OLL():
        # https://jperm.net/algs/2look/oll - refrence used
        class Edges(StrEnum):
            dot_shape = "F R U R' U' F' f R U R' U' f'"
            I_shape = "F R U R' U' F'"
            L_shape = "f R U R' U' f'"
        class Corners(StrEnum):
            Antisune = "R U2 R' U' R U' R'"
            H = "R U R' U R U' R' U R U2 R'"
            L = "F R' F' r U R U' r'"
            Pi = "R U2 R2 U' R2 U' R2 U2 R"
            headlight_sidelight = "R U2 R2 U' R2 U' R2 U2 R"
            Sune = "R U2 R2 U' R2 U' R2 U2 R"
            T = "r U R' U' r' F R F'"
            U = "R2 D R' U2 R D' R' U2 R"