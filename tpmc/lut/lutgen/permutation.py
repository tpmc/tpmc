class Permutation(tuple):
    def __new__ (cls, orientation, tup):
        obj = tuple.__new__(cls, tup)
        # Indicates the orientation, 1: normal -1: mirrored
        obj.orientation = orientation
        assert orientation == -1 or orientation == 1
        return obj
    # def __init__(self, orientation, tup):
    #     # tuple.__init__(self, tup)
    def __mul__ (self, other):
        if type(other) is Permutation:
            return Permutation(self.orientation*other.orientation, 
                               (other[x] for x in self))
        return type(other)(other[x] for x in self)
    def toBaseCase(self, other):
        return type(other)(other[x] for x in self)
    def fromBaseCase(self, other):
        inverse = [b for (a,b) in sorted([(self[i],i) for i in range(len(self))])]
        return type(other)(other[x] for x in inverse)
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
    def __hash__(self):
        return tuple.__hash__(self) ^ self.orientation.__hash__()
