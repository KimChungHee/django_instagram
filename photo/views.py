from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from .models import Photo
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.contrib import messages
from django.views.generic import RedirectView
from django.views.generic.base import View
from urllib.parse import urlparse


class PhotoList(ListView):
    model = Photo
    template_name_suffix = '_list'

class PhotoCreate(CreateView):
    model = Photo
    fields = ['text', 'image']
    template_name_suffix = '_create'
    success_url = '/'

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        if form.is_valid():
            # 올바르다면
            # form : 모델폼
            form.instance.save()
            return HttpResponseRedirect('/')
        else:
            # 올바르지 않다면
            return self.render_to_response({'form': form})

class PhotoUpdate(UpdateView):
    model = Photo
    fields = ['author','text', 'image']
    template_name_suffix = '_update'
    # success_url = '/'

    def dispatch(self, request, *args, **kwargs):
        object = self.get_object()
        if object.author != request.user:
            messages.warning(request, '수정할 권한이 없습니다.')
            return HttpResponseRedirect('/')
        else:
            return super(PhotoUpdate, self).dispatch(request, *args, **kwargs)

class PhotoDelete(DeleteView):
    model = Photo
    template_name_suffix = '_delete'
    success_url = '/'

    def dispatch(self, request, *args, **kwargs):
        object = self.get_object()
        if object.author != request.user:
            messages.warning(request, '삭제할 권한이 없습니다.')
            return HttpResponseRedirect('/')
        else:
            return super(PhotoDelete, self).dispatch(request, *args, **kwargs)

class PhotoDetail(DetailView):
    model = Photo
    template_name_suffix = '_detail'



class PhotoLike(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        else:
            if 'photo_id' in kwargs:
                photo_id = kwargs['photo_id']
                photo = Photo.objects.get(pk=photo_id)
                user = request.user

                if user in photo.like.all():
                    photo.like.remove(user)
                else:
                    photo.like.add(user)

            referer_url = request.META.get('HTTP_REFERER')
            path = urlparse(referer_url).path
            #좋아요를 눌러도 다른데로 가지않고 메인에 머물러기 만든거임
            return HttpResponseRedirect(path)

class PhotoFavorite(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        else:
            if 'photo_id' in kwargs:
                photo_id = kwargs['photo_id']
                photo = Photo.objects.get(pk=photo_id)
                user = request.user

                if user in photo.favorite.all():
                    photo.favorite.remove(user)
                else:
                    photo.favorite.add(user)

            referer_url = request.META.get('HTTP_REFERER')
            path = urlparse(referer_url).path
            #좋아요를 눌러도 다른데로 가지않고 메인에 머물러기 만든거임
            return HttpResponseRedirect(path)

class PhotoLikeList(ListView):
    model = Photo
    template_name = 'photo/photo_list.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "로그인을 하시오!")
            return HttpResponseRedirect('/')
        return super(PhotoLikeList, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        queryset = user.like_post.all()
        return queryset

class PhotoFavoriteList(ListView):
    model = Photo
    template_name = 'photo/photo_list.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "로그인을 하시오!")
            return HttpResponseRedirect('/')
        return super(PhotoFavoriteList, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        queryset = user.favorite_post.all()
        return queryset

# def document_detail(request, document_id):
#
#     document = get_object_or_404(Document, pk=document_id)
#
#     if request.method == "POST":
#         comment_form = commentForm(request.POST)
#         comment_form.instance.author_id = request.user.id
#         comment_form.instance.document_id = document_id
#         if comment_form.is_valid():
#             comment = comment_form.save()
#
#     comment_form = CommentForm()
#     comments = document.comments.all()
#
#     return render(request, 'board/document_detail.html', {'object':document, "comments":comments, "comment_form":comment_form})
#
# def comment(request, document_id):
#
#     if request.method ==
