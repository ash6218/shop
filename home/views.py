from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Product
from . import tasks
from django.contrib import messages
#
from bucket import bucket


class HomeView(View):
    def get(self, request):
        products = Product.objects.filter(available=True)
        return render(request, 'home/home.html', {'products':products})

class ProductDetaileView(View):
    def get(self, request, slug):
        product = Product.objects.get(slug=slug)
        return render(request, 'home/detail.html', {'product':product})
    

class BucketHome(View):
    template_name = 'home/bucket.html'
    def get(self, request):
        objects = tasks.all_bucket_objects_task()
        # all_bucket_objects_task.delay() if async.
        return render(request, self.template_name, {'objects':objects})
    
class DeleteBucketObject(View):

    # with celery
    def get(self, request, key):
        tasks.delete_object_task.delay(key)
        messages.success(request, 'your object will be deleted soon...', 'info')
        return redirect('home:bucket')
    """
    # without celery
    def get(self, request, key):
        bucket.delete_object(key)
        messages.success(request, 'your object deleted')
        return redirect('home:bucket')
    """

class Downlo9adBucketObject(View):
    def get(self, request, key):
        tasks.download_object_task.delay(key)
        messages.success(request, 'your object will be downloaded soon...', 'info')
        return redirect('home:bucket')
    """
    # without celery
    def get(self, request, key):
        bucket.delete_object(key)
        messages.success(request, 'your object deleted', 'info')
        return redirect('home:bucket')
    """