import heapq
import json
import os
from datetime import datetime
#Uso json por ser compatible y admitir distintos tipos de datos.
class GestorTareas:
    def __init__(self):
        self.heap = []
        self.tareas_completadas = set()
        self.archivo = "tareas.json"
        self.cargar_tareas()

    def cargar_tareas(self):
        """Carga las tareas desde un archivo JSON."""
        if os.path.exists(self.archivo):
            try:
                with open(self.archivo, "r") as f:
                    datos = json.load(f)
                print("Tareas cargadas del archivo:")
                for tarea in datos.get("tareas", []):
                    print(f"  - {tarea['nombre']} (Prioridad: {tarea['prioridad']}, Dependencias: {tarea['dependencias']})")
                    # Añadir las tareas al heap
                    heapq.heappush(self.heap, (
                        tarea["prioridad"],
                        tarea["nombre"],
                        tarea["dependencias"],
                        datetime.strptime(tarea["fecha_vencimiento"], "%Y-%m-%d") if tarea["fecha_vencimiento"] else None
                    ))
                self.tareas_completadas = set(datos.get("completadas", []))
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Error al cargar el archivo: {e}")
                print("El archivo está vacío o malformado. Inicializando datos...")
                self.heap = []
                self.tareas_completadas = set()
        else:
            print("Archivo no encontrado. Inicializando datos...")
            self.heap = []
            self.tareas_completadas = set()

    def guardar_tareas(self):
        """Guarda las tareas en un archivo JSON."""
        with open(self.archivo, "w") as f:
            json.dump({
                "tareas": [
                    {
                        "prioridad": tarea[0],
                        "nombre": tarea[1],
                        "dependencias": tarea[2],
                        "fecha_vencimiento": tarea[3].strftime("%Y-%m-%d") if tarea[3] else None
                    }
                    for tarea in self.heap
                ],
                "completadas": list(self.tareas_completadas)
            }, f, indent=4)
        print("Tareas guardadas en el archivo.")

    def agregar_tarea(self, nombre, prioridad, dependencias=[], fecha_vencimiento=None):
        """Añade una nueva tarea al sistema."""
        if not nombre:
            print("El nombre de la tarea no puede estar vacío.")
            return
        if not isinstance(prioridad, int):
            print("La prioridad debe ser un número entero.")
            return

        # Verificar si la fecha de vencimiento es válida
        if fecha_vencimiento:
            try:
                fecha_vencimiento = datetime.strptime(fecha_vencimiento, "%Y-%m-%d")
            except ValueError:
                print("La fecha de vencimiento no tiene un formato válido. Debe ser YYYY-MM-DD.")
                return
        else:
            fecha_vencimiento = None

        # Verificar que todas las dependencias estén completas
        if not self.tareas_completadas.issuperset(dependencias):
            print(f"Las siguientes dependencias no están completadas: {set(dependencias) - self.tareas_completadas}")
            return

        # Añadir la tarea al heap
        heapq.heappush(self.heap, (prioridad, nombre, dependencias, fecha_vencimiento))
        self.guardar_tareas()
        print(f"Tarea '{nombre}' añadida.")

    def mostrar_tareas(self):
        """Muestra todas las tareas pendientes en orden de prioridad."""
        print("Tareas pendientes:")
        # Mostrar todas las tareas ordenadas por prioridad
        if not self.heap:
            print("No hay tareas pendientes.")
        for prioridad, nombre, dependencias, fecha_vencimiento in sorted(self.heap):
            if fecha_vencimiento:
                print(f"- {nombre} (Prioridad: {prioridad}, Dependencias: {dependencias}, Fecha Vencimiento: {fecha_vencimiento.date()})")
            else:
                print(f"- {nombre} (Prioridad: {prioridad}, Dependencias: {dependencias})")

    def completar_tarea(self, nombre):
        """Marca una tarea como completada y la elimina del sistema."""
        nueva_heap = []
        encontrado = False
        for tarea in self.heap:
            if tarea[1] == nombre:
                encontrado = True
                self.tareas_completadas.add(nombre)
            else:
                nueva_heap.append(tarea)
        if encontrado:
            self.heap = nueva_heap
            heapq.heapify(self.heap)
            self.guardar_tareas()
            print(f"Tarea '{nombre}' completada.")
        else:
            print(f"Tarea '{nombre}' no encontrada.")

    def obtener_tarea_prioritaria(self):
        """Devuelve la tarea de mayor prioridad sin eliminarla."""
        if self.heap:
            tarea = self.heap[0]
            print(f"La tarea de mayor prioridad es: {tarea[1]} (Prioridad: {tarea[0]})")
        else:
            print("No hay tareas pendientes.")

if __name__ == "__main__":
    gestor = GestorTareas()

    while True:
        print("\n--- Gestor de Tareas ---")
        print("1. Añadir tarea")
        print("2. Mostrar tareas pendientes")
        print("3. Completar tarea")
        print("4. Obtener tarea de mayor prioridad")
        print("5. Salir")
        
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            nombre = input("Nombre de la tarea: ")
            try:
                prioridad = int(input("Prioridad de la tarea (número entero): "))
            except ValueError:
                print("La prioridad debe ser un número entero.")
                continue
            dependencias = input("Dependencias (separadas por comas, o deje vacío si no hay): ").split(",")
            dependencias = [d.strip() for d in dependencias if d.strip()]
            fecha_vencimiento = input("Fecha de vencimiento (formato YYYY-MM-DD, opcional): ")
            gestor.agregar_tarea(nombre, prioridad, dependencias, fecha_vencimiento)

        elif opcion == "2":
            gestor.mostrar_tareas()

        elif opcion == "3":
            nombre = input("Nombre de la tarea a completar: ")
            gestor.completar_tarea(nombre)

        elif opcion == "4":
            gestor.obtener_tarea_prioritaria()

        elif opcion == "5":
            print("Saliendo del gestor de tareas. ¡Hasta luego!")
            break

        else:
            print("Opción no válida. Intente de nuevo.")
