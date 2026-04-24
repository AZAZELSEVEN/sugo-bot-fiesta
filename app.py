import gradio as gr
import time

# 1. CONFIGURACIÓN
RESPUESTAS_PREDETERMINADAS = [
    "jajaja epa vale, ¿cómo estás?",
    "holii, ando un poquito full pero aquí estoy jaja",
    "epa mi loco, ¿todo bien?"
]

class SugoState:
    def __init__(self):
        self.app_lanzada = False
        self.cola_mensajes = []
        self.total_atendidos = 0

state = SugoState()

def procesar_sugo(mensaje_entrante):
    if not state.app_lanzada:
        time.sleep(5) # Simulación de los 5 segundos de arranque
        state.app_lanzada = True
        return "🚀 Sugo Chat Fiesta Lanzado. Enviando mensajes...", 0, 0

    if len(state.cola_mensajes) < 19: # Contamos hasta 19 para que el 20 dispare
        state.cola_mensajes.append(mensaje_entrante)
        return f"📥 En cola: {len(state.cola_mensajes)}/20", len(state.cola_mensajes), state.total_atendidos
    else:
        indice = (state.total_atendidos // 20) % len(RESPUESTAS_PREDETERMINADAS)
        respuesta = RESPUESTAS_PREDETERMINADAS[indice]
        state.total_atendidos += 20
        state.cola_mensajes = []
        return f"⚡ Lote completado. Respuesta: {respuesta}", 0, state.total_atendidos

# 2. INTERFAZ SIMPLIFICADA
with gr.Blocks() as demo:
    gr.Markdown("# 🛸 **SUGO-FIESTA CONTROL**")
    
    with gr.Row():
        cola_disp = gr.Number(label="Mensajes en Cola", value=0)
        total_disp = gr.Number(label="Total Atendidos", value=0)

    msg_input = gr.Textbox(label="Mensaje de Sugo")
    btn_enviar = gr.Button("Enviar")
    output_status = gr.Textbox(label="Estado")

    btn_enviar.click(
        procesar_sugo, 
        inputs=msg_input, 
        outputs=[output_status, cola_disp, total_disp]
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=10000)
