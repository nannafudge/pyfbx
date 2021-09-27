class FBXException(BaseException):
    def __init__(self, msg="", cause: BaseException = None):
        self.msg = msg
        self.__cause__ = cause

        super().__init__(msg)


class FBXSerializationException(FBXException):
    def __init__(self, msg="", data=None, cause: BaseException = None):
        self.data = data
        super().__init__(msg, cause)


class FBXValidationException(FBXException):
    def __init__(self, msg="", data: bytes = b'', cause: BaseException = None):
        self.data = data
        super().__init__(msg, cause)


class FBXTypeRegistrationException(FBXException):
    def __init__(self, msg="", type_: type = None, cause: BaseException = None):
        self.type_ = type_
        super().__init__(msg, cause)
