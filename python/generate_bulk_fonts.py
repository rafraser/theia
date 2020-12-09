from generate_letter_set import main as generate_letter_set


class dotdict(dict):
    """dot.notation access to dictionary attributes"""

    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


args = {
    "output": "output/test",
    "charset": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "font": "C:\\Windows\\Fonts\\Roboto-Bold.ttf"
    "fontname": "roboto",
    "quality": 6,
    "extrude": 0.05,
    "decimate": 0.08
}
generate_letter_set(dotdict(args))