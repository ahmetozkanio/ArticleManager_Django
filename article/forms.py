from django import forms
from .models import Article


class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        # article modelimizi kullanarak baslik ve icerik kismina mudahele edebiliriz
        fields = ["title", "content","article_image"]
