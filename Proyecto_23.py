import  gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import webbrowser

class ArteAscii(Gtk.Window):
    def __init__(self):
        super(ArteAscii, self).__init__(title = 'Arte ASCII')
        self.set_default_size(1000,700)
        self.set_resizable(False)   #fijar el size de la ventana

    #contenedores

        vbox = Gtk.VBox()
        self.add(vbox)
        grid = Gtk.Grid()
        grid.set_column_spacing(1)
        grid.set_row_spacing(1)
        vbox.pack_start(grid, True, True, 0)

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
        grid.attach(menu_bar, 0, 0, 5, 1)


    #metodos que se usan en el menu
    def cargar_imagen_accion(self, widget):
        pass
    def guardar_arte_accion(self, widget):
        pass
    def connect_accion(self, widget):
        pass
    def logout_accion(self, widget):
        pass
    def acerca_de_accion(self, widget):
        #aca saldra el dialogo con la informacion pedida
        vbox = Gtk.VBox()
        acerca_de_dialogo = Gtk.AboutDialog()
        acerca_de_dialogo.set_program_name('Proyecto final PM1')
        acerca_de_dialogo.set_version('Arte ASCII')
        acerca_de_dialogo.set_authors('MCM')
        acerca_de_dialogo.set_copyright('Desarrollo de interfaz gráfica en Gtk 3.0')
        acerca_de_dialogo.set_comments('Uso de Gtk 3.0')        #agregar lo que me falta depues de hacer el proyecto
        acerca_de_dialogo.set_website('https://github.com/MariajoseChinchilla/TestGit/blob/master/Main.py')
        vbox.pack_start(acerca_de_dialogo, False, False, 0)
        self.add(vbox)
        acerca_de_dialogo.run()
        acerca_de_dialogo.destroy()

    def codigo_fuente_accion(self, widget):
        webbrowser.open_new_tab('https://github.com/MariajoseChinchilla/TestGit/blob/master/Main.py')

win = ArteAscii()
win.connect('destroy', Gtk.main_quit)
win.show_all()
Gtk.main()