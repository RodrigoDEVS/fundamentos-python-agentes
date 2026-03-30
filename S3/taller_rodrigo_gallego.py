#Dia 2 - Estructuras de control
## while 

#nombre = input("¿Cómo te llamas?: ")
#print(f"Hola, {nombre}. Adios~")

#Estructura y lógica: while
## while condicion:
#   ...
#   ...
#   if(...):
#        break
##  Cuidado con los bucles infinitos! El truco? La 'actualización/gestión' de la condición
##  break, continue

#Previa del taller de la semana (Mini-taller II): Hacer un pseudoagente estilo consola
## ¿Qué podra hacer este agente por medio de comandos?
### Terminar la sesión - salir
### Responder un ping con un pong - ping
### Contar letras en una palabra: Total, vocales y consonantes - contar

## Librerias adicionales para el taller
from datetime import datetime

print("----- Iniciando el pseudoagente estilo consola -------")


# Login básico
usuario = input("Usuario: ").strip()
contrasena = input("Contraseña: ").strip()

# Se define la variable 'tries' para limitar los intentos de login a 3 (1 inicial + 2 adicionales)
tries = 2
rol_actual = ""

# El bucle while se ejecuta mientras las credenciales sean incorrectas y queden intentos disponibles
while not (
    (usuario == "admin" and contrasena == "admin") or 
    (usuario == "invitado" and contrasena == "invitado")
    ) and tries > 0:
    print(f"[Alerta] Credenciales incorrectas. Intentos restantes: {tries}")
    usuario = input("Usuario: ").strip()
    contrasena = input("Contraseña: ").strip()
    tries -= 1

# Si después de 3 intentos las credenciales siguen siendo incorrectas, se bloquea el acceso
if not (
    (usuario == "admin" and contrasena == "admin") or 
    (usuario == "invitado" and contrasena == "invitado")
    ):
    print("[Alerta] Usuario bloqueado. Cerrando sistema.")
    exit()

rol_actual = usuario  # Asignamos el rol basado en el usuario ingresado
print(f"Bienvenido, {usuario}.")

