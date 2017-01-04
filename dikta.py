import json

class Question:
    def __init__(self, question, multiple, answers, keys):
        if type(question) is not str or not question:
            raise ValueError('Question must be a non-empty string')

        if type(answers) is not dict or not answers:
            raise ValueError('Answers must be a non-empty dict')

        if type(keys) is not list or not keys:
            raise ValueError('Keys must be a non-empty list')

        if not set(keys) <= set(answers.keys()):
            raise IndexError('All keys must be among possible answers')

        if len(keys) != 1 and not multiple:
            raise IndexError('Single-choice question requires a single key')

        self._question = question
        self._answers = answers
        self._multiple = multiple
        self._keys = keys

    def __str__(self):
        return self._question

class Chapter:
    def __init__(self, title, questions):
        self._title = title
        self._questions = questions

    def __str__(self):
        return self._title

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
                        dct['answers'],
                        dct['keys'])

            return dct

        data = json.load(json_file, object_hook = object_factory)

        self._title = data['title']
        self._chapters = [];
        for ch in data['quiz']:
            self._chapters.append( Chapter(ch['chapter'], ch['questions']) )

    def __len__(self):
        return len(self._chapters)

    def __str__(self):
        return self._title
