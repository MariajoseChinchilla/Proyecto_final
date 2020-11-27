import sys
from PIL import Image, ImageDraw, ImageFont
import math as m
import os
import shutil

import  gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GdkPixbuf     #nos servira para tener informacion de la imagen, pixeles, etc

import webbrowser

class ArteAscii(Gtk.Window):
    #colocar como variable de clase para tener acceso a el en los metodos
    grid = Gtk.Grid()
    vbox=Gtk.VBox()
    box_corrimiento_vertical = Gtk.VBox()
    box_corrimiento_horizontal = Gtk.HBox()
    box_imagen_normal = Gtk.VBox()
    box_arte_ascii = Gtk.VBox()
    text_buffer = Gtk.TextBuffer()
    display_para_buffer = Gtk.TextView(buffer=text_buffer)
    label_normal = Gtk.Label('IMAGEN NORMAL')
    label_arte_ascii = Gtk.Label('IMAGEN EN ARTE ASCII')
    contador_guardadas = 0      #para llevar una numeracion al guardar

    #atributo de clase para pasar a ascii
    carac = '$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~i!lI;:,\"^`".'
    caracteres = [i for i in carac]

    def __init__(self):
        super(ArteAscii, self).__init__(title = 'Arte ASCII')
        self.set_default_size(1700,850)
        self.set_resizable(False)   #fijar el size de la ventana

    #contenedores

        self.add(self.vbox)
        self.grid.set_column_spacing(1)
        self.grid.set_row_spacing(1)
        self.vbox.pack_start(self.grid, True, True, 0)
        self.grid.attach(self.box_corrimiento_vertical, 400, 1, 1,1)
        self.grid.attach(self.box_corrimiento_horizontal, 3, 142 ,500,1)
        self.grid.attach(self.box_imagen_normal, 0, 150, 600,600)
        self.grid.attach(self.box_arte_ascii, 450, 150, 600, 600)
    #desarrollo del menu con opciones pedidas para el proyecto

        menu_bar = Gtk.MenuBar()

    #elementos del menu
        imagen = Gtk.MenuItem('Imagen')
        opciones_twitter = Gtk.MenuItem('Opciones de Twitter')
        ayuda = Gtk.MenuItem('Ayuda')

    #subelementos de los elementos del menu

        #submenu de imagen
        imagen_menu = Gtk.Menu()
        cargar_imagen_menu = Gtk.MenuItem('Cargar Imagen')
        imagen_menu.append(cargar_imagen_menu)
        guardar_arte = Gtk.MenuItem('Guardar Arte ASCII')
        imagen_menu.append(guardar_arte)
        imagen.set_submenu(imagen_menu)

        #acciones de las opciones del submenu de imagen
        cargar_imagen_menu.connect('activate', self.cargar_imagen_accion)
        guardar_arte.connect('activate', self.guardar_arte_accion)

        #submenu de opciones de twitter
        opciones_twitter_menu = Gtk.Menu()
        ingresar_credenciales = Gtk.MenuItem('Ingresar credenciales')
        opciones_twitter_menu.append(ingresar_credenciales)
        logout = Gtk.MenuItem('Salir de la cuenta')
        opciones_twitter_menu.append(logout)
        opciones_twitter.set_submenu(opciones_twitter_menu)

        #acciones de las opciones del submenu de twitter
        ingresar_credenciales.connect('activate', self.connect_accion)
        logout.connect('activate', self.logout_accion)

        #submenu de ayuda
        ayuda_menu = Gtk.Menu()
        acerca_de = Gtk.MenuItem('Acerca de')
        ayuda_menu.append(acerca_de)
        codigo_fuente = Gtk.MenuItem('Código fuente')
        ayuda_menu.append(codigo_fuente)
        ayuda.set_submenu(ayuda_menu)

        #acciones de las opciones del submenu de ayuda
        acerca_de.connect('activate', self.acerca_de_accion)
        codigo_fuente.connect('activate', self.codigo_fuente_accion)

    #agregar las ramas que se derivan del menu principal a este ultimo
        menu_bar.append(imagen)
        menu_bar.append(opciones_twitter)
        menu_bar.append(ayuda)
        self.grid.attach(menu_bar, 1, 0, 5, 1)

    #boton de guardar arte ascii que se muestra en la interfaz
    #este boton debera activarse solo cuando ya este cargada una imagen
    #tambien debera estar el boton de subir a Twitter
        tool_bar = Gtk.Toolbar()   #recordar que estos botones tienen que tener accion cuando haya una imagen cargada
        tool_bar.set_style(2)
        guardar_tool_bar = Gtk.ToolButton(Gtk.STOCK_SAVE)
        separador_tool_bar = Gtk.SeparatorToolItem()
        subir_tool_bar = Gtk.ToolButton(Gtk.STOCK_ADD)
        config_imagen_tool_bar = Gtk.ToolButton(Gtk.STOCK_EXECUTE)
        separador_2_tool_bar = Gtk.SeparatorToolItem()
        tool_bar.insert(guardar_tool_bar, 0)
        tool_bar.insert(separador_tool_bar, 1)
        tool_bar.insert(subir_tool_bar, 2)
        tool_bar.insert(separador_2_tool_bar, 3)
        tool_bar.insert(config_imagen_tool_bar, 4)
        tool_bar.set_halign(Gtk.Align.CENTER)
        self.vbox.pack_start(tool_bar, False, False, 20)

    #acciones para los botones del tool bar
        guardar_tool_bar.connect('clicked', self.guardar_arte_accion)
        subir_tool_bar.connect('clicked', self.connect_accion)
        config_imagen_tool_bar.connect('clicked', self.config_imagen)


    #textbuffer, este dejara un mensaje cuando se haya cargado una imagen
    #tambien servira para pasarle la informacion al boton de guardado para que se habilite o no
        self.display_para_buffer.set_size_request(30, 30)
        self.grid.attach(self.display_para_buffer, 1, 20, 5, 5)

    #label de imagen normal y con arte ascii
        self.grid.attach(self.label_normal, 10, 140, 1, 2)
        self.grid.attach(self.label_arte_ascii, 800, 140, 1, 2)

    #configuracion metodo
    def config_imagen(self, widget):
        VentanaConfiguraciones()
    #metodos que se usan en el menu
    def cargar_imagen_accion(self, widget):
        #se abrira un file chooser dialog para elegir el archivo que tiene la imgen
        #a partir de esta carga tambien se obtiene el nombre del archivo para cargar en el buffer y habilidar el guardado
        file_chooser_cargar_imagen = Gtk.FileChooserDialog('Seleccione una imagen', None, Gtk.FileChooserAction.OPEN,
                                       ('Cancelar', Gtk.ResponseType.CANCEL, 'Seleccionar', Gtk.ResponseType.OK))
        #agregar el filtro para que solo permita elegir imagenes
        file_chooser_cargar_imagen.set_default_response(Gtk.ResponseType.OK)
        filtro_file_chooser = Gtk.FileFilter()
        filtro_file_chooser.set_name('Imágenes')
        filtro_file_chooser.add_mime_type('Image/png')
        filtro_file_chooser.add_mime_type('Image/jpeg')
        filtro_file_chooser.add_mime_type('Image/jpg')
        filtro_file_chooser.add_pattern('*.png')
        filtro_file_chooser.add_pattern('*.jpeg')
        filtro_file_chooser.add_pattern('*.jpg')
        file_chooser_cargar_imagen.add_filter(filtro_file_chooser)

        respuesta = file_chooser_cargar_imagen.run()
        if respuesta == Gtk.ResponseType.OK:

            cadena_nombre_archivo = file_chooser_cargar_imagen.get_filename() #para obtener la ruta al archivo
            indice_diagonal = cadena_nombre_archivo[::-1].find('\\') #encontramos la ultima \ leyendo la cadena al reves
            indice_extension = cadena_nombre_archivo[::-1].find('.')
            texto_para_buffer = cadena_nombre_archivo[(len(cadena_nombre_archivo)-indice_diagonal):
                                                      (len(cadena_nombre_archivo)-indice_extension)-1]
            self.text_buffer.set_text('   {} ha sido cargado.'.format(texto_para_buffer))
    #ademas de decir en el buffer que hemos cargado la imagen, debemos cargar la imagen del lado izquierdo del window
    #al lado derecho aparecera la imagen en arte ascii, pero antes, debera mostrarse un dialogo para opciones de imagen
            imagen_cargada = GdkPixbuf.Pixbuf.new_from_file_at_size(str(cadena_nombre_archivo), 600,600)
            imagen_gtk = Gtk.Image()
            imagen_gtk.set_from_pixbuf(imagen_cargada)
            self.box_imagen_normal.remove(imagen_gtk)
            self.box_imagen_normal.pack_start(imagen_gtk, False, False, 0)

    #cargar el arte ascii a la par con las configuraciones que estan hasta el momento
    #el usuario podria cambiar esto si le da en el boton de execute dle tool bar
            if os.path.exists(os.path.abspath('ImEnAscii.png')):
                os.remove('ImEnAscii.png')      #para no cargar otro archivo
            self.final_ascii(cadena_nombre_archivo)
            im_cargada_ascii = GdkPixbuf.Pixbuf.new_from_file_at_size(os.path.abspath('ImEnAscii.png'), 600, 600)
            imagen_gtk_ascii = Gtk.Image()
            imagen_gtk_ascii.set_from_pixbuf(im_cargada_ascii)
            self.box_arte_ascii.remove(imagen_gtk_ascii)
            self.box_arte_ascii.pack_start(imagen_gtk_ascii, False, False, 0)

            self.show_all()

        elif respuesta == Gtk.ResponseType.CANCEL:
            pass

        file_chooser_cargar_imagen.destroy()

    def guardar_arte_accion(self, widget):
        #verifica si existe una ruta a un archivo ImEnAscii y guarda este que justamente es el que esta cargado
        if os.path.exists('ImEnAscii.png'):
            self.contador_guardadas += 1
            #cambiarle el nombre al archivo para guardarlo
            ruta_nombre_cambiado = str(os.path.abspath('ImEnAscii.png').strip('ImEnAscii.png')) + 'ArteAscii ' + str(self.contador_guardadas) + '.txt'
            os.rename(os.path.abspath('ImEnAscii.png'), ruta_nombre_cambiado)

        #damos un mensaje por un Gtk Dialog que indique que la imagen ha sido guardada
            dialogo = DialogoGuardado(self)
            respuesta = dialogo.run()

            if respuesta == Gtk.ResponseType.OK:
                pass
            dialogo.destroy()
        else:
            dialogo = NoHayArchivoCargado(self)
            respuesta = dialogo.run()

            if respuesta == Gtk.ResponseType.OK:
                pass
            dialogo.destroy()

    def connect_accion(self, widget):
        pass
    def logout_accion(self, widget):
        pass
    def acerca_de_accion(self, widget):
        #aca saldra el dialogo con la informacion pedida
        vbox = Gtk.VBox()
        acerca_de_dialogo = Gtk.AboutDialog()
        acerca_de_dialogo.set_program_name('Arte ASCII')
        acerca_de_dialogo.set_version('Proyecto final PM1')
        acerca_de_dialogo.set_authors('MCM')
        acerca_de_dialogo.set_copyright('Desarrollo de interfaz gráfica en Gtk 3.0')
        acerca_de_dialogo.set_comments('Uso de Gtk 3.0, API de Twitter y librerías estándar de Python 3.')        #agregar lo que me falta depues de hacer el proyecto
        acerca_de_dialogo.set_website('https://github.com/MariajoseChinchilla/Proyecto_final/blob/master/Proyecto.py')
        vbox.pack_start(acerca_de_dialogo, False, False, 0)
        self.add(vbox)
        acerca_de_dialogo.run()
        acerca_de_dialogo.destroy()

    def codigo_fuente_accion(self, widget):
        webbrowser.open_new_tab('https://github.com/MariajoseChinchilla/Proyecto_final/blob/master/Proyecto.py')

