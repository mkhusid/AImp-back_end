from django.core.exceptions import ValidationError
from django.core.exceptions import SuspiciousOperation
from django.core.validators import EmailValidator
from django.http import HttpResponseBadRequest, Http404
from django.utils.encoding import force_text
from django.utils.translation import ugettext as _


class EmailException(SuspiciousOperation):
    pass


class PassException(SuspiciousOperation):
    pass


class Min_pass_length(object):
    def __init__(self, min_length=8):
        self.min_length = min_length

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise PassException


class Mail_validator(EmailValidator):
    def __call__(self, value):
        value = force_text(value)
        ex = EmailException

        if not value or '@' not in value:
            raise ex

        user_part, domain_part = value.rsplit('@', 1)

        if not self.user_regex.match(user_part):
            raise ex

        if (domain_part not in self.domain_whitelist and
                not self.validate_domain_part(domain_part)):
            # Try for possible IDN domain-part
            try:
                domain_part = domain_part.encode('idna').decode('ascii')
                if self.validate_domain_part(domain_part):
                    return
            except UnicodeError:
                pass
            raise ex
