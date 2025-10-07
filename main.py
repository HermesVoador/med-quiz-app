import os
os.environ['KIVY_NO_ARGS'] = '1'

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.clock import Clock
import json
import random

Window.size = (360, 640)

class Database:
    def __init__(self):
        self.questoes = [
            {
                "numero": 1,
                "topico": "Cardiologia - Choque",
                "enunciado": "Paciente 70 anos em choque hipovolêmico pós-cirurgia. Melhor conduta:",
                "alternativas": {
                    "A": "Expansão com albumina",
                    "B": "Noradrenalina", 
                    "C": "Bicarbonato",
                    "D": "Expansão volêmica com cristaloides"
                },
                "resposta_correta": "D"
            },
            {
                "numero": 2,
                "topico": "Classificação do Choque", 
                "enunciado": "Causado por diminuição crítica do volume intravascular:",
                "alternativas": {
                    "A": "Choque anafilático",
                    "B": "Choque cardiogênico",
                    "C": "Choque hipovolêmico",
                    "D": "Choque distributivo"
                },
                "resposta_correta": "C"
            },
            {
                "numero": 3,
                "topico": "Tratamento do Choque",
                "enunciado": "Paciente em choque séptico com hipotensão persistente:",
                "alternativas": {
                    "A": "Aumentar antibiótico",
                    "B": "Iniciar vasopressores",
                    "C": "Suspender fluidos",
                    "D": "Administrar diuréticos"
                },
                "resposta_correta": "B"
            }
        ]
    
    def get_questoes_aleatorias(self, quantidade=3):
        return random.sample(self.questoes, min(quantidade, len(self.questoes)))

class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", padding=30, spacing=20)
        
        titulo = Label(
            text="[b]MED QUIZ[/b]\\nSimulados Offline",
            markup=True,
            font_size="24sp",
            size_hint=(1, 0.3)
        )
        layout.add_widget(titulo)
        
        botoes_layout = BoxLayout(orientation="vertical", spacing=15)
        
        btn_simulado = Button(
            text="🎯 INICIAR SIMULADO",
            size_hint=(1, 0.2),
            background_color=(0.2, 0.6, 0.8, 1),
            color=(1, 1, 1, 1),
            font_size="18sp"
        )
        btn_simulado.bind(on_press=self.iniciar_simulado)
        
        btn_sobre = Button(
            text="⭐ SOBRE",
            size_hint=(1, 0.2),
            background_color=(0.4, 0.4, 0.4, 1),
            color=(1, 1, 1, 1)
        )
        btn_sobre.bind(on_press=self.mostrar_sobre)
        
        botoes_layout.add_widget(btn_simulado)
        botoes_layout.add_widget(btn_sobre)
        layout.add_widget(botoes_layout)
        self.add_widget(layout)
    
    def iniciar_simulado(self, instance):
        app = App.get_running_app()
        app.iniciar_simulado()

    def mostrar_sobre(self, instance):
        content = BoxLayout(orientation="vertical", spacing=10, padding=20)
        content.add_widget(Label(text="MED QUIZ\\nApp de Simulados\\nDesenvolvido para estudos médicos"))
        btn_ok = Button(text="OK", size_hint_y=0.3)
        popup = Popup(title="Sobre", content=content, size_hint=(0.8, 0.4))
        btn_ok.bind(on_press=popup.dismiss)
        content.add_widget(btn_ok)
        popup.open()

class QuestaoScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.questoes = []
        self.indice_atual = 0
        self.acertos = 0
        
        layout = BoxLayout(orientation="vertical", padding=15, spacing=10)
        
        self.lbl_progresso = Label(text="1/3", size_hint=(1, 0.08), font_size="18sp")
        
        self.scroll_questao = ScrollView(size_hint=(1, 0.4))
        self.lbl_enunciado = Label(
            text="Carregando...",
            size_hint_y=None,
            text_size=(Window.width - 30, None),
            markup=True
        )
        self.lbl_enunciado.bind(texture_size=self.lbl_enunciado.setter("size"))
        self.scroll_questao.add_widget(self.lbl_enunciado)
        
        self.alternativas_layout = GridLayout(cols=1, spacing=8, size_hint=(1, 0.5))
        
        layout.add_widget(self.lbl_progresso)
        layout.add_widget(self.scroll_questao)
        layout.add_widget(self.alternativas_layout)
        self.add_widget(layout)
    
    def iniciar_simulado(self, questoes):
        self.questoes = questoes
        self.indice_atual = 0
        self.acertos = 0
        self.mostrar_questao()
    
    def mostrar_questao(self):
        if self.indice_atual >= len(self.questoes):
            self.finalizar_simulado()
            return
        
        questao = self.questoes[self.indice_atual]
        self.lbl_progresso.text = f"{self.indice_atual + 1}/{len(self.questoes)}"
        
        enunciado = f"[b]{questao['topico']}[/b]\\n\\n{questao['enunciado']}"
        self.lbl_enunciado.text = enunciado
        
        self.alternativas_layout.clear_widgets()
        for letra, texto in questao["alternativas"].items():
            btn = Button(
                text=f"{letra}) {texto}",
                size_hint_y=None,
                height=80,
                text_size=(Window.width - 40, None),
                halign="left",
                padding=(15, 10)
            )
            btn.letra = letra
            btn.questao = questao
            btn.bind(on_press=self.verificar_resposta)
            self.alternativas_layout.add_widget(btn)
    
    def verificar_resposta(self, instance):
        resposta_usuario = instance.letra
        resposta_correta = instance.questao.get("resposta_correta")
        
        if resposta_usuario == resposta_correta:
            instance.background_color = (0, 0.8, 0, 1)
            self.acertos += 1
        else:
            instance.background_color = (0.8, 0, 0, 1)
        
        Clock.schedule_once(self.proxima_questao, 1.5)
    
    def proxima_questao(self, dt):
        self.indice_atual += 1
        self.mostrar_questao()
    
    def finalizar_simulado(self):
        total = len(self.questoes)
        percentual = (self.acertos / total) * 100
        
        content = BoxLayout(orientation="vertical", spacing=10, padding=20)
        content.add_widget(Label(text="[b]RESULTADO[/b]", markup=True, font_size="20sp"))
        content.add_widget(Label(text=f"Acertos: {self.acertos}/{total}"))
        content.add_widget(Label(text=f"Nota: {percentual:.1f}%"))
        
        if percentual >= 70:
            content.add_widget(Label(text="🎉 Excelente!", font_size="18sp"))
        else:
            content.add_widget(Label(text="💪 Continue estudando!", font_size="18sp"))
        
        btn_fechar = Button(text="Voltar ao Menu", size_hint_y=0.3)
        popup = Popup(title="Fim do Simulado", content=content, size_hint=(0.9, 0.6))
        btn_fechar.bind(on_press=popup.dismiss)
        content.add_widget(btn_fechar)
        
        popup.bind(on_dismiss=lambda x: setattr(self.manager, "current", "menu"))
        popup.open()

class MedQuizApp(App):
    def __init__(self):
        super().__init__()
        self.database = Database()
    
    def build(self):
        self.title = "MED QUIZ"
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name="menu"))
        sm.add_widget(QuestaoScreen(name="questao"))
        return sm
    
    def iniciar_simulado(self):
        questoes = self.database.get_questoes_aleatorias(3)
        tela_questao = self.root.get_screen("questao")
        tela_questao.iniciar_simulado(questoes)
        self.root.current = "questao"

if __name__ == "__main__":
    MedQuizApp().run()
