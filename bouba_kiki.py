def bouba_kiki(word, language="en"):
    """
    Calculating word softness
    if n < 0: word is sharp
    if n > 0: word is soft
    if n == 0: word is neutral
    """
    l_t = {"ru": ('цйкшщзхфпржчт', 'бвгдлмн'),
           "en": ("bgmlwv", "dqrtpzxcksj")}
    hl, sl = l_t[language]
    hl_r, sl_r = 1, 1
    for letter in word:
        hl_r += 1 if letter in hl else 0
        sl_r += 1 if letter in sl else 0
    sl_r /= len(word)
    hl_r /= len(word)
    return sl_r - hl_r


def is_kiki(word, language="en"):
    return bouba_kiki(word, language=language) < 1


def is_bouba(word, language="en"):
    return bouba_kiki(word, language=language) > 1


if __name__ == "__main__":
    print(bouba_kiki("буба", language="ru"))
