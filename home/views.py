from django.shortcuts import render, redirect
from django.views import View
from .models import Product, Category, Comment, Favorite
from . import tasks
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ImageUploadForm, CommentForm, SearchForm, ApiQuestionForm
from bucket import bucket, list_s3_images
import os, requests
from utils import IsAdminUserMixin, get_api_headers
from shop import settings
from orders.forms import CartAddForm
from django.db.models import Q


class HomeView(View):
    form_class = SearchForm
    """we have different urls that links to this view, some wont send 
    category_slug and it ends with an error, unless we use category_slug=None"""
    def get(self, request, category_slug=None):
        products = Product.objects.filter(available=True)
        categories = Category.objects.filter(is_sub=False)
        #sub_categories = Category.objects.filter(is_sub=True)
        form = self.form_class
        if category_slug:
            category = Category.objects.get(slug=category_slug)
            products = products.filter(category=category)
        search_query = request.GET.get('search')
        if search_query:
            products = products.filter(
                Q(description__icontains=search_query) |
                Q(name__icontains=search_query))
        return render(request, 'home/home.html', {'products':products, 'categories':categories, 'form':form})
    

class ProductDetailView(View):
    def get(self, request, slug):
        product = Product.objects.get(slug=slug)
        comments = Comment.objects.filter(product=product)
        if request.user.is_authenticated:
            is_fav = Favorite.objects.filter(user=request.user, product=product).exists()
        else:
            is_fav = False
        return render(request, 'home/detail.html', {
            'product':product, 'form1':CartAddForm, 'form2':CommentForm, 'comments':comments, 'is_fav':is_fav})
    
    def post(self, request, slug):
        form2 = CommentForm(request.POST)
        if form2.is_valid():
            cd = form2.cleaned_data
            comment = Comment.objects.create(user=request.user, product=Product.objects.get(slug=slug), title=cd['title'], text=cd['text'])
            comment.save()
            return redirect('home:home')
    

class BucketHome(IsAdminUserMixin, View):
    template_name = 'home/bucket.html'
    def get(self, request):
        objects = tasks.all_bucket_objects_task()
        # all_bucket_objects_task.delay() if async.
        objects = sorted(objects, key=lambda x: x['LastModified'], reverse=True) # order by LastModified
        return render(request, self.template_name, {'objects':objects})
    
class DeleteBucketObject(IsAdminUserMixin, View):
    def get(self, request, key):
        if settings.CELERY_IS_ACTIVE:
            tasks.delete_object_task.delay(key)
            messages.success(request, 'your object will be deleted soon...', 'info')
        else:
            bucket.delete_object(key)
            print("settings.CELERY_IS_ACTIVE is False")
            messages.success(request, 'your object is deleted', 'success')
        next_url = request.GET.get('next') # super useful, by adding ?next={{ request.path }} at the end of url tag in html file!
        return redirect(next_url)
        #return redirect('home:bucket')


class DownloadBucketObject(IsAdminUserMixin, View):
    def get(self, request, key):
        if settings.CELERY_IS_ACTIVE:
            tasks.download_object_task.delay(key)
            messages.success(request, 'your object will be downloaded soon...', 'info')
        else:
            bucket.download_object(key)
            print("settings.CELERY_IS_ACTIVE is False")
            messages.success(request, 'your object is downloaded', 'success')
        return redirect('home:bucket')


class UploadImageView(IsAdminUserMixin, View):
    form_class = ImageUploadForm
    template_name = "home/upload.html"
    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form':form})
    
    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            image_file = request.FILES['image']
            name_from_form = form.cleaned_data['name']

            original_ext = os.path.splitext(image_file.name)[1] # .jpg or .png
            final_file_name = name_from_form + original_ext

            file_content = image_file.read()
            if settings.CELERY_IS_ACTIVE:
                tasks.upload_object_task.delay(final_file_name, file_content)
                messages.success(request, 'Your object is uploaded with custom name', 'info')
            else:
                bucket.upload_object(final_file_name, file_content)
                print("settings.CELERY_IS_ACTIVE is False")
                messages.success(request, 'Your object is uploaded', 'success')
            
            return redirect('home:bucket')

        messages.error(request, 'Something went wrong! Please try again', 'danger')
        return render(request, self.template_name, {'form': form})
    
class BucketPicsView(IsAdminUserMixin, View):
    template_name = 'home/bucketpics.html'
    def get(self, request):
        pics = list_s3_images()[1]
        return render(request, self.template_name, {'pics':pics})

class FavoriteView(LoginRequiredMixin, View):
    def get(self, request, slug):
        product = Product.objects.get(slug=slug)
        comments = Comment.objects.filter(product=product)
        user = request.user
        product = Product.objects.get(slug=slug)
        context = {'product':product, 'form1':CartAddForm, 'form2':CommentForm, 'comments':comments}
        already_fav = Favorite.objects.filter(user=user, product=product).first()
        print(already_fav)
        if already_fav is None:
            favorite = Favorite.objects.create(user=user, product=product)
            favorite.save()
            context['is_fav'] = True
            print(context['is_fav'])
            messages.success(request, f'the product "{product.name}" has been added to your favorite list.', 'success')
            return redirect('home:product_detail', slug=slug)
        context['is_fav'] = False
        print(context['is_fav'])
        already_fav.delete()
        messages.error(request, f'the product "{product.name}" has been removed from your favorite list.', 'warning')
        return redirect('home:product_detail', slug=slug)
    
