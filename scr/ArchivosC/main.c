#include "xgpio.h"
#include "xparameters.h"
#include "xil_printf.h"
#include "xiicps.h"
#include "sleep.h"
#include "Funciones.h"

extern XIicPs Iic;

#define I2C_DEVICE_ID        XPAR_XIICPS_0_DEVICE_ID
#define QMC5883_ADDR         0x0D

#define GPIO_VERILOG_ID      XPAR_AXI_GPIO_2_DEVICE_ID
#define GPIO_BUZZER          XPAR_AXI_GPIO_1_DEVICE_ID
#define GPIO_MOVIMIENTO          XPAR_AXI_GPIO_3_DEVICE_ID

#define VERILOG_CHANNEL      1


// ---------------------------------------------------------------------
//   MENÚ SIN LOGIN
// ---------------------------------------------------------------------


// ---------------------------------------------------------------------
//   MENÚ PRINCIPAL
// ---------------------------------------------------------------------


// =====================================================================
//                                MAIN
// =====================================================================
int main() {
	XGpio GpioMovimiento;
    XGpio GpioVerilog;
    XGpio buzzer_verilog;

    // Inicializar buzzer
    XGpio_Initialize(&buzzer_verilog, GPIO_BUZZER);
    XGpio_SetDataDirection(&buzzer_verilog, VERILOG_CHANNEL, 0x00000000);
    XGpio_Initialize(&GpioMovimiento, GPIO_MOVIMIENTO);
    XGpio_SetDataDirection(&GpioMovimiento, 1, 0xFFFFFFFF);
    // Inicializar GPIO teclado (entrada)
    XGpio_Initialize(&GpioVerilog, GPIO_VERILOG_ID);
    XGpio_SetDataDirection(&GpioVerilog, 1, 0xFFFFFFFF);

    // I2C
    XIicPs_Config *Cfg = XIicPs_LookupConfig(I2C_DEVICE_ID);
    XIicPs_CfgInitialize(&Iic, Cfg, Cfg->BaseAddress);
    XIicPs_SetSClk(&Iic, 100000);

    // LCD
    lcd_init();
    lcd_set_brightness(300);

    QMC_init();

    int logged = 0;


    // BUCLE PRINCIPAL
    while (1)
    {
        // ------------------------------------------------------
        //                      LOGIN / REGISTRO
        // ------------------------------------------------------
        if (!logged )
        {
            int opcion = mostrar_menu(&GpioVerilog);

            if (opcion == 1)
                crear_usuario_y_contrasena(&GpioVerilog);

            else if (opcion == 2)
                logged = comprobar_usuario(&GpioVerilog);

            continue; //  volver a menú login
        }


        // ------------------------------------------------------
        //                  MENU YA LOGEADO
        // ------------------------------------------------------
        int seleccion = menu_con_login(&GpioVerilog);

        // 1) Medir sensor
        if (seleccion == 1)
        {
            lcd_clear();

            while (1)
            {
                int x, y, z;

                mostrar_lectura_magnetometro(&x, &y, &z);
                u32 t = leer_teclado(&GpioVerilog);
                u32 valor = XGpio_DiscreteRead(&GpioMovimiento, 1);
                if(valor){
                	  lcd_clear();
                	                    lcd_print("  MOVIMIENTO");
                	                    XGpio_DiscreteWrite(&buzzer_verilog, 1, 1);
                	                    usleep(2000000);
                	                    lcd_clear();
                	                	XGpio_DiscreteWrite(&buzzer_verilog, 1, 0);


                }


                // ------------------------------------------------
                // Condiciones de peligro según los rangos que indicas
                // ------------------------------------------------
                int peligro = 0;

                if (x < -4000 || (x > -10 && x < 10) || x > 4000)
                    peligro = 1;
                if (y < -4000 || (y > -10 && y < 10) || y > 4000)
                    peligro = 1;
                if (z < -4000 || (z > -10 && z < 10) || z > 4000)
                    peligro = 1;

                if (peligro)
                {
                    lcd_clear();
                    lcd_print("PELIGRO");
                    usleep(2000000);
                    lcd_clear();
                    XGpio_DiscreteWrite(&buzzer_verilog, 1, 1); // Activar buzzer
                }

                // Apagar buzzer con tecla 2
                if (t == 0x2)
                {
                    XGpio_DiscreteWrite(&buzzer_verilog, 1, 0);
                }

                // Salir del bucle con tecla A
                if (t == 0xA)
                    break;

                usleep(200000);
            }
        }


        // 2) BUZZER ON
        else if (seleccion == 2)
        {
            XGpio_DiscreteWrite(&buzzer_verilog, 1, 1);
            lcd_clear();
            lcd_print("BUZZER ON");
        	usleep(1000000);
        	XGpio_DiscreteWrite(&buzzer_verilog, 1, 0);
        }


        else if (seleccion == 3)
        {
        	solicitar_usuario();
        }

        // 4) Nuevo user
        else if (seleccion == 4)
        {
         cambiar_contrasena(&GpioVerilog);

        }

        // 5) Cerrar sesión
        else if (seleccion == 5)
        {
        	 mostrar_fecha_desde_uart();


        }
        else if (seleccion == 6)
            {

        	    lcd_clear();
        	    lcd_set_cursor(0,0);
        	    lcd_print("Sesion cerrada");
        	    usleep(1500000);  // Mostrar mensaje 1.5 segundos

        	    logged = 0;        // Reiniciar estado de login
        	    continue;
            }
    }

    return 0;
}
