from rest_framework.exceptions import ValidationError


def validate_password(password):
    if len(password) < 6:
        raise ValidationError('Слишком короткий пароль')
    if not any([char.isdigit() for char in password]):
        raise ValidationError('Пароль должен содержать хотя бы одну цифру')
    if not any([char.isupper() for char in password]):
        raise ValidationError('Пароль должен содержать хотя бы одну заглавную букву')