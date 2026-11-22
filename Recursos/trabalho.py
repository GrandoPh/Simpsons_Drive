import pyttsx3

def falar_texto(mensagem):
    try:
        voz = pyttsx3.init()
        voz.say(mensagem)
        voz.runAndWait()
    except:
        print(mensagem)

def calcular_dificuldade(pontos):
    if pontos < 5:
        nivel = "Nivel 1 - Rua Calma"
    elif pontos >= 5 and pontos < 15:
        nivel = "Nivel 2 - Transito de Springfield"
    else:
        nivel = "Nivel 3 - Fuga da Policia!"
    return nivel
