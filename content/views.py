from django.shortcuts import render

from system_manager.helper import generate_unique_slug
from .models import *
from .serializers import *
# Create your views here.
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
import base64
from django.core.files.base import ContentFile
from django.utils.text import slugify

from django.utils.dateparse import parse_date
from django.utils import timezone
from rest_framework.pagination import PageNumberPagination




### Gallery


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def content(request):
    try:
        # g = Content.objects.all().order_by('-id')
        
        start_date_str = request.query_params.get('start_date')
        end_date_str = request.query_params.get('end_date')

        if start_date_str and end_date_str:
            start_date = parse_date(start_date_str)
            end_date = parse_date(end_date_str)
        
            if start_date_str == "null" and end_date_str == "null":
                g = Content.objects.all().order_by('-id')
                
            elif start_date_str == "null":
                g = Content.objects.filter(created_at__date__lte=end_date).order_by('-id')
            elif end_date_str == "null":
                g = Content.objects.filter(created_at__date__gte=start_date).order_by('-id')
            
            else:
                g = Content.objects.filter(created_at__date__range=(start_date, end_date)).order_by('-id')
                
        else:
            g = Content.objects.all().order_by('-id')
        
        serializer = ContentReadSerializer(g, many=True, context={'request': request})
        return Response({
            'code': status.HTTP_200_OK,
            'response': "Received Data Successfully",
            "data": serializer.data
        })
    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'response': "Data not Found",
            'error': str(e)
        })
        
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def contentPaginated(request):
    try:
        # g = Content.objects.all().order_by('-id')
        
        start_date_str = request.query_params.get('start_date')
        end_date_str = request.query_params.get('end_date')

        if start_date_str and end_date_str:
            start_date = parse_date(start_date_str)
            end_date = parse_date(end_date_str)
        
            if start_date_str == "null" and end_date_str == "null":
                g = Content.objects.all().order_by('-id')
                
            elif start_date_str == "null":
                g = Content.objects.filter(created_at__date__lte=end_date).order_by('-id')
            elif end_date_str == "null":
                g = Content.objects.filter(created_at__date__gte=start_date).order_by('-id')
            
            else:
                g = Content.objects.filter(created_at__date__range=(start_date, end_date)).order_by('-id')
                
        else:
            g = Content.objects.all().order_by('-id')
        
        paginator = PageNumberPagination()
        paginator.page_size = request.GET['count']
        result_page = paginator.paginate_queryset(g, request)
        
        
        result_serializer = ContentReadSerializer(result_page, many=True, context={'request': request})
        response = paginator.get_paginated_response(result_serializer.data)
        response = {
            'code': status.HTTP_200_OK,
            'message': 'Received Data Successfully',
            'pg_count': response.data['count'],
            'next': response.data['next'],
            'previous': response.data['previous'],
            'results': response.data['results']
        }

        return Response(response)
    
    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'response': "Data not Found",
            'error': str(e)
        })


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def getEmailSettings(request):
    try:
        g = SettingsEmail.objects.all().last()
        serializer = SettingsReadSerializer(g, context={'request': request})
        return Response({
            'code': status.HTTP_200_OK,
            'response': "Received Data Successfully",
            "data": serializer.data
        })
    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'response': "Data not Found",
            'error': str(e)
        })


