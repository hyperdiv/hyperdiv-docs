def render_value(v):
    if isinstance(v, str):
        return repr(v)
    return str(v)


def render_value_list(vs):
    return ", ".join([render_value(v) for v in vs])
