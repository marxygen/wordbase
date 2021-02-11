class WordbaseException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class IncorrectExecutionException(WordbaseException):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class WordNotFoundException(WordbaseException):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class CannotOpenDictionaryException(WordbaseException):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class CannotSaveDictionaryException(WordbaseException):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class EmptyDictionaryException(WordbaseException):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class CannotCompleteSearchException(WordbaseException):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
