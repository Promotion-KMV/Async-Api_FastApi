from functools import wraps
from http import HTTPStatus

from app.utils.exceptions import NotFoundError, BadLengthError, BadEmailError, BadIdFormat, BadPasswordError, \
    FieldValidationError, InvalidToken, AccessDenied, AlreadyExistsError


def class_route(self, rule, endpoint, **options):
    """
    This decorator allow add routed to class view.
    :param self: any flask object that have `add_url_rule` method.
    :param rule: flask url rule.
    :param endpoint: endpoint name
    """
    @wraps
    def wrapper(cls):
        self.add_url_rule(rule, view_func=cls.as_view(endpoint), **options)
        return cls

    return wrapper


def catch_exceptions(func):
    def wrapper(*args, **kwargs):
        try:
            value = func(*args, **kwargs)
        except NotFoundError as e:
            return e.message, HTTPStatus.NOT_FOUND
        except (BadEmailError, BadLengthError, BadIdFormat, BadPasswordError, FieldValidationError) as e:
            return e.message, HTTPStatus.BAD_REQUEST
        except InvalidToken as e:
            return e.message, HTTPStatus.UNAUTHORIZED
        except AccessDenied as e:
            return e.message, HTTPStatus.FORBIDDEN
        except AlreadyExistsError as e:
            return e.message, HTTPStatus.CONFLICT
        return value
    return wrapper