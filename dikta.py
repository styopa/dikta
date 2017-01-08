import json
import logging

class Question:
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
        self.options = options
        self.__opts = frozenset(options)
        self.multiple = multiple
        self._keys = keys

    def __str__(self):
        return self.question

    def answer(self, response):
        resp_set = frozenset(response)
        diff_set = resp_set - self.__opts
        if diff_set:
            opts = list(self.options)
            opts.sort()
            opts_str = ', '.join(opts)

            diff = list(diff_set)
            diff.sort()
            diff_str = ', '.join(diff)

            if len(diff) == 1:
                noun = 'Answer'
            else:
                noun = 'Answers'

            raise IndexError('%s %s not among options: %s' % (noun, diff_str, opts_str))

        self.answers = response

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

class Quiz:
    def __init__(self, json_file):
        def object_factory(dct):
            if 'question' in dct:
                try:
                    multiple = dct['multiple']
                except(IndexError):
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
