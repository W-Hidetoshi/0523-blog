#cording:utf-8
#mysite/blog/context.py

from .models import Category

def related(request):
    context ={
        'category_list':Category.objects.all(),
    }
    
    return context