#Banderas/Banderines - Booleanos 
#TO-DO: Agregar una memoria al pseudo agente utilizando listas y diccionarios   
historial_chat=[] 
mensaje = ""
comando_valido = True # Se agrega esta variable para controlar cuando se guarda el log y cuando no
sistema_activo = True
while sistema_activo:
    cmd = input("""Seleccione un comando para el pseudoagente:
- 'salir' para terminar la sesión
- 'ping' para recibir un pong
- 'contar' para contar letras, vocales y consonantes en una palabra
- 'fecha_hoy' para mostrar la fecha y hora actual
- 'validar_pass' para validar la fortaleza de una contraseña
- 'calculadora' para realizar operaciones matemáticas básicas
- 'historial' para mostrar el historial de comandos
Agente: """).strip().lower()

    if cmd == "salir":
        print("------Agente apagado. Vuelve pronto.------")
        sistema_activo = False
        mensaje = "Se ha solicitado terminar la sesión."
    elif cmd == "ping":
        print("pong.")
        mensaje = "Se ha enviado un ping y de respuesta se devolvió un pong."
    elif cmd =="contar":
        palabra = input("Ingrese una palabra: ").lower()
        tot_letras = len(palabra)
        tot_vocales = 0
        tot_cons = 0
        
        for p in palabra:
            if p in "aeiou":
                tot_vocales +=1
            else:
                tot_cons +=1
        
        print(f"Palabra ingresada: {palabra}")
        print(f"Total de vocales: {tot_vocales}")
        print(f"Total de consonantes: {tot_cons}")
        print(f"Total de letras: {tot_letras}")
        mensaje = f"""Se solicitó el conteo de la palabra {palabra}, dando como resultados:
            Vocales: {tot_vocales}
            Consonantes: {tot_cons}
            Total: {tot_letras}"""
    # Nueva funcionalidad: Mostrar fecha y hora actual
    elif cmd == "fecha_hoy":
        # Se obtiene la fecha y hora actual formateada como "DD/MM/YYYY HH:MM:SS"
        fecha_hora_actual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        # Solo el usuario 'admin' tiene acceso a esta información, se verifica el usuario antes de mostrarla
        if usuario == "admin":
            print(f"Fecha y hora actual: {fecha_hora_actual}")
            mensaje = f"[PseudoAgente] La fecha y hora actual es: {fecha_hora_actual}"
        else:
            mensaje = "[Acceso Denegado] Este comando requiere privilegios de administrador."  
            print("[Acceso Denegado] Este comando requiere privilegios de administrador.")
    # Nueva funcionalidad: Validar fortaleza de una contraseña
    elif cmd == "validar_pass":
        contrasena_a_validar = input("Ingrese la contraseña a validar: ").strip()
        # Se define la fortaleza de la contraseña basada en su longitud y la presencia de caracteres especiales
        if len(contrasena_a_validar) >= 8 and any(char in "!@#$%^&*()-_=+[]{}|;:'\",.<>?/" for char in contrasena_a_validar):
            mensaje = "La contraseña es fuerte."
            print("La contraseña es fuerte.")
        elif len(contrasena_a_validar) >= 6:
            mensaje = "La contraseña es moderada."
            print("La contraseña es moderada.")
        elif contrasena_a_validar == usuario:
            mensaje = "La contraseña no debe ser igual al nombre de usuario."
            print("La contraseña no debe ser igual al nombre de usuario.")
        else:
            mensaje = "La contraseña es débil."
            print("La contraseña es débil.")

    # Función de calculadora
    elif cmd == "calculadora":
        print("Ingrese la operación en formato: número1 operador número2 (ejemplo: 5 + 3)")
        num1 = input("Ingrese el primer número: ").strip()
        operador = input("Ingrese el operador (+, -, *, /): ").strip()
        num2 = input("Ingrese el segundo número: ").strip()
        try:
            num1 = float(num1)
            num2 = float(num2)
            if operador == "+":
                resultado = num1 + num2
            elif operador == "-":
                resultado = num1 - num2
            elif operador == "*":
                resultado = num1 * num2
            elif operador == "/":
                if num2 != 0:
                    resultado = num1 / num2
                else:
                    print("Error: División por cero no permitida.")
                    continue
            
            else:
                print("Operador no reconocido. Use +, -, *, o /.")
                continue
            mensaje = f"Se realizó la operación: {num1} {operador} {num2} = {resultado}"
            print(f"Resultado: {resultado}")
            # Captura de errores para entradas no numéricas o formato incorrecto
        except ValueError:
            print("Formato de operación incorrecto. Intente de nuevo.")
    elif cmd == "historial":
        historial = input("""Historial de Comandos:
- 'all' ver todo el historial
- 'clear' limpiar el historial
- 'buscar' buscar en el historial por palabra clave
""")
        if historial == "all":
            if not historial_chat:
                print("El historial está vacío.")
            else:
                print("Historial completo:")
                for entry in historial_chat:
                    print(entry)
        elif historial == "clear":
            historial_chat.clear()
            print("Se limpió el historial.")
        elif historial == "buscar":
            # Se almacena la entrada de busqueda, se limpian los espacios y se convierte a minusculas para facilitar la búsqueda
            keyword = input("Ingrese la palabra clave para buscar en el historial: ").strip().lower()
            # Se itera sobre el historial_chat para encontrar entradas que contengan la palabra clave "keyword" en el comando o en la descripción, se almacena el resultado en una nueva lista 'resultados'
            resultados = [entry for entry in historial_chat if keyword in entry['cmd'] or keyword in entry['descripcion']]
            if resultados:
                print(f"Resultados de búsqueda para '{keyword}':")
                for entry in resultados:
                    print(entry)
            else:
                # Si no se encuentran resultados, se muestra un mensaje indicando que no se encontraron coincidencias
                print(f"No se encontraron entradas en el historial que contengan '{keyword}'.")
        comando_valido = False # No se guarda el log para el comando de historial, ya que es una consulta al mismo
    else:
        print("------Comando desconocido. Intente de nuevo.-------")
        comando_valido = False
    
    #TO-DO: Taller de la semana - Búsqueda de memoria
    if comando_valido:
        d_log = {"timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "cmd": cmd,
                "rol": rol_actual,
                "descripcion": mensaje}
                    
        historial_chat.append(d_log)
    comando_valido = True # Se resetea la variable para el siguiente comando
    mensaje = "" # Se resetea el mensaje para el siguiente comando