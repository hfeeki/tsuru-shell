"""
Interpolation of strings for color printing.

Licensed under the MIT License (see LICENSE)

For more color printing suggestions, see e.g. 

    http://stackoverflow.com/questions/287871    
    https://github.com/brianmhunt/icolor.git
"""
import string

"""This is the number that goes in the insignificant decimal position of the map 
e.g. BLUE => x4, where x is 3 for foreground and 4 for background."""
_COLOR_MAP = dict(
        BLACK   = 0,
        RED     = 1,
        GREEN   = 2,
        YELLOW  = 3,
        BLUE    = 4,
        MAGENTA = 5,
        CYAN    = 6,
        WHITE   = 7,
        DEFAULT = 9,
        )

"A map of the name of an ANSI escape sequence to its number"
ANSI_CODE_MAP = dict(
        RESET = 0,
        BOLD = 1,
        INVERSE = 7,
        STRIKE = 9,
        UNBOLD = 22,
        )

for _color, _code in _COLOR_MAP.items():
    ANSI_CODE_MAP[_color] = 30 + _code # e.g. RED => 31
    ANSI_CODE_MAP["x" + _color] = 40 + _code # e.g. xRED = 41

"A map of the strings to the actual escape sequences"
ANSI_STRING_MAP = { name+";": "\033[%dm" % code 
                   for name, code in ANSI_CODE_MAP.items()}

class ColorTemplate(string.Template):
    """A string.Template descendent that maps color codes to ANSI escapes.

    A string template where the delimiter is '#' and the idpattern is 
    the all-caps name of an ANSI escape sequence followed by a semicolon
    e.g. #RED;, #RESET;, #BOLD;, etc..
    """
    delimiter = '#'

    """All of, and only, the ANSI uppercase escape sequence names e.g. 
    (RESET;|xDEFAULT;|DEFAULT;|...)"""
    idpattern = r'(%s);' % "|".join(c for c in ANSI_CODE_MAP.keys())

def cprint(msg, reset=True, template=ColorTemplate):
    """Same as cformat but prints a string.
    """
    print(cformat(msg, reset, template))

def cformat(msg, reset=True, template=ColorTemplate):
    """
    Transform msg so that colors e.g. #RED;, #BLUE;, etc are mapped to the
    corresponding ANSI escape codes. e.g.

    >>> cformat("This is #RED;a red string.")
    'This is \\x1b[31ma red string.\\x1b[0m'

    >>> cformat("This is #BLUE;a blue string.", reset=False)
    'This is \\x1b[34ma blue string.'

    >>> cformat("This is #xBLUE;a blue background.", reset=False)
    'This is \\x1b[44ma blue background.'

    The returned string is escaped unless reset=False
    """
    ct = ColorTemplate(msg)
    m = ct.safe_substitute(ANSI_STRING_MAP)

    if reset:
        m += ANSI_STRING_MAP['RESET;']

    return m

if __name__ == "__main__":
    cprint("""
    Color test:
        Red: #RED; red on black#RESET; #RED;...#RESET;
        Red bg: #xWHITE;red on white#RESET;
        Bold: #BOLD;Bolded.#RESET;
        Not colored: #red; #Red; ##RED;
    """)

    import doctest
    doctest.testmod()
    

