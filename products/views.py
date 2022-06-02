from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Category, Product, Comment, Slider, Like, Save
from django.utils.encoding import uri_to_iri
import itertools
from . import forms
from django.contrib import messages
from orders.forms import CartAddForm
from mixins import IsAdminUserMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from django.db.models import Count, Q, Max
from django.contrib.contenttypes.models import ContentType
from django.http import Http404
from django.views.generic import ListView


def my_grouper(n, iterable):
    args = [iter(iterable)] * n
    return ([e for e in t if e is not None] for t in itertools.zip_longest(*args))


class NavbarView(View):
    template_name = 'inc/navbar.html'

    def get(self, request):
        categories = Category.objects.filter(is_sub=False)
        context = {
            'categories': categories,
            }
        return render(request, self.template_name, context)


class HomeView(View):
    template_name = 'products/home.html'

    def get(self, request):
        sliders = Slider.objects.all()

        last_month = datetime.today() - timedelta(days=30)
        content_type_id = ContentType.objects.get(app_label='products', model='product')

        popular_products = Product.objects.filter(available=True).annotate(
        count=Count('hits', filter=Q(producthit__created__gt=last_month))).order_by('-count',)[:8]

        newest_products = Product.objects.filter(available=True).order_by('-updated', 'created')[:8]

        top_rate_products = Product.objects.filter(available=True).annotate(
        max=Max('rates',filter=Q(rates__content_type_id=content_type_id))).order_by('-max',)[:8]

        context = {
             'sliders': sliders,
             'popular_products': my_grouper(4, popular_products),
             'newest_products': my_grouper(4, newest_products),
             'top_rate_products': my_grouper(4, top_rate_products),
             }
        
        return render(request, self.template_name, context)


class CategoryFilterView(ListView):
    template_name = 'products/category_filter.html'
    paginate_by = 3
    context_object_name = 'products'

    def get_queryset(self):
        global category
        slug = self.kwargs.get('category_slug')
        category = get_object_or_404(Category, slug=uri_to_iri(slug), status=True)
        products = Product.objects.filter(category=category, available=True)
        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = category
        return context    


class ProductDetailView(View):
    template_name = 'products/product_detail.html'
    form_class = forms.CommentCreateForm
    form_class_reply = forms.CommentReplyForm
    form_class_add = CartAddForm

    def setup(self , request, *args, **kwargs):
        slug = kwargs.get('slug')
        self.product_instance = get_object_or_404(Product, slug=uri_to_iri(slug), available=True)
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class
        form_reply = self.form_class_reply
        form_add = self.form_class_add
        related_products = self.product_instance.related_product.all()
        grouped_related_products = my_grouper(4, related_products)
        comments = self.product_instance.productcomments.filter(is_reply=False, is_active=True)
        can_like = False
        can_save = False

        if request.user.is_authenticated and self.product_instance.user_can_like(request.user):
            can_like = True

        if request.user.is_authenticated and self.product_instance.user_can_save(request.user):
            can_save = True 

        ip_address = self.request.user.ip_address
        if ip_address not in self.product_instance.hits.all():
            self.product_instance.hits.add(ip_address)

        context = {
            'product': self.product_instance,
            'related_products': grouped_related_products,
            'comments': comments,
            'form': form,
            'form_reply': form_reply,
            'form_add': form_add,
            'can_like': can_like,
            'can_save': can_save,
        }
        return render(request, self.template_name, context)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
           new_comment = form.save(commit=False)
           new_comment.user = request.user
           new_comment.product = self.product_instance
           new_comment.save()
           messages.success(request, 'دیدگاه شما با موفقیت ثبت شد.پس از بررسی منتشر می شود.', 'success')
           return redirect('products:product_detail', self.product_instance.slug)
        return redirect('products:product_detail', self.product_instance.slug) 


class CreateReplyCommentView(LoginRequiredMixin, View):
    form_class = forms.CommentReplyForm

    def post(self, request, comment_id, slug):
        product = get_object_or_404(Product, slug=uri_to_iri(slug))
        comment = get_object_or_404(Comment, id=comment_id)
        form = self.form_class(request.POST)
        if form.is_valid():
            reply_comment = form.save(commit=False)
            reply_comment.user = request.user
            reply_comment.product = product
            reply_comment.reply = comment
            reply_comment.is_reply = True
            reply_comment.save()
            messages.success(request, 'پاسخ شما با موفقیت ثبت شد.پس از بررسی منتشر می شود.', 'success')
            return redirect('products:product_detail', product.slug)
        return redirect('products:product_detail', product.slug)            


class ProductLikeView(LoginRequiredMixin, View):
    def get(self, request, product_slug):
        product = get_object_or_404(Product, slug=uri_to_iri(product_slug))
        like = Like.objects.filter(product=product, user=request.user)
        if like.exists():
            like.delete()
        else:
            Like.objects.create(user=request.user, product=product) 
        return redirect('products:product_detail', product.slug)


class ProductSaveView(LoginRequiredMixin, View):
    def get(self, request, product_slug):
        product = get_object_or_404(Product, slug=uri_to_iri(product_slug))
        psave = Save.objects.filter(product=product, user=request.user)
        if psave.exists():
            psave.delete()
        else:
            Save.objects.create(user=request.user, product=product) 
        return redirect('products:product_detail', product.slug)


class ProductsLikeView(LoginRequiredMixin, View): 
    template_name ='products/products_like.html' 

    def get(self, request):
        likes = request.user.userlikes.all()
        context = {
            'likes': likes,
        }
        return render(request, self.template_name, context)


class ProductsSaveView(LoginRequiredMixin, View): 
    template_name ='products/products_save.html' 
         
    def get(self, request):
        saves = request.user.usersaves.all()
        context = {
            'saves': saves,
        }
        return render(request, self.template_name, context)    


class SearchProductsView(View):
    template_name ='products/product_search.html' 

    def get(self, request):
        search = request.GET.get('search')
        products = Product.objects.filter(name__icontains=request.GET['search'], available=True)
        if products is not None and search:
            context = {
                'products': products,
                'search': search
            }
            return render(request, self.template_name, context)
        raise Http404('لطفا کالای مورد نظرتان را وارد کنید')            


