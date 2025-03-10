import os

class LexicoCss:

    def __init__(self, entrada):
        self.listaCaracteres = list(entrada)
        self.texto = ""
        self.ruta = "output\\"
        self.listaErrores = list()
        self.bitacora = ""
    #ENDINIT
    
    def analisis(self):
        lexema = ""
        estado = 0
        fila = 1
        columna = 0
        indice = 0
        esPath = False
        path = ""

        while indice < len(self.listaCaracteres):
            caracter = self.listaCaracteres[indice]

            if estado == 0:
                self.bitacora += "Estado 0\n"
                if caracter == '\n':
                    fila += 1
                    estado = 0
                    columna = 0
                    self.texto += caracter
            
                elif (caracter == ' ' or caracter == '\r' or caracter == '\t' or caracter == '\b' or caracter == '\f'):
                    estado = 0
                    self.texto += caracter

                #comentarios
                elif caracter == '/':
                    estado = 1

                #estado símbolos
                elif (caracter == '=' or caracter == ';' or caracter == ',' or caracter == '(' or caracter == ')' or caracter == '{' or caracter == '}' or caracter == ':' or caracter == '%' or caracter == '.' or caracter == '*'):
                    estado = 2

                #estado letras
                elif ((ord(caracter) >= 65 and ord(caracter) <= 90) or (ord(caracter) >= 97 and ord(caracter) <= 122)):
                    estado = 3

                #estado numeros
                elif ((ord(caracter) >= 48 and ord(caracter) <= 57)):
                    estado = 4
                
                #reconocer números negativos
                elif caracter == '-':
                    estado = 5
                
                #estado cadenas y caracter
                elif ((ord(caracter) == 34) or (ord(caracter) == 39)):
                    estado = 6

                elif caracter == '#':
                    estado = 7
                
                #estado error
                else:
                    estado = -1
            #ENDIF

            if estado == 1:
                self.bitacora += "Estado 1\n"
                if caracter == '/':
                    #prueba += 1
                    lexema += caracter
                    estado = 1
                
                elif caracter == '*':
                    lexema += caracter
                    print("comentario empieza: " + lexema)
                    estado = 8
                    self.texto += lexema
                    lexema = ""

                else:
                    lexema = ""
                    estado = -1
                    #indice -= 1

            #reconocimiento de símbolos
            elif estado == 2:
                self.bitacora += "Estado 2\n"
                if (caracter == '=' or caracter == ';' or caracter == ',' or caracter == '(' or caracter == ')' or caracter == '{' or caracter == '}' or caracter == ':' or caracter == '%' or caracter == '.' or caracter == '*'):
                    if caracter == ':':
                        lexema += caracter
                        estado = 2

                    else:
                        print("símbolo: " + caracter)
                        self.bitacora += "Lexema aceptado -> Símbolo -> " + caracter + "\n"
                        self.texto += caracter
                        estado = 0
                        lexema = ""
                        #indice -= 1
                
                else:
                    print("símbolo: " + lexema)
                    self.bitacora += "Lexema aceptado -> Símbolo -> " + lexema + "\n"
                    self.texto += lexema
                    estado = 0
                    lexema = ""
                    indice -= 1
            
            #reconocimiento de id's
            elif estado == 3:
                self.bitacora += "Estado 3\n"
                if ((ord(caracter) >= 65 and ord(caracter) <= 90) or (ord(caracter) >= 97 and ord(caracter) <= 122) or (ord(caracter) >= 48 and ord(caracter) <= 57) or caracter == '-'):
                    lexema += caracter
                    estado = 3

                else:
                    print("id: " + lexema)
                    self.bitacora += "Lexema aceptado -> Id -> " + lexema + "\n"
                    self.texto += lexema
                    estado = 0
                    lexema = ""
                    indice -= 1
            
            #reconocimiento de números
            elif estado == 4:
                self.bitacora += "Estado 4\n"
                if (ord(caracter) >= 48 and ord(caracter) <= 57):
                    lexema += caracter
                    estado = 4

                elif caracter == '.':
                    lexema += caracter
                    estado = 9

                else:
                    print("numero: " + lexema)
                    self.bitacora += "Lexema aceptado -> Número -> " + lexema + "\n"
                    self.texto += lexema
                    estado = 0
                    lexema = ""
                    indice -= 1
            
            #reconocimiento de números negativos
            elif estado == 5:
                self.bitacora += "Estado 5\n"
                if (ord(caracter) >= 48 and ord(caracter) <= 57):
                    lexema += caracter
                    estado = 4
                
                elif caracter == '-':
                    lexema += caracter
                    estado = 5

                else:
                    print("símbolo: " + lexema)
                    self.bitacora += "Lexema aceptado -> Número -> " + lexema + "\n"
                    self.texto += lexema
                    estado = 0
                    lexema = ""
                    indice -= 1

            #reconocimiento de cadenas
            elif estado == 6:
                self.bitacora += "Estado 6\n"
                print("cadena | caracter empieza")
                self.texto += caracter
                estado = 66
                lexema = ""
                self.bitacora += "Lexema aceptado -> Símbolo -> " + caracter + "\n"

            #termina de reconocer cadenas
            elif estado == 66:
                self.bitacora += "Estado 6\n"
                if (ord(caracter) != 34 and ord(caracter) != 39):
                    lexema += caracter
                    estado = 66
                
                else:
                    print("contenido cadena | caracter " + lexema)
                    self.texto += lexema
                    self.bitacora += "Lexema aceptado -> . -> " + caracter + "\n"
                    estado = 10
                    lexema = ""
                    indice -= 1
            
            #reconocimiento de hexadecimal
            elif estado == 7:
                self.bitacora += "Estado 7\n"
                if (caracter == '#'):
                    lexema += caracter
                    estado = 7
                
                elif ((ord(caracter) >= 65 and ord(caracter) <= 90) or (ord(caracter) >= 97 and ord(caracter) <= 122) or (ord(caracter) >= 48 and ord(caracter) <= 57)):
                    lexema += caracter
                    estado = 11

                else:
                    print("símbolo: " + lexema)
                    self.bitacora += "Lexema aceptado -> Símbolo -> " + lexema + "\n"
                    self.texto += lexema
                    estado = 0
                    lexema = ""
                    indice -= 1
            
            #reconocimiento de comentarios multilinea
            elif estado == 8:
                self.bitacora += "Estado 8\n"
                if caracter != '*' and caracter != '\n':
                    if lexema.find("PATHW:") >= 0 and esPath == False:
                        esPath = True
                    
                    if esPath == True:
                        path += caracter
                    
                    lexema += caracter
                    estado = 8
                
                elif caracter == '\n':
                    lexema += caracter
                    columna = 0
                    fila += 1
                    #self.texto += caracter
                
                else:
                    print("comentario: " + lexema)
                    if esPath == True:
                        pathsplit = path.split('output')
                        self.ruta += pathsplit[1]
                        self.crearCarpeta(self.ruta)
                        esPath = False

                    self.texto += lexema
                    estado = 12
                    lexema = ""
                    indice -= 1
            
            #reconocimiento de la otra parte del decimal
            elif estado == 9:
                self.bitacora += "Estado 9\n"
                if (ord(caracter) >= 48 and ord(caracter) <= 57):
                    lexema += caracter
                    estado = 13

                elif caracter == '.':
                    lexema += caracter
                    estado = 9

                else:
                    estado = -1

            #termina de reconocer cadenas | caracteres
            elif estado == 10:
                self.bitacora += "Estado 10\n"
                print("cadena termina")
                self.texto += caracter
                estado = 0
                lexema = ""
                self.bitacora += "Lexema aceptado -> Símbolo -> " + caracter + "\n"
            
            #termina de reconocer caracteres
            elif estado == 11:
                self.bitacora += "Estado 11\n"
                if ((ord(caracter) >= 65 and ord(caracter) <= 90) or (ord(caracter) >= 97 and ord(caracter) <= 122) or (ord(caracter) >= 48 and ord(caracter) <= 57)):
                    lexema += caracter
                    estado = 11

                else:
                    print("símbolo: " + lexema)
                    self.bitacora += "Lexema aceptado -> NúmeroHexa -> " + lexema + "\n"
                    self.texto += lexema
                    estado = 0
                    lexema = ""
                    indice -= 1
            
            #reconoce el final de un comentario multilínea
            elif estado == 12:
                self.bitacora += "Estado 12\n"
                if (caracter == '*'):
                    lexema += caracter
                    self.texto += caracter
                    estado = 12

                elif caracter == '/':
                    lexema += caracter
                    estado = 14
                    self.texto += caracter

                elif caracter == '\n':
                    columna = 0
                    fila += 1
                    self.texto += caracter

                else:
                    estado = 8

            #reconocimiento de un número decimal
            elif estado == 13:
                self.bitacora += "Estado 13\n"
                if (ord(caracter) >= 48 and ord(caracter) <= 57):
                    lexema += caracter
                    estado = 13
                else:
                    print("decimal " + lexema)
                    self.bitacora += "Lexema aceptado -> Decimal -> " + lexema + "\n"
                    self.texto += lexema
                    estado = 0
                    lexema = ""
                    indice -= 1

            #estado de aceptación
            elif estado == 14:
                self.bitacora += "Estado 14\n"
                print("termina comentario: " + lexema)
                self.texto += caracter
                estado = 0
                lexema = ""       

            #reconocimiento de errores
            elif estado == -1:
                self.bitacora += "Estado Error\n"
                print("Error: " + caracter)
                self.bitacora += "Caracter no reconocido -> " + caracter + "\n"
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