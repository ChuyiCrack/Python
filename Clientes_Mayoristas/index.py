import sqlite3
from sqlite3 import IntegrityError
import pandas as pd
import time
import os

#Hello World

def Agregar_Cliente():
    conn = sqlite3.connect(Database_Name)
    cursor= conn.cursor()
    print("\x1b[1;33m"+"Estas en el Apartado para agregar clientes a la base de datos")
    print("")
    Nombre=input("\x1b[1;36m"+"Nombre: "+"\x1b[1;37m")
    print("")
    Apellido=input("\x1b[1;36m"+"Apellido: "+"\x1b[1;37m")
    os.system("cls")
    print("\x1b[1;32m"+"El nombre del cliente es "+"\x1b[1;37m"+Nombre+" "+Apellido+"\x1b[1;32m"+ ", Esta correcto? (si/no)")
    print("")
    User_Selection=input("\x1b[1;33m"+"---> "+"\x1b[1;37m")
    while not User_Selection in ("si","no"):
        User_Selection=input("\x1b[1;33m"+"---> "+"\x1b[1;37m")
    
    if User_Selection=="no":
        Nombre=input("\x1b[1;36m"+"Nombre: "+"\x1b[1;37m")
        print("")
        Apellido=input("\x1b[1;36m"+"Apellido: "+"\x1b[1;37m")
        print("")
        print("\x1b[1;33m"+f"Se cambio el nombre a {Nombre} {Apellido}")

    
    try:
        cursor.execute(f'''
                    INSERT INTO Clientes(Nombre,Apellido)
                    VALUES ("{Nombre}","{Apellido}")
                    ''')
        
    except IntegrityError:
        os.system("cls")
        print("\x1b[1;31m"+f"{Nombre} {Apellido} ya existe en la base de datos")
        time.sleep(2)
        os.system("cls")
        return 0
    
    cursor.execute(f'''
                   SELECT Cliente_ID FROM Clientes 
                   WHERE Nombre="{Nombre}" AND Apellido="{Apellido}"
                   ''')
    
    usrid=cursor.fetchone()
    Client_ID=usrid[0]
    print("")
    print(f"El Cliente {Nombre} {Apellido} tiene el ID: {Client_ID}")
    print("")
    a=input("Enter para continuar")
    os.system("cls")
    conn.commit()
    conn.close()

