from rest_framework.response import Response
from rest_framework import viewsets, generics

import base64
from django.core.files.base import ContentFile

from .models import OjetoModel
from .serializers import ObjetoSerializer

#region API requests

class ObjectFileViewSet(viewsets.ModelViewSet):
    serializer_class = IncidenciaSerializer
    queryset = Incidencia.objects.all()

    def file(self, request, pk):
        """Receive a file from a JSON request, as a base64 content."""
        #Objeto is a generic model, change if for yours
        objeto = Objeto.objects.get(id = pk)
        #Json attributes saved to variable
        name = request.data["nombre"]
        data = request.data["archivo"]
        #Slit the base64 string, [0] will be the file format, [1] will be the file content.
        format, imgstr = data.split(';base64,') 
        #from format we will get the extension.
        ext = format.split('/')[-1] 

        data = ContentFile(base64.b64decode(imgstr), name=name +'.' + ext) # You can save this as file instance.

        #With the file generated we can save it.
        objeto.archivo = data
        objeto.save()
        
        #Response with the serialized model.
        return Response(ObjetoSerializer(objeto).data)

#endregion