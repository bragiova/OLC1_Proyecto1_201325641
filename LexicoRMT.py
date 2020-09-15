
class LexicoRmt:

    def __init__(self, entrada):
        self.listaCaracteres = list(entrada)
        self.listaErrores = list()
        self.listaTokens = list()
    #ENDINIT
    
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
                    token = {'id': 9, 'token': "salto", 'valor': caracter}
                    self.listaTokens.append(token)
            
                elif (caracter == ' ' or caracter == '\r' or caracter == '\t' or caracter == '\b' or caracter == '\f'):
                    estado = 0

                #estado símbolos
                elif (caracter == '+' or caracter == '-' or caracter == '*' or caracter == '(' or caracter == ')' or caracter == '/'):
                    estado = 1

                #estado letras
                elif ((ord(caracter) >= 65 and ord(caracter) <= 90) or (ord(caracter) >= 97 and ord(caracter) <= 122)):
                    estado = 2

                #estado numeros
                elif ((ord(caracter) >= 48 and ord(caracter) <= 57)):
                    estado = 3
                
                #estado error
                else:
                    estado = -1
            #ENDIF

            #reconocimiento de símbolos
            if estado == 1:
                token = None
                if (caracter == '+' or caracter == '-' or caracter == '*' or caracter == '(' or caracter == ')' or caracter == '/'):
                    print("símbolo: " + caracter)

                    if caracter == '+':
                        token = {'id': 3, 'token': "mas", 'valor': caracter}
                    elif caracter == '-':
                        token = {'id': 4, 'token': "menos", 'valor': caracter}
                    elif caracter == '*':
                        token = {'id': 5, 'token': "por", 'valor': caracter}
                    elif caracter == '/':
                        token = {'id': 6, 'token': "div", 'valor': caracter}
                    elif caracter == '(':
                        token = {'id': 7, 'token': "para", 'valor': caracter}
                    elif caracter == ')':
                        token = {'id': 8, 'token': "parc", 'valor': caracter}

                    self.listaTokens.append(token)
                    estado = 0
                    lexema = ""
                    #indice -= 1
            
            #reconocimiento de id's
            elif estado == 2:
                if ((ord(caracter) >= 65 and ord(caracter) <= 90) or (ord(caracter) >= 97 and ord(caracter) <= 122) or (ord(caracter) >= 48 and ord(caracter) <= 57) or caracter == '_'):
                    lexema += caracter
                    estado = 2

                else:
                    print("id: " + lexema)
                    token = {'id': 1, 'token': "identificador", 'valor': lexema}
                    self.listaTokens.append(token)
                    estado = 0
                    lexema = ""
                    indice -= 1
            
            #reconocimiento de números
            elif estado == 3:
                if (ord(caracter) >= 48 and ord(caracter) <= 57):
                    lexema += caracter
                    estado = 3

                elif caracter == '.':
                    lexema += caracter
                    estado = 4

                else:
                    print("numero: " + lexema)
                    token = {'id': 2, 'token': "numero", 'valor': lexema}
                    self.listaTokens.append(token)
                    estado = 0
                    lexema = ""
                    indice -= 1
            
            #reconocimiento de la otra parte del decimal
            elif estado == 4:
                if (ord(caracter) >= 48 and ord(caracter) <= 57):
                    lexema += caracter
                    estado = 5

                elif caracter == '.':
                    lexema += caracter
                    estado = 4

                else:
                    estado = -1

            #reconocimiento de un número decimal
            elif estado == 5:
                if (ord(caracter) >= 48 and ord(caracter) <= 57):
                    lexema += caracter
                    estado = 5
                else:
                    print("decimal " + lexema)
                    token = {'id': 2, 'token': "numero", 'valor': lexema}
                    self.listaTokens.append(token)
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

    def imprimir(self):
        for tok in self.listaTokens:
            print(str(tok["id"]) + " - " + tok["token"] + " - " + str(tok["valor"]))
  
#ENDCLASS