#ACA EMPIEZA TODA LA PARTE DE PASAR UNA IMAGEN A ARTE ASCII
    #varias metodos para eso definidos aca
    def dimensiones(self, imagen):
        (W, H) = imagen.size
        ratio = H / float(W)
        nueva_altura = int(ratio * 100)
        newImage = imagen.resize((100, nueva_altura))
        return newImage, nueva_altura

    def escala_grises(self, imagen):
        # convertir a escalas grises
        return imagen.convert('L')

    def pix_en_ascii(self, imagen):
        rango = m.ceil(255 / len(self.caracteres))
        # elegir el mejor caracter para representar el pixel
        # el brillo esta entre 0 y 250, entonces se distribuye esto en la cantidad
        # total de caracteres
        # escoje en la lista de caracteres dependiendo del grupo de pixeles
        img = list(imagen.getdata())
        pixels_ascii = [self.caracteres[m.floor(pixel / rango)] for pixel in
                        img]

        return ''.join(pixels_ascii)

    def pasar_a_ascii(self, imagen):
        # pasar los caraceres elegidos a imagen
        imagen, alt = self.dimensiones(imagen)
        imagen = self.escala_grises(imagen)

        caracteres = self.pix_en_ascii(imagen)

        # Crea la imagen y el archivo .txt con el asciiArt
        fnt = ImageFont.load_default()
        outputImage = Image.new('RGB', (1000, 12 * alt), color=(0, 0, 0))
        drawImage = ImageDraw.Draw(outputImage)

        for i in range(alt):
            for j in range(100):
                drawImage.text((10 * j, 12 * i), caracteres[j + i * 100], font=fnt, fill=(255, 255, 255))
        outputImage.save('ImEnAscii.png')
        l = len(caracteres)

        imageAscii = [caracteres[i: i + 100] for i in
                      range(0, l, 100)]

        return "\n".join(imageAscii)

    def final_ascii(self, ruta):
        image = Image.open(ruta)
        self.pasar_a_ascii(image)

