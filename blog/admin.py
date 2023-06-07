#cording:utf-8
from django.contrib import admin
from .models import Post,Comment,Tag
from markdownx.admin import MarkdownxModelAdmin

#管理画面にpostモデルを登録
admin.site.register(Post,MarkdownxModelAdmin)
#管理画面にコメントモデルを登録
admin.site.register(Comment)
#管理画面にtagモデルを登録
admin.site.register(Tag)