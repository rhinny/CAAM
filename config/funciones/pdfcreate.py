from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch


def crear_pdf(request):
    #Datos dinámicos
    nombre_voluntario = f"{getattr(request.user, 'first_name', '')} {getattr(request.user, 'last_name', '')}".strip() or "Usuario de Prueba"
    programa = "KAIROS"
    
    #Crear respuesta pdf
    response = HttpResponse(content_type = 'application/pdf')
    response["Content-Disposition"] = 'Inline; filename="certificado.pdf"'
    
    #Crear lienzo
    c = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    #Fondo certificado
    c.setFillColorRGB(0.2, 0.4, 0.9) #Azul
    c.rect(0, 0, width, height, fill=1)
    #Marco blanco
    margin = 40
    c.setFillColor(colors.white)
    c.rect(margin, margin, width - 2*margin, height - 2*margin, fill=1)
    #Marco dorado interno
    c.setStrokeColor(colors.Color(0.9, 0.75, 0.2))
    c.setLineWidth(3)
    c.rect(margin + 15, margin + 15, width - 2*(margin + 15), height - 2*(margin + 15))

    #Texto superior
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(colors.black)
    c.drawCentredString(width / 2, height - 130, programa)

    #Linea 1
    c.setFont("Helvetica-Bold", 20)
    c.setFillColor(colors.black)
    c.drawCentredString(width / 2, height - 180, "RECONOCIMIENTO")
    #Linea 2
    c.setFont("Helvetica", 14)
    c.drawCentredString(width / 2, height - 210, "DE CUMPLIMIENTO A:")
    #Nombre voluntario
    c.setFont("Helvetica-Oblique", 22)
    c.setFillColorRGB(0.2, 0.2, 0.2)
    c.drawCentredString(width / 2, height - 250, nombre_voluntario)
    #Barra decorativa
    c.setStrokeColor(colors.Color(0.9, 0.75, 0.2))
    c.setLineWidth(1.5)
    c.line(width / 2 - 100, height - 260, width / 2 + 100, height - 260)
    #Agregar resto de texto a nuestro pdf
    c.setFont("Helvetica", 12) #Configuración de la fuente
    texto = (f"Por su destacada participación en las actividades programadas dentro de la "
             f"plataforma {programa}, completando la totalidad de sus citas asignadas "
             f"con compromiso y responsabilidad.")
    
    from reportlab.platypus import Paragraph
    from reportlab.lib.styles import getSampleStyleSheet

    styles = getSampleStyleSheet()
    style = styles["Normal"]
    style.fontName = "Helvetica"
    style.fontSize = 10
    style.leading = 14
    style.alignment = 1 # 1=centrado
    p = Paragraph(texto, style)
    p_width, p_height = p.wrap(width - 200, height)
    p.drawOn(c, 100, height - 340)

    """"
    text_obj = c.beginText(80, height - 320)
    text_obj.setFont("Helvetica", 10)
    text_obj.setFillColor(colors.black)
    text_obj.setLeading(14)
    text_obj.textLines(texto)
    c.drawText(text_obj)    
    """
    #Logo
    import os
    from django.conf import settings
    logo_path = os.path.join(settings.BASE_DIR, "static", "css", "Images", "logo1.png")
    try:
        c.drawImage(logo_path, width / 2 - 30, height - 430, width=60, height=60, mask='auto')
    except Exception as e:
        c.setFont("Helvetica", 8)
        c.drawCentredString(width / 2, height - 430, "[Logo no disponible]")    
        print("Error cargando logo: ", e)

    #Guardar el archivo PDF
    c.showPage()
    c.save()
    
    return response

