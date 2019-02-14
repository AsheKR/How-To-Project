from rest_framework import status
from rest_framework.exceptions import APIException, _get_error_details
from rest_framework_friendly_errors.mixins import FriendlyErrorMessagesMixin


class NotRequireSerializerFriendlyErrorMessagesMixin(FriendlyErrorMessagesMixin):
    def register_error(self, error_message, field_name=None,
                       error_key=None, error_code=None):
        if field_name is None:
            if error_code is None:
                raise ValueError('For non field error you must provide '
                                 'an error code')
            error = {'code': error_code, 'message': error_message,
                     'field': None}
        else:
            if error_key is None and error_code is None:
                raise ValueError('You have to provide either error key'
                                 ' or error code')
            if error_code is not None:
                error_code = error_code
            error = {'code': error_code, 'field': field_name,
                     'message': error_message}
        key = '%s_%s_%s' % (error_message, error_code, field_name)
        self.registered_errors[key] = error
        return error

    def register_error_400(self, error_message, field_name=None,
                       error_key=None, error_code=None):
        key = self.register_error(error_message, field_name, error_key, error_code)
        raise RestValidationError(key)

    def register_error_403(self, error_message, field_name=None,
                           error_key=None, error_code=None):
        key = self.register_error(error_message, field_name, error_key, error_code)
        raise PermissionDenied(key)


class RestValidationError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Invalid input.'
    default_code = 'invalid'

    def __init__(self, detail=None, code=None):
        if detail is None:
            detail = self.default_detail
        if code is None:
            code = self.default_code

        # For validation failures, we may collect many errors together,
        # so the details should always be coerced to a list if not already.
        if not isinstance(detail, dict) and not isinstance(detail, list):
            detail = [detail]

        self.detail = _get_error_details(detail, code)


class PermissionDenied(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 'Invalid input.'
    default_code = 'invalid'

    def __init__(self, detail=None, code=None):
        if detail is None:
            detail = self.default_detail
        if code is None:
            code = self.default_code

        # For validation failures, we may collect many errors together,
        # so the details should always be coerced to a list if not already.
        if not isinstance(detail, dict) and not isinstance(detail, list):
            detail = [detail]

        self.detail = _get_error_details(detail, code)

