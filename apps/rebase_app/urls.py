from django.urls import path
from . import views

urlpatterns = [    
    path('rebase/home', views.home, name='home'),
    path('logout', views.logout),
    path('rebase/add_text', views.add_text, name='add_text'),
    path('rebase/add_text2', views.add_text2, name='add_text2'),
    path('rebase/read', views.read, name='read'),
    # path('rebase/read_check', views.read_check, name='read_check'),
    path('rebase/video', views.video, name='video'),
    path('rebase/phrase', views.phrase, name='phrase'),
    path('rebase/phrase2', views.phrase2, name='phrase2'),
    path('rebase/listen', views.listen, name='listen'),
    path('rebase/contact', views.contact, name='contact'),
    path('rebase/success2', views.success2, name='success2'),
    path('rebase/users', views.users, name="users"),
    path('rebase/delete/<int:textId>', views.delete, name='delete'),
    path('rebase/<int:text_id>', views.read2, name='read2'),
    path('rebase/next/<int:text_id>', views.next),
    path('rebase/previous/<int:text_id>', views.previous),
    path('rebase/translate/<int:text_id>', views.translate),
    path('rebase/add_new_sentence/<int:text_id>', views.add_new_sentence),
    path('rebase/delete_sentence', views.delete_sentence, name='delete_sentence'),
    path('rebase/delete2/<int:textId>', views.delete2, name='delete2'),
    path('rebase/next_line', views.next_line, name='next_line'),
    path('rebase/thankyou', views.thankyou, name='thankyou')
]