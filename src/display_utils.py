def as_percent(x: float, precision: int = 1, include_percent_sign: bool = True) -> str:
    out = str(round((x-1)*100, precision))

    if x > 1:
        out = '+' + out

    if include_percent_sign:
        out += '%'

    return out
