"""Три алгоритми повертають індекс першого збігу або -1."""


def boyer_moore(text, pattern):
    """Правило поганого символу; збіг перевіряємо справа наліво."""
    m = len(pattern)
    last = {c: i for i, c in enumerate(pattern)}
    offset = 0
    while offset <= len(text) - m:
        j = m - 1
        while j >= 0 and pattern[j] == text[offset+j]:
            j -= 1
        if j < 0:
            return offset
        offset += max(1, j - last.get(text[offset+j], -1))
    return -1


def kmp(text, pattern):
    if not pattern:
        return 0
    prefix = [0] * len(pattern)
    j = 0
    for i in range(1, len(pattern)):
        while j and pattern[j] != pattern[i]:
            j = prefix[j-1]
        if pattern[j] == pattern[i]:
            j += 1
        prefix[i] = j
    j = 0
    for i, c in enumerate(text):
        while j and pattern[j] != c:
            j = prefix[j-1]
        if pattern[j] == c:
            j += 1
        if j == len(pattern):
            return i - j + 1
    return -1


def rabin_karp(text, pattern):
    m, n = len(pattern), len(text)
    if not m:
        return 0
    if m > n:
        return -1
    base, mod = 257, 1_000_000_007
    high = pow(base, m-1, mod)
    target = window = 0
    for a, b in zip(pattern, text):
        target = (target*base + ord(a)) % mod
        window = (window*base + ord(b)) % mod
    for i in range(n-m+1):
        if window == target and text.startswith(pattern, i):
            return i
        if i+m < n:
            window = ((window - ord(text[i])*high)*base + ord(text[i+m])) % mod
    return -1
