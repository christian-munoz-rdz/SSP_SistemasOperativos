import os, time

procesos_test = [
    {'nombre': 'Proceso 1', 'id': 1, 'operacion': '78+2', 'tiempo': 8},
    {'nombre': 'Proceso 2', 'id': 2, 'operacion': '56-23', 'tiempo': 5},
    {'nombre': 'Proceso 3', 'id': 3, 'operacion': '2*7', 'tiempo': 4},
    {'nombre': 'Proceso 4', 'id': 4, 'operacion': '3/8', 'tiempo': 8},
    {'nombre': 'Proceso 5', 'id': 5, 'operacion': '78%12', 'tiempo': 5},
    {'nombre': 'Proceso 6', 'id': 6, 'operacion': '2**6', 'tiempo': 4},
    {'nombre': 'Proceso 7', 'id': 7, 'operacion': '14//3', 'tiempo': 8},
    {'nombre': 'Proceso 8', 'id': 8, 'operacion': '6+7', 'tiempo': 5},
    {'nombre': 'Proceso 9', 'id': 9, 'operacion': '25-13', 'tiempo': 4},
    {'nombre': 'Proceso 10', 'id': 10, 'operacion': '4*2', 'tiempo': 7},
    {'nombre': 'Proceso 11', 'id': 11, 'operacion': '78/12', 'tiempo': 3},
    {'nombre': 'Proceso 12', 'id': 12, 'operacion': '9%2', 'tiempo': 5},
    {'nombre': 'Proceso 13', 'id': 13, 'operacion': '5**2', 'tiempo': 7},
    {'nombre': 'Proceso 14', 'id': 14, 'operacion': '10//2', 'tiempo': 6},
    {'nombre': 'Proceso 15', 'id': 15, 'operacion': '2+12', 'tiempo': 8},
    {'nombre': 'Proceso 16', 'id': 16, 'operacion': '5-3', 'tiempo': 8},
    {'nombre': 'Proceso 17', 'id': 17, 'operacion': '2*6', 'tiempo': 8},
    {'nombre': 'Proceso 18', 'id': 18, 'operacion': '15/2', 'tiempo': 8},
    {'nombre': 'Proceso 19', 'id': 19, 'operacion': '67%2', 'tiempo': 8},
    {'nombre': 'Proceso 20', 'id': 20, 'operacion': '6**2', 'tiempo': 8},
    {'nombre': 'Proceso 21', 'id': 21, 'operacion': '175//2', 'tiempo': 8},
    {'nombre': 'Proceso 22', 'id': 22, 'operacion': '2+56', 'tiempo': 8},
]

def executeProcess(procesos):
    # dividir lotes en grupos de 4
    lotes = []
    lote = []
    for proceso in procesos:
        lote.append(proceso)
        if len(lote) == 4:
            lotes.append(lote)
            lote = []
    if lote:
        lotes.append(lote)
	
    lote_en_ejecucion = 1
    lotes_pendientes = len(lotes) - 1
    procesos_terminados = []

    reloj_global = 0
    for lote in lotes:
        for proceso in lote:
            # mostramos el tiempo transcurrido
            tiempo_transcurrido = 0
            tiempo_restante = proceso['tiempo']
            resultado = eval(proceso['operacion'])
            for i in range(proceso['tiempo']):
                print(f"Procesando lote {lote_en_ejecucion}")
                print(f"Lotes Pendites: {lotes_pendientes}")
                print("=============================================")
                print(f"Ejecutando proceso")
                print(f"Nombre: {proceso['nombre']}")
                print(f"ID: {proceso['id']}")
                print(f"Operacion: {proceso['operacion']}")
                print(f"Tiempo estimado: {proceso['tiempo']} segundos")
                print(f"Tiempo transcurrido: {tiempo_transcurrido} segundos")
                tiempo_transcurrido += 1
                reloj_global += 1
                tiempo_restante -= 1
                print(f"Tiempo restante: {tiempo_restante} segundos")
                print(f"Procesos terminados:")
                # imprimir todos los procesos terminados en tabla
                print("\tID\t| Operacion\t|Resultado\t\n")
                print("==========================================================================================")
                for proceso_t in procesos_terminados:
                    print(f"\t{proceso_t['id']}\t|{proceso_t['operacion']}\t|{proceso_t['resultado']}\t\n")
                    print("==========================================================================================")
                print(f"Reloj Global: {reloj_global} segundos")
                print("=============================================")
                time.sleep(1)
                os.system("clear")
            
            procesos_terminados.append({
                "id": proceso['id'],
                "operacion": proceso['operacion'],
                "resultado": resultado
            })
        lote_en_ejecucion += 1
        lotes_pendientes -= 1

    print("Presione Enter para continuar")
    input()

executeProcess(procesos_test)