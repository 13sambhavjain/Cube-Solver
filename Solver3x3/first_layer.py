from .first_cross import FirstCross
from .first_corners import FirstCorners

class FirstLayer(FirstCorners, FirstCross):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    def solve_first_layer(self):
        self.solve_first_cross()
        self.solve_first_corners()