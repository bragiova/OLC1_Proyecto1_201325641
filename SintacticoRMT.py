from LexicoRMT import LexicoRmt

class SintacticoRmt:
    def __init__(self):
        self.indice = -1
        self.listaTokens = None
        self.error = False
        self.operacion = ""
        self.lista_operaciones = list()
    #ENDINIT

    def analizadorLexico(self, texto):
        lex = LexicoRmt(texto)
        lex.analisis()
        self.listaTokens = lex.listaTokens
    #END

    def analizadorSintactico(self):
        self.obtenerToken()
        self.secuencia()
    #ENDANALIZADORSINTACTICO

    def obtenerToken(self):
        self.indice += 1
        if self.indice < len(self.listaTokens):
            self.token = self.listaTokens[self.indice]
            if self.token["id"] != 9:
                self.operacion += self.token["valor"]
    #END

    def secuencia(self):
        while True:
            self.expresion()
            while self.token["id"] != 9:
                #print("Error")
                self.error = True
                self.obtenerToken()

            if self.token["id"] == 9:
                if self.error:
                    ope = {"operacion": self.operacion, "estado": "Incorrecto"}
                    self.lista_operaciones.append(ope)
                    print(self.operacion + " Incorrecto")
                else:
                    print(self.operacion + " Correcto")
                    ope = {"operacion": self.operacion, "estado": "Correcto"}
                    self.lista_operaciones.append(ope)
                
                self.error = False
                self.operacion = ""
            
            self.obtenerToken()

            if self.indice >= len(self.listaTokens):
                break
    #END

    def expresion(self):
        self.termino()
        while self.token["id"] == 3 or self.token["id"] == 4:
            self.obtenerToken()
            self.termino()
    #END
    
    def termino(self):
        self.factor()
        while self.token["id"] == 5 or self.token["id"] == 6:
            self.obtenerToken()
            self.factor()
    #END

    def factor(self):
        if self.token["id"] == 2:
            self.obtenerToken()
        elif self.token["id"] == 1:
            self.obtenerToken()
        elif self.token["id"] == 7:
            self.obtenerToken()
            self.expresion()
            if self.token["id"] != 8:
                self.error = True
            else:
                self.obtenerToken()
        else:
            self.error = True
    #END

#ENDCLASS