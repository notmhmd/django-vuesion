from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from .models import *


class BookListSerializer(serializers.ModelSerializer):
    uploaded_by = serializers.StringRelatedField()

    class Meta:
        model = Book
        fields = ['id', 'book_cover', 'title', 'description', 'approved', 'uploaded_by', 'author']
        extra_kwargs = {
            'book_cover': {'read_only': True},
            'uploaded_by': {'read_only': True}
        }


class BookDetailSerializer(serializers.ModelSerializer):
    uploaded_by = serializers.StringRelatedField()

    class Meta:
        model = Book
        fields = ['id', 'book_cover', 'title', 'description', 'approved', 'uploaded_by',
                  'author', 'approved_at', 'document', 'link', 'comments']


class FileUploadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = ['id', 'document', 'book_cover']


class CoverUploadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = ['book_cover']


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    book = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = '__all__'

