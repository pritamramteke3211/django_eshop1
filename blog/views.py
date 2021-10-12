
from django.shortcuts import render
from django.views import View
from .models import *

class BlogHomePage(View):
    template_name = 'blog/bhome.html'
    def get(self, request):
        blogs = Blogpost.objects.all()
        context={'blogs':blogs}
        return render(request,self.template_name,context)

def blogpost(request,id=None):
    blog = Blogpost.objects.get(post_id=id)
    context = {'blog':blog}
    return render(request,'blog/blogpost.html',context)