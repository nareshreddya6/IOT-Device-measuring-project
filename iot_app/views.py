from django.shortcuts import render
from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Device, TemperatureReading, HumidityReading
from .serializers import DeviceSerializer, TemperatureReadingSerializer, HumidityReadingSerializer
from django.utils.dateparse import parse_datetime

@api_view(['POST'])
def create_device(request):
    serializer = DeviceSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_readings(request, device_uid, parameter):
    start_on = parse_datetime(request.GET.get('start_on'))
    end_on = parse_datetime(request.GET.get('end_on'))

    if parameter == "temperature":
        readings = TemperatureReading.objects.filter(device__uid=device_uid, timestamp__range=(start_on, end_on))
        serializer = TemperatureReadingSerializer(readings, many=True)
    elif parameter == "humidity":
        readings = HumidityReading.objects.filter(device__uid=device_uid, timestamp__range=(start_on, end_on))
        serializer = HumidityReadingSerializer(readings, many=True)
    else:
        return Response({"error": "Invalid parameter"}, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.data)

@api_view(['GET'])
def list_devices(request):
    devices = Device.objects.all()
    serializer = DeviceSerializer(devices, many=True)
    return Response(serializer.data)

@api_view(['DELETE'])
def delete_device(request, device_uid):
    device = get_object_or_404(Device, uid=device_uid)
    device.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def retrieve_device(request, device_uid):
    device = get_object_or_404(Device, uid=device_uid)
    serializer = DeviceSerializer(device)
    return Response(serializer.data)


def device_graph(request):
    return render(request, 'iot_app/device_graph.html')



