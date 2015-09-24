__author__ = 'Ansis Rosmanis'

# We store a partition as a non-increasing zero-free list.
# This is a bijective representation of partitions (another one being using cycle types).
class Partition:

    # We can specify a partition either as a list of parts (not necessarily sorted) or its cycle type (see below)
    def __init__(self, parts=None, cycleType=None):
        self.parts = []
        if parts:
            self.parts = [p for p in parts if p]    # remove zeros
            self.parts.sort(reverse=True)
        elif cycleType:
            for i in range(len(cycleType),0,-1):
                if cycleType[i-1]:
                    self.parts += [i]*cycleType[i-1]

    def __eq__(self, other):
        return self.parts == other.parts    # note: consider using __dict__

    # The default way to print a partition
    def __str__(self):
        return str(self.parts)

    # The integer that is partitioned
    def number(self):
        return sum(self.parts)

    # Given a partition, cycleType is the list whose p-th entry (in 1-indexing)
    # tells how many times the part p appears in the partition. Note that trailing zeros have no influence.
    def cycleType(self):
        if self.parts:
            res = [0] * self.parts[0]
            for p in self.parts:
                res[p-1] += 1
            return res
        else:
            return []

    # The cycle type of length equal to the partitioned number
    def cycleTypeFull(self):
        return self.cycleType() + [0] * (self.number()-len(self.cycleType()))

    # Lexicographical order is a total ordering of all partitions of a given number.
    def precedes(self, other):
        if self.number() != other.number():
            raise ValueError('Comparing partitions of different numbers.')
        if self == other:
            return False
        for s,o in zip(self.parts, other.parts):
            if s > o:
                return True
            elif s < o:
                return False

    # Dominance is a partial ordering of all partitions of a given number.
    def dominates(self, other):
        if self.number() != other.number():
            raise ValueError('Comparing partitions of different numbers.')
        if self == other:
            return False
        difference = 0
        for s,o in zip(self.parts, other.parts):
            difference += s-o
            if difference < 0:
                return False
        return True

    # The next partition is the lexicographical order
    def next(self):
        cycleType = self.cycleType()
        if len(cycleType)<=1:   # We include < for the empty partition []
            return None
        i = 1
        while not cycleType[i]:
            i+=1
        cycleType[i]-=1     # We have one less part i+1 and ...
        cycleType[i-1]+=1   # ... we have one more part i.
        cycleType[0]+=1     # Add the remaining loose part 1.

        # At this point cycleType corresponds o a valid partition of the same number, but it may not be the right one.
        # We need to group together in parts i as many loose 1s as we can.
        ones = cycleType[0]
        cycleType[0] = 0
        cycleType[i-1] += ones//i
        if ones%i:
            cycleType[ones%i-1] = 1
        return Partition(cycleType=cycleType)

    # The previous partition is the lexicographical oredr
    def previous(self):
        if len(self.parts) <= 1:
            return None
        cycleType = self.cycleTypeFull()    # we use cycleTypeFull, as the length of cycleType might increase
        if cycleType[0] >= 2: # if there are two 1s, combine them
            cycleType[0]-=2
            cycleType[1]+=1
        else:
            i = 1
            while not cycleType[i]:
                i+=1
            if cycleType[0]==0 and cycleType[i]==1:
                cycleType[0] = i+1
                cycleType[i] = 0
                while not cycleType[i]:
                    i+=1
            cycleType[i+1] += 1
            cycleType[0] += (i+1)*(cycleType[i]-1) - 1
            cycleType[i] = 0    # note that i != 0
        return Partition(cycleType=cycleType)

    def transpose(self):
        cycleType = self.cycleType()
        res = []
        while cycleType:
            res.append(sum(cycleType))
            cycleType.pop(0)
        return Partition(res)

    # Ferrers diagram of the partition
    def Ferrers(self):
        return '\n'.join(['* ' * p for p in self.parts])