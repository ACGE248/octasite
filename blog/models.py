from django.db import models
from django.contrib.auth import get_user_model
import datetime
from django import forms
from django.db import models
from django.db.models import Q
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.tags import ClusterTaggableManager
from taggit.models import TaggedItemBase, Tag as TaggitTag
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet
from .utils import MarkdownField, MarkdownPanel
class BlogPage(RoutablePageMixin, Page):
    description = models.CharField(max_length=255, blank=True, )
    content_panels = Page.content_panels + [
    FieldPanel('description', classname="full")
     ]
    def get_context(self, request, *args, **kwargs):
        context = super(BlogPage, self).get_context(request, *args,**kwargs)
        context['posts'] = self.posts
        context['blog_page'] = self
        context['search_type'] = getattr(self, 'search_type', "")
        context['search_term'] = getattr(self, 'search_term', "")
        context["categories"] = BlogCategory.objects.all()
        context["tags"] = BlogPageTag.objects.all()
        all_posts = BlogPage.objects.live().public().order_by('-first_published_at')
        if request.GET.get('tag', None):
            tags = request.GET.get('tag')
            all_posts = self.posts.filter(tags__slug__in=[tags])
            context["posts"] = all_posts
        if request.GET.get('cat', None):
            cats = request.GET.get('cat')
            all_posts = self.posts.filter(categories__slug__in=[cats])
            context["posts"] = all_posts        
        return context
    def get_posts(self):
        return PostPage.objects.descendant_of(self).live().order_by('-date')
    @route(r'^$')
    def post_list(self, request, *args, **kwargs):
        self.posts = self.get_posts()
        return Page.serve(self, request, *args, **kwargs)
    @route(r'^search/$')
    def post_search(self, request, *args, **kwargs):
        search_query = request.GET.get('q', None)
        self.posts = self.get_posts()
        if search_query:
            self.posts = self.posts.filter(
        Q(body__icontains=search_query) | Q(title__icontains=search_query) | Q(excerpt__icontains=search_query))
        self.search_term = search_query
        self.search_type = 'search'
        return Page.serve(self, request, *args, **kwargs)
class PostPage(Page):
    body = RichTextField()
    date = models.DateTimeField(verbose_name="Post date", default=datetime.datetime.today)
    excerpt = MarkdownField(verbose_name='excerpt', blank=True,)
    header_image = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',)
    categories = ParentalManyToManyField('blog.BlogCategory', blank=True)
    tags = ClusterTaggableManager(through='blog.BlogPageTag', blank=True)
    content_panels = Page.content_panels + [
        ImageChooserPanel('header_image'),
        MarkdownPanel("body"),
        MarkdownPanel("excerpt"),
        FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
        FieldPanel('tags'),
    ]
    settings_panels = Page.settings_panels + [
        FieldPanel('date'),
    ]
    @property
    def blog_page(self):
        return self.get_parent().specific
    def get_context(self, request, *args, **kwargs):
        context = super(PostPage, self).get_context(request, *args, **kwargs)
        context['blog_page'] = self.blog_page
        context['post'] = self
        context["categories"] = BlogCategory.objects.all()
        context["tags"] = BlogPageTag.objects.all()
        if request.user:
            if not request.user.is_staff and not request.user.is_superuser:
                self.page_views = self.page_views + 1
                self.save()
        return context
    def get_absolute_url(self):
        return self.url
@register_snippet
class BlogCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=80)
    panels = [
        FieldPanel('name'),
        FieldPanel('slug'),
    ]
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey('PostPage', related_name='post_tags')
@register_snippet
class Tag(TaggitTag):
    class Meta:
        proxy = True
        
User = get_user_model()


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField()

    def __str__(self):
        return self.user.username
    
class Category(models.Model):
    title = models.CharField(max_length=20)
    subtitle = models.CharField(max_length=20)
    slug = models.SlugField()
    thumbnail = models.ImageField()

    def __str__(self):
        return self.title

class Post(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    overview = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    thumbnail = models.ImageField()
    categories = models.ManyToManyField(Category)
    featured = models.BooleanField()

    def __str__(self):
        return self.title

class HomePage(Page):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]
class BlogIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro')
    ]
    def get_context(self, request):
            # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        blogpages = self.get_children().live().order_by('-first_published_at')
        context['blogpages'] = blogpages
        return context
class BlogListingPage(RoutablePageMixin, Page):
    """Listing page lists all the Blog Detail Pages."""

    # Fields and panels

    def get_context(self, request, *args, **kwargs):
        """Adding custom stuff to our context."""
        context = super().get_context(request, *args, **kwargs)
        # Get all posts
        all_posts = BlogPage.objects.live().public().order_by('-first_published_at')

        if request.GET.get('tag', None):
            tags = request.GET.get('tag')
            all_posts = all_posts.filter(tags__slug__in=[tags])

        context["posts"] = all_posts
        return context