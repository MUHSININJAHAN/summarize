import os
from io import BytesIO
from django.core.files import File
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.shortcuts import render, redirect
from newspaper import Article
from textblob import TextBlob
from PIL import Image
from pytesseract import pytesseract
from .models import Registration as reg


def compressing(image, picturename):
    im = Image.open(image)
    im = im.convert('RGB')
    im_io = BytesIO()
    im.save(im_io, 'JPEG', quality=60)
    compressed_image = File(im_io, name=picturename)
    print(settings.STATIC_URL)
    print(settings.STATIC_ROOT)
    print(settings.STATICFILES_DIRS[0])
    FileSystemStorage(location=os.path.join(settings.STATICFILES_DIRS[0], 'UPLOAD', 'user',)).save(picturename,
                                                                                                    compressed_image)
def generate_summary(text, num_sentences):
    blob = TextBlob(text)
    sentences = blob.sentences

    # Calculate sentence scores based on polarity
    sentence_scores = {}
    for i, sentence in enumerate(sentences):
        sentence_scores[i] = sentence.sentiment.polarity

    # Sort the sentences by score
    sorted_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)

    # Generate the summary with the top 'num_sentences' sentences
    summary = ""
    for i in range(num_sentences):
        summary += str(sentences[sorted_sentences[i]]) + " "

    return summary


def Home(request):
    if 'VisitorStatus' not in request.session or request.session['VisitorStatus'] != "user":
        return redirect('Text:Home2')

    return render(request, 'text/index.html')

def Home2(request):
    return render(request, 'text/index2.html')

def Contact(request):
    return render(request, 'text/contact.html')

def About(request):
    if 'VisitorStatus' not in request.session or request.session['VisitorStatus'] != "user":
        return redirect('Text:Login')

    return render(request, 'text/about.html')

def Services(request):
    if 'VisitorStatus' not in request.session or request.session['VisitorStatus'] != "user":
        return redirect('Text:Login')

    return render(request, 'text/services.html')



def Text_to_summerize(request):

    if 'VisitorStatus' not in request.session or request.session['VisitorStatus'] != "user":
        return redirect('Text:Login')


    if request.method == 'GET':
        return render(request,'text/textsummerize.html')
    if request.method == 'POST':
        data = request.POST

        try:

            value = """{}""".format(data['text'])

            summary = generate_summary(value, 5)
            context = {
                'summery' : summary,
                'msg' : 'This is your Summery'
            }
            return render(request,'text/textsummerize.html',context)
        except:
            context = {
                'summery' : 'Your text is already small'
            }
            return render(request,'text/textsummerize.html',context)


def Link_to_summerize(request):

    if 'VisitorStatus' not in request.session or request.session['VisitorStatus'] != "user":
        return redirect('Text:Login')

    if request.method == 'GET':
        return render(request,'text/linksummerize.html')
    if request.method == 'POST':
        data = request.POST

        try:

            article = Article(data['link'])
            article.download()
            article.parse()
            article.nlp()

            context = {
                'summery' : article.summary,
                'msg' : 'This is your Summery'
            }
            return render(request,'text/linksummerize.html',context)
        except:
            context = {
                'summery' : 'This is not an appropriate link',
            }
            return render(request,'text/linksummerize.html',context)


def Img_to_summerize(request):
    if 'VisitorStatus' not in request.session or request.session['VisitorStatus'] != "user":
        return redirect('Text:Login')

    if request.method == 'GET':
        return render(request,'text/imgsummerize.html')
    if request.method == 'POST':
        # data = request.POST

        try:
            print(1)
            # Defining paths to tesseract.exe
            # and the image we would be using

            os.remove('static/UPLOAD/user/capture.jpg')

            new_name = 'capture.jpg'
            compressing(request.FILES['pictures'],new_name)

            print(2)
            path_to_tesseract = r"Tesseract-OCR/tesseract.exe"
            image_path = r"static/UPLOAD/user/capture.jpg"

            print(image_path)

            # Opening the image & storing it in an image object
            img = Image.open(image_path)

            # Providing the tesseract executable
            # location to pytesseract library
            pytesseract.tesseract_cmd = path_to_tesseract

            # Passing the image object to image_to_string() function
            # This function will extract the text from the image
            text = pytesseract.image_to_string(img)

            # Displaying the extracted text
            print(text[:-1])

            summary = generate_summary(text[:-1], 5)

            context = {
                'summery' : summary,
                'msg' : 'This is your Summery'
            }
            return render(request,'text/imgsummerize.html',context)

        except:
            context = {
                'summery' : 'This is not an appropriate img',
            }
            return render(request,'text/imgsummerize.html',context)


def Login(request):

    if request.method == 'GET':
        return render(request, 'text/login.html')

    if request.method == 'POST':
        # Login user
        data = request.POST
        email = data['email']
        password = data['passw']

        exists = reg.objects.filter(Email=email).exists()

        if not exists:
            context = {
                'msg': "Wrong Email"
            }

            return render(request, 'text/login.html', context)

        user = reg.objects.get(Email=email)

        if user.Password != password:

            context = {
                'msg' : "Wrong Password"
            }

            return render(request,'text/login.html',context)
        else:

            request.session['VisitorStatus'] = 'user'
            request.session["UserID"] = user.ID
            request.session["UserName"] = user.Name
            user.save()

            return redirect('Text:Home')


def Registration(request):

    if request.method == 'GET':
        return render(request,'text/reg.html')

    if request.method == 'POST':
        # Register user
        data = request.POST

        name = data['name']
        email = data['email']
        passw = data['passw']

        if reg.objects.filter(Email=email).exists():

            context = {
                'msg1' : "This Email Already Exist"
            }
            return render(request,'text/reg.html',context)

        else:

            new_member = reg(Name=name,Email=email,Password=passw)
            new_member.save()

            return redirect('Text:Login')


def Logout(request):

    if 'VisitorStatus' not in request.session or request.session['VisitorStatus'] != "user":
        return redirect('Text:Login')

    try:
        del request.session['VisitorStatus']
        del request.session["UserID"]
        del request.session["UserName"]
        return redirect('Text:Login')

    except:
        return redirect('Text:Login')