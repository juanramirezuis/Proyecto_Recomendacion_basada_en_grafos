import pandas as pd #dataframe
import networkx as nx #Usada para la creación del grafo de una forma más sencilla
import matplotlib.pyplot as plt #Esta libreria se usa para la creación de las graficas, SE USAN LABEL X,Y PARA LOS EJES Y OTRA PARA LOS TITULOS DEL GRAFICO
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QDesktopWidget
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt # Utiliza PyQt5 para la interfaz gráfica y se comunica con las funciones previamente definidas para mostrar juegos recomendadas y manejar las selecciones del usuario.
from random import sample #Utilza para seleccionar 10 elementos aleatorios en la lista "sample". En este caso, Juegos_names es una lista que contiene los nombres de todos los Juegos en l_juegos, y sample(juego_names, 10) selecciona aleatoriamente
#10 elementos de esa lista sin reemplazo. Estos 10 elementos representarán los juegos que se mostrarán en la interfaz gráfica como parte de las recomendaciones.
import sys #usada en la lineas 211-215

#cada libreria se instala con pip (nombre libreria install)

df_Juegos = pd.read_excel("D:\\JMRS\\Descargas\\Proyecto_Matematicas_Discretas_2024-2\\Proyecto_Matematicas_Discretas_2024-2\\Listado de juegos.xlsx")#ingresar dirección del archivo excel que venía en el winrar
g_Juegos = nx.Graph()#grafo


#creación del nodo
class Juego:

    def __init__(self, Nombre, GeneroA, GeneroB, Empresa, Año, Desarrolladores):

        self.Nombre = Nombre
        self.GeneroA = GeneroA
        self.GeneroB = GeneroB
        self.Empresa = Empresa
        self.Año = Año
        self.Desarrolladores = Desarrolladores

    def imprimir_Juego(self):

        print("Juego:", self.Nombre)
        print("Genero A:", self.GeneroA)
        print("Genero B:", self.GeneroB)
        print("Empresa:", self.Empresa)
        print("Año:", self.Año)
        #

#Dataframe
l_Juegos = []
for index, row in df_Juegos.iterrows():

    #DATAFRAME SE USA LIBRERIA PANDA, LAS PALABRAS RESERVADAS AQUÍ SON LAS UTILIZADAS PARA LA CREACIÓN DE LAS COLUMNAS DEL DATAFRAME
    Nombre = row['Nombre']
    GeneroA = row['GeneroA']
    GeneroB = row['GeneroB']
    Empresa = row['Empresa']
    Año = row['Año']
    Desarrolladores = row['Desarrolladores']

    #CREACIÓN OBJETO
    Juego_instance = Juego(Nombre, GeneroA, GeneroB, Empresa, Año, Desarrolladores)
    g_Juegos.add_node(Juego_instance)
    l_Juegos.append(Juego_instance)
#


#creación del grafo
for i in range(len(l_Juegos)): #LEN CONTAR NUMERO DE ELEMENTOS EN LA LISTA L_Juegos

    current_Juego = l_Juegos[i]

    for j in range(i + 1, len(l_Juegos)):

        next_Juego = l_Juegos[j]

        weight = 0
        #contar similitudes
        #categorias
        if current_Juego.GeneroA == next_Juego.GeneroA or current_Juego.GeneroA == next_Juego.GeneroB:
            weight += 1
        if current_Juego.GeneroB == next_Juego.GeneroA or current_Juego.GeneroB == next_Juego.GeneroB:
            weight += 1
        #Studio
        if current_Juego.Empresa == next_Juego.Empresa:
            weight += 1
        #año
        if current_Juego.Año == next_Juego.Año:
            weight += 1
        #Seiyus
        if current_Juego.Desarrolladores == next_Juego.Desarrolladores :
            weight += 1

        #aristas agregadas al grafo g_Juegos, las aristas son el número (peso) de similitudes
        if weight == 1:
            g_Juegos.add_edge(current_Juego, next_Juego, weight=1)
        elif weight == 2:
            g_Juegos.add_edge(current_Juego, next_Juego, weight=2)
        elif weight == 3:
            g_Juegos.add_edge(current_Juego, next_Juego, weight=3)
        elif weight == 4:
            g_Juegos.add_edge(current_Juego, next_Juego, weight=4)
#
pos = nx.spring_layout(g_Juegos)  # Define una disposición para los nodos (puedes ajustar esto según tus preferencias)
labels = {anime: anime.Nombre for anime in l_Juegos}  # Etiquetas para los nodos

# Dibuja nodos y aristas
nx.draw(g_Juegos, pos, with_labels=False, font_weight='bold', node_size=50)
nx.draw_networkx_labels(g_Juegos, pos, labels, font_size=8)

plt.title('Grafo de Juegos')
plt.show()


#TOMA DE ENTRADA EL Juego Y EL NÚMERO DE RECOMENDACIONES
def obtener_recomendaciones(Juego, num_recomendaciones):

    vecinos = list(g_Juegos.neighbors(Juego))
    pesos_similitud = {}

    for vecino in vecinos:

        peso = g_Juegos[Juego][vecino]['weight']
        pesos_similitud[vecino] = peso

    vecinos_ordenados = sorted(pesos_similitud, key = pesos_similitud.get, reverse=True)
    recomendaciones = vecinos_ordenados[:num_recomendaciones]
