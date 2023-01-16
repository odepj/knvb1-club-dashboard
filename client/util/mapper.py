def instantiateClassFromList(cls, List):
    return list(map(lambda x: cls(**x), List))


def flatten(S):
    if not S:
        return S
    if isinstance(S[0], list):
        return flatten(S[0]) + flatten(S[1:])
    return S[:1] + flatten(S[1:])
