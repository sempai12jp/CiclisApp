from kivy.metrics import dp
from kivy.uix.widget import Widget
import random
import webbrowser

from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.list import IRightBodyTouch

CONSEJOS = [
    "Usa casco siempre que salgas a pedalear.",
    "Respeta las señales de tránsito y cruces peatonales.",
    "Mantén tu bicicleta en buen estado.",
    "Usa luces y reflectantes de noche.",
    "Evita usar el celular mientras conduces.",
    "Planifica tu ruta antes de salir."
]

class ConsejosScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'consejos'

        # Root vertical: top for consejo (~38%), bottom for noticias (rest)
        root = MDBoxLayout(orientation='vertical', padding=dp(12), spacing=dp(10))

        # --- Consejo (parte superior) ---
        # Tarjeta de Consejo de Seguridad
        card = MDCard(
            orientation="vertical",
            padding=dp(16),
            spacing=dp(12),
            radius=[20, 20, 20, 20],
            elevation=3,
            size_hint=(0.96, 0.9),
            md_bg_color=(0.93, 1, 0.94, 1)
        )

        card.add_widget(MDLabel(
            text="Consejo de Seguridad",
            font_style="H6",
            halign="center",
            theme_text_color="Primary"
        ))

        self.label_consejo = MDLabel(
            text=random.choice(CONSEJOS),
            font_style="Body1",
            halign="center",
            theme_text_color="Secondary"
        )
        card.add_widget(self.label_consejo)

        btn_nuevo = MDRaisedButton(
            text="Nuevo consejo",
            icon="lightbulb-on-outline",
            md_bg_color=(0.18, 0.58, 0.18, 1),
            text_color=(1, 1, 1, 1),
            pos_hint={"center_x": 0.5},
            size_hint=(None, None),
            size=(dp(140), dp(40)),
            on_release=self.nuevo_consejo
        )
        card.add_widget(btn_nuevo)

        top_container = MDBoxLayout(size_hint_y=0.38, padding=(dp(8), dp(8)))
        top_container.add_widget(card)

        # --- Noticias (parte inferior) ---
        bottom_scroll = MDScrollView(size_hint_y=0.62)
        bottom_container = MDBoxLayout(orientation='vertical', padding=(dp(8), dp(8)), spacing=dp(8), size_hint_y=None)
        bottom_container.bind(minimum_height=bottom_container.setter('height'))

        noticias_card = MDCard(
            orientation="vertical",
            padding=dp(12),
            spacing=dp(10),
            radius=[16, 16, 16, 16],
            elevation=2,
            size_hint=(0.96, None),
            md_bg_color=(0.9, 0.96, 1, 1)
        )

        noticias_card.add_widget(MDLabel(
            text="Noticias y Leyes del Ciclismo",
            font_style="H6",
            halign="left",
            theme_text_color="Primary"
        ))

        noticias = [
            {
                "titulo": "Ley de Convivencia Vial",
                "desc": "Cómo protege a los ciclistas en la vía pública.",
                "link": "https://www.mtt.gob.cl/leydeconvivenciavial",
                "icon": "gavel"
            },
            {
                "titulo": "Consejos MTT para ciclistas",
                "desc": "Recomendaciones oficiales del Ministerio de Transportes.",
                "link": "https://www.mtt.gob.cl/seguridadvial/ciclistas",
                "icon": "bike"
            },
            {
                "titulo": "Infraestructura ciclista - Noticias",
                "desc": "Actualizaciones sobre ciclovías y proyectos locales.",
                "link": "https://www.latercera.com/",
                "icon": "newspaper"
            }
        ]

        noticias_list = MDBoxLayout(orientation='vertical', spacing=dp(8), padding=(0, dp(8)), size_hint_y=None)
        noticias_list.bind(minimum_height=noticias_list.setter('height'))

        for item in noticias:
            entry = MDCard(orientation='horizontal', padding=dp(8), size_hint=(1, None), height=dp(72), elevation=1)

            left = MDBoxLayout(orientation='vertical', size_hint=(0.82, 1))
            left.add_widget(MDLabel(text=item['titulo'], font_style='Subtitle1', halign='left'))
            left.add_widget(MDLabel(text=item['desc'], font_style='Caption', halign='left', theme_text_color='Secondary'))
            entry.add_widget(left)

            btn = MDIconButton(icon=item.get('icon', 'open-in-new'), pos_hint={'center_y': 0.5}, on_release=lambda inst, url=item['link']: webbrowser.open(url))
            entry.add_widget(btn)

            noticias_list.add_widget(entry)

        # Ajustar altura de noticias_card según contenido
        noticias_card.add_widget(noticias_list)

        btn_more = MDRaisedButton(text="Ver más noticias", pos_hint={"center_x": 0.5}, size_hint=(None, None), size=(dp(160), dp(40)), on_release=lambda x: webbrowser.open('https://www.mtt.gob.cl'))
        noticias_card.add_widget(btn_more)

        bottom_container.add_widget(noticias_card)
        bottom_scroll.add_widget(bottom_container)

        # Montar root
        root.add_widget(top_container)
        root.add_widget(bottom_scroll)
        self.add_widget(root)

    def nuevo_consejo(self, instance):
        self.label_consejo.text = random.choice(CONSEJOS)