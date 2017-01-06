import copy

(black, red, green, yellow, blue, magenta, cyan, white) = range(8)

class Text:
    def __init__(self, text, fg, bg, bold):
        self.text = text
        self.fg = fg
        self.bg = bg
        self.bold = bold

    def __str__(self):
        if self.fg is None:
            fg = ''
        else:
            if self.bold:
                bold = 1
            else:
                bold = 0

            fg = "\033[%i;%im" % (bold, 30 + self.fg)

        if self.bg is None:
            bg = ''
        else:
            bg = "\033[%im" % (40 + self.bg)

        if fg or bg:
            reset = "\033[0m"
        else:
            reset = ''

        return bg + fg + self.text + reset

class ColorText:
    def __init__(self, text = None):
        if text:
            self._texts = [Text(text, None, None, None)]
        else:
            self._texts = []

    def __str__(self):
        return ''.join( map(str, self._texts) )

    def fg(self, color):
        for text in self._texts:
            text.fg = color

        return self

    def bg(self, color):
        for text in self._texts:
            text.bg = color

        return self

    def bold(self, bold_):
        for text in self._texts:
            text.bold = bold_

        return self

    def __add__(self, other):
        result = copy.deepcopy(self)
        result._texts.extend(other._texts)
        return result
