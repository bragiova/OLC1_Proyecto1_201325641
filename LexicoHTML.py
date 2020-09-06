class LexicoHtml:

    def __init__(self, entrada):
        self.listaCaracteres = list(entrada)
        self.texto = ""
    
    def analisis(self):
        lexema = ""
        estado = 0
        fila = 0
        columna = 0
        indice = 0

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
                    estado = -1
            #ENDIF

            if estado == 1:
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
                    #if lexema == "//":
                        #print("comentario lineal empieza")
                        #estado = 8
                    #else:
                        #print("símbolo: " + lexema)
                        #estado = 0

                    #self.texto += lexema
                    lexema = ""
                    estado = -1
                    #indice -= 1

            #reconocimiento de símbolos
            elif estado == 2:
                if (caracter == '=' or caracter == ';' or caracter == ',' or caracter == '(' or caracter == ')' or caracter == '{' or caracter == '}' or caracter == ':' or caracter == '%' or caracter == '.' or caracter == '*'):
                    if caracter == ':':
                        lexema += caracter
                        estado = 2

                    else:
                        print("símbolo: " + caracter)
                        self.texto += caracter
                        estado = 0
                        lexema = ""
                        #indice -= 1
                
                else:
                    print("símbolo: " + lexema)
                    self.texto += lexema
                    estado = 0
                    lexema = ""
                    indice -= 1
            
            #reconocimiento de id's
            elif estado == 3:
                if ((ord(caracter) >= 65 and ord(caracter) <= 90) or (ord(caracter) >= 97 and ord(caracter) <= 122) or (ord(caracter) >= 48 and ord(caracter) <= 57) or caracter == '-'):
                    lexema += caracter
                    estado = 3

                else:
                    print("id: " + lexema)
                    self.texto += lexema
                    estado = 0
                    lexema = ""
                    indice -= 1
            
            #reconocimiento de números
            elif estado == 4:
                if (ord(caracter) >= 48 and ord(caracter) <= 57):
                    lexema += caracter
                    estado = 4

                elif caracter == '.':
                    lexema += caracter
                    estado = 9

                else:
                    print("numero: " + lexema)
                    self.texto += lexema
                    estado = 0
                    lexema = ""
                    indice -= 1
            
            #reconocimiento de números negativos
            elif estado == 5:
                if (ord(caracter) >= 48 and ord(caracter) <= 57):
                    lexema += caracter
                    estado = 4
                
                elif caracter == '-':
                    lexema += caracter
                    estado = 5

                else:
                    print("símbolo: " + lexema)
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
                    estado = 10
                    lexema = ""
                    indice -= 1
            
            #reconocimiento de hexadecimal
            elif estado == 7:
                if (caracter == '#'):
                    lexema += caracter
                    estado = 7
                
                elif ((ord(caracter) >= 65 and ord(caracter) <= 90) or (ord(caracter) >= 97 and ord(caracter) <= 122) or (ord(caracter) >= 48 and ord(caracter) <= 57)):
                    lexema += caracter
                    estado = 11

                else:
                    print("símbolo: " + lexema)
                    self.texto += lexema
                    estado = 0
                    lexema = ""
                    indice -= 1
            
            #reconocimiento de comentarios multilinea
            elif estado == 8:
                if caracter != '*' and caracter != '\n':
                    lexema += caracter
                    estado = 8
                
                elif caracter == '\n':
                    lexema += caracter
                    columna = 0
                    fila += 1
                    #self.texto += caracter
                
                else:
                    print("comentario: " + lexema)
                    self.texto += lexema
                    estado = 12
                    lexema = ""
                    indice -= 1
            
            #reconocimiento de la otra parte del decimal
            elif estado == 9:
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
                print("cadena termina")
                self.texto += caracter
                estado = 0
                lexema = ""
            
            #termina de reconocer caracteres
            elif estado == 11:
                if ((ord(caracter) >= 65 and ord(caracter) <= 90) or (ord(caracter) >= 97 and ord(caracter) <= 122) or (ord(caracter) >= 48 and ord(caracter) <= 57)):
                    lexema += caracter
                    estado = 11

                else:
                    print("símbolo: " + lexema)
                    self.texto += lexema
                    estado = 0
                    lexema = ""
                    indice -= 1
            
            #reconoce el final de un comentario multilínea
            elif estado == 12:
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
                if (ord(caracter) >= 48 and ord(caracter) <= 57):
                    lexema += caracter
                    estado = 13
                else:
                    print("decimal " + lexema)
                    self.texto += lexema
                    estado = 0
                    lexema = ""
                    indice -= 1

            #estado de aceptación
            elif estado == 14:
                print("termina comentario: " + lexema)
                self.texto += caracter
                estado = 0
                lexema = ""       

            #reconocimiento de errores
            elif estado == -1:
                print("Error: " + caracter)
                estado = 0
                lexema = ""
            #ENDIF

            indice += 1
            columna += 1
        #ENDWHILE
    #ENDANALISIS
  
    #ENDINIT
#ENDCLASS

pruebaArchivo = open("styles.css", "r")
lex = LexicoCss(str(pruebaArchivo.read()))
lex.analisis()
#escribir el archivo ya corregido
archivoSalida = open("ArchivoSalidaCSS.css", "w")
archivoSalida.write(lex.texto)
archivoSalida.close()