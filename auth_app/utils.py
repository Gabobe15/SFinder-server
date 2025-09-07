from django.contrib.auth.tokens import PasswordResetTokenGenerator


class ShortLivedResetTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        last_login_timestamp = None
        
        if user.last_login:
            last_login_timestamp = user.last_login.replace(microsecond=0, tzinfo=None)

        token_validity_seconds = 3600  # 1 hour

        return (
            str(user.pk) +
            str(user.password) +
            str(last_login_timestamp) +
            str(timestamp // token_validity_seconds)
        )

token_generator = ShortLivedResetTokenGenerator()