@api_view(['GET'])
def contentDetails(request, slug):
    try:
        g = Content.objects.get(slug__exact=slug)
        serializer = ContentSerializer(g)
        return Response({
            'code': status.HTTP_200_OK,
            'response': "Received Data Successfully",
            "data": serializer.data
        })

    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'response': "Data not Found",
            'error': str(e)
        })


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def settingsEdit(request):
    try:
        data = request.data
        g = SettingsEmail.objects.all().last()
        if ('image' in data and data['image'] == None) and g.image != None:
            data.pop('image')

        if 'image' in data and data['image'] != None:
            fmt, img_str = str(data['image']).split(';base64,')
            ext = fmt.split('/')[-1]
            img_file = ContentFile(base64.b64decode(img_str), name='temp.' + ext)
            data['image'] = img_file

        serializer = SettingsSerializer(g, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'code': status.HTTP_200_OK,
                'response': "Settings Updated Successfully",
                "data": serializer.data
            })
        else:
            return Response({
                'code': status.HTTP_400_BAD_REQUEST,
                'response': "Data not Valid",
                'error': serializer.errors
            })
    except SettingsEmail.DoesNotExist:
        data = request.data
        if ('image' in data and data['image'] == None) and g.image != None:
            data.pop('image')

        if 'image' in data and data['image'] != None:
            fmt, img_str = str(data['image']).split(';base64,')
            ext = fmt.split('/')[-1]
            img_file = ContentFile(base64.b64decode(img_str), name='temp.' + ext)
            data['image'] = img_file

        serializer = SettingsSerializer(data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'code': status.HTTP_200_OK,
                'response': "Settings Updated Successfully",
                "data": serializer.data
            })
        else:
            return Response({
                'code': status.HTTP_400_BAD_REQUEST,
                'response': "Data not Found",
            })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def contentCreate(request):
    try:
        data = request.data

        if 'image' in data and data['image'] != None:
            fmt, img_str = str(data['image']).split(';base64,')
            ext = fmt.split('/')[-1]
            img_file = ContentFile(base64.b64decode(img_str), name='temp.' + ext)
            data['image'] = img_file
        suffix = 1
        if Content.objects.filter(title__exact=data['title']).exists():
            print("yes")
            count = Content.objects.filter(title__exact=data['title']).count()
            print(count)
            suffix += count
            print("yes")
            slug = "%s-%s" % (slugify(data['title']), suffix)

        else:
            print("No")
            slug = "%s-%s" % (slugify(data['title']), suffix)

        data['slug'] = slug
        serializer = ContentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'code': status.HTTP_200_OK,
                'response': "Content Created Successfully",
                "data": serializer.data
            })
        else:
            return Response({
                'code': status.HTTP_400_BAD_REQUEST,
                'response': "Data not Valid",
                'error': serializer.errors
            })
    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'response': "Data not Found",
            'error': str(e)
        })
        



@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def contentEdit(request, pk):
    try:

        data = request.data
        g = Content.objects.get(id=pk)

        if ('image' in data and data['image'] == None) and g.image != None:
            data.pop('image')

        if 'image' in data and data['image'] != None:
            fmt, img_str = str(data['image']).split(';base64,')
            ext = fmt.split('/')[-1]
            img_file = ContentFile(base64.b64decode(img_str), name='temp.' + ext)
            data['image'] = img_file
        suffix = 1
        if Content.objects.filter(title__exact=data['title']).exists():
            print("yes")
            count = Content.objects.filter(title__exact=data['title']).count()
            print(count)
            suffix += count
            print("yes")
            slug = "%s-%s" % (slugify(data['title']), suffix)

        else:
            print("No")
            slug = "%s-%s" % (slugify(data['title']), suffix)

        data['slug'] = slug
        serializer = ContentSerializer(g, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'code': status.HTTP_200_OK,
                'response': "Content Updated Successfully",
                "data": serializer.data
            })
        else:
            return Response({
                'code': status.HTTP_400_BAD_REQUEST,
                'response': "Data not Valid",
                'error': serializer.errors
            })
    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'response': "Data not Found",
            'error': str(e)
        })


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def contentDelete(request, pk):
    try:
        g = Content.objects.get(id=pk)
        g.delete()
        return Response({
            'code': status.HTTP_200_OK,
            'response': "Data Deleted"
        })
    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'response': "Data not Found",
            'error': str(e)
        })


#Layout

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def layout(request):
    try:
        # g = Layout.objects.all()
        
        
        start_date_str = request.query_params.get('start_date')
        end_date_str = request.query_params.get('end_date')

        if start_date_str and end_date_str:
            start_date = parse_date(start_date_str)
            end_date = parse_date(end_date_str)
            
        #     g = Layout.objects.filter(published_at__date__range=(start_date, end_date))
            
        #     if start_date_str == "null":
                
        #         end_date = parse_date(end_date_str)
        #         g = Layout.objects.filter(published_at__date__lte=end_date)
                
        #     if end_date_str == "null":
                
        #         start_date = parse_date(start_date_str)
        #         g = Layout.objects.filter(published_at__date__gte=start_date)
        
            if start_date_str == "null":
                g = Layout.objects.filter(published_at__date__lte=end_date).order_by('-id')
            elif end_date_str == "null":
                g = Layout.objects.filter(published_at__date__gte=start_date).order_by('-id')
            else:
                g = Layout.objects.filter(published_at__date__range=(start_date, end_date)).order_by('-id')
                
        else:
            g = Layout.objects.all().order_by('-id')
        
    
        serializer = LayoutSerializer(g, many=True)
            
        return Response({
            'code': status.HTTP_200_OK,
            'response': "Received Data Successfully",
            "data": serializer.data
        })
    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'response': "Data not Found",
            'error': str(e)
        })
        
