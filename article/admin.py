from django.contrib import admin

from .models import Article, Comment
# Register your models here.

#sadece dahil ettik model olusturmadik admin de
admin.site.register(Comment)


#Article modelimizi admin paneline dahil ettik
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    class Meta:
        model = Article
        
        
        