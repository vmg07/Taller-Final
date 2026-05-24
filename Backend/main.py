import os
from datetime import datetime
from paquetes import Paquete
from envios import EnvioDB

# =======================================================
# BASE DE DATOS
# =======================================================

DB_NAME=os.path.join(
    os.path.dirname(__file__),
    "ruta_optima.db"
)

# =======================================================
# CREAR TABLAS
# =======================================================

def crear_base_datos():

    db=EnvioDB(DB_NAME)

    db.crear_tabla()


# =======================================================
# DATOS AUTOMÁTICOS
# =======================================================

def insertar_datos_prueba():

    db=EnvioDB(DB_NAME)

    conn=db.conectar()

    cursor=conn.cursor()


    # CLIENTES

    clientes=[

        (1,"Paula"),
        (2,"Valeria"),
        (3,"Isabella"),
        (4,"Carlos"),
        (5,"Juan"),
        (21,"Sofia"),
        (22,"Camila"),
        (23,"Andres"),
        (24,"Daniel"),
        (25,"Valentina"),
        (26,"Mateo"),
        (27,"Samuel"),
        (28,"Juliana"),
        (29,"Mariana"),
        (30,"Felipe")

    ]

    cursor.executemany("""

    INSERT OR IGNORE INTO clientes
    VALUES (?,?)

    """,clientes)


    # DESTINOS

    destinos=[

        ("Bogotá","Andina"),
        ("Medellín","Andina"),
        ("Cali","Pacífica"),
        ("Barranquilla","Caribe"),
        ("Cartagena","Caribe")

    ]

    cursor.executemany("""

    INSERT OR IGNORE INTO destinos
    VALUES (?,?)

    """,destinos)


    # ENVIOS

    envios=[

        (1,0.5,"Bogotá","Documento",5000,"2026-01-15"),

        (2,3,"Medellín","Paquetería",13000,"2026-02-18"),

        (3,12,"Cali","Carga",44000,"2026-03-10"),

        (4,2,"Barranquilla","Paquetería",12000,"2026-04-20"),

        (5,20,"Cartagena","Carga",60000,"2026-05-12"),

        (21,8,"Bogotá","Paquetería",18000,"2026-01-15"),

        (22,0.5,"Medellín","Documento",5000,"2026-01-28"),

        (23,20,"Cali","Carga",60000,"2026-02-10"),

        (24,3,"Barranquilla","Paquetería",13000,"2026-02-22"),

        (25,0.7,"Bogotá","Documento",5000,"2026-03-06"),

        (26,14,"Medellín","Carga",48000,"2026-03-25"),

        (27,5,"Cali","Paquetería",15000,"2026-04-08"),

        (28,28,"Barranquilla","Carga",76000,"2026-04-20"),

        (29,0.9,"Bogotá","Documento",5000,"2026-05-04"),

        (30,6,"Medellín","Paquetería",16000,"2026-05-18"),

        (31,18,"Cali","Carga",56000,"2026-06-02"),

        (32,4,"Barranquilla","Paquetería",14000,"2026-06-29"),

        (33,0.4,"Bogotá","Documento",5000,"2026-07-07"),

        (34,32,"Medellín","Carga",84000,"2026-07-24"),

        (35,7,"Cali","Paquetería",17000,"2026-08-09"),

        (36,1,"Barranquilla","Paquetería",11000,"2026-08-31"),

        (37,25,"Bogotá","Carga",70000,"2026-09-15"),

        (38,0.6,"Medellín","Documento",5000,"2026-10-11"),

        (39,9,"Cali","Paquetería",19000,"2026-11-03"),

        (40,38,"Barranquilla","Carga",96000,"2026-12-18")

    ]


    cursor.executemany("""

    INSERT OR IGNORE INTO envios(

    id_cliente,
    peso,
    destino,
    tipo,
    costo,
    fecha

    )

    VALUES(?,?,?,?,?,?)

    """,envios)


    conn.commit()

    conn.close()

    print("✅ Datos automáticos cargados")


# =======================================================
# CRUD
# =======================================================

def registrar_envio():

    try:

        id_cliente=int(
            input("Ingrese ID cliente:")
        )

        peso=float(
            input("Ingrese peso:")
        )

        destino=input(
            "Ingrese destino:"
        )


        fecha=datetime.now().strftime(
            "%Y-%m-%d"
        )

        paquete=Paquete(
            peso,
            destino
        )

        costo=paquete.calcular_costo()

        db=EnvioDB(DB_NAME)

        db.insertar(

            id_cliente,
            peso,
            destino,
            paquete.tipo,
            costo,
            fecha

        )

        print("✅ Registro exitoso")

    except:

        print("❌ Error")


def ver_envios():

    db=EnvioDB(DB_NAME)

    datos=db.consultar()

    for fila in datos:

        print(fila)


def actualizar_envio():

    try:

        id_envio=int(
            input("ID:")
        )

        nuevo=input(
            "Nuevo destino:"
        )

        db=EnvioDB(DB_NAME)

        db.actualizar(
            id_envio,
            nuevo
        )

    except:

        print("Error")


def eliminar_envio():

    try:

        id_envio=int(
            input("ID:")
        )

        db=EnvioDB(DB_NAME)

        db.eliminar(
            id_envio
        )

    except:

        print("Error")


# =======================================================
# MENU
# =======================================================

def menu():

    while True:

        print("\n======RUTA ÓPTIMA======")

        print("1 Registrar")
        print("2 Ver")
        print("3 Actualizar")
        print("4 Eliminar")
        print("5 Salir")

        opcion=input(
            "Seleccione:"
        )

        if opcion=="1":

            registrar_envio()

        elif opcion=="2":

            ver_envios()

        elif opcion=="3":

            actualizar_envio()

        elif opcion=="4":

            eliminar_envio()

        elif opcion=="5":

            break


if __name__=="__main__":

    crear_base_datos()

    insertar_datos_prueba()

    menu()