@api_view(['GET'])
def layoutFiltered(request, pub_st):
    try:
        start_date_str = request.query_params.get('start_date')
        end_date_str = request.query_params.get('end_date')

        if start_date_str and end_date_str:
            start_date = parse_date(start_date_str)
            end_date = parse_date(end_date_str)

            if not start_date and not end_date:
                return Response({
                    'code': status.HTTP_400_BAD_REQUEST,
                    'response': "Invalid date format. Please use YYYY-MM-DD format.",
                })
            g = Layout.objects.filter(published=pub_st, published_at__date__range=(start_date, end_date)).order_by('-id')
                
        elif start_date_str:
            start_date = parse_date(start_date_str)

            if not start_date:
                return Response({
                    'code': status.HTTP_400_BAD_REQUEST,
                    'response': "Invalid start_date format. Please use YYYY-MM-DD format.",
                })

            g = Layout.objects.filter(published=pub_st, published_at__date__gte=start_date).order_by('-id')
            
        elif end_date_str:
            end_date = parse_date(end_date_str)

            if not end_date:
                return Response({
                    'code': status.HTTP_400_BAD_REQUEST,
                    'response': "Invalid end_date format. Please use YYYY-MM-DD format.",
                })

            g = Layout.objects.filter(published=pub_st, published_at__date__lte=end_date).order_by('-id')
        else:
            g = Layout.objects.filter(published=pub_st).order_by('-id')

        serializer = LayoutSerializer(g, many=True)
        return Response({
            'code': status.HTTP_200_OK,
            'response': "Received Data Successfully",
            "data": serializer.data
        })
    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'response': "Data not Found",
            'error': str(e)
        })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def layoutCreate(request):
    try:
        data = request.data

        serializer = LayoutSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'code': status.HTTP_200_OK,
                'response': "Layout Created Successfully",
                "data": serializer.data
            })
        else:
            return Response({
                'code': status.HTTP_400_BAD_REQUEST,
                'response': "Data not Valid",
                'error': serializer.errors
            })
    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'response': "Data not Found",
            'error': str(e)
        })
        
        
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def layoutEdit(request, pk):
    try:

        data = request.data
        g = Layout.objects.get(id=pk)

        serializer = LayoutSerializer(g, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'code': status.HTTP_200_OK,
                'response': "Layout Updated Successfully",
                "data": serializer.data
            })
        else:
            return Response({
                'code': status.HTTP_400_BAD_REQUEST,
                'response': "Data not Valid",
                'error': serializer.errors
            })
    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'response': "Data not Found",
            'error': str(e)
        })
        
@api_view(['GET'])
def layoutDetails(request, pk):
    try:
        g = Layout.objects.get(id=pk)
        serializer = LayoutSerializer(g)
        return Response({
            'code': status.HTTP_200_OK,
            'response': "Received Data Successfully",
            "data": serializer.data
        })

    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'response': "Data not Found",
            'error': str(e)
        })
        
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def layoutDelete(request, pk):
    try:
        g = Layout.objects.get(id=pk)
        g.delete()
        return Response({
            'code': status.HTTP_200_OK,
            'response': "Data Deleted"
        })
    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'response': "Data not Found",
            'error': str(e)
        })
        
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def toggleLayoutStatus(request, pk):
    try:
        layout_instance = Layout.objects.get(id=pk)
        layout_instance.published = not layout_instance.published
        
        if layout_instance.published:
            layout_instance.published_at = timezone.now()
        else:
            layout_instance.published_at = None
        
        layout_instance.save()
        
        serializer = LayoutSerializer(layout_instance)
        return Response({
                'code': status.HTTP_200_OK,
                'response': "Publish Status Toggled Successfully",
                'data': serializer.data

            })

    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'response': "Data not found",
            'error': str(e)
        })

        
