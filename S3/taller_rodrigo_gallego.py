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

type Recuerdo = dict[str, str]
type MemoriaAgente = list[Recuerdo]

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
historial_chat: MemoriaAgente = [] 
mensaje = ""
comando_valido = True # Se agrega esta variable para controlar cuando se guarda el log y cuando no
sistema_activo = True

def pseudo_action(cmd: str, rol: str, historial: MemoriaAgente) -> None:
    global sistema_activo, mensaje, comando_valido
    if cmd == "salir":
        print("------Agente apagado. Vuelve pronto.------")
        sistema_activo = False
        mensaje = "Se ha solicitado terminar la sesión."
    elif cmd == "ping":
        print("pong.")
        mensaje = "Se ha enviado un ping y de respuesta se devolvió un pong."
    elif cmd == "contar":
        palabra = input("Ingrese una palabra: ").strip().lower()
        mensaje = contar_letras(palabra)
        print(mensaje)
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
            # print("[Acceso Denegado] Este comando requiere privilegios de administrador.")
            raise PermissionError("Acceso Denegado - Privilegios insuficientes.")
    # Nueva funcionalidad: Validar fortaleza de una contraseña
    elif cmd == "validar_pass":
        contrasena_a_validar = input("Ingrese la contraseña a validar: ").strip()
        # Se define la fortaleza de la contraseña basada en su longitud y la presencia de caracteres especiales
        mensaje = validar_pass(contrasena_a_validar)
        print(mensaje)
    # Función de calculadora
    elif cmd == "calculadora":
        try:
            resultado = calculadora()
            mensaje = f"Resultado: {resultado}"
            print(mensaje)
        except ValueError as ex:
            mensaje = f"Error: {ex}"
            print(mensaje)
    elif cmd == "historial":
        historial = input("""Historial de Comandos:
- 'all' ver todo el historial
- 'clear' limpiar el historial
- 'buscar' buscar en el historial por palabra clave
""")
        log: str = gestionar_historial(historial_chat, historial)
        print(log)
    else:
        print("------Comando desconocido. Intente de nuevo.-------")
        comando_valido = False
    
    almacenar_log(cmd, rol, mensaje, historial)

def almacenar_log(cmd: str, rol: str, descripcion: str, historial: MemoriaAgente) -> None:
    global comando_valido, mensaje
    if comando_valido:
        d_log: Recuerdo = {"timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "cmd": cmd,
                "rol": rol,
                "descripcion": descripcion}
                    
        historial.append(d_log)
    comando_valido = True # Se resetea la variable para el siguiente comando
    mensaje = "" # Se resetea el mensaje para el siguiente comando

def gestionar_historial(historial: MemoriaAgente, accion: str) -> str:
    global comando_valido
    log: str = ""
    if accion == "all":
        if not historial:
            log = "El historial está vacío."
        else:
            log += f"Historial completo:\n"
            for entry in historial:
                # se retorna el log con el historial completo entrada por entrada
                log += f"{entry}\n"
                
    elif accion == "clear":
        historial.clear()
        log = "Se limpió el historial."
    elif accion == "buscar":
        # Se almacena la entrada de busqueda, se limpian los espacios y se convierte a minusculas para facilitar la búsqueda
        keyword = input("Ingrese la palabra clave para buscar en el historial: ").strip().lower()
        # Se itera sobre el historial_chat para encontrar entradas que contengan la palabra clave "keyword" en el comando o en la descripción, se almacena el resultado en una nueva lista 'resultados'
        resultados: MemoriaAgente = [entry for entry in historial if keyword in entry['cmd'] or keyword in entry['descripcion']]
        if resultados:
            log += f"Resultados de búsqueda para '{keyword}':\n"
            for entry in resultados:
                log += f"{entry}\n"
        else:
            log=f"No se encontraron entradas en el historial que contengan '{keyword}'."
    comando_valido = False # No se guarda el log para el comando de historial, ya que es una consulta al mismo
    return log

def contar_letras(palabra: str) -> str:
    # quitar los espacios de la palabra para contar solo las letras
    palabra = palabra.replace(" ", "")
    tot_letras = len(palabra)
    tot_vocales = sum(1 for p in palabra if p in "aeiou")
    tot_consonantes = tot_letras - tot_vocales
    return f"Total de letras: {tot_letras}, Vocales: {tot_vocales}, Consonantes: {tot_consonantes}"

def calculadora() -> str:
    num1 = input("Ingrese el primer número: ").strip()
    operador = input("Ingrese el operador (+, -, *, /): ").strip()
    num2 = input("Ingrese el segundo número: ").strip()
    try:
        num1 = float(num1)
        num2 = float(num2)
    except ValueError:
        raise ValueError("Por favor, ingrese números válidos.")

    if operador == "+":
        return str(num1 + num2)
    elif operador == "-":
        return str(num1 - num2)
    elif operador == "*":
        return str(num1 * num2)
    elif operador == "/":
        if num2 != 0:
            return str(num1 / num2)
        else:
            raise ValueError("División por cero no permitida.")
    else:
        raise ValueError("Operador no reconocido. Use +, -, *, o /.")

def validar_pass(contrasena: str) -> str:
    if len(contrasena) >= 8 and any(char in "!@#$%^&*()-_=+[]{}|;:'\",.<>?/" for char in contrasena):
        return "La contraseña es fuerte."
    elif len(contrasena) >= 6:
        return "La contraseña es moderada."
    elif contrasena == usuario:
        return "La contraseña no debe ser igual al nombre de usuario."
    else:
        return "La contraseña es débil."

while sistema_activo:
    try:
        cmd = input("""Seleccione un comando para el pseudoagente:
- 'salir' para terminar la sesión
- 'ping' para recibir un pong
- 'contar' para contar letras, vocales y consonantes en una palabra
- 'fecha_hoy' para mostrar la fecha y hora actual
- 'validar_pass' para validar la fortaleza de una contraseña
- 'calculadora' para realizar operaciones matemáticas básicas
- 'historial' para mostrar el historial de comandos
Agente: """).strip().lower()
        pseudo_action(cmd, rol_actual, historial_chat)
    except Exception as e:
        print(f"[Error] {e}")
