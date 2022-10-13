import pyttsx3
import speech_recognition as sr
import pywhatkit
import yfinance as yf
import pyjokes
import webbrowser
import datetime
import wikipedia

#escuchar mic y devolver audio como texto
def transformar_audio_en_texto():
    #almacenar recognizer en variable
    r = sr.Recognizer()
    #configurar el microfono
    with sr.Microphone() as origen:
        #tiempo de espera
        r.pause_threshold = 0.8
        
        #informar que comenzo la grabación
        print("habla por favor")
        
        #guardar lo que escucho
        audio = r.listen(origen)
        
        try:
            #buscar en google
            pedido = r.recognize_google(audio, language = "es-ar")
            
            #prueba de que escucho
            print("Dijiste:" + pedido)
            
            #devolver pedido 
            return pedido
        
        #en caso de que no comprenda
        except sr.UnknownValueError:
            #prueba de que no comprendio
            print("no pude escuchar correctamente")
            
            #devolver error
            return "sigo esperando"
        
        #en caso de no resolver el peligro
        except sr.RequestError:
            #prueba de que comprendió
            print("no pude escuchar correctamente")
            
            #devolver error
            return "sigo esperando"
        #error inesperado
        except:
            #prueba de que comprendió
            print("algo ha salido mal")
            
            #devolver error
            return "sigo esperando"
        
#funcion para que el asistente pueda ser escuchado
def hablar(mensaje):
    #encender el motor de pyttsx3
    engine = pyttsx3.init()
    engine.setProperty("voice", id1)
    #pronunciar mensaje
    engine.say(mensaje)
    engine.runAndWait()

#opciones de voz    
id1 = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-ES_HELENA_11.0"
id2 = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"  

#informar el dia de la semana
def pedir_dia():
    #crear variable con datos de hoy
    dia = datetime.date.today()
    print(dia)
    
    #crear variable para el dia de semana
    dia_semana = dia.weekday()
    print(dia_semana)
    
    #diccionario con nombres de dias 
    calendario = {0: "Lunes", 1: "Martes", 2: "Miércoles", 3: "Jueves", 4: "Viernes"
                  ,5: "Sábado", 6: "Domingo"}
    
    #decir el dia de la semana
    hablar(f"Hoy es {calendario[dia_semana]}")
    
    
#informar hora
def pedir_hora():
    #crear una variable con datos de la hora
    hora = datetime.datetime.now()
    hora = f"En este momento son las {hora.hour} y {hora.minute}"
    print(hora)
    
    #decir la hora
    hablar(hora)
    
#saludo inicial
def saludo_inicial():
    #variable con datos de hora
    hora =  datetime.datetime.now()
    if hora.hour < 6 or hora.hour > 20:
        momento = "buenas noches"
    elif hora.hour >= 6 and hora.hour < 13:
        momento = "buen dia"
    else:
        momento = "buenas tardes"
    #decir el saludo
    hablar(f"{momento} soy tu asistente, en que puedo ayudarte?")

#funcion central del asistente
def pedir_cosas():
    #activar saludo inicial
    saludo_inicial()  
    
    #variable de fin
    comenzar = True
    
    while  comenzar:
        #activar micro y guardar en string
        pedido = transformar_audio_en_texto().lower()
        
        if "abrir youtube" in pedido:
            hablar ("con gusto, estoy abriendo youtube")
            webbrowser.open("http://www.youtube.com")
            continue
        elif "abrir navegador" in pedido:
            hablar ("perfecto, estoy abriendo el navegador")
            webbrowser.open("http://www.google.com")
            continue
        elif "qué día es hoy" in pedido:
            pedir_dia()
            continue
        elif "qué hora es" in pedido:
            pedir_hora()
            continue
        elif "busca en wikipedia" in pedido:
            hablar("ahí abro wikipedia")
            pedido = pedido.replace ("busca en wikipedia", "")
            wikipedia.set_lang("es")
            resultado = wikipedia.summary(pedido, sentences = 1)
            hablar("en wikipedia se encuentra lo siguiente")
            webbrowser.open(f"https://es.wikipedia.org/wiki/{pedido}")
            hablar(resultado)
            continue
        elif "busca en internet" in pedido:
            hablar("ya lo estoy buscando")
            pedido = pedido.replace ("busca en internet", "")
            pywhatkit.search(pedido)
            hablar("esto es lo que encontré")
            continue
        elif "reproducí"  in pedido:
            hablar("con gusto")
            pedido = pedido.replace ("reproducí", "")
            pywhatkit.playonyt(pedido)
            continue
        elif "chiste" in pedido:
            hablar(pyjokes.get_joke('es'))
            continue
        elif "precio de las acciones" in pedido:
            accion = pedido.split("de")[-1].strip()
            cartera ={"apple": "APPL", "amazon": "AMZN", "google": "GOOGl"}
            try:
                accion_buscada= cartera[accion]
                accion_buscada = yf.Ticker(accion_buscada)
                precio_actual = accion_buscada.info["regularMarketPrice"]
                hablar(f"la he encontrado el precio de {accion} es {precio_actual}")
                continue
            except:
                hablar("perdón pero no lo encontré")
                continue
        elif "cómo salió mi equipo" in pedido:
            hablar ("perfecto, estoy abriendo los resultados de los ultimos partidos")
            webbrowser.open("https://www.promiedos.com.ar")
            continue
        elif "quiero ver el correo" in pedido:
            hablar ("perfecto, estoy abriendo tu bandeja de entrada")
            webbrowser.open("https://outlook.live.com/mail/0/")
            continue
        elif "quiero ver instagram" in pedido:
            hablar ("perfecto, estoy abriendo instagram")
            webbrowser.open("https://www.instagram.com")
            continue
        elif "quiero ver el diario" in pedido:
            hablar ("perfecto, estoy buscando las últimas noticias")
            webbrowser.open("https://www.lacapital.com.ar")
            continue      
        elif "quiero ver directos" in pedido:
            hablar ("perfecto, estoy abriendo twitch")
            webbrowser.open("https://www.twitch.tv")
            continue     
        elif "precio del dólar" in pedido:
            hablar ("este es el precio del dolar en argentina")
            pywhatkit.search("precio del dolar argentina")
            continue
        elif "adiós" in pedido:
            hablar("un gusto ayudarte como siempre, nos vemos")   
            break

pedir_cosas()