def Agregar_Compra():
    os.system("cls")
    conn = sqlite3.connect(Database_Name)
    cursor= conn.cursor()
    p=0
    while p==0: 
        print("\x1b[1;33m"+"Estas en el Apartado para agregar Compras de Clientes")
        print("")
        print("\x1b[1;32m"+"Dame el ID del cliente que realizo una compra: ")
        print("")
        while True:
            try:
                User_ID=input("\x1b[1;36m"+"----> "+"\x1b[1;37m")
                User_ID=int(User_ID)
                break
            except ValueError:
                pass
        
        cursor.execute("SELECT Cliente_ID FROM Clientes")
        ALL_ID=cursor.fetchall()
        k=0
        for i in ALL_ID:
            for j in i:
                if j==User_ID:
                    k=1

            if k==1:
                break
        
        if k==0:
            print("\x1b[1;31m"+"Losiento el ID ("+"\x1b[1;37m"+ F"{User_ID}" +"\x1b[1;31m"+") no existe en la base de datos")
            time.sleep(3)
            os.system("cls")
            return 0
        
        cursor.execute(f"SELECT Nombre,Apellido FROM Clientes WHERE Cliente_ID={User_ID}")
        nombres=cursor.fetchone()
        print("")
        print(f"El cliente se llama {nombres[0]} {nombres[1]}, Esta correcto? (si/no)")
        print("")
        User_Selection=input("\x1b[1;33m"+"---> "+"\x1b[1;37m")
        while not User_Selection in ("si","no"):
            User_Selection=input("\x1b[1;33m"+"---> "+"\x1b[1;37m")
        
        if User_Selection=="si":
            cursor.execute("SELECT Precio FROM Productos")
            Precios=cursor.fetchall()
            print("")
            print("\x1b[1;37m"+"Se le va aplicar precio de mayoreo? (si/no)")
            print("")
            Mayoreo=input("\x1b[1;33m"+"---> "+"\x1b[1;37m")
            while not Mayoreo in ("si","no"):
                Mayoreo=input("\x1b[1;33m"+"---> "+"\x1b[1;37m")

            if Mayoreo=="si":
                Precio_Dama=((Precios[0][0])-20)
                Precio_Caballero=((Precios[1][0])-20)

            else:
                Precio_Dama=((Precios[0][0]))
                Precio_Caballero=((Precios[1][0]))
            
            
            os.system("cls")
            print("\x1b[1;33m"+"Cuantos perfumes compro el cliente: ")
            print("")
            Dama=int(input("\x1b[1;36m"+"Dama: "+"\x1b[1;37m"))
            print("")
            Caballero=int(input("\x1b[1;36m"+"Caballero: "+"\x1b[1;37m"))

            if Dama>0 and Caballero>0:
                Monto=((Dama*Precio_Dama)+(Caballero*Precio_Caballero))
                cursor.execute(f'''
                          INSERT INTO Ordenes_Clientes(Cliente_ID,Mayoreo,Monto)
                          VALUES ({User_ID},"{Mayoreo}",{Monto})  
                           ''')
                conn.commit()
                cursor.execute(f"SELECT Orden_ID FROM Ordenes_Clientes WHERE Cliente_ID={User_ID} ORDER BY Orden_ID DESC")
                ORd=cursor.fetchone()
                Orden_ID=ORd[0]
                cursor.execute(f'''
                               INSERT INTO Detalles_Ordenes (Orden_ID,Producto_ID,Cantidad)
                               VALUES ({Orden_ID},1,{Dama}),({Orden_ID},2,{Caballero})
                               ''')
            
            
            elif Dama>0 and Caballero<=0:
                Monto=((Dama*Precio_Dama))
                cursor.execute(f'''
                          INSERT INTO Ordenes_Clientes(Cliente_ID,Monto)
                          VALUES ({User_ID},"{Mayoreo}",{Monto})  
                           ''')
                conn.commit()
                cursor.execute(f"SELECT Orden_ID FROM Ordenes_Clientes WHERE Cliente_ID={User_ID} ORDER BY Orden_ID DESC")
                ORd=cursor.fetchone()
                Orden_ID=ORd[0]
                cursor.execute(f'''
                               INSERT INTO Detalles_Ordenes (Orden_ID,Producto_ID,Cantidad)
                               VALUES ({Orden_ID},1,{Dama})
                               ''')
            elif Dama<=0 and Caballero>0:
                Monto=(Caballero*Precio_Caballero)
                cursor.execute(f'''
                          INSERT INTO Ordenes_Clientes(Cliente_ID,Monto)
                          VALUES ({User_ID},"{Mayoreo}",{Monto})  
                           ''')
                conn.commit()
                cursor.execute(f"SELECT Orden_ID FROM Ordenes_Clientes WHERE Cliente_ID={User_ID} ORDER BY Orden_ID DESC")
                ORd=cursor.fetchone()
                Orden_ID=ORd[0]
                cursor.execute(f'''
                               INSERT INTO Detalles_Ordenes (Orden_ID,Producto_ID,Cantidad)
                               VALUES ({Orden_ID},2,{Caballero})
                               ''')
                
            else:
                os.system("cls")
                print("\x1b[1;31m"+"No se compro ningun Producto")
                conn.close()
                time.sleep(2)
                return 0
                
            conn.commit()
            conn.close()
            print("\x1b[1;32m"+"Se ha agregado exitosamente la compra en la base de datos")
            print("")
            a=input("\x1b[1;37m"+"Enter para continuar")
            p=1

        else:
            os.system("cls")
            pass


