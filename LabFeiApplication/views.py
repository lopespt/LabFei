import hashlib
import mimetypes
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.utils.importlib import import_module
from LabFeiApplication.management.commands.populate import laboratoryFiles
from LabFeiApplication.models import LaboratoryFile

from services import userService
from LabFei.annotations import request_path


@request_path(path='/')
def index(request):
    print("Entrei index")
    if request.method == 'GET':
        return render(request, 'index.html')
    else:
        user = userService.do_login(request)
        if user is not None:
            return redirect(to='/user/' + user.login)
        else:
            return render(request, 'index.html')


@request_path(path='/logout')
def logout(request):
    userService.do_logout(request)
    return redirect('/')


@request_path(path='/download.do')
def logout(request):
    file_id=int(request.GET['file_id'])
    file_hash=request.GET['hash_code']
    if hashlib.md5(str(file_id)).hexdigest() != file_hash:
        raise Exception('Incorrect file hash')

    file_db = LaboratoryFile.objects.filter(id=file_id).first()
    with open(file_db.file, 'r') as f:
        mime = mimetypes.guess_type(file_db.file)
        resp = HttpResponse(content=f.readlines(), content_type='%s' % mime[0])
        resp['Content-Disposition'] = 'attachment; filename=%s' % file_db.file.split('/')[-1]
    return resp
