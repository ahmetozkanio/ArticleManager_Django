from django.shortcuts import get_object_or_404, redirect, render, HttpResponse, reverse
# reverse dinamik url
from article.forms import ArticleForm

from article.models import Article, Comment
from django.contrib import messages

# Kullanici girisi kontrolu decorators
from django.contrib.auth.decorators import login_required

# Create your views here.


def articles(request):
    # search keyword icin
    # bu input degerimizi keyword ile aliyoruz GET request ile
    keyword = request.GET.get("keyword")
    # arama yapildiysa filtreleme yapilir
    if keyword:
        # keyword du title da varmi diye filter yapiyoruz veritabanindan title_contains
        articles = Article.objects.filter(title__contains=keyword)
        # sadece aramalarda cikan article lar gelecek
        return render(request, "articles.html", {"articles": articles})

    # tum article lari aldik
    articles = Article.objects.all()
    return render(request, "articles.html", {"articles": articles})


def index(request):
    context = {
        "numbers": [1, 2, 3, 4, 5, 6]
    }
    return render(request, "index.html", context)


def about(request):
    return render(request, "about.html")


def detail(request, id):
    # article = Article.objects.filter(id = id ).first()#ilk elemani aldik filter liste halinde getiriyor
    # id var ise getir yoksa 404 getir
    article = get_object_or_404(Article, id=id)

    # Comment yorum alani related_name = comments ile erisiyoruz
    comments = article.comments.all()
    return render(request, "detail.html", {"article": article, "comments": comments})


# Giris yapilmamissa bizi login sayfamiza yonledirecektir
@login_required(login_url="user:login")
def dashboard(request):
    # sadece giris yapmis kullanicin makalelerini almak icin filter metodu
    articles = Article.objects.filter(author=request.user)
    context = {
        "articles": articles
    }
    return render(request, "dashboard.html", context)

# Giris yapilmamissa bizi login sayfamiza yonledirecektir


@login_required(login_url="user:login")
def addArticle(request):
    # Form Kayit
    # request.POST bizim yazi alanlarimizi yukler
    # request.FILES ise bizim fotograf veya dosyalarimi yukler

    form = ArticleForm(request.POST or None, request.FILES or None)
    if form.is_valid():

        article = form.save(commit=False)
        # hangi kullanici giris yapmissa makale ona gore eklenecek
        article.author = request.user
        # aslinda kayit bu satirdan sonra oluyor cunku ustteki save() commit=false yaptik bilerek
        article.save()
        messages.success(request, "Makale basariyla olusturuldu")
        return redirect("article:dashboard")

    return render(request, "addarticle.html", {"form": form})

# Giris yapilmamissa bizi login sayfamiza yonledirecektir


@login_required(login_url="user:login")
def updateArticle(request, id):

    article = get_object_or_404(Article, id=id)
    form = ArticleForm(request.POST or None,
                       request.FILES or None, instance=article)
    if form.is_valid():

        article = form.save(commit=False)
        # hangi kullanici giris yapmissa makale ona gore eklenecek
        article.author = request.user
        # aslinda kayit bu satirdan sonra oluyor cunku ustteki save() commit=false yaptik bilerek
        article.save()
        messages.success(request, "Makale basariyla guncellendi")
        return redirect("article:dashboard")

    return render(request, "update.html", {"form": form})

# Giris yapilmamissa bizi login sayfamiza yonledirecektir


@login_required(login_url="user:login")
def deleteArticle(request, id):

    article = get_object_or_404(Article, id=id)
    article.delete()

    messages.success(request, "Makale basariyla silindi.")

    return redirect("article:dashboard")


def addComment(request, id):
    article = get_object_or_404(Article, id=id)

    if request.method == "POST":
        comment_author = request.POST.get("comment_author")
        comment_content = request.POST.get("comment_content")

        newComment = Comment(comment_author=comment_author,
                             comment_content=comment_content)

        newComment.article = article

        newComment.save()
    # reverse dinamik url ile redirect
    return redirect(reverse("article:detail", kwargs={"id": id}))
