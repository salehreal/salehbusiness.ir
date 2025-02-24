from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView
import logging
from pyexpat.errors import messages
from cart_module.models import CartModel
from .models import BlogModel, CommentModel

# Create your views here.
logger = logging.getLogger('blog_module')

def res_req(request):
    return JsonResponse({'status': 'success'})


class BlogListView(ListView):
    template_name = 'blog-list.html'
    model = BlogModel
    context_object_name = 'blogs'
    def get_context_data(self, **kwargs):
        context = super(BlogListView, self).get_context_data(**kwargs)
        context["blogs"] = BlogModel.objects.filter(is_active=True)
        user = self.request.user
        cart = CartModel.objects.filter(user_id=user.id, is_paid=False).first()
        context['cart'] = cart
        return context


class BlogDetailView(View):
    def get(self, request:HttpRequest, id):
        try:
            blog = BlogModel.objects.filter(id=id).first()
            comments_res = CommentModel.objects.filter(blog_id=blog.id, is_publish=True)
            comments = comments_res.filter(parent=None)
            user = request.user
            cart = CartModel.objects.filter(user_id=user.id, is_paid=False).first()
            return render(request, 'blog-detail.html', {
                'blog': blog,
                'comments': comments,
                'count_comment': len(comments_res),
                'cart': cart
            })
        except Exception as err:
            logger.debug(f'this error is : {err}')
            return render(request, '404.html', {

            })

    # def post(self, request: HttpRequest, id):
    #     blog = BlogModel.objects.filter(id=id).first()
    #     message = request.POST['message']
    #     user = request.user
    #     parent_ = request.POST['hidden-input']
    #     if parent_:
    #         new_comment = CommentModel.objects.create(user=user, text=message, blog=blog, parent_id=int(str(parent_)))
    #     else:
    #         new_comment = CommentModel.objects.create(user=user, text=message, blog=blog, parent=None)
    #     return redirect(reverse('blog-detail', args=[blog.id]))

def send_comment(request):
    text = request.GET.get("text")
    blog_id = int(request.GET.get("blog_id"))
    parent = request.GET.get("parent")
    if parent != 'false':
        new_comment = CommentModel.objects.create(user=request.user, text=text, blog_id=blog_id, parent_id=int(parent), is_publish=True)
    else:
        new_comment = CommentModel.objects.create(user=request.user, text=text, blog_id=blog_id, parent=None, is_publish=False)
    comments = CommentModel.objects.filter(blog_id=blog_id, is_publish=True)
    return render(request, 'comment-box.html', {
        'comments' : comments,
        'count_comment': len(comments),
    })