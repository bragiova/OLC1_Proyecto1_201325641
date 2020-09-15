import os
from graphviz import Digraph

class Lexico:

    def __init__(self, entrada):
        self.listaCaracteres = list(entrada)
        self.texto = ""
        self.ruta = "output\\"
        self.listaErrores = list()
        self.id = False
        self.comentariolineal = False
        self.comentariomulti = False
        self.cadena = False
        self.carac = False
        self.numero = False
        self.simbolo = False
        self.decimal = False
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
                    lexema += caracter
                    estado = 9

                else:
                    if lexema == "//":
                        print("comentario lineal empieza")
                        estado = 8
                    else:
                        print("símbolo: " + lexema)
                        estado = 0

                    self.texto += lexema
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
                        self.simbolo = True
                        self.texto += caracter
                        estado = 0
                        lexema = ""
                        #indice -= 1
                
                else:
                    print("símbolo: " + lexema)
                    self.simbolo = True
                    self.texto += lexema
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
                    self.id = True
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
                    estado = 10

                else:
                    print("numero: " + lexema)
                    self.numero = True
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
                    self.simbolo = True
                    self.texto += lexema
                    estado = 0
                    lexema = ""
                    indice -= 1

            #reconocimiento de cadenas
            elif estado == 6:
                #if (ord(caracter) == 34):
                    #estado == 6
                
                #else:
                print("cadena empieza")
                self.texto += caracter
                estado = 11
                lexema = ""
                #indice -= 1
            
            #reconocimiento de caracteres
            elif estado == 7:
                #if (ord(caracter) == 39):
                    #estado = 7
                
                #else:
                    print("caracter empieza")
                    self.texto += caracter
                    estado = 12
                    lexema = ""
                    #indice -= 1

            #reconocimiento de comentarios lineales
            elif estado == 8:
                if caracter != '\n':
                    if lexema.find("PATHW:") >= 0 and esPath == False:
                        esPath = True
                    
                    if esPath == True:
                        path += caracter

                    lexema += caracter
                    estado = 8

                else:
                    print("comentario lineal: " + lexema)
                    if esPath == True:
                        pathsplit = path.split('output')
                        self.ruta += pathsplit[1]
                        self.crearCarpeta(self.ruta)
                        esPath = False

                    self.texto += lexema
                    self.comentariolineal = True
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
                    self.texto += caracter
                
                else:
                    print("comentario multi " + lexema)
                    self.texto += lexema
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
                    self.texto += lexema
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
                    self.texto += lexema
                    estado = 16
                    lexema = ""
                    indice -= 1
            
            #reconoce el final de un comentario multilínea
            elif estado == 13:
                if (caracter == '*'):
                    self.texto += caracter
                    estado = 13

                elif caracter == '/':
                    estado = 17
                    self.texto += caracter

                elif caracter == '\n':
                    columna = 0
                    fila += 1
                    self.texto += caracter

                else:
                    estado = 9

            #reconocimiento de un número decimal
            elif estado == 14:
                if (ord(caracter) >= 48 and ord(caracter) <= 57):
                    lexema += caracter
                    estado = 14
                else:
                    print("decimal " + lexema)
                    self.decimal = True
                    self.texto += lexema
                    estado = 0
                    lexema = ""
                    indice -= 1
            
            #estado de aceptación
            elif estado == 15:
                print("cadena termina")
                self.cadena = True
                self.texto += caracter
                estado = 0
                lexema = ""

            #estado de aceptación
            elif estado == 16:
                print("termina caracter")
                self.carac = True
                self.texto += caracter
                estado = 0
                lexema = ""

            #estado de aceptación
            elif estado == 17:
                print("termina comentario multi")
                self.comentariomulti = True
                self.texto += lexema
                estado = 0
                lexema = ""       

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
    #ENDCREARCARPETA

    def generarArbol(self):
        dot = Digraph(comment='Reporte JS')
        dot.attr('node', shape='circle')
        dot.node("0", "JS")
        
        if (self.id):
            self.autoId(dot)
        
        if self.numero:
            self.autoNumero(dot)

        if self.comentariolineal:
            self.autoComentarioLineal(dot)

        if self.comentariomulti:
            self.autoComentarioMulti(dot)

        if self.cadena:
            self.autoCadena(dot)

        if self.carac:
            self.autoCaracter(dot)

        if self.decimal:
            self.autoDecimal(dot)

        dot.render('ReporteJS.gv', view=False)
        #print("Grafo de Estados Generado")
    #ENDGENERARARBOL

    def autoId(self, dot):
        dot.node("1", "ID")
        dot.node("I1", "S0")
        dot.node("I2", "S1", shape="doublecircle")
        dot.edge("0", "1")
        dot.edge("1", "I1")
        dot.edge("I1", "I2", "L")
        dot.edge("I2", "I2", "L,D,_")
    #END
    
    def autoComentarioLineal(self, dot):
        dot.node("2", "Comentario Lineal")
        dot.node("CL1", "S0")
        dot.node("CL2", "S1")
        dot.node("CL3", "S2", shape="doublecircle")
        dot.edge("0", "2")
        dot.edge("2", "CL1")
        dot.edge("CL1", "CL2", "/")
        dot.edge("CL2", "CL3", "/")
        dot.edge("CL3", "CL3", ".")
    #END

    def autoComentarioMulti(self, dot):
        dot.node("3", "Comentario Multilínea")
        dot.node("CM1", "S0")
        dot.node("CM2", "S1")
        dot.node("CM3", "S2")
        dot.node("CM4", "S3")
        dot.node("CM5", "S4", shape="doublecircle")
        dot.edge("0", "3")
        dot.edge("3", "CM1")
        dot.edge("CM1", "CM2", "/")
        dot.edge("CM2", "CM3", "*")
        dot.edge("CM3", "CM3", ".")
        dot.edge("CM3", "CM4", "*")
        dot.edge("CM4", "CM4", "*")
        dot.edge("CM4", "CM5", "/")
    #END

    def autoNumero(self, dot):
        dot.node("4", "Número")
        dot.node("N1", "S0")
        dot.node("N2", "S1")
        dot.node("N3", "S2", shape="doublecircle")
        dot.edge("0", "4")
        dot.edge("4", "N1")
        dot.edge("N1", "N2", "-")
        dot.edge("N1", "N3", "D")
        dot.edge("N2", "N3", "D")
        dot.edge("N3", "N3", "D")
    #END
    
    def autoDecimal(self, dot):
        dot.node("8", "Decimal")
        dot.node("D1", "S0")
        dot.node("D2", "S1")
        dot.node("D3", "S2", shape="doublecircle")
        dot.node("D4", "S3")
        dot.node("D5", "S4", shape="doublecircle")
        dot.edge("0", "8")
        dot.edge("8", "D1")
        dot.edge("D1", "D2", "-")
        dot.edge("D1", "D3", "D")
        dot.edge("D2", "D3", "D")
        dot.edge("D3", "D3", "D")
        dot.edge("D3", "D4", ".")
        dot.edge("D4", "D5", "D")
        dot.edge("D5", "D5", "D")
    #END

    def autoCadena(self, dot):
        dot.node("5", "Cadena")
        dot.node("C1", "S0")
        dot.node("C2", "S1")
        dot.node("C3", "S2", shape="doublecircle")
        dot.edge("0", "5")
        dot.edge("5", "C1")
        dot.edge("C1", "C2", "\"")
        dot.edge("C2", "C2", ".")
        dot.edge("C2", "C3", "\"")
    #END

    def autoCaracter(self, dot):
        dot.node("6", "Caracter")
        dot.node("CR1", "S0")
        dot.node("CR2", "S1")
        dot.node("CR3", "S2", shape="doublecircle")
        dot.edge("0", "6")
        dot.edge("6", "CR1")
        dot.edge("CR1", "CR2", "'")
        dot.edge("CR2", "CR2", ".")
        dot.edge("CR2", "CR3", "'")
    #END

    def autoSimbolo(self, dot):
        dot.node("7", "Símbolo")
        dot.node("S1", "S0")
        dot.node("S2", "S1", shape="doublecircle")
        dot.edge("0", "7")
        dot.edge("7", "S1")
        dot.edge("S1", "S2", "S")
    #END
  
#ENDCLASS

#pruebaArchivo = open("dibujo.js", "r")
#lex = Lexico(str(pruebaArchivo.read()))
#lex.analisis()
#escribir el archivo ya corregido
#archivoSalida = open(lex.ruta + "\\ArchivoSalidaJS.js", "w")
#archivoSalida.write(lex.texto)
#archivoSalida.close()
