import dikta
import color

class Console:
    def __init__(self, quiz):
        self._quiz = quiz

    def run_quiz(self):
        def answer(question):
            print(question)

            for idx in sorted(question.options.keys()):
                print("  %s. %s" % (idx.upper(), question.options[idx]))

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

        print( color.Text(self._quiz).bg(color.magenta).fg(color.white).bold(True) )

        for chapter in self._quiz:
            print( color.Text(chapter).fg(color.blue).bold(True) )

            for question in chapter:
                answer(question)
                print()

    def show_results(self):
        pass
