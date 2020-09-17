import os

class LexicoHtml:

    def __init__(self, entrada):
        self.listaCaracteres = list(entrada)
        self.texto = ""
        self.ruta = "output\\"
        self.listaErrores = list()
    #ENDINIT
    
    def analisis(self):
        lexema = ""
        estado = 0
        fila = 0
        columna = 0
        indice = 0
        esPath = False
        path = ""
        iniciotag = False
        fintag = False

        while indice < len(self.listaCaracteres):
            caracter = self.listaCaracteres[indice]

            if estado == 0:
                if caracter == '\n':
                    fila += 1
                    estado = 0
                    columna = 0
                    self.texto += caracter
            
                elif (caracter == ' ' or caracter == '\r' or caracter == '\t' or caracter == '\b' or caracter == '\f'):
                    estado = 0
                    self.texto += caracter

                #comentarios
                elif caracter == '<':
                    estado = 1

                #estado símbolos
                elif (caracter == '=' or caracter == '!' or caracter == '/' or caracter == '>'):
                    estado = 2

                #reconocer números negativos
                elif caracter == '-':
                    estado = 3

                #estado letras
                elif ((ord(caracter) >= 65 and ord(caracter) <= 90) or (ord(caracter) >= 97 and ord(caracter) <= 122)):
                    estado = 4

                #estado numeros
                elif ((ord(caracter) >= 48 and ord(caracter) <= 57)):
                    estado = 5
                
                #estado cadenas y caracter
                elif ((ord(caracter) == 34) or (ord(caracter) == 39)):
                    estado = 6
                
                #estado error
                else:
                    if iniciotag == True and fintag == False:
                        estado = -1
                    else:
                        self.texto += caracter
            #ENDIF

            if estado == 1:
                if caracter == '<':
                    lexema += caracter
                    estado = 1
                
                elif caracter == '!':
                    lexema += caracter
                    estado = 7
                    #self.texto += lexema
                    #lexema = ""

                else:
                    iniciotag = True
                    fintag = False
                    print("símbolo: " + lexema)
                    self.texto += lexema
                    lexema = ""
                    estado = 0
                    indice -= 1

            #reconocimiento de símbolos
            elif estado == 2:
                if (caracter == '-' or caracter == '=' or caracter == '!' or caracter == '/' or caracter == '>' or caracter == '<'):
                    print("símbolo: " + caracter)
                    self.texto += caracter
                    if (caracter == '>'):
                        iniciotag = False
                        fintag = True
                    estado = 0
                    lexema = ""
                    #indice -= 1

            #reconocimiento de números negativos
            elif estado == 3:
                if (ord(caracter) >= 48 and ord(caracter) <= 57):
                    lexema += caracter
                    estado = 5
                
                elif caracter == '-':
                    lexema += caracter
                    estado = 3

                else:
                    print("símbolo: " + lexema)
                    self.texto += lexema
                    estado = 0
                    lexema = ""
                    indice -= 1
            
            #reconocimiento de id's
            elif estado == 4:
                if ((ord(caracter) >= 65 and ord(caracter) <= 90) or (ord(caracter) >= 97 and ord(caracter) <= 122) or (ord(caracter) >= 48 and ord(caracter) <= 57)):
                    lexema += caracter
                    estado = 4

                else:
                    print("id: " + lexema)
                    self.texto += lexema
                    estado = 0
                    lexema = ""
                    indice -= 1
            
            #reconocimiento de números
            elif estado == 5:
                if (ord(caracter) >= 48 and ord(caracter) <= 57):
                    lexema += caracter
                    estado = 5

                elif caracter == '.':
                    lexema += caracter
                    estado = 8

                else:
                    print("numero: " + lexema)
                    self.texto += lexema
                    estado = 0
                    lexema = ""
                    indice -= 1

            #reconocimiento de cadenas
            elif estado == 6:
                print("cadena | caracter empieza")
                self.texto += caracter
                estado = 66
                lexema = ""

            #termina de reconocer cadenas
            elif estado == 66:
                if (ord(caracter) != 34 and ord(caracter) != 39):
                    lexema += caracter
                    estado = 66
                
                else:
                    print("contenido cadena | caracter " + lexema)
                    self.texto += lexema
                    estado = 9
                    lexema = ""
                    indice -= 1
            
            #reconocimiento de comentario
            elif estado == 7:
                if (caracter == '-'):
                    lexema += caracter
                    estado = 10

                else:
                    estado = -1

            #reconocimiento de la otra parte del decimal
            elif estado == 8:
                if (ord(caracter) >= 48 and ord(caracter) <= 57):
                    lexema += caracter
                    estado = 11

                elif caracter == '.':
                    lexema += caracter
                    estado = 8

                else:
                    if iniciotag == True and fintag == False:
                        estado = -1
                    else:
                        estado = 0

            #termina de reconocer cadenas | caracteres
            elif estado == 9:
                print("cadena termina")
                self.texto += caracter
                estado = 0
                lexema = ""

            #reconocimiento de comentario
            elif estado == 10:
                if (caracter == '-'):
                    lexema += caracter
                    print("comentario empieza: " + lexema)
                    self.texto += lexema
                    lexema = ""
                    estado = 12

                else:
                    estado = -1

            #reconocimiento de un número decimal
            elif estado == 11:
                if (ord(caracter) >= 48 and ord(caracter) <= 57):
                    lexema += caracter
                    estado = 11
                else:
                    print("decimal " + lexema)
                    self.texto += lexema
                    estado = 0
                    lexema = ""
                    indice -= 1
            
            #reconocimiento de comentarios multilinea
            elif estado == 12:
                if caracter != '-' and caracter != '\n':
                    if lexema.find("PATHW:") >= 0 and esPath == False:
                        esPath = True
                    
                    if esPath == True:
                        path += caracter

                    lexema += caracter
                    estado = 12
                
                elif caracter == '\n':
                    lexema += caracter
                    columna = 0
                    fila += 1
                
                else:
                    print("comentario: " + lexema)
                    if esPath == True:
                        pathsplit = path.split('output')
                        self.ruta += pathsplit[1]
                        self.crearCarpeta(self.ruta)
                        esPath = False

                    self.texto += lexema
                    estado = 13
                    lexema = caracter
                    #indice -= 1
            
            #reconocimiento de comentario
            elif estado == 13:
                if caracter == '-':
                    lexema += caracter
                    estado = 14

                else:
                    estado = -1

            #reconocimiento de comentario
            elif estado == 14:
                if caracter == '>':
                    fintag = True
                    iniciotag = False
                    lexema += caracter
                    estado = 15

                else:
                    estado = -1

            #estado de aceptación
            elif estado == 15:
                print("termina comentario: " + lexema)
                self.texto += lexema
                estado = 0
                lexema = ""
                indice -= 1    

            #reconocimiento de errores
            elif estado == -1:
                print("Error: " + caracter)
                error = {'fila': fila, 'columna': columna, 'desc_error': "El caracter "+ caracter + " no pertenece al lenguaje"}
                self.listaErrores.append(error)
                estado = 0
                lexema = ""
            #ENDIF

            indice += 1
            columna += 1
        #ENDWHILE
    #ENDANALISIS

    def crearCarpeta(self, ruta):
        os.makedirs(ruta, exist_ok=True)
  
#ENDCLASS