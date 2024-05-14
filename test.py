from pylatex import Document, Section, Math, NoEscape
from sympy import symbols, latex, parse_expr
import time

def identificar_operacion(expresion):
    operadores = {'+': 'Suma', '-': 'Resta', '*': 'Multiplicación', '/': 'División', 'log': 'Logaritmo', 'cos': 'Coseno', 'tan': 'Tangente'}
    
    for simbolo, titulo in operadores.items():
        if simbolo in expresion:
            return titulo
    return "Operación no identificada"

def generar_imagen(expresion):
    # Define los símbolos
    x = symbols('x')
    
    # Identifica la operación
    titulo_operacion = identificar_operacion(expresion)
    if titulo_operacion == "Operación no identificada":
        return "Operación no válida. No se pudo identificar la operación."
    
    # Parsea la expresión ingresada por el usuario
    try:
        start_time = time.time()  # Registra el tiempo de inicio
        expr = parse_expr(expresion)
        resultado = expr.evalf()
        end_time = time.time()  # Registra el tiempo de finalización
        tiempo_ejecucion = end_time - start_time
    except Exception as e:
        return f"No se pudo evaluar la expresión: {str(e)}"
    
    # Genera la representación LaTeX de la expresión y el resultado
    latex_expresion = f"${expresion} = {resultado}$"
    
    # Inicia un documento PDF
    doc = Document()
    
    # Agrega contenido al documento
    with doc.create(Section('Operación Matemática')):
        doc.append('Operación: ')
        doc.append(titulo_operacion)
        doc.append('\n')
        doc.append(latex_expresion)
        doc.append('\n')
        doc.append('Tiempo de ejecución: ')
        doc.append(str(tiempo_ejecucion))
        doc.append(' segundos')

    # Guarda el documento como PDF
    doc.generate_pdf('expresion_matematica', clean_tex=False)

    return "Imagen generada correctamente: expresion_matematica.pdf"

# Solicita al usuario que ingrese la expresión matemática
expresion_usuario = input("Ingresa la expresión matemática utilizando los símbolos adecuados: ")

# Genera la imagen con la expresión matemática y su resultado
print(generar_imagen(expresion_usuario))
