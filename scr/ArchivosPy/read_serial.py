import sys
import serial
import sqlite3
import math
from datetime import date

import numpy as np
from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QTabWidget, QMessageBox,
    QLabel, QSpacerItem, QSizePolicy, QTableWidget, QTableWidgetItem, QPushButton,
    QHeaderView
)
import pyqtgraph as pg

# Importar funciones externas
import Funciones
from Funciones import guardar_medidas, guardar_usuario, obtener_usuarios, obtener_todos_incidentes

# CONFIGURACIÓN
PUERTO = "COM17"
BAUDRATE = 115200
MAX_POINTS = 200
INCIDENTS_LIMIT = 200  # máximo filas a mostrar en tabla de incidentes

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Medidas del Sensor")
        self.resize(1200, 700)

        self.peligro_mostrado = False

        # Conectar UART
        try:
            self.arduino = serial.Serial(PUERTO, BAUDRATE, timeout=0.1)
        except Exception as e:
            print("ERROR: No se pudo conectar al dispositivo:", e)
            sys.exit()

        # Layout principal
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)

        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)

        # ------------------------------
        # Pestaña 1: Tiempo real
        # ------------------------------
        self.tab_realtime = QWidget()
        self.tabs.addTab(self.tab_realtime, "Tiempo Real")
        layout_tab = QHBoxLayout()
        self.tab_realtime.setLayout(layout_tab)

        layout_izq = QVBoxLayout()
        layout_tab.addLayout(layout_izq, stretch=3)

        self.combo_dias = QComboBox()
        self.combo_dias.addItem("Seleccionar día")
        self.combo_dias.addItems(self.obtener_dias_bd_excluyendo_hoy())
        self.combo_dias.currentTextChanged.connect(self.cambiar_dia_reporte)
        layout_izq.addWidget(self.combo_dias)

        self.graph = pg.PlotWidget(title="Medidas del Sensor en Tiempo Real")
        self.graph.setBackground("w")
        self.graph.showGrid(x=True, y=True)
        self.graph.addLegend()
        layout_izq.addWidget(self.graph, stretch=1)

        self.time = []
        self.data_x = []
        self.data_y = []
        self.data_z = []
        self.t = 0

        self.line_x = self.graph.plot([], [], name="X", pen=pg.mkPen('r', width=2))
        self.line_y = self.graph.plot([], [], name="Y", pen=pg.mkPen('g', width=2))
        self.line_z = self.graph.plot([], [], name="Z", pen=pg.mkPen('b', width=2))

        layout_der = QVBoxLayout()
        layout_tab.addLayout(layout_der, stretch=1)

        self.mag_label = QLabel("Magnitud:\n0.00")
        self.mag_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.mag_label.setFixedSize(180, 80)
        self.mag_label.setStyleSheet("""
            QLabel {
                background-color: #ffffff;
                border: 2px solid #8c8c8c;
                border-radius: 8px;
                font-size: 18px;
                font-weight: bold;
                color: #000000;
            }
        """)
        layout_der.addWidget(self.mag_label, alignment=QtCore.Qt.AlignmentFlag.AlignTop)
        layout_der.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        # ------------------------------
        # Pestaña 2: Reporte por día
        # ------------------------------
        self.tab_reporte = QWidget()
        self.tabs.addTab(self.tab_reporte, "Reporte del Día")
        self.reporte_layout = QVBoxLayout()
        self.tab_reporte.setLayout(self.reporte_layout)

        self.graph_reporte = pg.PlotWidget(title="Reporte del Día")
        self.graph_reporte.setBackground("w")
        self.graph_reporte.addLegend()
        self.reporte_layout.addWidget(self.graph_reporte)

        self.plot_x_reporte = self.graph_reporte.plot(pen=pg.mkPen('r', width=2), name="X")
        self.plot_y_reporte = self.graph_reporte.plot(pen=pg.mkPen('g', width=2), name="Y")
        self.plot_z_reporte = self.graph_reporte.plot(pen=pg.mkPen('b', width=2), name="Z")

        # ------------------------------
        # Pestaña 3: Usuarios
        # ------------------------------
        self.tab_usuarios = QWidget()
        self.tabs.addTab(self.tab_usuarios, "Usuarios")
        usuarios_layout = QVBoxLayout()
        self.tab_usuarios.setLayout(usuarios_layout)

        refresh_btn = QPushButton("Refrescar lista de usuarios")
        refresh_btn.clicked.connect(self.refresh_users_table)
        usuarios_layout.addWidget(refresh_btn, alignment=QtCore.Qt.AlignmentFlag.AlignLeft)

        self.table_users = QTableWidget()
        self.table_users.setColumnCount(3)
        self.table_users.setHorizontalHeaderLabels(["ID", "User", "Password (SHA256)"])
        self.table_users.horizontalHeader().setStretchLastSection(True)
        self.table_users.verticalHeader().setVisible(False)
        usuarios_layout.addWidget(self.table_users)
        self.refresh_users_table()

        # ------------------------------
        # Pestaña 4: Incidentes
        # ------------------------------
        self.tab_incidentes = QWidget()
        self.tabs.addTab(self.tab_incidentes, "Incidentes")
        inc_layout = QVBoxLayout()
        self.tab_incidentes.setLayout(inc_layout)

        refresh_inc_btn = QPushButton("Refrescar incidentes")
        refresh_inc_btn.clicked.connect(self.refresh_incidents_table)
        inc_layout.addWidget(refresh_inc_btn, alignment=QtCore.Qt.AlignmentFlag.AlignLeft)

        self.table_incidents = QTableWidget()
        self.table_incidents.setColumnCount(5)
        self.table_incidents.setHorizontalHeaderLabels(["Timestamp", "X", "Y", "Z", "Danger"])
        self.table_incidents.horizontalHeader().setStretchLastSection(False)
        self.table_incidents.setMinimumHeight(200)
        self.table_incidents.verticalHeader().setVisible(False)
        header = self.table_incidents.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        inc_layout.addWidget(self.table_incidents)
        self.refresh_incidents_table()

        # Timer UART
        self.timer = QtCore.QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()

    # =======================================
    # LECTURA UART Y ACTUALIZACIÓN
    # =======================================
    def update_plot(self):
        if self.arduino.in_waiting > 0:
            raw = self.arduino.readline().decode("utf-8", errors="ignore").strip()
            if not raw:
                return

            partes = raw.split(",")
            codigo = partes[0]

            # ---------------------------
            # Código 2 → Guardar usuario
            # ---------------------------
            if codigo == "2" and len(partes) == 3:
                ok = guardar_usuario(raw)
                msg = QMessageBox()
                msg.setWindowTitle("Usuario Guardado")
                msg.setIcon(QMessageBox.Icon.Information)
                msg.setText(f"El usuario '{partes[1]}' fue guardado correctamente.")
                msg.exec()
                self.refresh_users_table()
                return

            # ---------------------------
            # Código 3 → LOGIN
            # ---------------------------
            if codigo == "3" and len(partes) == 3:
                ok = Funciones.comprobar_login(raw)
                self.arduino.write(b"T\n" if ok else b"F\n")
                msg = QMessageBox()
                msg.setWindowTitle("Inicio de Sesión")
                if ok:
                    msg.setIcon(QMessageBox.Icon.Information)
                    msg.setText(f"Inicio de sesión exitoso para el usuario '{partes[1]}'")
                else:
                    msg.setIcon(QMessageBox.Icon.Warning)
                    msg.setText("Usuario o contraseña incorrectos")
                msg.exec()
                return

            # ---------------------------
            # Código 1 → Medidas
            # ---------------------------
            if codigo == "1" and len(partes) == 4:
                try:
                    x, y, z = map(float, partes[1:4])
                except ValueError:
                    return

                magnitud = math.sqrt(x**2 + y**2 + z**2)

                # ----------------------------------------------------
                # Determinar danger según rangos exactos del C
                # ----------------------------------------------------
                danger = 0
                if x < -4000 or (-10 < x < 10) or x > 4000:
                    danger = 1
                if y < -4000 or (-10 < y < 10) or y > 4000:
                    danger = 1
                if z < -4000 or (-10 < z < 10) or z > 4000:
                    danger = 1

                # Guardar en BD (sin usar LIMITE para danger)
                conn = sqlite3.connect("data.db")
                guardar_medidas(0, raw, conn)  # el 0 solo por compatibilidad
                conn.close()

                # ALERTA DANGER
                if danger == 1:
                    self.arduino.write(b"4\n")
                    self.arduino.write(b"11\n")
                    if not self.peligro_mostrado:
                        self.peligro_mostrado = True
                        msg = QMessageBox()
                        msg.setWindowTitle("PELIGRO DE MEDICIÓN")
                        msg.setIcon(QMessageBox.Icon.Critical)
                        msg.setText("⚠️ Se detectó una medición peligrosa.\nRevisa el sensor.")
                        msg.exec()
                else:
                    self.peligro_mostrado = False

                self.actualizar_recuadro_magnitud(magnitud, danger)

                if danger == 1:
                    self.refresh_incidents_table()

                self.data_x.append(x)
                self.data_y.append(y)
                self.data_z.append(z)
                self.time.append(self.t)
                self.t += 1

                if len(self.data_x) > MAX_POINTS:
                    self.data_x.pop(0)
                    self.data_y.pop(0)
                    self.data_z.pop(0)
                    self.time.pop(0)

                self.line_x.setData(self.time, self.data_x)
                self.line_y.setData(self.time, self.data_y)
                self.line_z.setData(self.time, self.data_z)
                return
        
        # Obtener último incidente
        
            # ---------------------------
            # Código 5 → Cambiar contraseña
            # ---------------------------
            if codigo == "5" and len(partes) == 3:
                ok = Funciones.cambiar_contraseña(raw)
                msg = QMessageBox()
                msg.setWindowTitle("Cambio de Contraseña")
                if ok:
                    self.arduino.write(b"T\n")
                    msg.setIcon(QMessageBox.Icon.Information)
                    msg.setText(f"Contraseña de '{partes[1]}' actualizada correctamente.")
                    self.refresh_users_table()
                else:
                    self.arduino.write(b"F\n")
                    msg.setIcon(QMessageBox.Icon.Warning)
                    msg.setText(f"No se pudo actualizar la contraseña de '{partes[1]}'.")
                msg.exec()
                return

            # ---------------------------
            # Código 8 → Consultar usuario en sesión
            # ---------------------------
            if codigo == "8":
                user = Funciones.obtener_usuario_sesion()
                respuesta = (user + "\n") if user else "\n"
                self.arduino.write(respuesta.encode('utf-8'))
                msg = QMessageBox()
                msg.setWindowTitle("Usuario en sesión")
                msg.setIcon(QMessageBox.Icon.Information)
                msg.setText(f"El usuario es: {user if user else 'N/A'}")
                msg.exec()
                return
            if codigo == "10":
    # Obtener último incidente
                incidentes = obtener_todos_incidentes(limit=1)  # Solo el más reciente
                if incidentes:
                    ultimo = incidentes[0]
                    timestamp, x, y, z, danger = ultimo
                    # Formatear cadena para enviar por UART
                    # Por ejemplo: "2025-12-11 10:05:00,X=123.45,Y=67.89,Z=0.12"
                    mensaje = f"{timestamp},X={x:.2f},Y={y:.2f},Z={z:.2f}\n"
                    self.arduino.write(mensaje.encode('utf-8'))
                    print("Enviado último incidente:", mensaje.strip())
                else:
                    self.arduino.write(b"No hay incidentes\n")
                    print("No hay incidentes para enviar.")
                return

    # =======================================
    # Actualizar recuadro de magnitud
    # =======================================
    def actualizar_recuadro_magnitud(self, magnitud, danger):
        self.mag_label.setText(f"Magnitud:\n{magnitud:.2f}")
        if danger == 1:
            self.mag_label.setStyleSheet("""
                QLabel {
                    background-color: #ffe6e6;
                    border: 2px solid #d9534f;
                    border-radius: 8px;
                    font-size: 18px;
                    font-weight: bold;
                    color: #8b0000;
                }
            """)
        else:
            self.mag_label.setStyleSheet("""
                QLabel {
                    background-color: #ffffff;
                    border: 2px solid #8c8c8c;
                    border-radius: 8px;
                    font-size: 18px;
                    font-weight: bold;
                    color: #000000;
                }
            """)

    # =======================================
    # Días almacenados en BD (excluir hoy)
    # =======================================
    def obtener_dias_bd_excluyendo_hoy(self):
        try:
            conn = sqlite3.connect("data.db")
            cursor = conn.cursor()
            cursor.execute("""
                SELECT DISTINCT DATE(timestamp)
                FROM medidas
                WHERE DATE(timestamp) < DATE('now','localtime')
                ORDER BY DATE(timestamp) DESC
            """)
            dias = [row[0] for row in cursor.fetchall() if row[0] is not None]
        except Exception:
            dias = []
        finally:
            conn.close()
        return dias

    def cambiar_dia_reporte(self, dia):
        if dia != "Seleccionar día":
            self.actualizar_reporte(dia)

    # =======================================
    # Reporte del día
    # =======================================
    def actualizar_reporte(self, dia):
        x_data = Funciones.obtener_dia_x(dia)
        y_data = Funciones.obtener_dia_y(dia)
        z_data = Funciones.obtener_dia_z(dia)
        time_axis = [i * 5 for i in range(len(x_data))]

        self.plot_x_reporte.setData(time_axis, x_data)
        self.plot_y_reporte.setData(time_axis, y_data)
        self.plot_z_reporte.setData(time_axis, z_data)
        self.graph_reporte.setTitle(f"Reporte del Día: {dia}")

    # =======================================
    # TAB USUARIOS
    # =======================================
    def refresh_users_table(self):
        rows = obtener_usuarios()
        self.table_users.setRowCount(0)
        for row in rows:
            r_idx = self.table_users.rowCount()
            self.table_users.insertRow(r_idx)
            for c_idx, val in enumerate(row):
                item = QTableWidgetItem(str(val))
                item.setFlags(item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
                self.table_users.setItem(r_idx, c_idx, item)

    # =======================================
    # TAB INCIDENTES
    # =======================================
    def refresh_incidents_table(self, limit=INCIDENTS_LIMIT):
        rows = obtener_todos_incidentes(limit=limit)
        self.table_incidents.setRowCount(0)
        for row in reversed(rows):
            r_idx = self.table_incidents.rowCount()
            self.table_incidents.insertRow(r_idx)
            for c_idx, val in enumerate(row):
                item = QTableWidgetItem(str(val) if not isinstance(val, float) else f"{val:.3f}")
                item.setFlags(item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
                self.table_incidents.setItem(r_idx, c_idx, item)


# ------------------------------
# INICIAR APP
# ------------------------------
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
