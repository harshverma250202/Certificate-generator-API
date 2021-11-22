from django.http.response import FileResponse, HttpResponse, JsonResponse
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.units import inch
import json
from django.views.generic import View
from django.db import connection
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from PIL import ImageFont


class EadCertificateVIew(View):

    def post(self, request, *args, **kwargs):

        data = json.loads(request.body)
        email = data['email']
        suggestion = data['suggestion']
        city = data['city']
        rating = data['rating']
        # print(city)
        with connection.cursor() as cur:
            cur.execute(
                "SELECT * FROM ead_certificate_2021 WHERE ead_certificate_2021.email=%s AND ead_certificate_2021.attended_city=%s", (email, city))
            info = cur.fetchone()
            # print(info)
            if info:
                name = info[1]
                date = info[2]
                organisation=info[3]
                # organisation = 'indiaindiaindiaindiaindiaindiaindiaindiaindiaindiaindiaindiaindiaindia'
                templateCert = ImageReader('static/images/ead_certificate.png')
                buffer = io.BytesIO()
                # Create the PDF object, using the buffer as its "file."
                # size of the certificate is A4
                p = canvas.Canvas(buffer, pagesize=(11.7*inch, 8.3*inch))
                pdfmetrics.registerFont(
                    TTFont('Lato-Bold', 'static/font/Lato-Bold.ttf'))
                font = ImageFont.truetype('static/font/Lato-Bold.ttf', 18)
                namesize, _ = font.getsize(name)
                organisation_size, _ = font.getsize(organisation)
                city_size, _ = font.getsize(city)
                print(organisation_size, _)
                # width of name placeholder in certi 835 1680    image width is 2000 pixel
                muly = 1340/550.0
                nameXpos = ((1680+835)/2)-namesize*muly/2
                organisationXpos = ((1680+340)/2)-organisation_size*muly/2
                cityXpos = ((1100+1580)/2)-city_size*muly/2
                multiplier = (11.7/2000)
                p.setFont("Lato-Bold", 18)
                p.drawImage(templateCert, 0, 0, width=11.7 *
                            inch, height=8.3*inch)
                p.drawString((multiplier*nameXpos)*inch, 316, name)
                p.drawString(multiplier*cityXpos*inch, 262, city)
                if(organisationXpos <= 340):
                    organisationXpos = 345
                    p.setFont("Lato-Bold", 15)
                p.drawString(multiplier*organisationXpos *
                             inch, 288, organisation)

                p.showPage()
                p.save()

                buffer.seek(0)
                if(info[9] == 0):
                    cur.execute("UPDATE ead_certificate_2021 SET ead_certificate_2021.suggestion=%s,ead_certificate_2021.rating = %s,ead_certificate_2021.has_Created = %b WHERE ead_certificate_2021.email=%s AND ead_certificate_2021.attended_city=%s ", (suggestion, rating, 1, email, city))

                # cur.execute("UPDATE ead_certificate_2021 SET ead_certificate_2021.suggestion=%s,ead_certificate_2021.rating = %s WHERE ead_certificate_2021.email=%s AND ead_certificate_2021.attended_city=%s ", (suggestion, rating,email,city))
                return FileResponse(buffer, filename='hello.pdf')
            else:
                return JsonResponse({'error': 'Invalid Email or City'})
    def get(self, request, *args, **kwargs):

        return JsonResponse({
            "status": "success",
        })

class LsmCertificateVIew(View):

    def post(self, request, *args, **kwargs):

        data = json.loads(request.body)
        email = data['email']
        suggestion = data['suggestion']
        event = data['city']
        rating = data['rating']
        # print(event)
        with connection.cursor() as cur:
            cur.execute(
                "SELECT * FROM lsm_certificate_2021 WHERE lsm_certificate_2021.email=%s ", [email])
            info = cur.fetchone()
            # print(info)
            if info:
                name = info[1]
                date = info[2]
                organisation = info[3]
                # organisation='indiaindiaindiaindiaindiaindiaindiaindiainaindia'
                templateCert = ImageReader('static/images/lsm_certificate.png')
                buffer = io.BytesIO()
                # Create the PDF object, using the buffer as its "file."
                # size of the certificate is A4
                p = canvas.Canvas(buffer, pagesize=(11.7*inch, 8.3*inch))
                pdfmetrics.registerFont(
                    TTFont('Lato-Bold', 'static/font/Lato-Bold.ttf'))
                font = ImageFont.truetype('static/font/Lato-Bold.ttf', 18)
                namesize, _ = font.getsize(name)
                organisation_size, _ = font.getsize(organisation)
                print(organisation_size, _)
                # width of name placeholder in certi 835 1680         image width is 2000 pixel
                muly = 1340/550.0
                nameXpos = ((1690+845)/2)-namesize*muly/2
                organisationXpos = ((1690+486)/2)-organisation_size*muly/2
                multiplier = (11.7/2000)
                p.setFont("Lato-Bold", 18)
                p.drawImage(templateCert, 0, 0, width=11.7 *
                            inch, height=8.3*inch)
                p.drawString((multiplier*nameXpos)*inch, 307, name)
                if(organisationXpos <= 486):
                    organisationXpos = 490
                    p.setFont("Lato-Bold", 15)
                p.drawString(multiplier*organisationXpos *
                             inch, 279, organisation)

                p.showPage()
                p.save()

                buffer.seek(0)
                if(info[9] == 0):  # status whether certificate is created or not before this request
                    cur.execute("UPDATE lsm_certificate_2021 SET lsm_certificate_2021.suggestion=%s,lsm_certificate_2021.rating = %s,lsm_certificate_2021.has_Created = %b WHERE lsm_certificate_2021.email=%s  ", (suggestion, rating, 1, email))

                # cur.execute("UPDATE lsm_certificate_2021 SET lsm_certificate_2021.suggestion=%s,lsm_certificate_2021.rating = %s WHERE lsm_certificate_2021.email=%s  ", (suggestion, rating,email))
                return FileResponse(buffer, filename='hello.pdf')
            else:
                return JsonResponse({'error': 'Invalid Email or event'})
    def get(self, request, *args, **kwargs):
    
        return JsonResponse({
            "status": "success",
        })