import os
from pdf2image import convert_from_path
from PIL import Image
from pylatex import Document, Subsection, Math
from pylatex.utils import italic
import sympy as sp
import ast





def create_pdf(expressions, output_path):
    # Crear la instancia de Document
    doc = Document()

    # Contenido
    with doc.create(Subsection('Expresiones y Resultados:')):
        for expression in expressions:
            with doc.create(Math()):
                doc.append(expression.replace('^', r'\textasciicircum'))  # Reemplazar '^' con '\textasciicircum'
                doc.append('=')  # Mostrar el signo de igual
                doc.append(expression.replace('^', '**'))  # Mostrar la expresión con '^' reemplazado por '**'

    # Generar el PDF
    doc.generate_pdf(output_path, clean_tex=False)  # No incluir el argumento 'crop'

# Solicitar expresiones al usuario
def main():
    expressions = []
    print("Ingrese las expresiones separadas por comas:")
    expressions_input = input().split(',')
    for expression in expressions_input:
        expressions.append(expression.strip())  # Eliminar espacios en blanco alrededor de cada expresión
    create_pdf(expressions, "output.pdf")
# Solicitar expresiones al usuario
def main():
    expressions = []
    print("Ingrese las expresiones separadas por comas:")
    expressions_input = input().split(',')
    for expression in expressions_input:
        expressions.append(expression.strip())  # Eliminar espacios en blanco alrededor de cada expresión
    create_pdf(expressions, "output.pdf")

# Solicitar expresiones al usuario
def main():
    expressions = []
    print("Ingrese las expresiones separadas por comas:")
    expressions_input = input().split(',')
    for expression in expressions_input:
        expressions.append(expression.strip())  # Eliminar espacios en blanco alrededor de cada expresión
    create_pdf(expressions, "output.pdf")
# Solicitar expresiones al usuario
def main():
    expressions = []
    print("Ingrese las expresiones separadas por comas:")
    expressions_input = input().split(',')
    for expression in expressions_input:
        expressions.append(expression.strip())  # Eliminar espacios en blanco alrededor de cada expresión
    create_pdf(expressions, "output.pdf")


# Solicitar expresiones al usuario
def main():
    print("Ingrese las expresiones separadas por comas:")
    expressions_input = input().split(',')
    create_pdf(expressions_input, "output.pdf")

# Solicitar expresiones al usuario
def main():
    expressions = []
    print("Ingrese las expresiones separadas por comas:")
    expressions_input = input().split(',')
    for expression in expressions_input:
        expressions.append(expression.strip())  # Eliminar espacios en blanco alrededor de cada expresión
    create_pdf(expressions, "output.pdf")



def create_image_from_pdf(pdf_path, output_path):
    images = convert_from_path(pdf_path)
    if images:
        for i, image in enumerate(images):
            image.save(f"{output_path}_{i}.jpg", "JPEG")

def crop_image(image, crop_box, output_path):
    cropped_image = image.crop(crop_box)
    cropped_image.save(output_path + '.jpg')  # Agregar la extensión .jpg al nombre del archivo


def create_cropped_image_from_pdf(pdf_path, output_path, crop_box):
    images = convert_from_path(pdf_path)
    if images:
        page = images[0]
        crop_image(page, crop_box, output_path)

if __name__ == '__main__':
    # Solicitar la expresión matemática al usuario
    math_expression = input("Ingrese la expresión matemática: ")
    create_pdf(math_expression, 'full')
    create_image_from_pdf('full.pdf', 'full_pdf_image')


    create_cropped_image_from_pdf('full.pdf', 'crop_image', (300, 300, 1300, 600))
