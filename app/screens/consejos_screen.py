from kivy.metrics import dp
from kivy.animation import Animation
import random
import webbrowser

from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDIconButton, MDRectangleFlatIconButton
from kivymd.uix.scrollview import MDScrollView


# --- Consejos aleatorios ---
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

        # --- Layout principal ---
        root = MDBoxLayout(orientation='vertical')
        scroll = MDScrollView(do_scroll_x=False)
        content = MDBoxLayout(
            orientation='vertical',
            padding=dp(16),
            spacing=dp(22),
            size_hint_y=None
        )
        content.bind(minimum_height=content.setter('height'))

        # ==============================
        # SECCIÓN: Consejo de Seguridad
        # ==============================
        consejo_card = MDCard(
            orientation='vertical',
            padding=(dp(24), dp(20)),
            spacing=dp(14),
            radius=[16, 16, 16, 16],
            elevation=1,  # 🔽 sombra reducida
            size_hint=(0.95, None),
            adaptive_height=True,
            pos_hint={'center_x': 0.5},
            md_bg_color=(0.95, 0.99, 0.95, 1)
        )

        # Contenedor interno
        inner_box = MDBoxLayout(
            orientation='vertical',
            spacing=dp(12),
            adaptive_height=True
        )

        # Título principal
        inner_box.add_widget(MDLabel(
            text="Consejo de Seguridad",
            font_style="H5",
            halign="center",
            bold=True,
            theme_text_color="Primary"
        ))

        # Texto del consejo
        self.label_consejo = MDLabel(
            text=random.choice(CONSEJOS),
            halign="center",
            font_style="Body1",
            theme_text_color="Secondary",
            size_hint_y=None,
            height=dp(40)
        )
        inner_box.add_widget(self.label_consejo)

        # Separador visual
        from kivy.uix.widget import Widget
        from kivy.graphics import Color, Rectangle
        divider = Widget(size_hint_y=None, height=dp(1))
        with divider.canvas.before:
            Color(0.8, 0.9, 0.8, 1)
            self.rect = Rectangle(size=divider.size, pos=divider.pos)
        divider.bind(pos=lambda inst, val: setattr(self.rect, 'pos', inst.pos))
        divider.bind(size=lambda inst, val: setattr(self.rect, 'size', inst.size))
        inner_box.add_widget(divider)

        # Botón "Nuevo consejo"
        btn_nuevo = MDRectangleFlatIconButton(
            text="Nuevo consejo",
            icon="refresh",
            theme_icon_color="Custom",
            icon_color=(1, 1, 1, 1),
            text_color=(1, 1, 1, 1),
            md_bg_color=(0.15, 0.6, 0.15, 1),
            size_hint=(None, None),
            size=(dp(190), dp(44)),
            pos_hint={'center_x': 0.5},
            on_release=self.nuevo_consejo
        )
        inner_box.add_widget(btn_nuevo)

        consejo_card.add_widget(inner_box)
        content.add_widget(consejo_card)

        # ==============================
        # SECCIÓN: Noticias y Leyes
        # ==============================
        content.add_widget(MDLabel(
            text="Noticias y Leyes del Ciclismo",
            font_style="H6",
            halign="left",
            size_hint_y=None,
            height=dp(32),
            theme_text_color="Primary"
        ))

        noticias = [
            {
                'titulo': 'Ley de Convivencia Vial',
                'desc': 'Cómo protege a los ciclistas en la vía pública.',
                'link': 'https://www.mtt.gob.cl/leydeconvivenciavial',
                'icon': 'gavel'
            },
            {
                'titulo': 'Consejos MTT para ciclistas',
                'desc': 'Recomendaciones oficiales del Ministerio de Transportes.',
                'link': 'https://www.mtt.gob.cl/seguridadvial/ciclistas',
                'icon': 'bike'
            },
            {
                'titulo': 'Infraestructura ciclista - Noticias',
                'desc': 'Actualizaciones sobre ciclovías y proyectos locales.',
                'link': 'https://www.latercera.com/',
                'icon': 'newspaper'
            }
        ]

        for item in noticias:
            card = MDCard(
                orientation='horizontal',
                padding=(dp(14), dp(10)),
                spacing=dp(10),
                size_hint=(0.95, None),
                height=dp(86),
                radius=[14, 14, 14, 14],
                elevation=1,  # 🔽 sombra reducida
                pos_hint={'center_x': 0.5},
                md_bg_color=(0.96, 0.98, 1, 1)
            )

            # Texto
            text_box = MDBoxLayout(orientation='vertical', spacing=dp(4))
            text_box.add_widget(MDLabel(
                text=item['titulo'],
                font_style='Subtitle1',
                theme_text_color='Primary'
            ))
            text_box.add_widget(MDLabel(
                text=item['desc'],
                font_style='Caption',
                theme_text_color='Secondary'
            ))

            # Icono para abrir enlace
            icon_btn = MDIconButton(
                icon=item['icon'],
                pos_hint={'center_y': 0.5},
                theme_icon_color="Custom",
                icon_color=(0.1, 0.4, 0.8, 1),
                on_release=lambda inst, url=item['link']: webbrowser.open(url)
            )

            card.add_widget(text_box)
            card.add_widget(icon_btn)
            content.add_widget(card)

        # ==============================
        # BOTÓN FINAL
        # ==============================
        content.add_widget(
            MDRaisedButton(
                text="Ver más noticias",
                md_bg_color=(0.18, 0.6, 0.18, 1),
                text_color=(1, 1, 1, 1),
                size_hint=(None, None),
                size=(dp(190), dp(44)),
                pos_hint={'center_x': 0.5},
                elevation=1,  # 🔽 sombra reducida
                on_release=lambda x: webbrowser.open('https://www.mtt.gob.cl')
            )
        )

        # Espacio inferior
        content.add_widget(MDBoxLayout(size_hint_y=None, height=dp(24)))

        scroll.add_widget(content)
        root.add_widget(scroll)
        self.add_widget(root)

    # ==============================
    # FUNCIÓN: animar cambio de consejo
    # ==============================
    def nuevo_consejo(self, instance):
        new_text = random.choice(CONSEJOS)
        anim = Animation(opacity=0, d=0.15)

        def set_text(*args):
            self.label_consejo.text = new_text

        def fade_in(*args):
            Animation(opacity=1, d=0.25).start(self.label_consejo)

        anim.bind(on_complete=lambda *a: (set_text(), fade_in()))
        anim.start(self.label_consejo)
