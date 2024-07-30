from django.shortcuts import render
from .models import *
from .serializers import *
# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
import base64
from django.core.files.base import ContentFile
from django.utils.text import slugify
from django.core.mail import send_mail, EmailMessage
from content.models import *
from django.utils.crypto import get_random_string
import threading
@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @login_required
# @permission_required(['auth.view_user'], raise_exception=True)
def sendMail(request):
    try:


        if SettingsEmail.objects.all().exists():
            email = SettingsEmail.objects.all().last().email

            thread = threading.Thread(target=sendtoSpecificMail, args=(request.data, email))
            thread.start()
            return Response({
                'code': status.HTTP_200_OK,
                'response': "Successfully Sent Email",

            })
        else:
            return Response({
                'code': status.HTTP_400_BAD_REQUEST,
                'response': "Entered Email is not valid.",

            })

    except Exception as e:
        system_manager.views.log(request.path, e)
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'response': "Email send Failed",
            "error": str(e)

        })


def sendtoSpecificMail(data, email):
    print(data)
    subject = data.get('subject')
    email_body =data.get('body')

    email_from = f'Support <support@nextcart.shop>'
    recipient_list = [email]
    mail_send = EmailMessage(
        subject=subject,
        to=recipient_list,
        from_email=email_from,
        body=email_body
    )
    mail_send.content_subtype = "html"
    mail_send.send()

# # NewsLetter


# @api_view(['GET'])
# # @login_required
# def newsletter(request):
#     try:
#         news = Newsletter.objects.all()
#         serializer = NewsletterSerializer(news, many=True)
#         return Response({
#             'code': status.HTTP_200_OK,
#             'response': "Received Data Successfully",
#             "data": serializer.data
#         })
#     except Exception as e:
#         return Response({
#             'code': status.HTTP_400_BAD_REQUEST,
#             'response': "Data not Found",
#             'error': str(e)
#         })


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def newsletterCreate(request):
#     try:
#         data = request.data
#         serializer = NewsletterSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({
#                 'code': status.HTTP_200_OK,
#                 'response': "Created Successfully",
#                 "data": serializer.data
#             })
#         else:
#             return Response({
#                 'code': status.HTTP_400_BAD_REQUEST,
#                 'response': "Data not Valid",
#                 'error': serializer.errors
#             })
#     except Exception as e:
#         return Response({
#             'code': status.HTTP_400_BAD_REQUEST,
#             'response': "Data not Found",
#             'error': str(e)
#         })


# @api_view(['PATCH'])
# @permission_classes([IsAuthenticated])
# def newsletterEdit(request, pk):
#     try:

#         data = request.data
#         news = Newsletter.objects.get(id=pk)
#         serializer = NewsletterSerializer(news, data=data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({
#                 'code': status.HTTP_200_OK,
#                 'response': "Updated Successfully",
#                 "data": serializer.data
#             })
#         else:
#             return Response({
#                 'code': status.HTTP_400_BAD_REQUEST,
#                 'response': "Data not Valid",
#                 'error': serializer.errors
#             })
#     except Exception as e:
#         return Response({
#             'code': status.HTTP_400_BAD_REQUEST,
#             'response': "Data not Found",
#             'error': str(e)
#         })


# @api_view(['DELETE'])
# @permission_classes([IsAuthenticated])
# def newsletterDelete(request, pk):
#     try:
#         trainingType = Newsletter.objects.get(id=pk)
#         trainingType.delete()
#         return Response({
#             'code': status.HTTP_200_OK,
#             'response': "Deleted"
#         })
#     except Exception as e:
#         return Response({
#             'code': status.HTTP_400_BAD_REQUEST,
#             'response': "Data not Found",
#             'error': str(e)
#         })
    
# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def toggleNewsStatus(request, pk):
#     try:
#         news = Newsletter.objects.get(id=pk)
#         news.published = not news.published
#         news.save()
#         serializer = NewsletterSerializer(news)
#         return Response({
#                 'code': status.HTTP_200_OK,
#                 'response': "Publish Status Toggled Successfully",
#                 'data': serializer.data

#             })

#     except Exception as e:
#         return Response({
#             'code': status.HTTP_400_BAD_REQUEST,
#             'response': "Data not found",
#             'error': str(e)
#         })
