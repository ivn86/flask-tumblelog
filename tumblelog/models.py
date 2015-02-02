# -*- coding: utf-8 -*-
import datetime
from flask import url_for
from tumblelog import db


class Post(db.DynamicDocument):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    title = db.StringField(verbose_name=u"Заголовок", max_length=255, required=True)
    slug = db.StringField(max_length=255, required=True)
    comments = db.ListField(db.EmbeddedDocumentField('Comment'))

    def get_absolute_url(self):
        return url_for('post', kwargs={"slug": self.slug})

    def __unicode__(self):
        return self.title

    @property
    def post_type(self):
        return self.__class__.__name__

    meta = {
        'allow_inheritance': True,
        'indexes': ['-created_at', 'slug'],
        'ordering': ['-created_at']
    }

class BlogPost(Post):
    body = db.StringField(verbose_name=u"Текст",required=True)


class Video(Post):
    embed_code = db.StringField(verbose_name=u"Код для блога",required=True)


class Image(Post):
    image_url = db.StringField(verbose_name=u"URL картинки",required=True, max_length=255)


class Quote(Post):
    body = db.StringField(verbose_name=u"Цитата",required=True)
    author = db.StringField(verbose_name=u"Имя автора", required=True, max_length=255)


class Comment(db.EmbeddedDocument):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    body = db.StringField(verbose_name=u"Комментарий", required=True)
    author = db.StringField(verbose_name=u"Имя", max_length=255, required=True)
