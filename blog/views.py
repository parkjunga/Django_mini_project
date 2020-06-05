from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.dates import ArchiveIndexView, YearArchiveView,MonthArchiveView
from django.views.generic.dates import DayArchiveView, TodayArchiveView

from blog.models import Post
import pandas as pd

# Create your views here.

class PostLV(ListView):
    model = Post
    template_name = 'blog/post_all.html' # tmplate_name 을 지정하지 않으면 post_list 가 기본파일로 되어 넘어가게됨
    context_object_name = 'posts' #별도로 지정하여도 object_list 는 사용 가능하다.
    paginate_by = 2

class PostDV(DetailView):
    model = Post

class PostAV(ArchiveIndexView):
    model = Post
    date_field ='modify_dt'

class PostYAV(YearArchiveView):
    model = Post
    date_field = 'modify_dt'
    make_object_list = True

class PostMAV(MonthArchiveView):
    model = Post
    date_field = 'modify_dt'

class PostDAV(DayArchiveView):
    model = Post
    date_field = 'modify_dt'

class PostTAV(TodayArchiveView):
    model = Post
    date_field = 'modify_dt'

