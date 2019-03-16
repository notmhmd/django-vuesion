from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.authentication import TokenAuthentication
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_201_CREATED
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from rest_framework.parsers import FileUploadParser
from rest_framework.views import APIView
from rest_framework import parsers
from rest_framework import viewsets
from rest_framework import decorators


from .models import *
from .forms import BookForm
from .serializers import BookListSerializer, BookDetailSerializer,\
    FileUploadSerializer, CoverUploadSerializer, CommentSerializer
# Create your views here.


class BookApprovalApiView(ListCreateAPIView):
    model = Book
    queryset = Book.objects.all()
    authentication_classes = [TokenAuthentication]
    serializer_class = BookListSerializer

    def post(self, request, *args, **kwargs):
        book_title = request.data.get("title")
        book_author = request.data.get("author")
        book_description = request.data.get("description")
        book_cover = request.data["book_cover"]
        serial = self.serializer_class(data=request.data)
        if request.data.get("document") is not None:
            book_document = request.data.get("document")
            if serial.is_valid():
                book = Book(title=book_title, author=book_author, description=book_description)
                book.uploaded_by = request.user
                book.book_cover = book_cover
                book.document = book_document
                book.save()
                return Response(serial.data, status=HTTP_201_CREATED)
            return Response(serial.errors, status=HTTP_400_BAD_REQUEST)

        if serial.is_valid():
            book = Book(title=book_title, author=book_author, description=book_description)
            book.uploaded_by = request.user
            book.book_cover = book_cover
            book.save()
            return Response(serial.data, status=HTTP_201_CREATED)
        return Response(serial.errors, status=HTTP_400_BAD_REQUEST)


class BookManagementApiListView(ListAPIView):
    model = Book
    queryset = Book.objects.filter(approved=True)
    authentication_classes = [TokenAuthentication]
    serializer_class = BookDetailSerializer



class BookCommentApiListView(ListCreateAPIView):
    model = Book
    authentication_classes = [TokenAuthentication]
    serializer_class = CommentSerializer

    def get_queryset(self):
        book_id = self.kwargs.get("pk")
        book = self.model.objects.get(id=book_id)
        return book.comments.all()

    def post(self, request, *args, **kwargs):
        user = self.request.user
        book = self.model.objects.get(id=self.kwargs.get("pk"))
        text = self.request.data["text"]
        com = book.comments.create(author=user, book=book, text=text)
        serial = self.serializer_class(com)
        return Response(serial.data, status=HTTP_200_OK)


class BookManagementApiDetailView(RetrieveUpdateDestroyAPIView):
    model = Book
    queryset = Book.objects.filter(approved=True)
    authentication_classes = [TokenAuthentication]
    serializer_class = BookDetailSerializer


class BookUploadApiView(APIView):
    parser_classes = [FileUploadParser]

    def post(self, request, format=None):
        if 'file' not in request.data:
            raise ParseError("Empty Content")

        file = request.data['file']
        book_id = request.META["HTTP_X_BOOKID"]
        book = Book.objects.get(id=book_id)
        if book is None:
            raise ParseError("No Book With Such ID")

        book.document.save(file.name, file, save=True)
        book.save()
        file_serial = FileUploadSerializer(book)

        return Response(file_serial.data, status=HTTP_201_CREATED)


class CoverUploadApiView(viewsets.ModelViewSet):
    serializer_class = FileUploadSerializer
    queryset = Book.objects.filter(approved=True)

    @decorators.action(
        detail=True,
        methods=["PUT"],
        serializer_class=CoverUploadSerializer,
        parser_classes=[parsers.MultiPartParser, parsers.FormParser])
    def pic(self, request, pk):
        obj = self.get_object()
        serializer = self.serializer_class(obj, data=request.data, partial=True)
        if serializer.is_valid():
            file = request.data['file']
            obj.book_cover.save(file.name, file, save=True)
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, HTTP_400_BAD_REQUEST)



@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
def approve_book(request):
    book_id = request.data.get("book_id")
    if book_id is None:
        return Response({'error': 'please provide a valid Book ID'}, HTTP_400_BAD_REQUEST)
    book = Book.objects.get(id=book_id)
    user = request.user
    if not book:
        return Response({'error': 'Wrong Information'}, HTTP_404_NOT_FOUND)
    if book.approved:
        book.approve(user)
        return Response({'msg': "Book has been Disproved Successfully"}, HTTP_200_OK)
    else:
        book.approve(user)
        return Response({'msg': "Book has been Proved Successfully"}, HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
def approve_comment(request):
    comment_id = request.data.get("comment_id")
    if comment_id is None:
        return Response({'error': 'please provide a valid Comment ID'}, HTTP_400_BAD_REQUEST)
    comment = Comment.objects.get(id=comment_id)
    if not comment:
        return Response({'error': 'Wrong Information'}, HTTP_404_NOT_FOUND)
    if comment.approved_comment:
        comment.approve()
        return Response({'msg': "Comment has been Disproved Successfully"}, HTTP_200_OK)
    else:
        comment.approve()
        return Response({'msg': "Comment has been Proved Successfully"}, HTTP_200_OK)



