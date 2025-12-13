  [![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/eiNgq3fR)
[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-2e0aaae1b6195c2367325f4f02e2d04e9abb55f0b24a779b69b11b9e10269abc.svg)](https://classroom.github.com/online_ide?assignment_repo_id=22047085&assignment_repo_type=AssignmentRepo)
# Sistema de seguridad para la detección y monitoreo de campos magnéticos 

En este repositorio se presenta el desarrollo completo de un sistema de seguridad para la detección y monitoreo de campos magnéticos, implementado sobre un *System on Chip* (SoC) en la FPGA [**Zybo Z7**](https://digilent.com/reference/programmable-logic/zybo-z7/reference-manual), basada en la arquitectura **Zynq-7000**. El proyecto abarca desde el diseño del SoC en **Vivado 2023-1**, mediante el uso de *Block Design*, hasta la programación del procesador ARM en **Vitis 2023-1** y la integración con una aplicación de supervisión desarrollada en Python.

El sistema integra diversos periféricos como un magnetómetro triaxial para la medición del campo magnético, un sensor de movimiento PIR, un teclado matricial, una pantalla LCD y un buzzer de alarma, los cuales se comunican con el procesador a través de interfaces **AXI-GPIO** e **I2C**. A partir de las mediciones obtenidas, el sistema calcula la magnitud del campo magnético, detecta condiciones de riesgo cuando se superan umbrales definidos y activa mecanismos de alerta tanto a nivel local como a nivel de software.

Adicionalmente, el proyecto incluye una aplicación en PC que permite la visualización en tiempo real de las componentes X, Y y Z del campo magnético, el registro histórico de mediciones e incidentes organizados por fecha, y la gestión de usuarios mediante una base de datos con contraseñas cifradas. De esta manera, el proyecto demuestra la integración completa entre hardware reconfigurable, software y aplicaciones de alto nivel, aplicando conceptos fundamentales comunicación hardware–software y monitoreo de variables físicas en tiempo real.


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

El proyecto surge ante la necesidad de contar con herramientas accesibles que permitan supervisar y controlar la exposición a campos magnéticos en entornos donde estos pueden alcanzar niveles elevados, como instalaciones industriales, zonas con equipos eléctricos de alta potencia o espacios de trabajo con riesgo potencial para las personas. La ausencia de sistemas de monitoreo continuo y de fácil integración motiva el desarrollo de una solución que combine medición en tiempo real, detección de riesgo y registro histórico de eventos.

El sistema desarrollado permite adquirir las componentes del campo magnético en los ejes X, Y y Z, procesar esta información para calcular la magnitud del campo y evaluar automáticamente si los valores medidos se encuentran dentro de rangos seguros. Cuando se detectan niveles considerados peligrosos, el sistema activa mecanismos de alerta visuales y sonoros, proporcionando una respuesta inmediata ante situaciones de riesgo.

La interacción con el usuario se realiza tanto de manera local como remota. A nivel local, el sistema cuenta con una pantalla LCD, un teclado matricial y un buzzer que facilitan la visualización de datos, la navegación por menús y la notificación de alarmas. A nivel remoto, una aplicación desarrollada en Python permite visualizar en tiempo real la evolución del campo magnético mediante gráficas, consultar la magnitud instantánea del campo y acceder a un registro histórico de mediciones organizadas por fecha.

Adicionalmente, el sistema incorpora un módulo de gestión de usuarios, donde se almacenan credenciales de acceso de forma segura mediante contraseñas cifradas, así como un registro detallado de incidentes asociados a exposiciones peligrosas al campo magnético. Esta información queda almacenada en una base de datos, lo que permite realizar análisis posteriores y evidenciar el comportamiento del entorno monitoreado a lo largo del tiempo.

En conjunto, el proyecto propone una solución integral de monitoreo, análisis y registro de campos magnéticos, orientada a mejorar la seguridad y la toma de decisiones en entornos con posibles riesgos asociados a la exposición prolongada a este tipo de campos.



## Informe

El [informe Final del Proyecto](InformeFinal.pdf) documenta de manera detallada todo el proceso de desarrollo del proyecto, abarcando desde la definición del problema y la justificación de la solución propuesta, hasta el diseño e implementación completa del sistema. En este documento se explica con profundidad la arquitectura hardware y software del sistema, incluyendo el diseño del *System on Chip*, la configuración de los periféricos y la interacción entre la lógica programable y el procesador.

Adicionalmente, el informe presenta un análisis detallado del software desarrollado en lenguaje *C*, describiendo el funcionamiento de cada uno de los archivos *.c* y *.h*, sus funciones principales, la comunicación con los periféricos, la gestión de usuarios, el manejo de eventos de riesgo y el flujo general del programa. También se incluye la descripción del software de supervisión en PC, el registro histórico de datos, los resultados obtenidos durante las pruebas, las conclusiones del proyecto y las referencias empleadas.



## Implementación

Para comprender de manera integral el funcionamiento del sistema desarrollado, se realizó un [video explicativo](https://youtu.be/mwqJV5wtScI) en el cual se presenta el comportamiento general del proyecto, la interacción entre los periféricos implementados y el flujo de operación del sistema de seguridad para el monitoreo de campos magnéticos. En este video se explica cómo se adquieren las mediciones del sensor, cómo se procesa la información para calcular la magnitud del campo magnético, la detección de condiciones de riesgo y la activación de alarmas, así como la visualización de los datos tanto en la interfaz local como en la aplicación desarrollada en PC.

Adicionalmente, se muestra la integración entre el hardware implementado en la FPGA, el software desarrollado en lenguaje C y la aplicación de supervisión en Python, permitiendo evidenciar el funcionamiento completo del sistema en tiempo real. Para acceder a la explicación detallada del funcionamiento del proyecto, haga clic en el siguiente enlace en la miniatura del video:

<p align="center">
  <a href="https://youtu.be/mwqJV5wtScI" target="_blank">
    <img src="https://img.youtube.com/vi/mwqJV5wtScI/0.jpg" alt="Video explicativo del sistema de monitoreo de campos magnéticos" style="width:480px; border: 2px solid #ccc; border-radius: 8px;">
  </a>
</p>

El [diseño de bloques del proyecto](ProcesadorProyectoFINAL.pdf) se realizó con el objetivo de integrar los diferentes periféricos de entrada y salida con el sistema de procesamiento de manera organizada y eficiente, permitiendo una correcta interacción entre el hardware y el software.

El sistema está basado en un Processing System (PS), desde el cual se ejecuta el programa desarrollado en Vitis. Este bloque se encarga de la lógica principal del sistema, como la lectura de sensores, la gestión del usuario, el control de alarmas y la toma de decisiones frente a condiciones de riesgo.

<p align="center">
<img width="1133" height="761" alt="ProcesadorProyectoFINAL" src="https://github.com/user-attachments/assets/845b8a8d-f59e-4128-98ef-8c523eb2c240" />
</p> 

La comunicación entre el procesador y los periféricos se realiza a través de un bus AXI, utilizando un AXI Interconnect que conecta distintos bloques AXI GPIO. Estos módulos permiten:

- Leer las entradas del teclado matricial.
- Recibir la señal del sensor de movimiento PIR.
- Controlar dispositivos de salida como el buzzer de alerta.

Adicionalmente, se implementó un módulo personalizado en Verilog para la decodificación del teclado matricial, el cual se ejecuta en la lógica programable (PL) y entrega la información ya procesada al procesador, facilitando su uso desde el software.

El diseño también incluye bloques de memoria BRAM, utilizados para el manejo interno de datos y variables de control, así como módulos de reset y sincronización necesarios para el correcto funcionamiento del sistema.
Las conexiones físicas hacia los sensores y actuadores se definieron mediante el archivo de restricciones (XDC), asegurando una correcta asignación de pines en la Zybo Z7.

## Lista de anexos

En la [carpeta scr](scr/) se incluyen los **archivos fuente del proyecto**, correspondientes tanto al desarrollo del sistema embebido como a la aplicación de visualización.  La carpeta contiene los programas escritos en **lenguaje C (.c y .h)** utilizados en el entorno **Vitis** para el control del sistema, así como los **archivos en Python (.py)** empleados en la aplicación de monitoreo y análisis.  Además se incluyen archivos de utilizad como el propio wrapper generado por Vivado e incluso el archivo .Xdc utilizado por el grupo para el uso de los pines físicos de la FPGA.

El funcionamiento y la lógica de estos archivos se encuentran **debidamente explicados y documentados en el [informe del Proyecto](InformeFinal.pdf)**.

<!-- CREAR UN DIRECTORIO CON EL NOMBRE "src" DONDE INVLUYAN LAS FUENTE (.c Y .h) QUE CREARON PARA EL PROOYECTO-->

<!-- NO OLVIDAD SUBIR EL PDF GENERADOR EN DEL BLOCK DESIGN-->
