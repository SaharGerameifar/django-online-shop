from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, phone_number, email, full_name, password):
        if not phone_number:
            raise ValueError('لطفا شماره موبایل خود را وارد کنید.')

        if not email:
            raise ValueError('لطفا ایمیل خود را وارد کنید.')    

        if not full_name:
            raise ValueError('لطفا نام و نام خانوادگی خود را وارد کنید.')  

        user = self.model(phone_number=phone_number, email=self.normalize_email(email), full_name=full_name)
        user.set_password(password)
        user.save(using=self._db)
        return user 

    def create_superuser(self, phone_number, email, full_name, password): 
        user = self.create_user(phone_number, email, full_name, password)
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user 
