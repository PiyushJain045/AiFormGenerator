from django.urls import path
from . import views


urlpatterns = [
    path('', views.home.as_view(), name='home'),
    path('form-add', views.add_field.as_view(), name='add_field'),
    path('form-remove', views.remove_form, name="remove-form"),
    path('sub-options', views.GetSuboptions.as_view(), name="get_suboptions"),
    path('User-Forms', views.save_form_data, name="user-forms"),
    path('view-form/<int:form_id>/', views.view_form, name="view-form"),
    path('share-form/<uuid:unique_id>/', views.share_form, name="share-form"),
    path('fill-form/<uuid:unique_id>/', views.fill_form, name="fill-form"),
    path('Analysis/<uuid:unique_id>/', views.analysis, name="analysis"),
    path('templates/<slug:slug>', views.templates_view, name='templates'),
    path('design_df/', views.dynamic_form_view, name='design_df'),
    path('demo_design/', views.demo_design, name='demo_design')
]
