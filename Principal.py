from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter.scrolledtext import ScrolledText
from tkinter import messagebox
import os
import threading
from LexicoJS import Lexico
from LexicoHTML import LexicoHtml
from LexicoCSS import LexicoCss
from SintacticoRMT import SintacticoRmt


class Principal:

    def __init__(self, window):
        self.ventana = window
        self.ventana.title("ML WEB")
        self.extensionArchivo = ""
        self.listaErroresGeneral = list()
        self.reportecss = ""
        self.lexi = None
        self.sintactico = None

        frame = LabelFrame(self.ventana, text = '')
        frame.grid(row=0,column=0,columnspan=20,pady=20, sticky=N+S+E+W)

        #############################################_MENU_#############################################

        menubarra = Menu(self.ventana)
        menuarchivo = Menu(menubarra, tearoff = 0, font=("Comic Sans MS", 9))
        menuarchivo.add_command(label="Nuevo")
        menuarchivo.add_command(label="Abrir", command=self.abrirArchivo)
        menuarchivo.add_command(label="Guardar")
        menuarchivo.add_command(label="Guardar como")
        menuarchivo.add_separator()
        menuarchivo.add_command(label="Salir", command=self.terminar)
        menubarra.add_cascade(label="Archivo", menu=menuarchivo)

        menuejecutar = Menu(menubarra, tearoff=0, font=("Comic Sans MS", 9))
        menuejecutar.add_command(label="Analizar", command=self.analizar)
        menubarra.add_cascade(label="Ejecutar", menu=menuejecutar)

        menureportes = Menu(menubarra, tearoff=0, font=("Comic Sans MS", 9))
        menureportes.add_command(label="Reporte JavaScript", command=self.reporteJs)
        menureportes.add_command(label="Reporte CSS", command=self.bitacoraCss)
        menureportes.add_command(label="Errores Léxicos", command=self.generarHtmlErrores)
        menureportes.add_command(label="Sintáctico", command=self.reporteSintactico)
        menubarra.add_cascade(label="Reportes", menu=menureportes)

        self.ventana.config(menu=menubarra)

        self.labelcursor = Label(frame, text='A', font=("Comic Sans MS", 9))
        self.labelcursor.grid(row=6,column=5)
        ############################################_ENTRADA_############################################
        #self.labelarchivo = Label(frame, text='Archivo de Entrada:', font=("Comic Sans MS", 9)).grid(row=3,column=5)
        self.labelarchivo = Label(frame, text='Archivo de Entrada:', font=("Comic Sans MS", 9))
        self.labelarchivo.grid(row=3,column=5)
        self.entrada = Text(frame, height=30, width=80, wrap=NONE, font=("Comic Sans MS", 10))
        self.entrada.grid(row=4,column=5, sticky=N+S+E+W)

        scrollvertical = Scrollbar(frame, orient=VERTICAL, command=self.entrada.yview)
        scrollvertical.grid(row=4, column=6, sticky=N+S+W)

        scrollhorizontal = Scrollbar(frame, orient=HORIZONTAL, command=self.entrada.xview)
        scrollhorizontal.grid(row=5, column=5, sticky=E+W+N)
        self.entrada.configure(yscrollcommand=scrollvertical.set, xscrollcommand=scrollhorizontal.set)

        ############################################_SALIDA_############################################3
        Label(frame,text='Consola', font=("Comic Sans MS", 9)).grid(row=3,column=16, sticky=N+S+E+W)
        self.salida = Text(frame, height=30, width=60, wrap=NONE, font=("Consolas", 9), bg="black", fg="white")
        self.salida.grid(row=4,column=16, sticky=N+S+E+W)

        scrollverticalConsola = Scrollbar(frame, orient=VERTICAL, command=self.salida.yview)
        scrollverticalConsola.grid(row=4, column=17, sticky=N+S+W)

        scrollhorizontalConsola = Scrollbar(frame, orient=HORIZONTAL, command=self.salida.xview)
        scrollhorizontalConsola.grid(row=5, column=16, sticky=E+W+N)
        self.salida.configure(yscrollcommand=scrollverticalConsola.set, xscrollcommand=scrollhorizontalConsola.set)

        self.ventana.grid_columnconfigure(0, weight=1)
        self.ventana.grid_rowconfigure(0, weight=1)

        frame.grid_columnconfigure(5, weight=1)
        #frame.grid_columnconfigure(8, weight=1)
        frame.grid_columnconfigure(6, weight=1)
        frame.grid_columnconfigure(16, weight=1)
        frame.grid_columnconfigure(17, weight=1)

        frame.grid_rowconfigure(3, weight=1)
        frame.grid_rowconfigure(4, weight=1)
        frame.grid_rowconfigure(5, weight=1)
        frame.grid_rowconfigure(6, weight=1)
    #END


    def abrirArchivo(self):
        filename = askopenfilename(filetypes=(("Archivos HTML", "*.html"), ("Archivos JS", "*.js"), ("Archivos CSS", "*.css"), ("Archivos RMT", "*.rmt")))

        archivo = open(filename,"r", encoding="utf-8")
        texto = archivo.read()
        archivo.close()

        nombreArchivo = os.path.split(filename)
        extension = nombreArchivo[1].split('.')
        self.extensionArchivo = extension[1]

        self.labelarchivo.configure(text=nombreArchivo[1])

        self.entrada.delete(1.0, END)
        self.entrada.insert(INSERT,texto)
        return
    #END


    def analizar(self):
        texto = self.entrada.get("1.0",END)

        if self.extensionArchivo == "js":
            self.lexi = Lexico(texto)
            self.lexi.analisis()
            self.crearArchivoCorregido(self.lexi.ruta, self.lexi.texto)
            if len(self.lexi.listaErrores) > 0:
                self.obtenerErrores(self.lexi.listaErrores)
        
        elif self.extensionArchivo == "css":
            self.lexi = LexicoCss(texto)
            self.lexi.analisis()
            self.crearArchivoCorregido(self.lexi.ruta, self.lexi.texto)
            if len(self.lexi.listaErrores) > 0:
                self.obtenerErrores(self.lexi.listaErrores)
        
        elif self.extensionArchivo == "html":
            self.lexi = LexicoHtml(texto)
            self.lexi.analisis()
            #escribir el archivo ya corregido
            self.crearArchivoCorregido(self.lexi.ruta, self.lexi.texto)
            if len(self.lexi.listaErrores) > 0:
                self.obtenerErrores(self.lexi.listaErrores)
        
        elif self.extensionArchivo == "rmt":
            self.sintactico = SintacticoRmt()
            self.sintactico.analizadorLexico(texto)
            self.sintactico.analizadorSintactico()
        
        else:
            messagebox.showerror("ML WEB", "Archivo con extensión no permitida para el análisis")
            return

        messagebox.showinfo("ML WEB", "Análisis finalizado")
    #END

    def crearArchivoCorregido(self, ruta, texto):
        #escribir el archivo ya corregido
        archivoSalida = open(ruta + "\\" + self.labelarchivo['text'], "w")
        archivoSalida.write(texto)
        archivoSalida.close()

    def terminar(self):
        self.ventana.destroy()
        return
    #END

    def obtenerErrores(self, listaerrores):
        self.salida.delete(1.0, END)
        consola = "\t\t\tERRORES LÉXICOS\nFila\tColumna\tError\n"
        for error in listaerrores:
            errorGeneral = {"fila": str(error['fila']), "columna": str(error['columna']), "desc_error": str(error['desc_error'])}
            consola += str(error['fila']) + "\t" + str(error['columna']) + "\t" + str(error['desc_error']) + "\n"
            #print(str(error['fila']) + " - " + str(error['columna']) + " - " + str(error['desc_error']))
            self.listaErroresGeneral.append(errorGeneral)
        self.salida.insert(INSERT,consola)
    #END

    def generarHtmlErrores(self):
        if len(self.listaErroresGeneral) == 0:
            messagebox.error("ML WEB", "No se registraron errores en el archivo")
            return

        if self.extensionArchivo == "js":
            lenguaje = "JavaScript"
        elif self.extensionArchivo == "css":
            lenguaje = "CSS"
        elif self.extensionArchivo == "html":
            lenguaje = "HTML"

        contador = 0
        html = "<!DOCTYPE html>\n"
        html += "<html>\n"
        html += "\t<head>\n"
        html += "\t\t<meta charset = \"utf-8\">\n"
        html += "\t\t<title>Reporte de Errores</title>\n"
        html += "\t\t<style>\n"
        html += "\t\t\ttable, th, td{\n\t\t\t\tborder: 3px solid blue;\n"
        html += "\t\t\t\tborder-collapse: collapse;\n\t\t\t}\n"
        html += "\t\t\tth, td, h2{\n\t\t\t\ttext-align: center;\n\t\t\t}\n"
        html += "\t\t</style>\n"
        html += "\t</head>\n"
        html += "\t<body>\n"
        html += "\t\t<h2>Reporte de Errores L&eacutexicos " + lenguaje + "</h2>\n"
        html += "\t\t<table align= \"center\">\n"
        html += "\t\t\t<tr>\n\t\t\t\t" + "<th>No.</th>\n\t\t\t\t" + "<th>Fila</th>\n\t\t\t\t" + "<th>Columna</th>\n\t\t\t\t" + "<th>Error</th>\n\t\t\t"
        html += "</tr>\n"
        
        for error in self.listaErroresGeneral:
            contador += 1
            html += "\t\t\t<tr>\n\t\t\t\t" + "<td>" + str(contador) + "</td>\n\t\t\t\t" + "<td>" + error["fila"] + "</td>\n\t\t\t\t" + "<td>" + error["columna"] + "</td>\n\t\t\t\t" + "<td>" + error["desc_error"] + "</td>\n\t\t\t" + "</tr>\n\t\t"

        html += "</table>\n\t" + "</body>\n" + "</html>"
        self.crearArchivoErrores(lenguaje, html)
        #messagebox.showinfo("ML WEB", "Reporte de errores léxicos del lenguaje " + lenguaje+ " finalizado")
        self.listaErroresGeneral.clear()
        os.system("Errores_"+lenguaje+".html")
    #END

    def crearArchivoErrores(self, lenguaje, contenido):
        archivoErrores = open("Errores_"+lenguaje+".html", "w")
        archivoErrores.write(contenido)
        archivoErrores.close()
    #END

    def bitacoraCss(self):
        self.salida.delete(1.0, END)
        self.salida.insert(INSERT,self.lexi.bitacora)
    #END

    def reporteJs(self):
        self.lexi.generarArbol()
        os.system("ReporteJS.gv.pdf")
    #END

    def reporteSintactico(self):
        contador = 0
        html = "<!DOCTYPE html>\n"
        html += "<html>\n"
        html += "\t<head>\n"
        html += "\t\t<meta charset = \"utf-8\">\n"
        html += "\t\t<title>Reporte An&aacutelisis Sint&aacutectico</title>\n"
        html += "\t\t<style>\n"
        html += "\t\t\ttable, th, td{\n\t\t\t\tborder: 3px solid blue;\n"
        html += "\t\t\t\tborder-collapse: collapse;\n\t\t\t}\n"
        html += "\t\t\tth, td, h2{\n\t\t\t\ttext-align: center;\n\t\t\t}\n"
        html += "\t\t</style>\n"
        html += "\t</head>\n"
        html += "\t<body>\n"
        html += "\t\t<h2>Reporte An&aacutelisis Sint&aacutectico</h2>\n"
        html += "\t\t<table align= \"center\">\n"
        html += "\t\t\t<tr>\n\t\t\t\t" + "<th>No.</th>\n\t\t\t\t" + "<th>Operaci&oacuten</th>\n\t\t\t\t" + "<th>Estado</th>\n\t\t\t\t"
        html += "</tr>\n"
        
        for ope in self.sintactico.lista_operaciones:
            contador += 1
            html += "\t\t\t<tr>\n\t\t\t\t" + "<td>" + str(contador) + "</td>\n\t\t\t\t" + "<td>" + ope["operacion"] + "</td>\n\t\t\t\t" + "<td>" + ope["estado"] + "</td>\n\t\t\t\t" + "</tr>\n\t\t"

        html += "</table>\n\t" + "</body>\n" + "</html>"

        self.crearArchivoSintactico(html)
        os.system("Sintactico.html")
    #END

    def crearArchivoSintactico(self, contenido):
        archivoSintactico = open("Sintactico.html", "w")
        archivoSintactico.write(contenido)
        archivoSintactico.close()
    #END

    #def obtenerDiccionario(self):
        #if self.extensionArchivo == "js":
            #diccionariojs = {
                #palabra: ['var', 'if', 'else', 'for', 'while', 'do', 'continue', 'break', 'return', 'function', 'constructor', 'class', 'this'],
                #simbolo: ['+', '-', '/', '*', '<', '>', '=', ';', ',', '.', '&', '|', '!', '(', ')', '{', '}', '"', '\'', ]
            #}

#END

###################################################################################################
if __name__ == '__main__':
    window = Tk()
    app = Principal(window)
    window.mainloop()