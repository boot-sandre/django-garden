from django.http import HttpResponse, HttpRequest

from ninja import Router
from ninja import File
from ninja.files import UploadedFile

from garden.core_ninja.schemas import TimeEventContract


router = Router()


@router.get("/hello")
def hello(request):
    return "Hello world"


@router.post("/get_back_data")
def get_back_data(request: HttpRequest, data: TimeEventContract):
    html = "<html><body>%s</body></html>" % data
    return HttpResponse(html)


@router.post("/get_back_filename")
def get_back_filename(request: HttpRequest, fileToUpload: UploadedFile = File(...)):
    html = "<html><body>%s</body></html>" % str(fileToUpload)
    return HttpResponse(html)
