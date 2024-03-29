#cording:utf-8
from django.urls import path,re_path,include
from . import views

urlpatterns=[
    
    path('',views.PostListView.as_view(),name='post_list'),
    path('accounts/',include('django.contrib.auth.urls')),
    path('post/<int:pk>',views.post_detail,name='post_detail'),
    path('post/new/', views.post_new, name = 'post_new'),
    path('post/<int:pk>/edit',views.post_edit,name = 'post_edit'),
    path('drafts/', views.post_draft_list, name='post_draft_list'),
    path('post/<pk>/publish', views.post_publish,name='post_publish'),
    path('post/<pk>/remove', views.post_remove,name='post_remove'),
    path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
    path('comment/<int:pk>/approve/', views.comment_approve, name='comment_approve'),
    path('comment/<int:pk>/remove/', views.comment_remove, name='comment_remove'),
    path('category/<str:category>/',views.PostListView.as_view(),name='category'),
    
]
# 記事編集用
def post_edit(request,pk):
    post = get_object_or_404(Post,pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST,instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail',pk=post.pk)
        else:
            form = PostForm(instance=post)
        return render(request, 'blog/post_edit.html', {'form': form})
            
