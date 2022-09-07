from django.core.validators import ValidationError


def username_validate(event):
    if "@" in event:
        raise ValidationError("you can't use '@' in username")

