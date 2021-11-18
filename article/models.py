from django.db import models
from ckeditor.fields import RichTextField
# Create your models here.


class Article(models.Model):
    # djangonun icindeki hazir olan authentication tablosundan bir tane
    # foreignKey aliyoruz
    # cunku her bir article bir kullaniciya ait olmali
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    # normal kullanim TextField() biz ck editorde olan RichText Field i kullandik
    # content = models.TextField()
    content = RichTextField()

    # bu bize o anki tarihi atar.Veri eklendiginde
    created_date = models.DateTimeField(auto_now_add=True)

    # Image Eklenecek alan 
    article_image = models.FileField(blank=True,null=True, verbose_name='Makaleye Fotograf Yukleyin')

    # def str bize admin panelinde title bilgisini ozellestirerek gosteriyor
    def __str__(self):
        return self.title

    #modelimizde en son eklenen en ustte gosterildi
    class Meta:
        ordering = ['-created_date']

class Comment(models.Model):
    # article a yorum olarak ikincil anahtar ekledik yani bir article a bagli olacak yorumumuz
    article = models.ForeignKey(Article,on_delete = models.CASCADE,verbose_name = "Makale",related_name= "comments")
    #yazar
    comment_author = models.CharField(max_length = 50, verbose_name = "Isim")
    #icerik-yorum
    comment_content = models.CharField(max_length = 200,verbose_name = "Yorum")
    # yorum yapilis tarihi ####### aouto_now_add o anki tarihi aliyoruz
    comment_date = models.DateTimeField(auto_now_add = True)

    # def str bize admin panelinde yazilan bilgiyi ozellestirerek gosteriyor
    #ForeignKey de hata veriyor
    def __str__(self):
        return self.comment_content

    class Meta:
        ordering = ['-comment_date']