def Checar_Ordenes():
    os.system("cls")
    conn = sqlite3.connect(Database_Name)
    cursor= conn.cursor()
    print("\x1b[1;33m"+"Estas en el Apartado para Checar Ordenes de Clientes")
    print("")
    print("\x1b[1;32m"+"Dame el ID del cliente que quieras ver sus ordenes: ")
    print("")
    while True:
        try:
            User_ID=input("\x1b[1;36m"+"----> "+"\x1b[1;37m")
            User_ID=int(User_ID)
            break
        except ValueError:
            pass     
    
    cursor.execute("SELECT Cliente_ID FROM Clientes")
    ALL_ID=cursor.fetchall()
    k=0
    for i in ALL_ID:
        for j in i:
            if j==User_ID:
                k=1

        if k==1:
            break
        
    if k==0:
        os.system("cls")
        print("\x1b[1;31m"+"Losiento el ID ("+"\x1b[1;37m"+ F"{User_ID}" +"\x1b[1;31m"+") no existe en la base de datos")
        conn.close()
        time.sleep(3)
        return 0
    
    cursor.execute(f"SELECT Nombre,Apellido FROM Clientes WHERE Cliente_ID={User_ID}")
    nombres=cursor.fetchone()
    print("\x1b[1;36m"+f"El cliente se llama {nombres[0]} {nombres[1]}, Esta correcto?")
        
    User_Selection=input("\x1b[1;33m"+"---> "+"\x1b[1;37m")
    while not User_Selection in ("si","no"):
        User_Selection=input("\x1b[1;33m"+"---> "+"\x1b[1;37m")

    if User_Selection=="si":
        os.system("cls")
        print("\x1b[1;33m"+f"Aqui estan todas las ordenes hechas por el cliente con ID {User_ID}"+"\x1b[1;37m")
        sql=f'''
            SELECT OC.Orden_ID,C.Cliente_ID,C.Nombre,C.Apellido,OC.Dia,OC.Monto FROM Ordenes_Clientes OC
            INNER JOIN Clientes C ON C.Cliente_ID=OC.Cliente_ID
            WHERE C.Cliente_ID={User_ID} ORDER BY Orden_ID DESC  
            '''
        DF=pd.read_sql(sql,conn)
        print("")
        print(DF)
        print("")
        print("\x1b[1;36m"+"Quieres ver Mas informacion de alguna Orden? (si/no)")
        print("")

        User_Selection=input("\x1b[1;33m"+"---> "+"\x1b[1;37m")
        while not User_Selection in ("si","no"):
            User_Selection=input("\x1b[1;33m"+"---> "+"\x1b[1;37m")

        if User_Selection=="si":
            print("")
            print("\x1b[1;33m"+"Dame el Orden_ID de la orden que quieras ver mas informacion")
            print("")
            while True:
                try:
                    Orden_ID=input("\x1b[1;36m"+"----> "+"\x1b[1;37m")
                    Orden_ID=int(Orden_ID)
                    break
                except ValueError:
                    pass

            cursor.execute(f"SELECT Orden_ID FROM Ordenes_Clientes WHERE Cliente_ID={User_ID}")
            ALL_ID=cursor.fetchall()
            k=0
            for i in ALL_ID:
                for j in i:
                    if j==Orden_ID:
                        k=1

                if k==1:
                    break

            if k==0:
                os.system("cls")
                print("\x1b[1;31m"+"Losiento el Orden_ID ("+"\x1b[1;37m"+ F"{Orden_ID}" +"\x1b[1;31m"+f") no existe o no la realizo el Cliente con el ID {User_ID}")
                time.sleep(3)
                conn.close()
                os.system("cls")
                return 0
            
            os.system("cls")
            sql=f'''
                        SELECT P.Producto_ID,P.Nombre,P.Precio,D_O.Cantidad,P.Precio*D_O.Cantidad as Pago FROM Detalles_Ordenes D_O
                        INNER JOIN Productos P ON D_O.Producto_ID=P.Producto_ID 
                        WHERE D_O.Orden_ID={Orden_ID}    
            '''
            print("\x1b[1;33m"+f"Mas detalle sobre la Orden con el ID {Orden_ID}"+"\x1b[1;37m")
            print("")
            DF=pd.read_sql(sql,conn)
            cursor.execute(f'''
                            SELECT Monto FROM Ordenes_Clientes WHERE Orden_ID={Orden_ID}
                           ''')
            monto=cursor.fetchone()
            Monto_Total=monto[0]
            cursor.execute(f"SELECT Mayoreo FROM Ordenes_Clientes WHERE Orden_ID={Orden_ID}")
            Mayoreo=((cursor.fetchone())[0])
            cursor.execute(f'''
                           SELECT sum(P.Precio*D_O.Cantidad) FROM Detalles_Ordenes D_O
                           INNER JOIN Productos P ON D_O.Producto_ID=P.Producto_ID 
                           WHERE D_O.Orden_ID={Orden_ID}
                           ''')
            Monto_Inicial=((cursor.fetchone())[0])
            print(DF)
            print(f"Monto: ${Monto_Inicial}")
            print(f"Mayoreo: {Mayoreo}  Descuento: ${Monto_Inicial-Monto_Total} ")
            print(f"Monto Final= ${Monto_Total}")
            print("")
            a=input("\x1b[1;36m"+"Enter Para Continuar")
            conn.close()
            

            
            

    
    else:
        os.system("cls")
        print("\x1b[1;31m"+"Volviendo al menu")
        time.sleep(1.5)
        conn.close()
        os.system("cls")
        
        
def Checar_ID():
    os.system("cls")
    conn = sqlite3.connect(Database_Name)
    cursor= conn.cursor()
    print("\x1b[1;33m"+"Estas en el Apartado para Checar ID de cliente")
    print("")
    Nombre=input("\x1b[1;36m"+"Nombre: "+"\x1b[1;37m")
    print("")
    Apellido=input("\x1b[1;36m"+"Apellido: "+"\x1b[1;37m")
    cursor.execute(f'''
                   SELECT Cliente_ID FROM Clientes
                   WHERE Nombre LIKE "{Nombre}" AND Apellido LIKE "{Apellido}"
                   ''')
    ID=cursor.fetchone()
    

    if ID==None:
        os.system('cls')
        print("\x1b[1;31m"+"Este cliente no existe")
        conn.close()
        time.sleep(2)
        return 0

    else:
        User_ID=ID[0]
        cursor.execute(f'''
                       SELECT Nombre,Apellido FROM Clientes
                       WHERE Cliente_ID={User_ID}
                       ''')
        nombre=cursor.fetchone()
        print("")
        os.system("cls")
        print("\x1b[1;33m"+f"El Cliente {nombre[0]} {nombre[1]} tiene el ID "+"\x1b[1;32m",User_ID)
        print("")
        conn.close()
        a=input("\x1b[1;37m"+"Enter Para Continuar")
        os.system("cls")

