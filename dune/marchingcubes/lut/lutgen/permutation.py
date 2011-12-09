class Permutation(tuple):
    def __new__ (cls, o, t):
        return tuple.__new__(cls, t)
    def __init__(self, o, t):
        # Indicates the orientation, 1: normal -1: mirrored
        self.orientation = o
        assert o == -1 or o == 1
        tuple.__init__(self, t)
    def __mul__ (self, other):
        if type(other) is Permutation:
            return Permutation(self.orientation*other.orientation, (other[x] for x in self))
        if type(other) is tuple:
            return tuple(other[x] for x in self)
        if type(other) is list:
            return list(other[x] for x in self)
        assert 0
    def __pow__(self, other):
        assert type(other) is int
        if other == 1:
            return self
        else:
            return self*(self**(other-1))
    def map(self, other):
        return type(other)(self[x] for x in other)
    def __repr__ (self):
        return ['?','+','-'][self.orientation] + tuple.__repr__(self)

