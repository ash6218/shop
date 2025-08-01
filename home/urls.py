from django.urls import path, include
from . import views

app_name = 'home'

bucket_urls = [
    path('', views.BucketHome.as_view(), name='bucket'),
    path('delete_obj/<str:key>', views.DeleteBucketObject.as_view(), name='delete_obj_bucket'),
    path('download_obj/<str:key>', views.DownloadBucketObject.as_view(), name='download_obj_bucket'),
    path('upload/', views.UploadImageView.as_view(), name='upload'),
    
]

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('category/<slug:category_slug>', views.HomeView.as_view(), name='category_filter'),
    path('bucket/', include(bucket_urls)),
    path('bucket_pics/',views.BucketPicsView.as_view(), name='bucket_pics'),
    path('product/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('favorite/<slug:slug>/', views.FavoriteView.as_view(), name='product_fav'),
    path('favorites_list/', views.MyFavoritesListView.as_view(), name='my_fav_pr'),
    
    
]
# bucket should be higher than product_detail and delete
# path('upload_obj/', views.UploadBucketObject.as_view(), name='upload_obj_bucket'),