from rest_framework.parsers import MultiPartParser, FormParser       
#Blogs

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def getBlogs(request):
    try:
        
        start_date_str = request.query_params.get('start_date')
        end_date_str = request.query_params.get('end_date')

        if start_date_str and end_date_str:
            start_date = parse_date(start_date_str)
            end_date = parse_date(end_date_str)
        
            if start_date_str == "null" and end_date_str == "null":
                g = Blogs.objects.all().order_by('-id')
                
            elif start_date_str == "null":
                g = Blogs.objects.filter(created_at__date__lte=end_date).order_by('-id')
            elif end_date_str == "null":
                g = Blogs.objects.filter(created_at__date__gte=start_date).order_by('-id')
            
            else:
                g = Blogs.objects.filter(created_at__date__range=(start_date, end_date)).order_by('-id')
                
        
        else:
            g = Blogs.objects.all().order_by('-id')
        
        
        serializer = BlogSerializer(g, many=True)
        return Response({
            'code': status.HTTP_200_OK,
            'response': "Received Data Successfully",
            "data": serializer.data
        })
    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'response': "Data not Found",
            'error': str(e)
        })
        
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def getBlogsPaginated(request):
    try:
        
        start_date_str = request.query_params.get('start_date')
        end_date_str = request.query_params.get('end_date')

        if start_date_str and end_date_str:
            start_date = parse_date(start_date_str)
            end_date = parse_date(end_date_str)
        
            if start_date_str == "null" and end_date_str == "null":
                g = Blogs.objects.all().order_by('-id')
                
            elif start_date_str == "null":
                g = Blogs.objects.filter(created_at__date__lte=end_date).order_by('-id')
            elif end_date_str == "null":
                g = Blogs.objects.filter(created_at__date__gte=start_date).order_by('-id')
            
            else:
                g = Blogs.objects.filter(created_at__date__range=(start_date, end_date)).order_by('-id')
                
        
        else:
            g = Blogs.objects.all().order_by('-id')
            
        
        paginator = PageNumberPagination()
        paginator.page_size = request.GET['count']
        result_page = paginator.paginate_queryset(g, request)
        
        result_serializer = BlogSerializer(result_page, many=True)
        response = paginator.get_paginated_response(result_serializer.data)
        response = {
            'code': status.HTTP_200_OK,
            'message': 'Received Data Successfully',
            'pg_count': response.data['count'],
            'next': response.data['next'],
            'previous': response.data['previous'],
            'results': response.data['results']
        }
        
        return Response(response)
    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'response': "Data not Found",
            'error': str(e)
        })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def createBlog(request):
    try:
        project_data = request.POST.dict()
        if 'file' in request.FILES:
            project_data['file'] = request.FILES['file']
        else:
            # Assign default file path to 'pdf' field
            project_data['file'] = None

        serializer = BlogSerializer(data=project_data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'code': status.HTTP_200_OK,
                'response': "File created Successfully",
                "data": serializer.data
            })
        else:
            return Response({
                'code': status.HTTP_400_BAD_REQUEST,
                'response': "Data not Valid",
                'error': serializer.errors
            })
    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'response': "Data not Found",
            'error': str(e)
        })

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteBlog(request, pk):
    try:
        project = Blogs.objects.get(id=pk)
        project.delete()
        return Response({
            'code': status.HTTP_200_OK,
            'response': "Data Deleted"
        })
    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'response': "Data not Found",
            'error': str(e)
        })
        
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def contentDraft(request):
    try:

        try:
            eod_draft = LayoutDraft.objects.all().last()
            serializer = LayouttDraftSerializer(eod_draft)
            return Response({
                'code': status.HTTP_200_OK,
                'response': "Content Draft Retrieved Successfully",
                'data': serializer.data
            })
        except LayoutDraft.DoesNotExist:
            null_data = {
                'subject': None,
                'inner_html': None,
                'value': None
            }
            return Response({
                'code': status.HTTP_200_OK,
                'response': "No Content Drafts found for today",
                'data': null_data
            })
    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'response': "Data not Found",
            'error': str(e)
        })
        
        
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def contentDraftEdit(request):
    try:
        data = request.data
        g = LayoutDraft.objects.all().last()
        

        serializer = LayouttDraftSerializer(g, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'code': status.HTTP_200_OK,
                'response': "Layout Draft Updated Successfully",
                "data": serializer.data
            })
        else:
            return Response({
                'code': status.HTTP_400_BAD_REQUEST,
                'response': "Data not Valid",
                'error': serializer.errors
            })
    except LayoutDraft.DoesNotExist:
        data = request.data
        # if ('image' in data and data['image'] == None) and g.image != None:
        #     data.pop('image')

    

        serializer = LayouttDraftSerializer(data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'code': status.HTTP_200_OK,
                'response': "Layout Draft Updated Successfully",
                "data": serializer.data
            })
        else:
            return Response({
                'code': status.HTTP_400_BAD_REQUEST,
                'response': "Data not Found",
            })
        
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def contentDraftDelete(request, pk):
    try:
        eod = LayoutDraft.objects.get(id=pk)
        eod.delete()
        return Response({
            'code': status.HTTP_200_OK,
            'response': "Ticket Deleted"
        })
    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'response': "Data not Found",
            'error': str(e)
        })
        