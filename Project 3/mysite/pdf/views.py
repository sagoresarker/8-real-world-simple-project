from django.shortcuts import render
import pdfkit
from django.http import HttpResponse
from django.template import loader
import io


# Create your views here.
from .models import Profile


def accept(request):
    if request.method == "POST":
        name = request.POST.get("name", "")
        email = request.POST.get("email", "")
        phone = request.POST.get("phone", "")
        summary = request.POST.get("summery", "")
        degree = request.POST.get("degree", "")
        school = request.POST.get("school", "")
        university = request.POST.get("university", "")
        previous_work = request.POST.get("previous_work", "")
        skills = request.POST.get("skills", "")

        profile = Profile(name=name, email=email, phone=phone, summary=summary,
                            degree=degree, school=school, university=university, previous_work=previous_work, skills=skills)

        profile.save()


    return render(request, 'pdf/accept.html')


def resume(request, id):
    user_profile = Profile.objects.get(id=id)
    template = loader.get_template('pdf/resume.html')

    context = {
        'user_profile': user_profile,
    }


    html = template.render(context)

    options = {
        "page-size":"Letter",
        "encoding":"UTF-8"
    }

    pdf = pdfkit.from_string(html, False, options)

    response = HttpResponse(pdf, content_type='application/pdf')

    response['Content-Disposition'] = 'attatchment'
    filename = "resume.pdf"

    return response

def list(request):
    profiles = Profile.objects.all()

    return render(request, 'pdf/list.html', {'profiles':profiles})