class MyFavoritesListView(LoginRequiredMixin, View):
    def get(self, request):
        favorites = Favorite.objects.filter(user=request.user)
        products =[]
        for fav in favorites:
            products.append(fav.product)
        return render(request, 'home/my_favorite.html', {'products':products})
    
class ApiView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'home/api.html')
    

class PersonApiRequestView(LoginRequiredMixin, View):
    def get(self, request):
        try:
            url = 'http://127.0.0.1:8000/'
            headers = get_api_headers(request)
            json_response = requests.get(url, headers=headers).json()
            print(f'api response: {json_response}')
            return render(request, 'home/api_result.html', {'json_response':json_response})
        except:
            messages.error(request, 'API connection failed.', 'warning')
            return redirect('home:home')
        
class UserApiRequestView(LoginRequiredMixin, View):
    def get(self, request):
        try:
            url = 'http://127.0.0.1:8000/accounts/user'
            headers = get_api_headers(request)
            json_response = requests.get(url, headers=headers).json()
            return render(request, 'home/api_user_result.html', {'json_response':json_response})
        except:
            messages.error(request, 'API connection failed.', 'warning')
            return redirect('home:home')
        
class QuestionApiRequestView(LoginRequiredMixin, View):
    def get(self, request):
        try:
            url = 'http://127.0.0.1:8000/questions/'
            headers = get_api_headers(request)
            json_response = requests.get(url, headers=headers).json()
            request.session['questions'] = json_response # using sessions for update
            return render(request, 'home/api_q_get.html', {'json_response':json_response})
        except:
            messages.error(request, f'API connection failed:{json_response}', 'warning')
            return redirect('home:api')

class QuestionApiCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = ApiQuestionForm()
        return render(request, 'home/api_q_create.html', {'form':form})

    def post(self, request):
        form = ApiQuestionForm(request.POST)
        if form.is_valid():
            try:
                url = 'http://127.0.0.1:8000/question/create/'
                headers = get_api_headers(request)
                json_response = requests.post(url, headers=headers, json=form.cleaned_data).json()
                print(f'data: {form.cleaned_data}')
                print(f'api response: {json_response}')
                messages.success(request, f'new question is created: {json_response}', 'success')
                return redirect('home:api_question')
            except:
                messages.error(request, f'API connection failed:{json_response}', 'warning')
                return redirect('home:api')
        return render(request, 'home/api_q_create.html', {'json_response':json_response})
    
class QuestionApiUpdateView(LoginRequiredMixin, View):
    def get(self, request, pk):
        """url = 'http://127.0.0.1:8000/questions/' 
        headers = get_api_headers(request)
        json_response = requests.get(url, headers=headers).json() # do it with sessions
        question_data = next((i for i in json_response if int(i['id'])==pk), None)"""
        question_data = next((i for i in request.session['questions'] if int(i['id'])==pk), None)
        # using sessions is easier but there might be some problems due to delays that need update
        form = ApiQuestionForm(initial=question_data)
        return render(request, 'home/api_q_update.html', {'form':form})

    def post(self, request, pk):
        data = request.POST
        form = ApiQuestionForm(data)
        if form.is_valid():
            try:
                url = f'http://127.0.0.1:8000/question/update/{pk}/'
                headers = get_api_headers(request)
                json_response = requests.put(url, headers=headers, json=form.cleaned_data).json()
                
                try:
                    detail = json_response['detail']
                    messages.error(request, f'question is not updated: {detail}', 'warning')
                except:
                    messages.success(request, f'question is updated: title: "{json_response['title']}" - body: "{json_response['body']}"', 'success')
                return redirect('home:api_question')
            except:
                messages.error(request, f'API connection failed:{json_response}', 'warning')
                return redirect('home:api')
        return render(request, 'home/api_q_update.html', {'json_response':json_response})
    
class QuestionApiDeleteView(LoginRequiredMixin, View):
    def get(self, request, pk):
            url = f'http://127.0.0.1:8000/question/delete/{pk}/'
            headers = get_api_headers(request)
            requests.delete(url, headers=headers)
            url2 = 'http://127.0.0.1:8000/questions/'
            json_response = requests.get(url2, headers=headers).json()
            question_data = next((i for i in json_response if int(i['id'])==pk), None)
            try:
                a = question_data['id']==pk
                messages.error(request, 'question can not be deleted', 'warning')
            except:
                messages.success(request, 'question is deleted', 'success')
            return redirect('home:api_question')

"""question_session = request.sesseion['question']
        test1 = pk
        print('+++++++++++++++++++')
        print(question_session, '========', test1)"""