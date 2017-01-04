class Question:
    def __init__(self, question, answers, multiple, keys):
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
