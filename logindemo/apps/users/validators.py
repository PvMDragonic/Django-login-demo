from django.utils.translation import gettext as _
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import (
    UserAttributeSimilarityValidator,
    MinimumLengthValidator, 
    CommonPasswordValidator, 
    NumericPasswordValidator
)

from difflib import SequenceMatcher
import re

class CustomStrictUserAttributeSimilarityValidator(UserAttributeSimilarityValidator):
    # Couldn't call it from the original validator, so just re-created it here.
    def _is_similar(self, password, user_value):
        seq = SequenceMatcher(
            a = password.lower(), 
            b = user_value.lower()
        )
        return seq.quick_ratio() >= self.max_similarity

    def validate(self, password, user = None):
        if not user:
            return
        
        for attribute_name in self.user_attributes:
            value = getattr(user, attribute_name, None)

            if not value or not isinstance(value, str):
                continue

            if password == value:
                raise ValidationError(
                    _(f"Your password cannot be the same as your {attribute_name}."),
                    code = 'password_too_similar',
                )
            
            if self._is_similar(password, value):
                raise ValidationError(
                    _(f"Your password is too similar to your {attribute_name}."),
                    code = 'password_too_similar',
                )

    # Not shown in sign-up form, but required by Django for other stuff like password change form.  
    def get_help_text(self):
        return "Your password cannot be identical or similar to your usename."

class CustomMinimumLengthValidator(MinimumLengthValidator):
    def validate(self, password, user = None):
        if len(password) < self.min_length:
            raise ValidationError(
                _(f"Your password is too short and must contain at least {self.min_length} characters."),
                code = 'password_too_short',
            )
        
    def get_help_text(self):
        return "Your password must be at least 8 characters long."

class CustomCommonPasswordValidator(CommonPasswordValidator):
    def validate(self, password, user = None):
        if password.lower().strip() in self.passwords:
            raise ValidationError(
                _("That password is too similar to commonly used ones."),
                code = 'password_too_common',
            )
        
    def get_help_text(self):
        return "Your password must not be too similar to commonly used ones."
    
class CustomNumericPasswordValidator(NumericPasswordValidator):
    def validate(self, password, user = None):
        if password.isdigit():
            raise ValidationError(
                _("Your password must not be entirely numeric."),
                code = 'password_entirely_numeric',
            )
        
    def get_help_text(self):
        return "Your password cannot be entirely numeric."

class CustomUppercaseValidator:
    def validate(self, password, user = None):
        if not re.search(r'[A-Z]', password):
            raise ValidationError(
                _("Your password must contain at least one uppercase letter."),
                code = 'password_no_upper',
            )
        
    def get_help_text(self):
        return "Your password must contain at least one uppercase letter."
        
class CustomSymbolValidator:
    def validate(self, password, user = None):
        if not re.search(r'[\W_]', password):
            raise ValidationError(
                _("Your password must contain at least one symbol (e.g. !, @, #, etc.)."),
                code = 'password_no_symbol',
            )
        
    def get_help_text(self):
        return "Your password must contain at least one symbol character."