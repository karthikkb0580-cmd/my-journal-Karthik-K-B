from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ArticleForm
from .models import Article, Category



def home(request):
    latest_articles = Article.objects.filter(is_published=True).select_related("author")[:5]
    return render(request, "journal/home.html", {"latest_articles": latest_articles})


def article_list(request):
    articles = (
        Article.objects.filter(is_published=True)
        .select_related("author")
        .prefetch_related("categories")
    )

    query = request.GET.get("q", "").strip()
    if query:
        articles = articles.filter(
            Q(title__icontains=query)
            | Q(subtitle__icontains=query)
            | Q(body__icontains=query)
        )

    category_id = request.GET.get("category")
    if category_id:
        articles = articles.filter(categories__id=category_id)

    return render(request, "journal/article_list.html", {
        "articles": articles.distinct(),
        "categories": Category.objects.all(),
        "query": query,
        "selected_category": category_id,
    })


def article_detail(request, pk):
    article = get_object_or_404(
        Article.objects.select_related("author").prefetch_related("categories"),
        pk=pk,
        is_published=True,
    )
    return render(request, "journal/article_detail.html", {"article": article})

@login_required
def my_articles(request):
    articles = Article.objects.filter(author=request.user).prefetch_related("categories")
    return render(request, "journal/my_articles.html", {"articles": articles})


@login_required
def article_create(request):
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)   # build the article, but don't save yet
            article.author = request.user       # the SERVER decides the author
            article.save()                      # now save it
            form.save_m2m()                     # then save the categories (many-to-many)
            return redirect("journal:my_articles")
    else:
        form = ArticleForm()
    return render(request, "journal/article_form.html", {
        "form": form,
        "page_heading": "Create an article",
    })


@login_required
def article_update(request, pk):
    article = get_object_or_404(Article, pk=pk, author=request.user)   # ownership check
    if request.method == "POST":
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect("journal:my_articles")
    else:
        form = ArticleForm(instance=article)
    return render(request, "journal/article_form.html", {
        "form": form,
        "page_heading": "Edit an article",
    })


@login_required
def article_delete(request, pk):
    article = get_object_or_404(Article, pk=pk, author=request.user)   # ownership check
    if request.method == "POST":
        article.delete()
        return redirect("journal:my_articles")
    return render(request, "journal/article_confirm_delete.html", {"article": article})
