# -*-coding:utf-8-*-

from .models import Tag

def related(request):
    context = {
        'tag_list':Tag.objects.all(),
    }
    
    return context