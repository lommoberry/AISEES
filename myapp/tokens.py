from django.contrib.auth.tokens import PasswordResetTokenGenerator
class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        # six.text_type is replaced with str since Django 3.0+ supports Python 3.6+ only.
        return str(user.pk) + str(timestamp) + str(user.is_active)

account_activation_token = TokenGenerator()