def Mostar_Clientes():
    os.system("cls")
    conn = sqlite3.connect(Database_Name)
    print("\x1b[1;33m"+"Aqui estan los clientes que estan registrados en la base de datos"+"\x1b[1;37m")
    print("")
    DF=pd.read_sql("SELECT * FROM Clientes",conn)
    print(DF)
    print("")
    a=input("\x1b[1;36m"+"Enter to continue")
    conn.close()
    os.system("cls")


Database_Name="DB_Clientes_Mayoreo.DB"

#Creacion de Base de datos y tablas si no existe, si existe no es necesario crearlas todo de nuevo
if not os.path.exists(Database_Name):
    conn = sqlite3.connect(Database_Name)
    cursor= conn.cursor()
    cursor.execute('''
                  CREATE TABLE Clientes(
                    Cliente_ID INTEGER,
                    Nombre TEXT,
                    Apellido TEXT,
                    PRIMARY KEY (Cliente_ID AUTOINCREMENT)
                    UNIQUE(Nombre,Apellido)
                   ) 
                   ''')
    
    cursor.execute('''
                    CREATE TABLE Ordenes_Clientes(
                    Orden_ID INTEGER,
                    Cliente_ID INTEGER,
                    Mayoreo TEXT,
                    Monto INETEGER,
                    Dia DATE DEFAULT CURRENT_DATE,
                    FOREIGN KEY (Cliente_ID) REFERENCES Clientes(Cliente_ID),
                    PRIMARY KEY (Orden_ID AUTOINCREMENT)
                )
                   ''')
    cursor.execute('''
                    CREATE TABLE Productos(
                    Producto_ID INTEGER,
                    Nombre TEXT,
                    Precio INTEGER,
                    PRIMARY KEY (Producto_ID AUTOINCREMENT)
                    )
                   ''')
    
    cursor.execute('''
                   INSERT INTO Productos(Nombre,Precio)
                   VALUES ("Dama",120),("Caballero",120)
                   ''')
    
    cursor.execute('''
                    CREATE TABLE Detalles_Ordenes(
                    DetalleOrden_ID INTEGER,
                    Orden_ID INTEGER,
                    Producto_ID INTEGER,
                    Cantidad INTEGER,
                    PRIMARY KEY (DetalleOrden_ID AUTOINCREMENT),
                    FOREIGN KEY (Orden_ID) REFERENCES Ordenes_Clientes(Orden_ID),
                    FOREIGN KEY (Producto_ID) REFERENCES Productos(Producto_ID_ID)
                    )
                   ''')
    
    conn.commit()
    conn.close()

while True:
    os.system("cls")
    print("\x1b[1;33m"+"Bienvenido a la Base de Datos de Clientes")
    print("")
    print("\x1b[1;37m"+"Agregar Cliente a la Base de Datos ---> (1)")
    print("")
    print("\x1b[1;37m"+"Agregar Compra de Cliente ---> (2)")
    print("")
    print("\x1b[1;37m"+"Checar Pedidos de Un Cliente ---> (3)")
    print("")
    print("\x1b[1;37m"+"Checar Clientes en Base de Datos ---> (4)")
    print("")
    print("\x1b[1;37m"+"Buscar ID de Cliente ---> (5)")
    print("")
    while True:
        try:
            User_Selection=input("\x1b[1;32m"+"----> "+"\x1b[1;37m")
            User_Selection=int(User_Selection)
            break
        except ValueError:
            pass
    
    
    while not User_Selection in (1,2,3,4,5):
        while True:
            try:
                User_Selection=input("\x1b[1;32m"+"----> "+"\x1b[1;37m")
                User_Selection=int(User_Selection)
                break
            except ValueError:
                pass


    if User_Selection==1:
        os.system("cls")
        Agregar_Cliente()

    elif User_Selection==2:
        os.system("cls")
        Agregar_Compra()

    elif User_Selection==3:
        os.system("cls")
        Checar_Ordenes()

    elif User_Selection==4:
        os.system("cls")
        Mostar_Clientes()

    else:
        os.system("cls")
        Checar_ID()
