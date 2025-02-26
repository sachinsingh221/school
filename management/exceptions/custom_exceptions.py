from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException
from school_api.enums import ResponseStatus
 
 
def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
    if response is not None:
        response.status_code = 200
        data = response.data
        response.data = {}
        errors = []
        for field, value in data.items():
            errors.append("{} : {}".format(field, "".join(value)))
        response.data['status'] = getattr(exc, 'status', ResponseStatus.ERROR)
        response.data['errors'] = errors
        return response



class ClientException(APIException):
    default_detail = "something went wrong"
    default_code = "error"
    status = ResponseStatus.ERROR
    fields = {}

    def __init__(self, detail=None, code=None, status=None):
        if detail is None:
            detail = self.default_detail
        if code is None:
            code = self.default_code
        if status is not None:
            self.status = status
        super().__init__(detail, code)
