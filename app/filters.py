def middle(value):
    if len(value) % 2 == 1:
        len_value = (len(value) - 1) / 2
        value = value[int(len_value)]
    return value
