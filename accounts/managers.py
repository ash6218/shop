from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, phone_number, email, full_name, password):
        if not phone_number:
            raise ValueError('user must have phone number')

        if not email:
            raise ValueError('user must have email')
        
        if not full_name:
            raise ValueError('user must have full name')
        
        # django will validate password automatically, as it's defined in BaseUserManager.
        
        user = self.model(phone_number=phone_number, email=self.normalize_email(email), full_name=full_name) 
        # as we already defined object in new User model, the model here is set as User.
        user.set_password(password)
        # password should not entered in user as a raw field, instead we use set_password to hash it.
        user.save(using=self._db)
        # using=self._db is recommended by django to reach database more optimized.
        return user

    def create_superuser(self, phone_number, email, full_name, password):
        user = self.create_user(phone_number, email, full_name, password)
        # as create_super_user have all the elements of create_user, we called the first methos here.
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

