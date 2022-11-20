
import time
import threading


""" def ejecucion_horaria(segundos):

    print("Thread ejecuta cada %d" % segundos)
    for i in range(100):
        print(
            "     VALOR BITCOIN  {{valor}}                    Ejecucion horaria, pasada %d" % i)
        time.sleep(segundos)
 """

def test_valor(test):
    a = 1
    for i in range(100):
        print(
            "     VALOR BITCOIN  {{valor}}                    Ejecucion horaria, pasada %d" % i)
    time.sleep(test)



# Aqui creamos el thread.
# El primer argumento es el nombre de la funcion que contiene el codigo.
# El segundo argumento es una lista de argumentos para esa funcion .
# Ojo con la coma al final!
""" hilo = threading.Thread(target=ejecucion_horaria, args=(3,))
hilo.start() """

hilo2 = threading.Thread(target=test_valor, args=(2,))
hilo2.start()

# Iniciamos la ejecución del thread,

# La ejecución sigue de inmediato aqui, mientras el thread
# ejecuta en paralelo.
""" for i in range(100):
    print(" %d" % i)
    time.sleep(1) """
