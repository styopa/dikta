import sys

import dikta

class Console:
    def __init__(self, quiz):
        self._quiz = quiz

    def run_quiz(self):
        def color_print(msg, fg = None, bg = None, bold = False):
            if fg is None:
                fg_esc = ''
            else:
                if bold:
                    bold_esc = 1
                else:
                    bold_esc = 0

                fg_esc = "\033[%i;%im" % (bold_esc, 30 + fg)

            if bg is None:
                bg_esc = ''
            else:
                bg_esc = "\033[" + str(40 + bg) + "m"

            reset = "\033[0m"

            print(bg_esc + fg_esc + msg + reset)

        (BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE) = range(8)

        color_print(str(self._quiz), fg = MAGENTA, bold = True)

        for chapter in self._quiz:
            color_print(str(chapter), fg = BLUE, bold = True)

            for question in chapter:
                print(question)

                for idx in sorted(question.answers.keys()):
                    print("  %s. %s" % (idx.upper(), question.answers[idx]))

                print()
