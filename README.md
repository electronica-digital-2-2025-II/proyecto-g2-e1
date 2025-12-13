[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/eiNgq3fR)
[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-2e0aaae1b6195c2367325f4f02e2d04e9abb55f0b24a779b69b11b9e10269abc.svg)](https://classroom.github.com/online_ide?assignment_repo_id=22047085&assignment_repo_type=AssignmentRepo)
# Sistema de seguridad para la detección y monitoreo de campos magnéticos 

En este repositorio se presenta el desarrollo completo de un sistema de seguridad para la detección y monitoreo de campos magnéticos, implementado sobre un *System on Chip* (SoC) en la FPGA [**Zybo Z7**](https://digilent.com/reference/programmable-logic/zybo-z7/reference-manual), basada en la arquitectura **Zynq-7000**. El proyecto abarca desde el diseño del SoC en **Vivado 2023-1**, mediante el uso de *Block Design*, hasta la programación del procesador ARM en **Vitis 2023-1** y la integración con una aplicación de supervisión desarrollada en Python.

El sistema integra diversos periféricos como un magnetómetro triaxial para la medición del campo magnético, un sensor de movimiento PIR, un teclado matricial, una pantalla LCD y un buzzer de alarma, los cuales se comunican con el procesador a través de interfaces **AXI-GPIO** e **I2C**. A partir de las mediciones obtenidas, el sistema calcula la magnitud del campo magnético, detecta condiciones de riesgo cuando se superan umbrales definidos y activa mecanismos de alerta tanto a nivel local como a nivel de software.

Adicionalmente, el proyecto incluye una aplicación en PC que permite la visualización en tiempo real de las componentes \(X\), \(Y\) y \(Z\) del campo magnético, el registro histórico de mediciones e incidentes organizados por fecha, y la gestión de usuarios mediante una base de datos con contraseñas cifradas. De esta manera, el proyecto demuestra la integración completa entre hardware reconfigurable, software y aplicaciones de alto nivel, aplicando conceptos fundamentales comunicación hardware–software y monitoreo de variables físicas en tiempo real.


# Integrantes

- Daniel Sepúlveda Suárez

- Juan Felipe Gaitán Nocua

- Samuel Mahecha Arango

Indice:

1. [Descripción](#descripción)
2. [Informe](#informe)
3. [Implementación](#implementacion)
4. [Lista de anexos](#anexos)

## Descripción

<!-- Descripción general y lo mas completa posible del proyecto" -->

## Informe

<!-- Link que permita acceder al Informe, el cual debe estar subido a este repositorio -->

## Implementación

<!-- Video explicativo del funcionamiento del proytecto -->


<!-- CREAR UN DIRECTORIO CON EL NOMBRE "src" DONDE INVLUYAN LAS FUENTE (.c Y .h) QUE CREARON PARA EL PROOYECTO-->

<!-- NO OLVIDAD SUBIR EL PDF GENERADOR EN DEL BLOCK DESIGN-->
