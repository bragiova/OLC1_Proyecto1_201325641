from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.scrolledtext import ScrolledText
from tkinter import messagebox
import os
import threading
import re
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
        self.pathArchivo = ""
        self.esNuevo = False

        frame = LabelFrame(self.ventana, text = '')
        frame.grid(row=0,column=0,columnspan=20,pady=20, sticky=N+S+E+W)

        #############################################_MENU_#############################################
        menubarra = Menu(self.ventana)
        menuarchivo = Menu(menubarra, tearoff = 0, font=("Comic Sans MS", 9))
        menuarchivo.add_command(label="Nuevo", command=self.archivoNuevo)
        menuarchivo.add_command(label="Abrir", command=self.abrirArchivo)
        menuarchivo.add_command(label="Guardar", command=self.guardarArchivo)
        menuarchivo.add_command(label="Guardar como", command=self.guardarComo)
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

        #self.labelcursor = Label(frame, text='A', font=("Comic Sans MS", 9))
        #self.labelcursor.grid(row=6,column=5)

        ############################################_ENTRADA_############################################
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
        frame.grid_columnconfigure(6, weight=1)
        frame.grid_columnconfigure(16, weight=1)
        frame.grid_columnconfigure(17, weight=1)

        frame.grid_rowconfigure(3, weight=1)
        frame.grid_rowconfigure(4, weight=1)
        frame.grid_rowconfigure(5, weight=1)
        #frame.grid_rowconfigure(6, weight=1)
    #END

    def archivoNuevo(self):
        texto = self.entrada.get(1.0, END)
        if texto != "":
            self.entrada.delete(1.0, END)
        
        self.labelarchivo.configure(text="Archivo nuevo")
        self.esNuevo = True

    def abrirArchivo(self):
        filename = askopenfilename(filetypes=(("Archivos HTML", "*.html"), ("Archivos JS", "*.js"), ("Archivos CSS", "*.css"), ("Archivos RMT", "*.rmt")))
        self.pathArchivo = filename

        if filename:
            self.extensionArchivo = ""
            self.esNuevo = False
            archivo = open(filename,"r", encoding="utf-8")
            texto = archivo.read()
            archivo.close()

            nombreArchivo = os.path.split(filename)
            extension = nombreArchivo[1].split('.')
            self.extensionArchivo = extension[1]

            self.labelarchivo.configure(text=nombreArchivo[1])

            self.entrada.delete(1.0, END)
            self.entrada.insert(INSERT,texto)

            #pintado de palabras
            #self.pintarComentarioLineal()
            self.pintarComentarioMulti()
            #self.pintarOperadores()
            #self.pintarIntBoolean()
            #self.pintarCadenas()
            #self.pintarReservadas()
        return
    #END

    def guardarArchivo(self):
        try:
            if self.esNuevo:
                self.guardarComo()
                self.esNuevo = False
                return

            texto = self.entrada.get(1.0, END)
            archivo_guardar = open(self.pathArchivo, "w", encoding="utf-8")
            archivo_guardar.write(str(texto))
            archivo_guardar.close()
            messagebox.showinfo("ML WEB", "Cambios guardados")
        except:
            messagebox.showwarning("ML WEB", "Error al tratar de guardar archivo")

    def guardarComo(self):
        try:
            filename = asksaveasfilename(filetypes=(("Archivos HTML", "*.html"), ("Archivos JS", "*.js"), ("Archivos CSS", "*.css"), ("Archivos RMT", "*.rmt")))
            texto = self.entrada.get(1.0, END)

            if filename:
                archivo_guardar = open(filename, "w", encoding="utf-8")
                archivo_guardar.write(str(texto))
                archivo_guardar.close()

                nombreArchivo = os.path.split(filename)
                extension = nombreArchivo[1].split('.')
                self.extensionArchivo = extension[1]
                self.labelarchivo.configure(text=nombreArchivo[1])
            return
        except:
            messagebox.showwarning("ML WEB", "Error al tratar de guardar archivo")


    def analizar(self):
        if self.esNuevo:
            messagebox.showerror("ML WEB", "Primero debe guardar el archivo con alguna de las extensiones permitidas")
            return

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
        try:
            #escribir el archivo ya corregido
            archivoSalida = open(ruta + "\\" + self.labelarchivo['text'], "w")
            archivoSalida.write(texto)
            archivoSalida.close()
        except:
            messagebox.showwarning("ML WEB", "Error al tratar de crear archivo corregido")

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
            self.listaErroresGeneral.append(errorGeneral)
        self.salida.insert(INSERT,consola)
    #END

    def generarHtmlErrores(self):
        if len(self.listaErroresGeneral) == 0:
            messagebox.showerror("ML WEB", "No se registraron errores en el archivo")
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
        self.listaErroresGeneral.clear()
        try:
            os.system("Errores_"+lenguaje+".html")
        except:
            print("Error al tratar de abrir el archivo de errores")
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
        try:
            self.lexi.generarArbol()
            os.system("ReporteJS.gv.pdf")
        except:
            print("Error al tratar de abrir el reporte JS")
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
        try:
            os.system("Sintactico.html")
        except:
            print("Error al tratar de abrir el reporte Sintáctico")
    #END

    def crearArchivoSintactico(self, contenido):
        archivoSintactico = open("Sintactico.html", "w")
        archivoSintactico.write(contenido)
        archivoSintactico.close()
    #END

    def pintarReservadas(self):
        
        palabra = ['var', 'if', 'else', 'for', 'while', 'do', 'continue', 'break', 'return', 'function', 'constructor', 'class', 'this']
        self.entrada.tag_config('res', foreground='red')
        count1 = IntVar()

        for word in palabra:
            idx = 1.0
            while True:
                idx = self.entrada.search(word, idx, nocase=1, count=count1, stopindex=END, regexp=True)
                if not idx: break
                lastidx = '%s+%dc' % (idx, len(word))
                self.entrada.tag_add('res', idx, lastidx)
                idx = lastidx
    #END

    def pintarCadenas(self):
        expcadenacarac = "(\"|')(.*)(\"|')"
        self.entrada.tag_config('cadenas', foreground='yellow2')
        count1 = IntVar()

        idx = 1.0
        while True:
            idx = self.entrada.search(expcadenacarac, idx, nocase=1, count=count1, stopindex=END, regexp=True)
            if not idx: break
            lastidx = '%s+%dc' % (idx, count1.get())
            self.entrada.tag_add('cadenas', idx, lastidx)
            idx = lastidx
    #END

    def pintarOperadores(self):
        expoperadores = "[+]|-|/|[*]|==|!=|<|>|>=|<=|[||]|&&|!"
        self.entrada.tag_config('ope', foreground='orange')
        count1 = IntVar()

        idx = 1.0
        while True:
            idx = self.entrada.search(expoperadores, idx, nocase=1, count=count1, stopindex=END, regexp=True)
            if not idx: break
            lastidx = '%s+%dc' % (idx, count1.get())
            self.entrada.tag_add('ope', idx, lastidx)
            idx = lastidx
        
    def pintarComentarioLineal(self):
        expcomentlinea = "//.*"
        self.entrada.tag_config('comentlineal', foreground='gray')
        count1 = IntVar()

        idx = 1.0
        while True:
            idx = self.entrada.search(expcomentlinea, idx, nocase=1, count=count1, stopindex=END, regexp=True)
            if not idx: break
            lastidx = '%s+%dc' % (idx, count1.get())
            self.entrada.tag_add('comentlineal', idx, lastidx)
            idx = lastidx
    #END

    def pintarComentarioMulti(self):
        expcomentmulti = "((/\*)[^*]*(\*/))|((/\*)(.*)(\*+/))"
        self.entrada.tag_config('comentmulti', foreground='gray')
        count1 = IntVar()

        idx = 1.0
        while True:
            idx = self.entrada.search(expcomentmulti, idx, nocase=1, count=count1, stopindex=END, regexp=True)
            if not idx: break
            lastidx = '%s+%dc' % (idx, count1.get())
            self.entrada.tag_add('comentmulti', idx, lastidx)
            idx = lastidx
    #END

    def pintarIntBoolean(self):
        expintboolean = "\d|true|false"
        self.entrada.tag_config('int', foreground='blue')
        count1 = IntVar()

        idx = 1.0
        while True:
            idx = self.entrada.search(expintboolean, idx, nocase=1, count=count1, stopindex=END, regexp=True)
            if not idx: break
            lastidx = '%s+%dc' % (idx, count1.get())
            self.entrada.tag_add('int', idx, lastidx)
            idx = lastidx
    

#END

###################################################################################################
if __name__ == '__main__':
    window = Tk()
    app = Principal(window)
    window.mainloop()