class VentanaConfiguraciones(Gtk.Window):       #ventana que se va a abrir para las configuraciones de la imagen
    #los datos que el usuario ingresaran como atributos de clase para ser accedidos luego en la otra clase
    box = Gtk.VBox()
    def __init__(self):
        super(VentanaConfiguraciones, self).__init__(title = 'Configuraciones')
        self.set_default_size(420,420)
        self.set_resizable(False)
    #contenedores para el window
        self.add(self.box)
    #demas detalles de la ventana
        label_titulo = Gtk.Label('CONFIGURACIONES PARA EL ARTE ASCII')
        num_filas = Gtk.Entry()
        label_num_filas = Gtk.Label('Ingrese el número de filas')
        num_columnas = Gtk.Entry()
        label_num_columnas = Gtk.Label('Ingrese el número de columnas')
        label_invertir_imagen = Gtk.Label('¿Invertir imagen?')
        radio_boton_si = Gtk.RadioButton.new_with_label_from_widget(None, 'Sí')
        radio_boton_si.connect('toggled', self.si_invertir)
        radio_boton_no = Gtk.RadioButton.new_from_widget(radio_boton_si)
        radio_boton_no.set_label('No')
        radio_boton_no.connect('toggled', self.no_invertir)
    #algunos formatos para alinear los radio botones
        radio_boton_si.set_halign(Gtk.PositionType.BOTTOM)
        radio_boton_no.set_halign(Gtk.PositionType.BOTTOM)
        radio_boton_si.set_valign(Gtk.PositionType.RIGHT)
        radio_boton_no.set_valign(Gtk.PositionType.RIGHT)
    #configuraciones de formato para las entradas
        num_filas.set_halign(Gtk.PositionType.BOTTOM)
        num_columnas.set_halign(Gtk.PositionType.BOTTOM)
        num_filas.set_valign(Gtk.PositionType.RIGHT)
        num_columnas.set_valign(Gtk.PositionType.RIGHT)
    #poner en el box
        self.box.pack_start(label_titulo, False, False, 40)
        self.box.pack_start(label_num_filas, False, False, 15)
        self.box.pack_start(num_filas, False, False, 0)
        self.box.pack_start(label_num_columnas, False, False, 15)
        self.box.pack_start(num_columnas, False, False, 0)
        self.box.pack_start(label_invertir_imagen, False, False, 15)
        self.box.pack_start(radio_boton_si, False, False, 0)
        self.box.pack_start(radio_boton_no, True, True, 0)
        self.show_all()

    #acciones de los radio botones
    def si_invertir(self, widget):
        pass
    def no_invertir(self, widget):
        pass

#esta es la clase del dialogo que avisa que un archivo ha sido guardado
class DialogoGuardado(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, 'Arte Ascii guardado', parent, Gtk.DialogFlags.MODAL, (
            Gtk.STOCK_OK, Gtk.ResponseType.OK
        ))
        self.set_default_size(100,100)
        self.set_resizable(False)
        self.set_border_width(30)

        area = self.get_content_area()
        area.add(Gtk.Label('Su arte ASCII fue guardado en el current working directory con la numeración correspondiente.'))
        self.show_all()

#esta es la clase para cuando no hay ningun archivo cargado
class NoHayArchivoCargado(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, 'No hay imagen cargada', parent, Gtk.DialogFlags.MODAL, (
            Gtk.STOCK_OK, Gtk.ResponseType.OK
        ))
        self.set_default_size(100,100)
        self.set_resizable(False)
        self.set_border_width(30)

        area = self.get_content_area()
        area.add(Gtk.Label('Ninguna imagen ha sido cargada.'))
        self.show_all()


win = ArteAscii()
win.connect('destroy', Gtk.main_quit)
win.show_all()
Gtk.main()