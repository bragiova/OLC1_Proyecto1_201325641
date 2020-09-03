class Lexico:

    def __init__(self, entrada):
        self.listaCaracteres = list(entrada)
    
    def analisis(self):
        lexema = ""
        estado = 0
        fila = 0
        columna = 0
        indice = 0

        #prueba = 0

        while indice < len(self.listaCaracteres):
            caracter = self.listaCaracteres[indice]

            if estado == 0:
                if caracter == '\n':
                    fila += 1
                    estado = 0
                    columna = 0
            
                elif (caracter == ' ' or caracter == '\r' or caracter == '\t' or caracter == '\b' or caracter == '\f'):
                    estado = 0

                #comentarios
                elif caracter == '/':
                    estado = 1

                elif caracter == '*':
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

                elif caracter == '.':
                    estado = 2
                
                #estado cadenas
                elif (ord(caracter) == 34):
                    estado = 6
                
                #estado caracter
                elif (ord(caracter) == 39):
                    estado = 7

                #estado símbolos
                elif ((ord(caracter) >= 40 and ord(caracter) <= 44) or (ord(caracter) >= 58 and ord(caracter) <= 62) or caracter == '&' or caracter == '.' or caracter == '/' or caracter == '[' or caracter == ']' or caracter == '{' or caracter == '}' or caracter == '|'):
                    estado = 2
                
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
                    estado = 9

                else:
                    if lexema == "//":
                        print("comentario lineal empieza")
                        estado = 8
                    else:
                        print("símbolo: " + lexema)
                        estado = 0

                    lexema = ""
                    indice -= 1

            #reconocimiento de símbolos
            elif estado == 2:
                if ((ord(caracter) >= 40 and ord(caracter) <= 44) or (ord(caracter) >= 58 and ord(caracter) <= 62) or caracter == '&' or caracter == '.' or caracter == '/' or caracter == '[' or caracter == ']' or caracter == '{' or caracter == '}' or caracter == '|'):
                    if(caracter == '+' or caracter == '-' or caracter == '&' or caracter == '|' or caracter == '=' or caracter == '<' or caracter == '>'):
                        lexema += caracter
                        estado = 2

                    else:
                        print("símbolo: " + caracter)
                        estado = 0
                        lexema = ""
                        #indice -= 1
                
                else:
                    print("símbolo: " + lexema)
                    estado = 0
                    lexema = ""
                    indice -= 1
            
            #reconocimiento de id's
            elif estado == 3:
                if ((ord(caracter) >= 65 and ord(caracter) <= 90) or (ord(caracter) >= 97 and ord(caracter) <= 122) or (ord(caracter) >= 48 and ord(caracter) <= 57) or caracter == '_'):
                    lexema += caracter
                    estado = 3

                else:
                    print("id: " + lexema)
                    estado = 0
                    lexema = ""
                    indice -= 1
            
            #reconocimiento de números
            elif estado == 4:
                if (ord(caracter) >= 48 and ord(caracter) <= 57):
                    lexema += caracter
                    estado = 4

                elif caracter == '.':
                    estado = 10

                else:
                    print("numero: " + lexema)
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
                    estado = 0
                    lexema = ""
                    indice -= 1

            #reconocimiento de cadenas
            elif estado == 6:
                #if (ord(caracter) == 34):
                    #estado == 6
                
                #else:
                print("cadena empieza")
                estado = 11
                lexema = ""
                #indice -= 1
            
            #reconocimiento de caracteres
            elif estado == 7:
                #if (ord(caracter) == 39):
                    #estado = 7
                
                #else:
                    print("caracter empieza")
                    estado = 12
                    lexema = ""
                    #indice -= 1

            #reconocimiento de comentarios lineales
            elif estado == 8:
                if caracter != '\n':
                    lexema += caracter
                    estado = 8

                else:
                    print("comentario lineal: " + lexema)
                    estado = 0
                    lexema = ""
                    indice -= 1
            
            #reconocimiento de comentarios multilinea
            elif estado == 9:
                if caracter != '*':
                    lexema += caracter
                    estado = 9
                
                elif caracter == '\n':
                    columna = 0
                    fila += 1
                
                else:
                    print("comentario multi " + lexema)
                    estado = 13
                    lexema = ""
                    indice -= 1
            
            #reconocimiento de la otra parte del decimal
            elif estado == 10:
                if (ord(caracter) >= 48 and ord(caracter) <= 57):
                    lexema += caracter
                    estado = 14

                elif caracter == '.':
                    lexema += caracter
                    estado = 10

                else:
                    estado = -1

            #termina de reconocer cadenas
            elif estado == 11:
                if (ord(caracter) != 34):
                    lexema += caracter
                    estado = 11
                
                else:
                    print("contenido cadena " + lexema)
                    estado = 15
                    lexema = ""
                    indice -= 1
            
            #termina de reconocer caracteres
            elif estado == 12:
                if (ord(caracter) != 39):
                    lexema += caracter
                    estado = 12
                else:
                    print("contenido caracter " + lexema)
                    estado = 16
                    lexema = ""
                    indice -= 1
            
            #reconoce el final de un comentario multilínea
            elif estado == 13:
                if (caracter == '*'):
                    estado = 13

                elif caracter == '/':
                    estado = 17

                elif caracter == '\n':
                    columna = 0
                    fila += 1

                else:
                    estado = 9

            #reconocimiento de un número decimal
            elif estado == 14:
                if (ord(caracter) >= 48 and ord(caracter) <= 57):
                    lexema += caracter
                    estado = 14
                else:
                    print("decimal " + lexema)
                    estado = 0
                    lexema = ""
                    indice -= 1
            
            #estado de aceptación
            elif estado == 15:
                print("cadena termina")
                estado = 0
                lexema = ""

            #estado de aceptación
            elif estado == 16:
                print("termina caracter")
                estado = 0
                lexema = ""

            #estado de aceptación
            elif estado == 17:
                print("termina comentario multi")
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

pruebaArchivo = open("ejemplo.js", "r")
lex = Lexico(str(pruebaArchivo.read()))
lex.analisis()