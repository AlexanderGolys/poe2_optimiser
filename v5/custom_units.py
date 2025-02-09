import numpy as np


class Vector:
    def __init__(self, lst):
        self.value = lst
        if isinstance(lst, Vector):
            self.value = lst.value

    def __str__(self):
        return f'{self.value}'

    def __getitem__(self, i):
        return self.value[i]

    def __setitem__(self, i, value):
        self.value[i] = value

    def __len__(self):
        return len(self.value)

    def __iter__(self):
        return iter(self.value)

    def __contains__(self, item):
        return item in self.value

    def __hash__(self):
        return hash(self.value)

    def __add__(self, other):
        return self.__class__([a + b for a, b in zip(self.value, other.value)])

    def __sub__(self, other):
        return self.__class__([a - b for a, b in zip(self.value, other.value)])

    def __mul__(self, other):
        if isinstance(other, (Vector, np.ndarray, list, tuple)):
            return self.__class__([a * b for a, b in zip(self.value, other.value)])
        return self.__class__([a * other for a in self.value])

    def __truediv__(self, other):
        return self.__class__([a / other for a in self.value])

    def __eq__(self, other):
        return all(a == b for a, b in zip(self.value, other.value))

    def __neg__(self):
        return self.__class__([-a for a in self.value])

    def __repr__(self):
        return str(self)

    def __round__(self, n=None):
        return self.__class__([round(a, n) for a in self.value])

    def __format__(self, format_spec):
        return '(' + ', '.join([a.__format__(format_spec) for a in self.value]) + ')'

    def mean(self):
        return sum(self.value, self.value[0]*0) * (1.0/len(self.value))

    def lucky_mean(self):
        if len(self.value) != 2:
            raise ValueError('Lucky mean can only be calculated for 2 values')
        return self.value[0]/3 + 2*self.value[1]/3

    def sum(self):
        return sum(self.value, self.value[0]*0)


class Percent:
    def __init__(self, value):
        self.value = value
        if isinstance(value, Percent):
            self.value = value.value

    def __str__(self):
        return f'{self.value * 100}%'

    def __mul__(self, c):
        return self.__class__(self.value * c)

    def __eq__(self, other):
        if isinstance(other, (int, float)):
            return self.value == other
        return self.value == other.value

    def __hash__(self):
        return hash(self.value)

    def __neg__(self):
        return self.__class__(-self.value)

    def __add__(self, other):
        if isinstance(other, (int, float)):
            return self.__class__(self.value + other)
        return self.__class__(self.value + other.value)

    def __sub__(self, other):
        return self.__class__(self.value - other.value)

    def __round__(self, n=None):
        return self.__class__(round(self.value, n))

    def __format__(self, format_spec):
        if format_spec != '' and format_spec is not None:
            return f'{self.value * 100:{format_spec}}%'
        return f'{round(self.value * 100)}%'


def dict_vector_wrapper(*keys, basetype=None):
    basewrap = basetype or (lambda x: x)

    def dec(cls):

        class Wrapped(cls):
            KEYS = list(keys)

            def __init__(self, *args, **kwargs):
                if len(args) == 0:
                    z = list(kwargs.values())[0]*0
                    args = [[z] * len(self.KEYS)]
                super().__init__(list(map(basewrap, args[0])) + [basewrap(0)] * (len(self.KEYS) - len(args[0])))
                for key, value in kwargs.items():
                    if key.capitalize() in self.KEYS:
                        self[key] = basewrap(value)

            def dict(self):
                return {key: value for key, value in zip(self.KEYS, self)}

            def __getitem__(self, key):
                if isinstance(key, str):
                    return self.dict()[key]
                return super().__getitem__(key)

            def __setitem__(self, key, value):
                if key in self.KEYS:
                    self.value[self.KEYS.index(key.capitalize())] = value
                else:
                    super().__setitem__(key, value)

            def __add__(self, other):
                return self.__class__([a + b for a, b in zip(self.value, other.value)])



        return Wrapped
    return dec


@dict_vector_wrapper('Lightning', 'Fire', 'Cold', 'Chaos', basetype=Percent)
class ResistanceVector(Vector):
    def __str__(self):
        return f'Lightning: {self.value[0]}, Fire: {self.value[1]}, Cold: {self.value[2]}, Chaos: {self.value[3]}'


@dict_vector_wrapper('Physical', 'Lightning', 'Fire', 'Cold', 'Chaos')
class DamageTypeVector(Vector):
    def __str__(self):
        return f'Physical: {self.value[0]}, Lightning: {self.value[1]}, Fire: {self.value[2]}, Cold: {self.value[3]}, Chaos: {self.value[4]}'


def maximum(a, b):
    if isinstance(a, Vector):
        return a.__class__([maximum(x, y) for x, y in zip(a, b)])
    return max(a, b)


def minimum(a, b):
    if isinstance(a, Vector):
        return a.__class__([minimum(x, y) for x, y in zip(a, b)])
    if isinstance(a, Percent):
        return Percent(min(a.value, b.value))
    return min(a, b)


class PerAilmentThreshold(Percent):
    def __str__(self):
        return f'{self.value * 100}% per 4% of enemy Ailment Threshold'

    def __format__(self, format_spec):
        if format_spec != '' and format_spec is not None:
            return f'{self.value * 100:{format_spec}}% per 4% of enemy Ailment Threshold'
        return f'{round(self.value * 100)}% per 4% of enemy Ailment Threshold'
