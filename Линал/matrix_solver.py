class Item(float):
    round = 8

    def __bool__(self):
        if round(self, self.round):
            return True
        return False

    def __repr__(self):
        out = round(self, self.round)
        if out == 0:
            out = 0.
        return str(out)


class Row(list):

    def __init__(self, lst):
        super().__init__([Item(x) for x in lst])

    def copy(self):
        return Row(super().copy())

    def __repr__(self) -> str:
        return '\t'.join(map(str, self))


class Matrix(list):
    """
    Matrix M * N

    matrix[i, j] <=> row i, column j
    """

    def __init__(self, mat):
        self.m, self.n = len(mat), len(mat[0])
        mat = [Row(_row) for _row in mat]
        super().__init__(mat)

    def __getitem__(self, item):
        if isinstance(item, tuple):
            return super().__getitem__(item[0])[item[1]]
        return super().__getitem__(item)

    def __setitem__(self, item, value):
        if isinstance(item, tuple):
            self[item[0]][item[1]] = value
            return
        super().__setitem__(item, value)

    def copy(self):
        return Matrix([row.copy() for row in self])

    def e1(self, i, j, k):
        self[i] = Row([
            Item(self[i, n] + self[j, n] * k)
            for n in range(self.n)
        ])

    def e2(self, i, j):
        self[i], self[j] = self[j], self[i]

    def e3(self, i, k):
        self[i] = Row([Item(n / k) for n in self[i]])

    def column(self, j, start=0):
        return [self[m, j] for m in range(start, self.m)]

    def transpose(self):
        mat = self.copy()
        return Matrix([[x for x in mat.column(i)] for i in range(mat.n)])

    def trace(self):
        s = 0
        for i in range(self.n):
            s += self[i, i]
        return s

    def reduce(self):
        for i in range(self.m):
            for j in range(self.n):
                if any(self.column(j, i)):
                    break
            else:
                return

            for current_i in range(i, self.n):
                if self[current_i, j]:
                    break
            else:
                continue
            self.e2(i, current_i)
            for m in range(self.m):
                if m != i:
                    self.e1(m, i, -self[m, j] / self[i, j])
            self.e3(i, self[i, j])

    def __add__(self, other):
        assert self.n == other.n and self.m == other.m
        return Matrix([[x + y for x, y in zip(self[i], other[i])] for i in range(self.m)])

    def __sub__(self, other):
        assert self.n == other.n and self.m == other.m
        return Matrix([[x - y for x, y in zip(self[i], other[i])] for i in range(self.m)])

    def __rmul__(self, other):
        return self.__mul__(other)

    def __mul__(self, other):
        if isinstance(other, Matrix):
            assert self.n == other.m
            return Matrix([
                [sum([(x * y) for x, y in zip(self[i], other.column(j))]) for j in range(other.n)]
                for i in range(self.m)
            ])
        mat = self.copy()
        for i in range(self.m):
            mat.e3(i, 1 / other)
        return mat

    def __invert__(self):
        return self.transpose()

    def __pow__(self, power, modulo=None):
        mat = self.copy()
        original = self.copy()
        for _ in range(1, power):
            mat *= original
        return mat

    def __repr__(self):
        return '\n'.join(map(str, self))


def tr(mat: Matrix):
    return mat.trace()


def e1(i, j, k):
    matrix.e1(i - 1, j - 1, k)
    return matrix


print()

A = Matrix([
    [1, -3, 2],
    [-1, 1, 0],
    [1, 0, -1]
    [1, 2, 5]
]

b = Matrix([[3], [3], [1], [13]])

print(())

