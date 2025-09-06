from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from . forms import MyPasswordResetForm, MySetPasswordForm



urlpatterns=[
    path('dashboard/', views.Home , name='dashboard-home'),
    path('staff/', views.Staff , name='dashboard-staff'),
    path('staff/view/<int:pk>/', views.staff_detail , name='dashboard-staff-detail'),
    path('product/', views.Product_View, name='dashboard-product'),
    path('product/delete/<int:pk>/', views.Product_delete, name='dashboard-product-delete'),
    path('product/update/<int:pk>/', views.Product_update, name='dashboard-product-update'),
    path('order/', views.Order_By, name='dashboard-order'),
    
    

    # user register login , logout , forget passward
    path('register/', views.Register, name='register'),
    path('', auth_views.LoginView.as_view(template_name='user/login.html'), name='user-login'),
    #path('logout/', auth_views.LoginView.as_view(template_name='user/logout.html'), name='user-logout'),
    path('logout/', views.logout_view, name='user-logout'),
    path('profile/', views.Profile, name='user-profile'),
    path('profile/update/', views.Profile_update, name='user-profile-update'),

    # passward reset 
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='user/password_reset.html',  form_class=MyPasswordResetForm), name='password-reset'),
    path('password-reset/done', auth_views.PasswordResetDoneView.as_view(template_name='user/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='user/password_reset_confirm.html', form_class=MySetPasswordForm), name='password_reset_confirm'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='user/password_reset_complete.html'),name='password_reset_complete'),


] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
