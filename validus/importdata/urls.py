from django.urls import path

from . import views

app_name = 'importdata'
urlpatterns = [
    path('', view=views.ShowAllSheets.as_view(), name='all_sheets'),
    path('add/', view=views.AddNewSheet.as_view(), name='add'),
    path('upload/', view=views.upload_sheet, name='upload'),
]
