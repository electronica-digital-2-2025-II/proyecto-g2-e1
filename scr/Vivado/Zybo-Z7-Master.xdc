## This file is a general .xdc for the Zybo Z7 Rev. B
## It is compatible with the Zybo Z7-20 and Zybo Z7-10
## To use it in a project:             
                                                                                                                                                                                                                                                         
##Pmod Header JC        
set_property -dict { PACKAGE_PIN V15   IOSTANDARD LVCMOS33     } [get_ports { row_0[0] }]; #IO_L10P_T1_34 Sch=jc_p[1]  
set_property PULLUP true [get_ports { row_0[0] }] 			 
set_property -dict { PACKAGE_PIN W15   IOSTANDARD LVCMOS33     } [get_ports { row_0[1] }]; #IO_L10N_T1_34 Sch=jc_n[1]
set_property PULLUP true [get_ports { row_0[1] }] 		     
set_property -dict { PACKAGE_PIN T11   IOSTANDARD LVCMOS33     } [get_ports { row_0[2] }]; #IO_L1P_T0_34 Sch=jc_p[2] 
set_property PULLUP true [get_ports { row_0[2] }]              
set_property -dict { PACKAGE_PIN T10   IOSTANDARD LVCMOS33     } [get_ports { row_0[3] }]; #IO_L1N_T0_34 Sch=jc_n[2] 
set_property PULLUP true [get_ports { row_0[3] }] 
             
set_property -dict { PACKAGE_PIN W14   IOSTANDARD LVCMOS33 } [get_ports {col_0_0[0]}]; #IO_L8P_T1_34 Sch=jc_p[3]              
set_property -dict { PACKAGE_PIN Y14   IOSTANDARD LVCMOS33 } [get_ports {col_0_0[1]}]; #IO_L8N_T1_34 Sch=jc_n[3] 
set_property -dict { PACKAGE_PIN T12   IOSTANDARD LVCMOS33 } [get_ports {col_0_0[2]}]; 
set_property -dict { PACKAGE_PIN U12   IOSTANDARD LVCMOS33 } [get_ports {col_0_0[3]}]; 

##Pmod Header JD                                                                                                                  

set_property -dict { PACKAGE_PIN T14   IOSTANDARD LVCMOS33 } [get_ports {GPIO_1_tri_i[0]}];
set_property -dict { PACKAGE_PIN U14   IOSTANDARD LVCMOS33 } [get_ports {IIC_0_0_scl_io}]; 
set_property PULLUP true [get_ports {IIC_0_0_scl_io}]
set_property -dict { PACKAGE_PIN U15   IOSTANDARD LVCMOS33 } [get_ports {IIC_0_0_sda_io}]; 
set_property PULLUP true [get_ports {IIC_0_0_sda_io}] 
set_property -dict { PACKAGE_PIN V18   IOSTANDARD LVCMOS33     } [get_ports {GPIO_0_tri_o[0]}]; #IO_L2P_T0_34 Sch=jc_p[4]  