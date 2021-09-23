from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
from . import models
from .models import Profile, User_uuid, Rom
from .forms import ProfileForm, UserForm, User_uuidForm, Device_name_Form, Sensor_name_Form
from django.db.models import Count, Max, Min, Avg




#------------------------------------------------------------------------------
@login_required(login_url="/login/")
def index(request):
    uuid = models.User_uuid.objects.filter(user=request.user).values('UUID')
    devices = models.Rom.objects.filter(UUID__in=uuid, family_id='01')
    side_temp = models.Rom.objects.filter(family_id='28')

    context = {'devices':devices, 'side_temp':side_temp}
    context['segment'] = 'index'

    html_template = loader.get_template( 'index.html' )
    return HttpResponse(html_template.render(context, request))




#------------------------------------------------------------------------------

@login_required(login_url="/login/")
def profile(request):
    uuid = models.User_uuid.objects.filter(user=request.user).values('UUID')
    devices = models.Rom.objects.filter(UUID__in=uuid, family_id='01')
    side_temp = models.Rom.objects.filter(family_id='28')

    profile = models.Profile.objects.filter(user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            username = user_form.cleaned_data['username']
            first_name = user_form.cleaned_data['first_name']
            last_name = user_form.cleaned_data['last_name']
            email = user_form.cleaned_data['email']
            password1 = user_form.cleaned_data['password1']
            password2 = user_form.cleaned_data['password2']
            phone = profile_form.cleaned_data['phone']
            address = profile_form.cleaned_data['address']
            user_photo = profile_form.cleaned_data['user_photo']
            user_form.save()
            profile_form.save()
            context = {'user_form':user_form, 'profile_form':profile_form, 'devices':devices}
            context['segment'] = 'profile'

            html_template = loader.get_template( 'accounts/profile.html' )
            return HttpResponse(html_template.render(context, request))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

    context = {'user_form':user_form, 'profile_form':profile_form, 'side_temp':side_temp, 'devices':devices}
    context['segment'] = 'profile'

    html_template = loader.get_template( 'accounts/profile.html' )
    return HttpResponse(html_template.render(context, request))





#------------------------------------------------------------------------------

@login_required(login_url="/login/")
def nodes(request):
    uuid = models.User_uuid.objects.filter(user=request.user).values('UUID')
    devices = models.Rom.objects.filter(UUID__in=uuid, family_id='01')
    side_temp = models.Rom.objects.filter(family_id='28')
    device_name_Form = Device_name_Form(request.POST)
    user_uuid_Form = User_uuidForm(request.POST, instance=request.user)

    if request.method == 'POST':

        if device_name_Form.is_valid():
            uuid = device_name_Form.cleaned_data['Device_UUID']
            obj = get_object_or_404(models.Rom, UUID=uuid, family_id='01')
            obj.name = device_name_Form.cleaned_data['Device_name']
            obj.save()
            context = {'user_uuid_Form': user_uuid_Form, 'devices':devices, 'device_name_Form':device_name_Form}
            return render(request, 'nodes.html', context)

        if user_uuid_Form.is_valid():
            obj = User_uuid()
            obj.UUID = user_uuid_Form.cleaned_data['UUID']
            obj.user = user_uuid_Form.created_by=request.user
            obj.save()
            context = {'user_uuid_Form': user_uuid_Form, 'devices':devices, 'device_name_Form':device_name_Form}
            return render(request, 'nodes.html', context)
    else:
        user_uuid_Form = User_uuidForm(request.POST)

    context = {'user_uuid_Form':user_uuid_Form, 'devices':devices, 'side_temp':side_temp, 'device_name_Form':device_name_Form}
    context['segment'] = 'nodes'
    html_template = loader.get_template( 'nodes.html' )
    return HttpResponse(html_template.render(context, request))




@login_required(login_url="/login/")
def nodes_detail(request, id):
    uuid = models.User_uuid.objects.filter(user=request.user).values('UUID')
    devices = models.Rom.objects.filter(UUID__in=uuid, family_id='01')
    side_temp = models.Rom.objects.filter(family_id='28')

    node = get_object_or_404(models.Rom, id=id)
    sensors = models.Rom.objects.filter(node_id=node.node_id)
    sensors_uuid = models.Rom.objects.filter(node_id=node.node_id).values('UUID')

#--------- Temp12 -------------------------------------------------------------
    temp12 = models.Temp12.objects.filter(UUID__in=sensors_uuid)
    temp_uuid = models.Temp12.objects.filter(UUID__in=sensors_uuid).values('UUID').distinct()
    temp_just_uuid=list(temp_uuid.values_list('UUID', flat=True))

    i=0
    temp_data = []
    temp_last_7_chart = []
    while i < len(temp_just_uuid):
        Temp12_value = models.Temp12.objects.filter(UUID=temp_just_uuid[i]).values_list('temp', flat=True).latest('created_on')
        max = models.Temp12.objects.filter(UUID=temp_just_uuid[i]).aggregate(Max('temp'))['temp__max']
        min = models.Temp12.objects.filter(UUID=temp_just_uuid[i]).aggregate(Min('temp'))['temp__min']
        avg = models.Temp12.objects.filter(UUID=temp_just_uuid[i]).aggregate(Avg('temp'))['temp__avg']
        last_update = models.Temp12.objects.filter(UUID=temp_just_uuid[i]).values_list('created_on', flat=True).latest('created_on')
        data_feeding =  { 'UUID':temp_just_uuid[i], 'last_temp':Temp12_value, 'max_temp':max, 'min_temp':min, 'avg_temp':avg, 'last_update':last_update }
        temp_data.append(data_feeding)
        last7 = list(models.Temp12.objects.filter(UUID=temp_just_uuid[i]).values_list('temp', flat=True).order_by('-created_on')[:7])
        last7.reverse()
        last7_data =  { 'UUID':temp_just_uuid[i], 'data':last7 }
        temp_last_7_chart.append(last7_data)
        i+=1

    context = {
    'devices':devices,
    'side_temp':side_temp,
    'node':node,
    'sensors':sensors,
    'temp12':temp12,
    'temp_data':temp_data,
    'temp_last_7_chart':temp_last_7_chart
    }
    context['segment'] = 'nodes_detail'
    html_template = loader.get_template( 'nodes_detail.html' )
    return HttpResponse(html_template.render(context, request))

#------------------------------------------------------------------------------



@login_required(login_url="/login/")
def sensors_detail(request, id):
    uuid = models.User_uuid.objects.filter(user=request.user).values('UUID')
    devices = models.Rom.objects.filter(UUID__in=uuid, family_id='01')
    side_temp = models.Rom.objects.filter(family_id='28')
    sensor_name_form = Sensor_name_Form(request.POST)

    sensor = get_object_or_404(models.Rom, id=id)

    Temp12_value = models.Temp12.objects.filter(UUID=sensor.UUID).values_list('temp', flat=True).latest('created_on')
    max = models.Temp12.objects.filter(UUID=sensor.UUID).aggregate(Max('temp'))['temp__max']
    min = models.Temp12.objects.filter(UUID=sensor.UUID).aggregate(Min('temp'))['temp__min']
    avg = models.Temp12.objects.filter(UUID=sensor.UUID).aggregate(Avg('temp'))['temp__avg']
    last_update = models.Temp12.objects.filter(UUID=sensor.UUID).values_list('created_on', flat=True).latest('created_on')
    last7 = list(models.Temp12.objects.filter(UUID=sensor.UUID).values_list('temp', flat=True).order_by('-created_on')[:7])
    last7.reverse()

    if request.method == 'POST':
        if sensor_name_form.is_valid():
            obj = sensor
            obj.name = sensor_name_form.cleaned_data['Sensor_name']
            obj.save()
            context = {'devices':devices,'side_temp':side_temp,'sensor':sensor,'Temp12_value':Temp12_value,'max':max,'min':min,'avg':avg,'last_update':last_update,'last7':last7,'sensor_name_form':sensor_name_form}
            return render(request, 'sensors_detail.html', context)


    context = {'devices':devices,
     'side_temp':side_temp,
     'sensor':sensor,
     'Temp12_value':Temp12_value,
     'max':max,
     'min':min,
     'avg':avg,
     'last_update':last_update,
     'last7':last7,
     'sensor_name_form':sensor_name_form
      }
    context['segment'] = 'sensors_detail'
    html_template = loader.get_template( 'sensors_detail.html' )
    return HttpResponse(html_template.render(context, request))

#------------------------------------------------------------------------------





@login_required(login_url="/login/")
def sensors(request):
    uuid = models.User_uuid.objects.filter(user=request.user).values('UUID')
    devices = models.Rom.objects.filter(UUID__in=uuid, family_id='01')
    side_temp = models.Rom.objects.filter(family_id='28')

    device_node_id = models.Rom.objects.filter(UUID__in=uuid, family_id='01').values('node_id')
    sensor_temp = models.Temp12.objects.filter(UUID__in=device_node_id)

    context = {'devices':devices, 'side_temp':side_temp, 'sensor_temp':sensor_temp}
    context['segment'] = 'sensors'
    html_template = loader.get_template( 'sensors.html' )
    return HttpResponse(html_template.render(context, request))














@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template      = request.path.split('/')[-1]
        context['segment'] = load_template

        html_template = loader.get_template( load_template )
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template( 'page-404.html' )
        return HttpResponse(html_template.render(context, request))

    except:

        html_template = loader.get_template( 'page-500.html' )
        return HttpResponse(html_template.render(context, request))





# End
