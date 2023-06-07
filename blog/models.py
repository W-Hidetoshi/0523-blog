#-*-cording:utf-8-*-
from django.conf import settings
from django.db import models
from django.utils import timezone

# カテゴリーモデル
class Category(models.Model):
    name = models.CharField('カテゴリー',max_length=50)
    
    def __str__(self):
        return self.name


#投稿のシステム部分
class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null = True)
    
    #追加部分
    category = models.ForeignKey(
        Category,on_delete=models.PROTECT
    )
    
    
    def publish(self):
        self.published_date = timezone.now()
        self.save()
        
    def __str__(self):
        return self.title
    
    def approved_comments(self):
        return self.comments.filter(approved_comment=True)

#以下はコメント部分　CASCADE:全部消し　
class Comment(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text    

    