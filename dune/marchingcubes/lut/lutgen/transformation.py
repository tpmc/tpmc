from permutation import Permutation

class Transformation(Permutation):
    def __new__(cls, orientation, inverted, tup):
        return Permutation.__new__(cls, orientation, tup)
    def __init__(self, orientation, inverted, tup):
        assert inverted == 0 or inverted == 1
        self.inverted = inverted
        Permutation.__init__(self, orientation, tup)
    def __mul__(self, other):
        if type(other) is Transformation:
            return Transformation(self.orientation*other.orientation, 
                                  self.inverted ^ other.inverted, 
                                  (other[x] for x in self))
        return Permutation.__mul__(self, other)
    def __pow__(self, other):
        if self.inverted==0:
            return self*other
        if type(other) is tuple:
            return tuple(1-other[x] for x in self)
        if type(other) is list:
            return list(1-other[x] for x in self)
        assert 0
    def transform(self, other):
        if type(other) is tuple:
            return
        assert 0
    def __repr__(self):
        return Permutation.__repr__(self) + ['', '^-1'][self.inverted]
    def __eq__(self, other):
        return self.inverted == other.inverted \
            and Permutation.__eq__(self, other)
