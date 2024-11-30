from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, nickname, password=None, **extra_fields):
        if not nickname:
            raise ValueError("The Email field must be set")
        user = self.model(**extra_fields)
        user.set_password(password)  # This will only hash passwords locally if needed
        user.save(using=self._db)
        return user

    def create_superuser(self, nickname, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(nickname, password, **extra_fields)
    
class User(AbstractBaseUser):
    password = models.CharField(max_length=128)  # Ensure this exists
    last_login = models.DateTimeField(null=True, blank=True)
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    nickname = models.CharField(max_length=200, unique=True, null=False)
    name = models.CharField(max_length=200, unique=False, null=False)
    profile_picture_path = models.CharField(unique=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'nickname'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "User"
    
    def has_perm(self, perm, obj=None):
        # return self.is_superuser
        return True

    def has_module_perms(self, app_label):
        # return self.is_superuser
        return True

class Posts(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    post_image_path = models.CharField(unique=True, null=False)
    post_description = models.CharField(unique=False, null=True)
    user = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)

    class Meta:
        db_table = "Posts"
        managed = False

class Hashtags(models.Model):
    id = models.AutoField(primary_key=True)
    hashtag_name = models.CharField(max_length=200, null=False) 

    class Meta:
        db_table = "Hashtags"
        managed = False

class Post_hashtags(models.Model):
    hashtag_id = models.ForeignKey(Hashtags, on_delete=models.CASCADE, db_column="hashtag_id")
    post_id = models.ForeignKey(Posts, on_delete=models.CASCADE, db_column="post_id")

    class Meta:
        db_table = "Post_hashtags"
        managed = False
        unique_together = ('post_id', 'hashtag_id')

class Comments(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateField(auto_now_add=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column="user_id")
    post_id = models.ForeignKey(Posts, on_delete=models.CASCADE, db_column="post_id")
    comment_text = models.CharField(max_length=1000, null=False)

    class Meta:
        db_table = "Comments"
        managed = False