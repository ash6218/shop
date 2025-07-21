from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Product, UploadImage
from . import tasks
from django.contrib import messages
from .forms import ImageUploadForm
from bucket import bucket
import os
from utils import IsAdminUserMixin


class HomeView(View):
    def get(self, request):
        products = Product.objects.filter(available=True)
        return render(request, 'home/home.html', {'products':products})


class ProductDetailView(IsAdminUserMixin, View):
    def get(self, request, slug):
        product = Product.objects.get(slug=slug)
        return render(request, 'home/detail.html', {'product':product})
    

class BucketHome(IsAdminUserMixin, View):
    template_name = 'home/bucket.html'
    def get(self, request):
        objects = tasks.all_bucket_objects_task()
        # all_bucket_objects_task.delay() if async.
        return render(request, self.template_name, {'objects':objects})
    
class DeleteBucketObject(IsAdminUserMixin, View):

    # with celery
    def get(self, request, key):
        tasks.delete_object_task.delay(key)
        messages.success(request, 'your object will be deleted soon...', 'info')
        return redirect('home:bucket')


class DownloadBucketObject(IsAdminUserMixin, View):
    def get(self, request, key):
        tasks.download_object_task.delay(key)
        messages.success(request, 'your object will be downloaded soon...', 'info')
        return redirect('home:bucket')


class UploadImageView(IsAdminUserMixin, View):
    form_class = ImageUploadForm
    template_name = "home/upload.html"
    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form':form})
    """
    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            name=form.cleaned_data['name']
            #bucket.upload_object(name)
            tasks.upload_object_task.delay(name)
            #UploadImage(name=form.cleaned_data['name'], image=request.FILES['image']).save()
            messages.success(request, 'your object is uploaded', 'success')
            return redirect('home:bucket')
        messages.error(request, 'something went wrong! please try again', 'danger')
        return render(request, self.template_name, {'form':form})
    """
    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            image_file = request.FILES['image']
            name_from_form = form.cleaned_data['name']

            original_ext = os.path.splitext(image_file.name)[1] # .jpg or .png
            final_file_name = name_from_form + original_ext

            file_content = image_file.read()

            tasks.upload_object_task.delay(final_file_name, file_content)

            messages.success(request, 'Your object is uploaded with custom name', 'success')
            return redirect('home:bucket')

        messages.error(request, 'Something went wrong! Please try again', 'danger')
        return render(request, self.template_name, {'form': form})