#DEVUELVE UNA LISTA DE RECOMENDACIONES SIMILARES A EL Juego SELECCIONADO, DEVUELVE ORDENADAS POR SIMILITUD (ENCARGADA LA PALABRA RESERVADA SORTED Y REVERSE = TRUE)
    return recomendaciones

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("¿Qué Juego deseas jugar?")
        self.juego_labels = []
        self.selected_juego = None
        
        self.create_juego_labels()
        self.create_subtitle()
        
        central_widget = QWidget(self)
        layout = QVBoxLayout()
        layout.addWidget(self.subtitle_label, alignment=Qt.AlignTop | Qt.AlignLeft)
        
        rows = [self.juego_labels[i:i + 5] for i in range(0, len(self.juego_labels), 5)]
        for row in rows:
            row_layout = QHBoxLayout()
            for widget in row:
                row_layout.addWidget(widget)
            layout.addLayout(row_layout)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        self.resize(1500, 600)
    
    def create_juego_labels(self):
        juego_Nombre = [juego.Nombre for juego in l_Juegos ]
        selected_juegos = sample(juego_Nombre, 10)
        
        for juego_Nombre in selected_juegos:
            image_path = f"D:\\JMRS\\Descargas\\Proyecto_Matematicas_Discretas_2024-2\\Proyecto_Matematicas_Discretas_2024-2\\Fotos Juegos\\{juego_Nombre}.jpg"  #Por favor insertar aquí la ruta de la carpeta Fotos Anime que venía en el archivo winrar
            pixmap = QPixmap(image_path)
            pixmap = pixmap.scaled(185, 285, Qt.AspectRatioMode.KeepAspectRatio)
            
            juego_label = QLabel(self)
            juego_label.setPixmap(pixmap)
            juego_label.setAlignment(Qt.AlignCenter)
            juego_label.mousePressEvent = lambda event, juego=juego_Nombre: self.select_juego(juego)
            
            juego_Nombre_label = QLabel(self)
            juego_Nombre_label.setText(juego_Nombre)
            juego_Nombre_label.setAlignment(Qt.AlignCenter)
            juego_Nombre_label.setStyleSheet("font-size: 11pt;")

            layout = QVBoxLayout()
            layout.addWidget(juego_label)
            layout.addWidget(juego_Nombre_label)

            container_widget = QWidget()
            container_widget.setLayout(layout)
            self.juego_labels.append(container_widget)

    def create_subtitle(self):
        self.subtitle_label = QLabel(self)
        self.subtitle_label.setText("Selecciona un Juego:")
        self.subtitle_label.setFont(QFont("Times New Roman", 12, QFont.Bold))

    def mostrar_recomendaciones(self, juego):
        num_recomendaciones = 10
        recomendaciones = obtener_recomendaciones(juego, num_recomendaciones)

        print("Recomendaciones para", juego.Nombre, ":")

        for recomendacion in recomendaciones:
            print(recomendacion.Nombre)

        self.mostrar_recomendaciones_imagenes(recomendaciones)

    def select_juego(self, juego_Nombre):
        self.selected_juego = juego_Nombre
        print("Juego seleccionado", juego_Nombre)
        selected_juego = next((juego for juego in l_Juegos if juego.Nombre == juego_Nombre), None)

        if selected_juego:
            self.mostrar_recomendaciones(selected_juego)
        else:
            print("No se encontró ese juego en la lista.")

    def mostrar_recomendaciones_imagenes(self, recomendaciones):
        layout = QVBoxLayout()
        subtitle_label = QLabel(self)
        subtitle_label.setText("Juegos Recomendados:")
        subtitle_label.setFont(QFont("Times New Roman", 16, QFont.Bold))
        layout.addWidget(subtitle_label, alignment=Qt.AlignTop | Qt.AlignLeft)

        for i in range(0, len(recomendaciones), 5):
            row_layout = QHBoxLayout()
            for recomendacion in recomendaciones[i:i + 5]:
                container_widget = QWidget()
                container_layout = QVBoxLayout()
                image_path = f"D:\\JMRS\\Descargas\\Proyecto_Matematicas_Discretas_2024-2\\Proyecto_Matematicas_Discretas_2024-2\\Fotos Juegos\\{recomendacion.Nombre}.jpg" #Por favor insertar aquí la ruta de la carpeta Fotos Anime que venía en el archivo winrar
                pixmap = QPixmap(image_path)
                pixmap = pixmap.scaled(185, 285)
                juego_label = QLabel(self)
                juego_label.setPixmap(pixmap)
                juego_label.setAlignment(Qt.AlignCenter)               
                container_layout.addWidget(juego_label)
                juego_Nombre_label = QLabel(self)
                juego_Nombre_label.setText(recomendacion.Nombre)
                juego_Nombre_label.setAlignment(Qt.AlignCenter)
                juego_Nombre_label.setStyleSheet("font-size: 11pt;")
                container_layout.addWidget(juego_Nombre_label)
                
                container_widget.setLayout(container_layout)    
                row_layout.addWidget(container_widget)
            
            layout.addLayout(row_layout)
        
        self.setCentralWidget(QWidget())
        self.centralWidget().setLayout(layout)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())