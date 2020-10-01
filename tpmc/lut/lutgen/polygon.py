"""
contains class for polygon representation and for computation of a
list of polygons
"""

class PolygonList(object):
    """
    represents a list of polygons. can merge itself and check if
    another list is equal
    """
    def __init__(self, polygons):
        self.polygons = polygons
    def merge(self):
        """ merges the list of polygons as far as possible """
        def remove_inner_nodes(vlist):
            """ 
            removes inner nodes from a list, 
            eg [1, (1,2) ,2] --> [1, 2]
            """
            i = 0
            while i < len(vlist):
                if (type(vlist[i]) is tuple 
                    and vlist[(i-1) % len(vlist)] in vlist[i] 
                    and vlist[(i+1) % len(vlist)] in vlist[i]):
                    vlist.pop(i)
                else:
                    i += 1
        changed = True
        # simply loop through the list and check if anything can be merged
        # until nothing changes anymore
        while changed:
            changed = False
            for i in range(len(self.polygons)) :
                for j in range(i+1, len(self.polygons)) :
                    # i connected to j
                    conn = self.polygons[i].connected(self.polygons[j])
                    # i connected to reverse of j
                    rconn = \
                        self.polygons[i].connected(self.polygons[j].reverse())
                    if conn >= 0 or rconn >= 0:
                        vlist = list(self.polygons[i].merge(self.polygons[j]))
                        remove_inner_nodes(vlist)
                        self.polygons.append(Polygon(vlist))
                        self.polygons.pop(j)
                        self.polygons.pop(i)
                        changed = True
                        break
                if changed:
                    break
    def __ne__(self, other):
        return not __eq__(self,other)
    def __eq__(self, other):
        """ 
        returns true if first and second list form the same set of 
        polygons 
        """
        self.merge()
        other.merge()
        first = [set(x) for x in self.polygons]
        second = [set(x) for x in other.polygons]
        if (len(first) == len(second) 
            and sum(1 for x in first if x in second) == len(first)):
            return True
        else:
            return False
    def __repr__(self):
        return str(self.polygons)


class Polygon(list):
    """
    represents a sequence of vertices forming a polygon. All vertices
    are connected to their neighbours, the last and the first vertex
    are connected.
    """
    def __new__(cls, vertices):
        return list.__new__(cls, vertices)
    def reverse(self):
        """ returns a new Polygon in reversed order """
        return Polygon(reversed(self))
    def __lshift__(self, amount):
        return Polygon(self[amount:]+self[:amount])
    def __rshift__(self, amount):
        return self.__lshift__(-amount)
    def connected(self, other):
        """ returns index of the first vertex of a connection to other """
        start = -1
        ls = len(self)
        lo = len(other)
        for (i, v) in enumerate(self) :
            if (v in other 
                and (self[(i+1) % ls] == other[(other.index(v)+1) % lo] 
                     or self[(i-1) % ls] == other[(other.index(v)-1) % lo])):
                start = i
                break
        if start >= 0:
            if start == 0 and not list.__eq__(self, other):
                while self[start-1] in other:
                    start = (start - 1) % len(self)
            return start
        else:
            return -1
    def merge(self, other):
        """ 
        returns a merged version of this polygon and other at the 
        connection returned by self.connected(other) (or reversed)
        """
        # find start of the merging position
        temp_other = Polygon(other)
        start = self.connected(temp_other)
        # if no connection was found
        if start < 0:
            temp_other = temp_other.reverse()
            start = self.connected(temp_other)
        # are the polygons connected?
        if start >= 0:
            # move start to the end of the list
            merged = list(self << start+1)
            start_in_other = temp_other.index(merged[-1])
            # remove inner nodes
            inner_count = 0
            while len(merged)>1 and merged[1] in other:                
                merged.pop(0)
                inner_count += 1
            # get index of one past end of connection in other
            other_index = (start_in_other+inner_count+2) % len(temp_other)
            # insert nodes from other to front of merged in reversed order
            while other_index != start_in_other:
                merged.insert(0, temp_other[other_index])
                other_index = (other_index + 1) % len(temp_other)
            return Polygon(merged)
        else:
            raise RuntimeError('polygons are not connected')
    def __eq__(self, other):        
        if len(self)!=len(other):
            return False
        srev = self.reverse()
        for offset in range(len(self)):
            if (list.__eq__(self >> offset, other) 
                or list.__eq__(srev >> offset, other)):
                return False
        return True
    def __repr__(self):
        return list.__repr__(self)
