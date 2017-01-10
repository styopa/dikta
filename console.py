import dikta
import color
import logging

def header1(text):
    print( color.Text(text).bg(color.magenta).fg(color.white).bold(True) )

def header2(text):
    print( color.Text(text).fg(color.blue).bold(True) )

class Console:
    def __init__(self, quiz):
        self._quiz = quiz

    def run_quiz(self):
        def answer(question):
            print(question)

            for idx in sorted(question.options.keys()):
                print("  %s. %s" % (idx, question.options[idx]))

            if question.multiple:
                opt = 'multiple'
            else:
                opt = 'one'

            while True:
                try:
                    response = input("Choose %s: " % opt)
                    question.answer(response)
                    break
                except IndexError as err:
                    print( color.Text(err).fg(color.red).bold(True) )

        header1(self._quiz)

        for chapter in self._quiz:
            header2(chapter)

            for question in chapter:
                answer(question)
                print()

    def show_mistakes(self):
        def print_mistakes(question):
            print(question)
            logging.debug('Keys: %s' % ', '.join(question.keys))

            for idx in sorted(question.options.keys()):
                correct = idx in question.keys
                selected = idx in question.answers

                if not correct and not selected:
                    continue

                if correct:
                    color_ = color.green
                else:
                    color_ = color.red

                if selected:
                    marker = ">>"
                else:
                    marker = "  "

                opt = "%s%s. %s" % (marker, idx, question.options[idx])
                print( color.Text(opt).fg(color_) )

        printed_header = False
        for chapter in self._quiz:
            printed_chapter = False
            for question in chapter:
                if not question.correct:

                    if not printed_header:
                        printed_header = True
                        header1('Incorrect answers')

                    if not printed_chapter:
                        header2(chapter)
                        printed_chapter = True

                    print_mistakes(question)
                    print()
