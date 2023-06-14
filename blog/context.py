#cording:utf-8
#mysite/blog/context.py

from .models import Category,Post#models.pyからCategoryモデルをimport 

def related(request):
    context ={
        'category_list':Category.objects.all(),     #category_listを辞書型で定義
        'post_list':Post.objects.all(),  #post_listを辞書型で定義
    }
    
    return context

