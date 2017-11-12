# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Max
from django.template.loader import get_template
from django.db.models import Q
from django import forms


class RegToken(models.Model):
    user_id = models.ForeignKey(User)
    token = models.TextField()


class UserInfo(models.Model):
    age = models.IntegerField(null=True)
    short_bio = models.TextField(max_length=420, null=True)
    profile_picture = models.ImageField(upload_to='grumblr/images/profile_picture', null=True)
    user_id = models.OneToOneField(User, related_name='userinfo')


class Following(models.Model):
    user = models.ForeignKey(User, related_name='profile', default='')
    follow = models.ForeignKey(User, related_name='follow', default='')

    class Meta:
        unique_together = (("user", "follow"),)


class BlogPost(models.Model):
    blog_text = models.CharField(max_length=42)
    published_time = models.DateTimeField(auto_now=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.blog_text

    def __str__(self):
        return self.__unicode__()

    # Returns all recent additions
    @staticmethod
    def get_items(time="1970-01-01T00:00+00:00", username=''):
        try:
            following = Following.objects.filter(user=username)
        except ObjectDoesNotExist:
            return BlogPost.objects.order_by('-published_time').filter(published_time__gt=time).filter(
                user_id=username).distinct()
            # https://stackoverflow.com/questions/739776/django-filters-or

        return BlogPost.objects.order_by('-published_time').filter(published_time__gt=time).filter(
            Q(user_id__in=following.values_list('follow', flat=True)) | Q(user_id=username)).distinct()
        # Returns all recent additions

    @staticmethod
    def get_profile_items(time="1970-01-01T00:00+00:00", username=''):
        return BlogPost.objects.filter(published_time__gt=time).filter(user_id=username).order_by('-published_time').distinct()

    @property
    def html(self):
        template = get_template('grumblr/blogpost.html')
        context = {}
        context['item'] = self
        context['form'] = AddCommentForm(id=self.id)
        # https://djangobook.com/templates-in-views/
        return template.render(context)

    @staticmethod
    def get_max_time():
        return BlogPost.objects.all().aggregate(Max('published_time'))[
                   'published_time__max'] or "1970-01-01T00:00+00:00"

class Comment(models.Model):
    comment_text = models.CharField(max_length=42)
    published_time = models.DateTimeField(auto_now=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    blogpost_id = models.ForeignKey(BlogPost, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.comment_text

    def __str__(self):
        return self.__unicode__()

    # Returns all recent additions
    @staticmethod
    def get_comments(time="1970-01-01T00:00+00:00", blogpostid=''):
        blogpost = BlogPost.objects.get(id=blogpostid)
        return Comment.objects.order_by('-published_time').filter(published_time__gt=time).filter(blogpost_id=blogpost).distinct()
        # Returns all recent additions

    @property
    def html(self):
        template = get_template('grumblr/comments.html')
        context = {}
        context['comment'] = self
        # https://djangobook.com/templates-in-views/
        return template.render(context)

    @staticmethod
    def get_max_time_comment():
        return Comment.objects.all().aggregate(Max('published_time'))[
                   'published_time__max'] or "1970-01-01T00:00+00:00"

#https://docs.djangoproject.com/en/1.11/topics/forms/modelforms/
class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment_text',)

    def clean(self):
        return super(AddCommentForm, self).clean()

    def __init__(self, *args, **kwargs):
        self.blogpost_id = kwargs.pop('id')
        super(AddCommentForm, self).__init__(*args, **kwargs)

        self.fields['comment_text'].widget = forms.Textarea(attrs={'class': 'text-post', 'rows':'5', 'maxlength':'42', 'id':'new_comment-' + str(self.blogpost_id)})