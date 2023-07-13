from django.contrib.auth.tokens import PasswordResetTokenGenerator

'''Файл для создания токена при подитверждении почты пользователя'''
class EmailVerificationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
                str(user.is_active) + str(user.pk) + str(timestamp)
        )


email_verification_token = EmailVerificationTokenGenerator()