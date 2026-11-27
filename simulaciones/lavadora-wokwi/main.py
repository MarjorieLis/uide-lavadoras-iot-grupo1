"""GTA S5 - Simulación de lavadora compartida en Wokwi (ESP32/MicroPython).

Broker PUBLICO de pruebas: no usar claves reales ni equipos eléctricos.
El LED representa una carga de BAJA TENSION, nunca una lavadora a 110/120 V.
"""
import network
import time
import ujson
from machine import ADC, Pin
from umqtt.simple import MQTTClient

# Wokwi conecta a Internet mediante la red Wi-Fi ficticia Wokwi-GUEST.
WIFI_SSID = 'Wokwi-GUEST'
WIFI_PASS = ''

# Broker compartido de PRUEBAS. La VM escuchará este MISMO broker remoto.
BROKER = 'broker.emqx.io'
PUERTO = 1883
NODO = 'g1-marjorielis-lav01'
BASE = b'uide/g1/marjorielis/lavadora01'
T_ESTADO = BASE + b'/estado'
T_EVENTO = BASE + b'/evento'
T_DATOS = BASE + b'/telemetria'
T_COMANDO = BASE + b'/cmd'

# GPIO34: perilla que representa la lectura del sensor de corriente.
# GPIO4: botón que simula la confirmación del pago.
# GPIO2: LED que indica que la carga de demostración está habilitada.
medidor = ADC(Pin(34))
medidor.atten(ADC.ATTN_11DB)
boton = Pin(4, Pin.IN, Pin.PULL_UP)
indicador = Pin(2, Pin.OUT, value=0)

estado = 'BLOQUEADA'
ultimo_cmd_id = None
ciclo_id = None
inicio_habilitado = 0
conectado = None
contador_eventos = 0
ultimo_boton = 1
ultimo_cambio_boton = 0


def mensaje(**campos):
    """En todos los mensajes se identifica el nodo."""
    datos = {'nodo': NODO}
    datos.update(campos)
    return ujson.dumps(datos)


def publicar_estado(mqtt):
    global estado
    mqtt.publish(T_ESTADO, mensaje(estado=estado), qos=1, retain=True)
    print('Estado MQTT:', estado)


def publicar_evento(mqtt, tipo):
    global contador_eventos
    contador_eventos += 1
    evento_id = 'EV-%d-%03d' % (time.ticks_ms(), contador_eventos)
    payload = mensaje(evento=tipo, event_id=evento_id, ciclo_id=ciclo_id)
    mqtt.publish(T_EVENTO, payload, qos=1)
    print('Evento MQTT:', payload)


def cambiar_estado(nuevo, mqtt):
    global estado
    if estado == nuevo:
        return
    estado = nuevo
    indicador.value(1 if estado in ('HABILITADA', 'LAVANDO') else 0)
    publicar_estado(mqtt)


def habilitar(cmd_id, mqtt):
    global ultimo_cmd_id, ciclo_id, inicio_habilitado
    if estado != 'BLOQUEADA' or not cmd_id or cmd_id == ultimo_cmd_id:
        print('Autorizacion rechazada (estado o cmd_id repetido)')
        return
    ultimo_cmd_id = cmd_id
    ciclo_id = 'C-%d' % time.ticks_ms()
    inicio_habilitado = time.ticks_ms()
    cambiar_estado('HABILITADA', mqtt)
    publicar_evento(mqtt, 'autorizado')


def recibir_comando(topic, payload):
    if topic != T_COMANDO or conectado is None:
        return
    try:
        datos = ujson.loads(payload)
        if datos.get('accion') == 'habilitar':
            # Un mensaje de pruebas; no representa un pago real.
            habilitar(datos.get('cmd_id'), conectado)
        else:
            print('Comando no reconocido')
    except (ValueError, TypeError) as err:
        print('JSON invalido:', err)


def conectar_wifi():
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    if not wifi.isconnected():
        print('Conectando a Wi-Fi...')
        wifi.connect(WIFI_SSID, WIFI_PASS)
        for _ in range(100):
            if wifi.isconnected():
                break
            time.sleep_ms(150)
    if not wifi.isconnected():
        raise OSError('Sin Wi-Fi de Wokwi')
    print('Wi-Fi conectado. IP:', wifi.ifconfig()[0])


def conectar_mqtt():
    global conectado
    mqtt = MQTTClient(NODO, BROKER, port=PUERTO, keepalive=15)
    mqtt.set_callback(recibir_comando)
    # El broker publicara este mensaje cuando el nodo desaparezca SIN DISCONNECT.
    # La retencion permite que un nuevo suscriptor vea el ultimo estado.
    mqtt.set_last_will(T_ESTADO, mensaje(estado='desconectado'), retain=True, qos=1)
    mqtt.connect()
    mqtt.subscribe(T_COMANDO, qos=1)
    conectado = mqtt
    publicar_estado(mqtt)
    print('MQTT conectado:', BROKER, 'tema:', BASE.decode())
    return mqtt


def operar(mqtt):
    global ultimo_boton, ultimo_cambio_boton
    ultima_telemetria = time.ticks_ms() - 5000
    ultimo_ping = time.ticks_ms()
    fin_en = None
    while True:
        mqtt.check_msg()
        ahora = time.ticks_ms()
        val = medidor.read()
        detectado = val > 1800  # Girar la perilla a mas del 45 % para simular consumo.

        pulsado = boton.value()
        if ultimo_boton == 1 and pulsado == 0 and time.ticks_diff(ahora, ultimo_cambio_boton) > 350:
            habilitar('BOTON-%d' % ahora, mqtt)
            ultimo_cambio_boton = ahora
        ultimo_boton = pulsado

        if estado == 'HABILITADA':
            if detectado:
                cambiar_estado('LAVANDO', mqtt)
                publicar_evento(mqtt, 'inicio')
            elif time.ticks_diff(ahora, inicio_habilitado) >= 600000:
                cambiar_estado('BLOQUEADA', mqtt)
                publicar_evento(mqtt, 'autorizacion_vencida')

        elif estado == 'LAVANDO' and not detectado:
            cambiar_estado('FINALIZADA', mqtt)
            publicar_evento(mqtt, 'fin')
            fin_en = ahora

        elif estado == 'FINALIZADA' and fin_en is not None:
            if time.ticks_diff(ahora, fin_en) > 3500:
                cambiar_estado('BLOQUEADA', mqtt)
                fin_en = None

        if time.ticks_diff(ahora, ultima_telemetria) >= 5000:
            texto = mensaje(estado=estado, lectura=val, consumo_simulado=detectado)
            mqtt.publish(T_DATOS, texto, qos=0)
            print('JSON publicado:', texto)
            ultima_telemetria = ahora

        if time.ticks_diff(ahora, ultimo_ping) > 5000:
            mqtt.ping()
            ultimo_ping = ahora
        time.sleep_ms(200)


print('ESP32 - Lavadora compartida - GTA S5')
print('Boton: autorizacion de prueba. Perilla: consumo simulado. LED: carga.')

while True:
    try:
        conectado = None
        indicador.off() if estado == 'BLOQUEADA' else None
        conectar_wifi()
        cliente = conectar_mqtt()
        operar(cliente)
    except (OSError, ValueError, AssertionError) as err:
        print('Fallo de red/MQTT:', err, 'Reintentando en 4 s')
        conectado = None
        time.sleep(4)
