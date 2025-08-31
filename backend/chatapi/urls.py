from django.urls import path
from chatapi.views import ChatView

urlpatterns = [
    path('chat/', ChatView.as_view(), name='chat'),
]
