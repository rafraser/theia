from generate_letter_set import main as generate_letter_set

# This file is very scuffed I'm sorry

CHARSET_FULL = "ABCDEFGHIJKLMNOPQRSTVUWXYZabcdefghijklmnopqrstuvwyxz1234567890!@#$%&"
FONT_ROOT = "C:\\Windows\\Fonts\\"


class dotdict(dict):
    """dot.notation access to dictionary attributes"""

    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


def make_font(
    fontfile,
    fontname,
    quality=6,
    extrude=0.05,
    decimate=0.08,
    charset="ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890",
):
    args = {
        "output": "output/" + fontname,
        "charset": charset,
        "font": FONT_ROOT + fontfile,
        "fontname": fontname,
        "quality": quality,
        "extrude": extrude,
        "decimate": decimate,
    }
    generate_letter_set(dotdict(args))


if __name__ == "__main__":
    # make_font("Roboto-Bold.ttf", "roboto")
    # make_font("futura medium bt.ttf", "futura")
    # make_font("coolvetica rg.ttf", "coolvetica")
    # make_font("GOTHIC.TTF", "centurygothic")
    # make_font("Montserrat-Medium", "montserrat")
    # make_font("HELR45W.ttf", "helvetica")
    # make_font("LemonMilk.otf", "lemonmilk")
    # make_font("PAPYRUS.TTF", "papyrus")
    # make_font("JOKERMAN.TTF", "jokerman")
    make_font("wingding.ttf", "wingdings", charset=CHARSET_FULL)
