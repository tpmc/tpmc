class Permutation(tuple):
    def __new__ (cls, orientation, tup):
        return tuple.__new__(cls, tup)
    def __init__(self, orientation, tup):
        # Indicates the orientation, 1: normal -1: mirrored
        self.orientation = orientation
        assert orientation == -1 or orientation == 1
        tuple.__init__(self, tup)
    def __mul__ (self, other):
        if type(other) is Permutation:
            return Permutation(self.orientation*other.orientation, 
                               (other[x] for x in self))
        return type(other)(other[x] for x in self)
    def __pow__(self, other):
        assert type(other) is int
        if other == 1:
            return self
        else:
            return self*(self**(other-1))
    def map(self, other):
        return type(other)(self[x] for x in other)
    def __repr__ (self):
        return ['?', '+', '-'][self.orientation] + tuple.__repr__(self)

