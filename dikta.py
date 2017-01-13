import json
import logging
import re

class Question:
    __junction = re.compile(r'\b(and|or|maybe)\b', re.IGNORECASE)

    def __init__(self, question, multiple, options, keys):
        if type(question) is not str or not question:
            logging.error('question type is %s' % type(question))
            raise ValueError('Question must be a non-empty string')

        if type(options) is not dict or not options:
            logging.error('options type is %s' % type(options))
            raise ValueError('Answers must be a non-empty dict')

        if type(keys) is not list or not keys:
            logging.error('keys type is %s' % type(keys))
            raise ValueError('Keys must be a non-empty list')

        if not set(keys) <= set(options.keys()):
            raise IndexError('All keys must be among possible options')

        if len(keys) != 1 and not multiple:
            raise IndexError('Single-choice question requires a single key')

        self.question = question
        self.multiple = multiple
        self.keys = list( map(lambda k: k.upper(), keys) )
        self.correct = False # assume the worst
        self.options = {}
        for opt in options:
            self.options[str(opt).upper()] = options[opt]

    def __str__(self):
        return self.question

    def answer(self, text):
        no_junc = __class__.__junction.sub('', text).upper()
        filtered_response = frozenset(no_junc) & frozenset(self.options)
        logging.debug('Answered: %s' % ', '.join(list(filtered_response)))
        if filtered_response:
            n = len(filtered_response)
            if n > 1 and not self.multiple:
                raise IndexError('Only one answer expected, %i given' % n)
            else:
                self.answers = list(filtered_response)
                diff = filtered_response ^ frozenset(self.keys)
                self.correct = not bool(diff)
        else:
            raise IndexError( 'Nothing in "%s" matches options %s' %
                (text, ', '.join(self.options)) )

class Chapter:
    def __init__(self, title, questions):
        self._title = title
        self._questions = questions
        logging.debug('Loaded %i questions in chapter "%s"' %
            (len(questions), title))

    def __str__(self):
        return self._title

    def __iter__(self):
        for question in self._questions:
            yield question

    def __len__(self):
        return len(self._questions)

    def score(self):
        n = 0
        for question in self._questions:
            if question.correct:
                n = n + 1

        return n

class Quiz:
    def __init__(self, json_file, number = None, title = None):
        def object_factory(dct):
            if 'question' in dct:
                try:
                    multiple = dct['multiple']
                except IndexError:
                    multiple = False

                return Question(
                        dct['question'],
                        multiple,
                        dct['options'],
                        dct['keys'])

            return dct

        data = json.load(json_file, object_hook = object_factory)

        self._title = data['title']
        self._chapters = [];
        for ch in data['quiz']:
            self._chapters.append( Chapter(ch['chapter'], ch['questions']) )

        logging.debug('Loaded %i chapters in quiz "%s"' % (len(self._chapters), self))

    def __len__(self):
        return len(self._chapters)

    def __str__(self):
        return self._title

    def __iter__(self):
        for chapter in self._chapters:
            yield chapter
