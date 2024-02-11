import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from app.models import Client, Files
from django.core.files.base import ContentFile


@csrf_exempt #for development testing only
def submit(request):
     if request.method == "POST":
        data = json.loads(request.POST.get('data'))
        references = json.loads(request.POST.get('references'))
        data.update({"references":references})
        # Extracting files data
        files = request.FILES.getlist('files[]')
        cv_files = request.FILES.getlist('cv[]')
        lor_files = request.FILES.getlist('LOR[]')
        audio_file = request.FILES.get('audio')

        # process the data for db save
        client = Client()
        client.json = json.dumps(data)
        client.save()
        context = {"message":"data saved!!",'next_url': f"http://{request.META['HTTP_HOST']}/client/{client.id}"}

        # For files
        for file_f in files:
            file = Files()
            file.file_type = "FILE"
            file.file = file_f
            file.client = client
            file.save()
     
        for cv in cv_files: # for cv
            file = Files()
            file.file_type = "CV"
            file.file = cv
            file.client = client
            file.save()

        for lor_file in lor_files: # for LOR
            file = Files()
            file.file_type = "LOR"
            file.file = lor_file
            file.client = client
            file.save()

        if audio_file: # for audio file
            file = Files()
            file.file_type = "AUDIO"
            audio_blob = audio_file.read()
            file.file = ContentFile(audio_blob, name='audio.mp3')  
            file.client = client
            file.save()

        # whole json
        #print(json.dumps(data))
     return JsonResponse(context)
    

def get_client_info(request,id):
    client = Client.objects.get(id=id)
    data =json.loads(client.json)
    files = Files.objects.filter(client_id=id)
    data.update({
        "files": list(files.filter(file_type="FILE").values('file')),
        "cv": list(files.filter(file_type="CV").values('file')),
        "LOR": list(files.filter(file_type="LOR").values('file')),
        "audio": list(files.filter(file_type="AUDIO").values('file')),
        })
    
    return JsonResponse(data)