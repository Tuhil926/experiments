class Vector:
    def __init__(self, *components):
        if isinstance(components[0], list) or isinstance(components[0], tuple):
            self.components = list(components[0])
        else:
            self.components = list(components)
        self.dimension = len(self.components)

    def __add__(self, other):
        v1 = self.components
        v2 = other.components
        if self.dimension >= other.dimension:
            for i in range(other.dimension):
                v1[i] += v2[i]
            return Vector(v1)
        else:
            for i in range(self.dimension):
                v2[i] += v1[i]
            return Vector(v2)

    def __sub__(self, other):
        v1 = self.components
        v2 = other.components
        if self.dimension >= other.dimension:
            for i in range(other.dimension):
                v1[i] -= v2[i]
            return Vector(v1)
        else:
            for i in range(self.dimension):
                v2[i] = v1[i] - v2[i]
            for j in range(self.dimension, other.dimension):
                v2[j] *= -1
            return Vector(v2)

    def __mul__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            v = self.components
            for i in range(self.dimension):
                v[i] *= other
            return Vector(v)

        elif isinstance(other, Vector):
            v1 = self.components
            v2 = other.components
            if self.dimension >= other.dimension:
                sum = 0
                for i in range(other.dimension):
                    sum += v1[i] * v2[i]
                return sum
            else:
                sum = 0
                for i in range(self.dimension):
                    sum += v1[i] * v2[i]
                return sum

    def __rmul__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            v = self.components
            for i in range(self.dimension):
                v[i] *= other
            return Vector(v)

    def __mod__(self, other):
        if isinstance(other, Vector) and self.dimension <=3 and other.dimension <=3:
            res = [self[1]*other[2] - self[2]*other[1], self[2]*other[0] - self[0]*other[2], self[0]*other[1] - self[1]*other[0]]
            return Vector(res)
        else:
            raise TypeError("For cross product, two vectors of dimension less than 3 are required")

    def __getitem__(self, item):
        try:
            return self.components[item]
        except IndexError:
            return 0

    def __str__(self):
        return str(self.components)

    def __truediv__(self, other):
        return self*(1/other)

    def mag(self):
        sum = 0
        for component in self.components:
            sum += component**2
        return sum ** 0.5

    def unit(self):
        return Vector(((1/self.mag())*self).components)


vector1 = Vector(1, 1, 1)
vector2 = Vector(2, 2, 1)

print(vector2.unit()*vector1.unit())