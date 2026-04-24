import gradio as gr
import time

# 1. CONFIGURACIÓN DE RESPUESTAS RÁPIDAS
# Estas se usarán para limpiar la cola de 20 mensajes de ráfaga
RESPUESTAS_PREDETERMINADAS = [
    "jajaja epa vale, ¿cómo estás?",
    "holii, ando un poquito full pero aquí estoy jaja",
    "epa mi loco, ¿todo bien?",
    "vale, cuéntame más pues jaja"
]

class SugoState:
    def __init__(self):
        self.conteo_inicial = 5
        self.app_lanzada = False
        self.cola_mensajes = []
        self.total_atendidos = 0

state = SugoState()

def procesar_sugo(mensaje_entrante):
    # Lógica del temporizador de 5 segundos al encender
    if not state.app_lanzada:
        while state.conteo_inicial > 0:
            time.sleep(1)
            state.conteo_inicial -= 1
        state.app_lanzada = True
        return "🚀 Sugo Chat Fiesta Lanzado. Capturando notificaciones..."

    # Lógica de la Cola (Capacidad 20)
    if len(state.cola_mensajes) < 20:
        state.cola_mensajes.append(mensaje_entrante)
        return f"📥 Mensaje en cola ({len(state.cola_mensajes)}/20). Esperando lote..."

    # Lógica de Respuesta en Ráfaga (Al llegar a 20)
    else:
        # Elegimos una respuesta rápida según el total para variar un poco
        indice = (state.total_atendidos // 20) % len(RESPUESTAS_PREDETERMINADAS)
        respuesta_final = RESPUESTAS_PREDETERMINADAS[indice]
        
        state.total_atendidos += len(state.cola_mensajes)
        state.cola_mensajes = [] # Limpiamos la cola para el siguiente lote
        
        return f"⚡ Lote de 20 completado. Respondiendo a todos: '{respuesta_final}'"

# 2. INTERFAZ TIPO DASHBOARD (Estilo Novamine)
with gr.Blocks(theme=gr.themes.Monochrome()) as demo:
    gr.Markdown("# 🛸 **SUGO-FIESTA CONTROL CENTER**")
    
    with gr.Row():
        # Indicadores en tiempo real
        timer_disp = gr.Number(label="Timer Arranque", value=5, interactive=False)
        cola_disp = gr.Number(label="Mensajes en Cola", value=0, interactive=False)
        total_disp = gr.Number(label="Total Procesados", value=0, interactive=False)

    with gr.Column():
        msg_input = gr.Textbox(label="Entrada de Notificación", placeholder="Simula un mensaje de Sugo...")
        btn_enviar = gr.Button("Enviar a la Cola")
        output_status = gr.Textbox(label="Acción del Bot")

    # Función para conectar la interfaz con la lógica
    def trigger(m):
        res = procesar_sugo(m)
        return res, state.conteo_inicial, len(state.cola_mensajes), state.total_atendidos

    btn_enviar.click(
        trigger, 
        inputs=msg_input, 
        outputs=[output_status, timer_disp, cola_disp, total_disp]
    )

    # Refresco automático cada segundo para el Dashboard
    demo.load(
        lambda: (state.conteo_inicial, len(state.cola_mensajes), state.total_atendidos),
        None,
        [timer_disp, cola_disp, total_disp],
        every=1
    )

if __name__ == "__main__":
    # Render necesita que el puerto sea el 10000 o el que asigne el sistema
    demo.launch(server_name="0.0.0.0", server_port=10000)
