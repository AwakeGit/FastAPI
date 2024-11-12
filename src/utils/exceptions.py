class FileTooLargeError(Exception):
    def __init__(self, message="Файл слишком большой"):
        self.message = message
        super().__init__(self.message)


class DocumentNotFoundError(Exception):
    def __init__(self, message="Документ не найден"):
        self.message = message
        super().__init__(self.message)


class DocumentAlreadyExistsError(Exception):
    def __init__(self, message="Документ уже существует"):
        self.message = message
        super().__init__(self.message)


class DocumentNotSavedError(Exception):
    def __init__(self, message="Документ не сохранен"):
        self.message = message
        super().__init__(self.message)
