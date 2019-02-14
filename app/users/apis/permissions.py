from rest_framework.permissions import BasePermission

from base.base_error_mixins import NotRequireSerializerFriendlyErrorMessagesMixin


class MustNotAuthenticated(NotRequireSerializerFriendlyErrorMessagesMixin, BasePermission):

    def has_permission(self, request, view):
        if bool(request.user and
                request.user.is_authenticated):
            self.register_error_403(error_message='로그인된 유저로 실행할 수 없습니다.',
                                    error_code='3022',
                                    field_name='login_failed')
        return True
