from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter.scrolledtext import ScrolledText
from tkinter import messagebox
import os
from LexicoJS import Lexico
from LexicoHTML import LexicoHtml
from LexicoCSS import LexicoCss


class Ejemplo2:

    def __init__(self, window):
        self.ventana = window
        self.ventana.title("ML WEB")
        self.extensionArchivo = ""

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
        menureportes.add_command(label="Árbol JavaScript")
        menureportes.add_command(label="Errores Léxicos")
        menubarra.add_cascade(label="Reportes", menu=menureportes)

        self.ventana.config(menu=menubarra)

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
        frame.grid_columnconfigure(6, weight=1)
        frame.grid_columnconfigure(16, weight=1)
        frame.grid_columnconfigure(17, weight=1)

        frame.grid_rowconfigure(3, weight=1)
        frame.grid_rowconfigure(4, weight=1)
        frame.grid_rowconfigure(5, weight=1)
    #END


    def abrirArchivo(self):
        filename = askopenfilename()

        archivo = open(filename,"r")
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
            lex = Lexico(texto)
            lex.analisis()
            self.crearArchivoCorregido(lex.ruta, lex.texto)
        
        elif self.extensionArchivo == "css":
            lex = LexicoCss(texto)
            lex.analisis()
            self.crearArchivoCorregido(lex.ruta, lex.texto)

        elif self.extensionArchivo == "html":
            lex = LexicoHtml(texto)
            lex.analisis()
            #escribir el archivo ya corregido
            self.crearArchivoCorregido(lex.ruta, lex.texto)
        
        else:
            messagebox.showerror("ML WEB", "Archivo con extensión no permitida para el análisis")
            return

        self.printSalida()
    #END


    def printSalida(self):
        #texto = "Finalizó el análisis"
        #self.salida.insert(INSERT,texto)

        messagebox.showinfo("ML WEB", "Análisis finalizado")
        #messagebox.showerror("Error", "Texto a mostrar:\n")
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
#END

###################################################################################################
if __name__ == '__main__':
    window = Tk()
    app = Ejemplo2(window)
    window.mainloop()