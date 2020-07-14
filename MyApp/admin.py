from django.contrib import admin
from MyApp.models import Post, Job, PostComment

# Register your models here.
admin.site.site_header = 'ConnectGlobe Admin'

admin.site.register(Post)
admin.site.register(Job)
admin.site.register(PostComment)
