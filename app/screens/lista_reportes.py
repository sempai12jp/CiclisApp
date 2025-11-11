from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRectangleFlatIconButton
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.list import MDList, OneLineListItem
from kivymd.uix.textfield import MDTextField
from kivy.metrics import dp
from app.utils.ui import show_snackbar
import os
import json
import csv


class ListaReportes(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'lista_reportes'
        from kivymd.uix.toolbar import MDTopAppBar

        # Layout principal
        layout = MDBoxLayout(orientation='vertical', padding=dp(16), spacing=dp(10))

        # Barra superior
        self.toolbar = MDTopAppBar(
            title='Reportes guardados',
            left_action_items=[['arrow-left', lambda x: self.volver_principal(x)]],
            elevation=1
        )
        layout.add_widget(self.toolbar)

        # ==============================
        # SECCIÓN: FILTROS
        # ==============================
        filtros_card = MDCard(
            orientation='vertical',
            padding=dp(16),
            spacing=dp(12),
            radius=[12, 12, 12, 12],
            elevation=1,
            md_bg_color=(0.97, 0.98, 0.99, 1),
            size_hint_x=0.96,
            pos_hint={'center_x': 0.5}
        )

        filtros_card.add_widget(MDLabel(
            text="Filtrar reportes",
            font_style="Subtitle1",
            halign="left",
            theme_text_color="Primary"
        ))

        # Campos de filtro (vertical)
        filtros_inputs = MDBoxLayout(
            orientation='vertical',
            spacing=dp(10),
            size_hint_y=None,
            adaptive_height=True
        )
        self.filter_tipo = MDTextField(
            hint_text='Tipo de peligro',
            mode='rectangle',
            size_hint_x=1
        )
        self.filter_fecha = MDTextField(
            hint_text='Fecha (YYYY-MM-DD)',
            mode='rectangle',
            size_hint_x=1
        )
        filtros_inputs.add_widget(self.filter_tipo)
        filtros_inputs.add_widget(self.filter_fecha)
        filtros_card.add_widget(filtros_inputs)

        # ==============================
        # SECCIÓN: BOTONES PEQUEÑOS Y CENTRADOS
        # ==============================
        botones_row = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(10),
            size_hint_y=None,
            height=dp(36),
            adaptive_width=True,
            pos_hint={'center_x': 0.5}
        )

        btn_width = dp(90)
        btn_height = dp(32)

        btn_filtrar = MDRectangleFlatIconButton(
            text='Filtrar',
            icon='filter',
            size_hint=(None, None),
            size=(btn_width, btn_height),
            md_bg_color=(0.18, 0.6, 0.18, 1),
            text_color=(1, 1, 1, 1),
            icon_color=(1, 1, 1, 1),
            on_release=self.aplicar_filtro
        )

        btn_export = MDRectangleFlatIconButton(
            text='Exportar',
            icon='file-export',
            size_hint=(None, None),
            size=(btn_width, btn_height),
            md_bg_color=(0.1, 0.5, 0.8, 1),
            text_color=(1, 1, 1, 1),
            icon_color=(1, 1, 1, 1),
            on_release=self.exportar_csv
        )

        btn_borrar = MDRectangleFlatIconButton(
            text='Borrar',
            icon='delete',
            size_hint=(None, None),
            size=(btn_width, btn_height),
            md_bg_color=(0.8, 0.2, 0.2, 1),
            text_color=(1, 1, 1, 1),
            icon_color=(1, 1, 1, 1),
            on_release=self.confirmar_borrar_todos
        )

        botones_row.add_widget(btn_filtrar)
        botones_row.add_widget(btn_export)
        botones_row.add_widget(btn_borrar)

        # Contenedor centrado
        botones_container = MDBoxLayout(
            orientation='horizontal',
            adaptive_height=True,
            adaptive_width=True,
            pos_hint={'center_x': 0.5}
        )
        botones_container.add_widget(botones_row)

        filtros_card.add_widget(botones_container)
        layout.add_widget(filtros_card)

        # ==============================
        # SECCIÓN: LISTA DE REPORTES
        # ==============================
        lista_card = MDCard(
            orientation='vertical',
            padding=dp(14),
            radius=[12, 12, 12, 12],
            elevation=1,
            md_bg_color=(1, 1, 1, 1),
            size_hint_x=0.96,
            pos_hint={'center_x': 0.5}
        )

        lista_card.add_widget(MDLabel(
            text="Reportes registrados",
            font_style="Subtitle1",
            halign="left",
            theme_text_color="Primary"
        ))

        self.scroll = MDScrollView()
        self.md_list = MDList()
        self.scroll.add_widget(self.md_list)
        lista_card.add_widget(self.scroll)
        layout.add_widget(lista_card)

        self.add_widget(layout)
        self.load_reportes()

    # ==============================
    # FUNCIONES DE GESTIÓN
    # ==============================
    def volver_principal(self, instance):
        if self.manager:
            self.manager.current = 'principal'

    def load_reportes(self):
        app_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        file_path = os.path.join(app_root, 'reportes_peligro.json')
        self.md_list.clear_widgets()

        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                tipo_filtro = self.filter_tipo.text.strip().lower()
                fecha_filtro = self.filter_fecha.text.strip()

                if not data:
                    self.md_list.add_widget(OneLineListItem(text='No hay reportes guardados'))
                    return

                for rpt in data:
                    if tipo_filtro and tipo_filtro not in rpt.get('tipo', '').lower():
                        continue
                    if fecha_filtro and fecha_filtro not in rpt.get('fecha', ''):
                        continue

                    fecha = rpt.get('fecha', '')
                    calle = rpt.get('calle', '---')
                    tipo = rpt.get('tipo', '---')
                    texto = f"{calle} — {tipo} ({fecha.split('T')[0] if fecha else ''})"

                    item = OneLineListItem(
                        text=texto,
                        on_release=lambda x, r=rpt: self.mostrar_detalle(r)
                    )
                    self.md_list.add_widget(item)
            except Exception:
                self.md_list.add_widget(OneLineListItem(text='Error al cargar los reportes'))
        else:
            self.md_list.add_widget(OneLineListItem(text='No hay reportes guardados'))

    def mostrar_detalle(self, reporte):
        from kivymd.uix.dialog import MDDialog
        from kivymd.uix.button import MDFlatButton, MDRaisedButton
        texto = (
            f"Calle: {reporte.get('calle')}\n"
            f"Tipo: {reporte.get('tipo')}\n"
            f"Descripción: {reporte.get('descripcion')}\n"
            f"Fecha: {reporte.get('fecha')}"
        )

        def _close(obj):
            dialog.dismiss()

        def _elim(obj):
            dialog.dismiss()
            self.eliminar_reporte(reporte)

        dialog = MDDialog(
            title='Detalle del reporte',
            text=texto,
            buttons=[
                MDFlatButton(text='Cerrar', on_release=_close),
                MDRaisedButton(text='Eliminar', on_release=_elim)
            ]
        )
        dialog.open()

    def eliminar_reporte(self, reporte):
        app_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        file_path = os.path.join(app_root, 'reportes_peligro.json')
        if not os.path.exists(file_path):
            show_snackbar('No hay archivo de reportes')
            return
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            nueva = [r for r in data if r.get('fecha') != reporte.get('fecha')]
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(nueva, f, indent=2, ensure_ascii=False)
            show_snackbar('Reporte eliminado')
            self.load_reportes()
        except Exception as e:
            show_snackbar(f'Error eliminando reporte: {e}')

    def aplicar_filtro(self, instance):
        self.load_reportes()

    def exportar_csv(self, instance):
        app_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        file_path = os.path.join(app_root, 'reportes_peligro.json')
        csv_path = os.path.join(app_root, 'reportes_peligro.csv')
        if not os.path.exists(file_path):
            show_snackbar('No hay reportes para exportar')
            return
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['calle', 'tipo', 'descripcion', 'fecha'])
                for r in data:
                    writer.writerow([r.get('calle'), r.get('tipo'), r.get('descripcion'), r.get('fecha')])
            show_snackbar(f'Exportado a {csv_path}')
        except Exception as e:
            show_snackbar(f'Error exportando CSV: {e}')

    def confirmar_borrar_todos(self, instance):
        from kivymd.uix.dialog import MDDialog
        from kivymd.uix.button import MDFlatButton, MDRaisedButton

        def _cancel(obj):
            dlg.dismiss()

        def _confirm(obj):
            dlg.dismiss()
            self.borrar_todos()

        dlg = MDDialog(
            title='Confirmar acción',
            text='¿Deseas borrar todos los reportes?',
            buttons=[
                MDFlatButton(text='Cancelar', on_release=_cancel),
                MDRaisedButton(text='Borrar', on_release=_confirm)
            ]
        )
        dlg.open()

    def borrar_todos(self):
        app_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        file_path = os.path.join(app_root, 'reportes_peligro.json')
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump([], f, indent=2, ensure_ascii=False)
            show_snackbar('Todos los reportes han sido borrados')
            self.load_reportes()
        except Exception as e:
            show_snackbar(f'Error borrando reportes: {e}')





