from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):
    def create_user(self, email, username, nickname, fullname, birthday, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """

        if not email:
            raise ValueError("Users must have email")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            fullname=fullname,
            nickname=nickname,
            birthday=birthday,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, username, fullname, nickname, email, birthday, password=None
    ):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            username,
            fullname,
            nickname,
            birthday,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    username = models.CharField(max_length=100)
    fullname = models.CharField(max_length=100)
    nickname = models.CharField(max_length=100)

    birthday = models.DateField(blank=True)
    join_date = models.DateField(auto_now_add=True)

    follower = models.ManyToManyField(
        "self", symmetrical=False, related_name="followee", blank=True
    )

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "nickname", "fullname", "birthday"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


# - username(필수) : 로그인 시 사용할 id입니다.
# - password(필수) : 로그인 시 사용할 비밀번호입니다.
# - email(필수) : 사용자의 이메일 주소입니다.
# - fullname(필수) : 사용자의 이름입니다.
# - nickname(필수) : 사용자의 닉네임입니다.
#     - 다른 사람의 닉네임과 중복되지 않도록 설정합니다.
# - birthday : 사용자의 생일년월일 입니다.
# - join_date : 회원가입 일자 및 시간입니다.
#     - 회원가입 한 시간을 자동으로 저장하도록 설정합니다.
# - is_active : 계정 활성화 여부입니다.
#     - True 혹은 False를 저장할 수 있으며, 기본값으로 True를 저장하도록 설정합니다.
