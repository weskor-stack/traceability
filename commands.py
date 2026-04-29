__author__ = "Edgar Bonilla Rivas"
__copyright__ = "Copyright (C) 2025 Author Name"
__license__ = "AUTOMATYCO"
__version__ = "v2.0.0"

# maria DB
import conexion


pressfit = "commit,Pressfit,F,50,10,100,Numeric,N,PASSED,Comentarios,dwell_time,D,500,498,502,Numeric,mm,PASSED,Comentarios,dwell_time,S,100,95,110,Numeric,mm/s,PASSED,Comentarios,dwell_time,P2173404-00-C:SEYU26061A0764,1/"
screwing = "commit,Screwing,T,1.25,1,1.8,Numeric,N,PASSED,Comentario,A,31250,2900,3500,Numeric,degrees,FAILED,Comentario,PX,50,47,55,Numeric,mm,PASSED,Comentario,PY,150,140,160,Numeric,mm,PASSED,Comentario,4,P2173404-00-C:SEYU26061A0765,1/"
inspection_vs = "commit,Inspection,VS,M,8000,7500,8500,Numeric,N,PASSED,Comentarios,PX,500,475,525,Numeric,mm,PASSED,Comentarios,PY,500,475,525,Numeric,mm,PASSED,Comentarios,P2173404-00-C:SEYU26061A0766,1/"
inspection_xt = "commit,Inspection,XT,PX,500,475,525,Numeric,mm,PASSED,Comentarios,PY,500,475,525,Numeric,mm,PASSED,Comentarios,CPC,400,395,405,Numeric,mm,PASSED,Comentarios,CPE,400,395,405,Numeric,mm,PASSED,Comentarios,CAD,1,1,1,Boolean,DBU,PASSED,Comentarios,P2173404-00-C:SEYU26061A0765,1/"
electrical = "commit,Electrical,Ct,1.25,1,1.8,Numeric,N,OK,Comentario,V,31250,2900,3500,Numeric,degrees,FAILED,Comentario,Cr,50,47,55,Numeric,mm,PASSED,Comentario,R,150,140,160,Numeric,mm,PASSED,Comentario,P2173404-00-C:SEYU26061A0765,1/"

continuity_ok = 'commit,Continuity,Continuity1,10,50,F,PASS,20,Ejemplo de error del defecto,P2173404-00-C:SEYU26061A0765,1/'

continuity_fail = 'commit,Continuity,Continuity1,10,50,F,FAIL,5,Ejemplo de error del defecto,1/'

leak1 = "commit,Leak,tiempo_prueba,resultado,PASSED/FAILED,unit,descripcion,extra1,extra2,1/"
leak2 = "commit,Leak,Numeric,14.25,PASSED,psi,DESCRIPCION,1.0,1.0,Leak,P2173404-00-C:SEYU26061A0765,1/"
temperatura = "commit,Temperature,start (timestamp),salida al proceso (timestamp),temp_inicial,temp_final,unit,descripcion,extra1,extra2,P2173404-00-C:SEYU26061A0765,1/"
welding = 'commit,Welding,welding_time,welding_power,100,mm,PASSED,description,P2173404-00-C:SEYU26061A0765,1/'

heatstake = 'commit,Heatstake,heatstake,cicle_time,serial_number(P2173404-00-C:SEYU26061A0765),program_name,times_tamp,grade,description,1/'
heatstake = "commit,Heatstake,heatstake,cicle_time,P2173404-00-C:SEYU26061A0765,program_name,times_tamp,grade,description,1/"

graph_image = 'commit,Graph,graph,data_image,description,P2173404-00-C:SEYU26061A0765,1/'

cadenas = temperatura.split(',')
# print(len(cadenas))
name = "P2173404-00-C:SEYU26061A0765"

def commit(cadena, name_piece):
    options = cadena.split(',')
    data_for_table = []
    # print(cadena)
    # return options[1]
    # print(len(options))
    
    match options[1]:
        case "Pressfit":
            # station = conexion.stations()
            print(options)
            print(len(options))
            print(options[-3])
            if len(options) == 32:
                force = options[2:11]
                distance = options[11:20]
                speed = options[20:-3]
                print(force)
                print(distance)
                print(speed)
                result = ""
                result_distance = ""
                result_speed = ""
                if force[6] =='PASSED':
                    result = "PASS"
                else:
                    result = "FAIL"
                
                if distance[6] =='PASSED':
                    result_distance = "PASS"
                else:
                    result_distance = "FAIL"
                
                if speed[6] =='PASSED':
                    result_speed = "PASS"
                else:
                    result_speed = "FAIL"

                if force[0] == 'F' and distance[0] == 'D' and speed[0] == 'S':
                    force_measurement = conexion.parameters_pressfit(force,options[-3])
                    if force_measurement != 'GENERAL_ERROR' and force_measurement != 'FAILED':
                        data_for_table.append([
                            "Force",  # Measurement
                            force[1],  # Value
                            force[2],  # Lower limit
                            force[3],  # Upper limit
                            force[4],  # Type
                            force[5],  # Unit
                            result
                            # force[8]   # Result
                        ])
                    elif force_measurement == 'FAILED':
                        return "FAILED", []
                    distance_measurement = conexion.parameters_pressfit(distance,options[-3])
                    if distance_measurement != 'GENERAL_ERROR' and distance_measurement != 'FAILED':
                        data_for_table.append([
                        "Distance",  # Measurement
                            distance[1],  # Value
                            distance[2],  # Lower limit
                            distance[3],  # Upper limit
                            distance[4],  # Type
                            distance[5],  # Unit
                            result_distance
                            # distance[8]   # Result
                        ])
                    elif distance_measurement == 'FAILED':
                        return "FAILED", []
                    speed_measurement = conexion.parameters_pressfit(speed,options[-3])
                    if speed_measurement != 'GENERAL_ERROR' and speed_measurement != 'FAILED':
                        data_for_table.append([
                            "Speed",  # Measurement
                            speed[1],  # Value
                            speed[2],  # Lower limit
                            speed[3],  # Upper limit
                            speed[4],  # Type
                            speed[5],  # Unit
                            result_speed
                            # speed[8]   # Result
                        ])
                    elif speed_measurement == 'FAILED':
                        return "FAILED", []
                        
                    return "PASSED", data_for_table
                else:
                    return "FAILED", []
            else:
                return "FAILED", []
        case "Screwing":
            # print(options)
            # print(len(options))
            # print(options[-4])
            if len(options) == 38:
                torque = options[2:10]
                angle = options[10:18]
                px = options[18:26]
                py = options[26:-4]

                result_torque = ""
                result_angle = ""
                result_spx = ""
                result_spy = ""

                torque.append(options[-4])
                angle.append(options[-4])
                px.append(options[-4])
                py.append(options[-4])
                # print(torque)
                # print(angle)
                # print(px)
                # print(py)
                if torque[6] =='PASSED':
                    result_torque = "PASS"
                else:
                    result_torque = "FAIL"
                
                if angle[6] =='PASSED':
                    result_angle = "PASS"
                else:
                    result_angle = "FAIL"
                
                if px[6] =='PASSED':
                    result_spx = "PASS"
                else:
                    result_spx = "FAIL"
                
                if py[6] =='PASSED':
                    result_spy = "PASS"
                else:
                    result_spy = "FAIL"

                if torque[0] == 'T' and angle[0] == 'A' and px[0] == 'PX' and py[0] == 'PY':
                    torque_measurement = conexion.parameters_screwing(torque,options[-3])
                    if torque_measurement != 'GENERAL_ERROR' and torque_measurement != 'FAILED':
                        data_for_table.append([
                            torque[0],# "Torque",  # Measurement
                            torque[1],  # Value
                            torque[2],  # Lower limit
                            torque[3],  # Upper limit
                            torque[4],  # Type
                            torque[5],  # Unit
                            result_torque
                            # torque[8]   # Result
                        ])
                    elif torque_measurement == 'FAILED':
                        return "FAILED", []
                    angle_measurement = conexion.parameters_screwing(angle,options[-3])
                    if angle_measurement != 'GENERAL_ERROR' and angle_measurement != 'FAILED':
                        data_for_table.append([
                            angle[0],  # Measurement
                            angle[1],  # Value
                            angle[2],  # Lower limit
                            angle[3],  # Upper limit
                            angle[4],  # Type
                            angle[5],  # Unit
                            result_angle
                            # angle[8]   # Result
                        ])
                    elif angle_measurement == 'FAILED':
                        return "FAILED", []
                    px_measurement = conexion.parameters_screwing(px,options[-3])
                    if px_measurement != 'GENERAL_ERROR' and px_measurement != 'FAILED':
                        data_for_table.append([
                            px[0],  # Measurement
                            px[1],  # Value
                            px[2],  # Lower limit
                            px[3],  # Upper limit
                            px[4],  # Type
                            px[5],  # Unit
                            result_spx
                            # px[8]   # Result
                        ])
                    elif px_measurement == 'FAILED':
                        return "FAILED", []
                    py_measurement = conexion.parameters_screwing(py,options[-3])
                    if py_measurement != 'GENERAL_ERROR' and py_measurement != 'FAILED':
                        data_for_table.append([
                            py[0],  # Measurement
                            py[1],  # Value
                            py[2],  # Lower limit
                            py[3],  # Upper limit
                            py[4],  # Type
                            py[5],  # Unit
                            result_spy
                            # py[8]   # Result
                        ])
                    elif py_measurement == 'FAILED':
                        return "FAILED", []

                    return "PASSED", data_for_table
                else:
                    return "FAILED", []
            else:
                return "FAILED", []
        case "Inspection":
            # station = conexion.stations()
            result_m = ""
            result_ipx = ""
            result_ipy = ""
            result_cpc = ""
            result_cpe = ""
            result_cad = ""
            
            
            if options[2] == "VS":
                if len(options) == 30:
                    if "M" in options and "PX" in options and "PY" in options:
                        startM = options.index("M")
                        endM = options.index("M")+8
                        startPx = options.index("PX")
                        endPx = options.index("PX")+8
                        startPy = options.index("PY")
                        endPy = options.index("PY")+8
                            
                        if endM != "PX" and endM != "PY":
                            measurement = options[startM:endM]
                            # print(measurement)
                        else:
                            return "FAILED", []

                        if endPx != "M" and endPx != "PY":
                            position_x = options[startPx:endPx]
                            # print(position_x)
                        else:
                            return "FAILED",[]
                                
                        if endPy != "M" and endPy != "PX":
                            position_y = options[startPy:endPy]
                            # print(position_y)
                        else:
                            return "FAILED",[]
                        
                        if measurement[6] =='PASSED':
                            result_m = "PASS"
                        else:
                            result_m = "FAIL"
                        
                        if position_x[6] =='PASSED':
                            result_ipx = "PASS"
                        else:
                            result_ipx = "FAIL"
                        
                        if position_y[6] =='PASSED':
                            result_ipy = "PASS"
                        else:
                            result_ipy = "FAIL"


                        measurementInspection = conexion.parameters_inspection_vs(measurement,options[-3])
                        if measurementInspection != 'GENERAL_ERROR' and measurementInspection != 'FAILED':
                            data_for_table.append([
                                position_x[4],  # Measurement
                                position_x[1],  # Value
                                position_x[2],  # Lower limit
                                position_x[3],  # Upper limit
                                position_x[4],  # Type
                                position_x[5],  # Unit
                                result_ipx
                            ])
                        elif measurementInspection == 'FAILED':
                            return "FAILED", []
                        positionPx = conexion.parameters_inspection_vs(position_x,options[-3])
                        if positionPx != 'GENERAL_ERROR' and positionPx != 'FAILED':
                            data_for_table.append([
                                position_x[4],  # Measurement
                                position_x[1],  # Value
                                position_x[2],  # Lower limit
                                position_x[3],  # Upper limit
                                position_x[4],  # Type
                                position_x[5],  # Unit
                                result_ipx
                            ])
                        elif positionPx == 'FAILED':
                            return "FAILED", []
                        positionPy = conexion.parameters_inspection_vs(position_y,options[-3])
                        if positionPy != 'GENERAL_ERROR' and positionPy != 'FAILED':
                            data_for_table.append([
                                position_y[4],  # Measurement
                                position_y[1],  # Value
                                position_y[2],  # Lower limit
                                position_y[3],  # Upper limit
                                position_y[4],  # Type
                                position_y[5],  # Unit
                                result_ipy
                            ])
                        elif positionPy == 'FAILED':
                            return "FAILED", []
                        
                        return "PASSED", data_for_table

                        # if(measurementInspection == "FAILED" or positionPx == "FAILED" or positionPy == "FAILED"):
                        #     return "FAILED",[]
                        # else:
                        #     return "PASSED", data_for_table
                    else:
                        return "FAILED",[]
                else:
                    return "FAILED",[]
                # print(options[2])
            elif options[2] == "XT":
                if len(options) == 46:
                    if "PX" in options and "PY" in options and "CPC" in options and "CPE" in options and "CAD" in options:
                        # print(options[2])
                        startPx2 = options.index("PX")
                        endPx2 = options.index("PX")+8
                        startPy2 = options.index("PY")
                        endPy2 = options.index("PY")+8
                        startCPC = options.index("CPC")
                        endCPC = options.index("CPC")+8
                        startCPE = options.index("CPE")
                        endCPE = options.index("CPE")+8
                        startCAD = options.index("CAD")
                        endCAD = options.index("CAD")+8

                        if endPx2 != "CPC" and endPx2 != "PY" and endPx2 != "CPE" and endPx2 != "CAD":
                            position_x2 = options[startPx2:endPx2]
                            # print(position_x2)
                        else:
                            return "FAILED",[]
                            
                        if endPy2 != "CPC" and endPy2 != "PX" and endPy2 != "CPE" and endPy2 != "CAD":
                            position_y2 = options[startPy2:endPy2]
                            # print(position_y2)
                        else:
                            return "FAILED",[]
                            
                        if endCPC != "PX" and endCPC != "PY" and endCPC != "CPE" and endCPC != "CAD":
                            cpc = options[startCPC:endCPC]
                            # print(cpc)
                        else:
                            return "FAILED",[]
                            
                        if endCPE != "PX" and endCPE != "PY" and endCPE != "CPC" and endCPE != "CAD":
                            cpe = options[startCPE:endCPE]
                            # print(cpe)
                        else:
                            return "FAILED",[]
                            
                        if endCAD != "PX" and endCAD != "PY" and endCAD != "CPC" and endCAD != "CPE":
                            cad = options[startCAD:endCAD]
                            # print(cad)
                        else:
                            return "FAILED",[]

                        
                        if position_x2[6] =='PASSED':
                            result_ipx = "PASS"
                        else:
                            result_ipx = "FAIL"
                        
                        if position_y2[6] =='PASSED':
                            result_ipy = "PASS"
                        else:
                            result_ipy = "FAIL"
                        
                        if cpc[6] =='PASSED':
                            result_cpc = "PASS"
                        else:
                            result_cpc = "FAIL"
                        
                        if cpe[6] =='PASSED':
                            result_cpe = "PASS"
                        else:
                            result_cpe = "FAIL"

                        if cad[6] =='PASSED':
                            result_cad = "PASS"
                        else:
                            result_cad = "FAIL"


                        positionPxT = conexion.parameters_inspection_xt(position_x2,options[-3])
                        if positionPxT != 'GENERAL_ERROR' and positionPxT != 'FAILED':
                            data_for_table.append([
                                position_x2[0],  # Measurement
                                position_x2[1],  # Value
                                position_x2[2],  # Lower limit
                                position_x2[3],  # Upper limit
                                position_x2[4],  # Type
                                position_x2[5],  # Unit
                                result_ipx
                            ])
                        elif positionPxT == 'FAILED':
                            return "FAILED", []
                        positionPyT = conexion.parameters_inspection_xt(position_y2,options[-3])
                        if positionPyT != 'GENERAL_ERROR' and positionPyT != 'FAILED':
                            data_for_table.append([
                                position_y2[0],  # Measurement
                                position_y2[1],  # Value
                                position_y2[2],  # Lower limit
                                position_y2[3],  # Upper limit
                                position_y2[4],  # Type
                                position_y2[5],  # Unit
                                result_ipy
                            ])
                        elif positionPyT == 'FAILED':
                            return "FAILED", []
                        cpcT = conexion.parameters_inspection_xt(cpc,options[-3])
                        if cpcT != 'GENERAL_ERROR' and cpcT != 'FAILED':
                            data_for_table.append([
                                cpc[0],
                                cpc[1],  # Value
                                cpc[2],  # Lower limit
                                cpc[3],  # Upper limit
                                cpc[4],  # Type
                                cpc[5],  # Unit
                                result_cpc
                            ])
                        elif cpcT == 'FAILED':  
                            return "FAILED", []
                        cpeT = conexion.parameters_inspection_xt(cpe,options[-3])
                        if cpeT != 'GENERAL_ERROR' and cpeT != 'FAILED':
                            data_for_table.append([
                                cpe[0],
                                cpe[1],  # Value
                                cpe[2],  # Lower limit
                                cpe[3],  # Upper limit
                                cpe[4],  # Type
                                cpe[5],  # Unit
                                result_cpe
                            ])
                        elif cpeT == 'FAILED':
                            return "FAILED", []
                        cadT = conexion.parameters_inspection_xt(cad,options[-3])
                        if cadT != 'GENERAL_ERROR' and cadT != 'FAILED':
                            data_for_table.append([
                                cad[0],  # Measurement
                                cad[1],  # Value
                                cad[2],  # Lower limit
                                cad[3],  # Upper limit
                                cad[4],  # Type
                                cad[5],  # Unit
                                result_cad
                            ])
                        elif cadT == 'FAILED':
                            return "FAILED", []

                        return "PASSED", data_for_table
                    
                        # if(positionPxT == "FAILED" or positionPyT == "FAILED" or cpcT == "FAILED" or cpeT == "FAILED" or cadT == "FAILED"):
                        #     return "FAILED",[]
                        # else:
                        #     return "PASSED",data_for_table
                    else:
                        return "FAILED",[]
                else:
                    return "FAILED",[]          
            else:
                # print("Ninguna de las anteriores")
                return "FAILED",[]
        case "Electrical":
            result_electrical_continuity = ""
            result_voltage = ""
            result_current = ""
            result_resistance = ""

            if len(options) == 37:
                continuidad = options[2:10]
                voltaje = options[10:18]
                corriente = options[18:26]
                resistencia = options[26:-3]

                print(continuidad)
                print(voltaje)
                print(corriente)
                print(resistencia)

                if continuidad[6] =='PASSED':
                    result_electrical_continuity = "PASS"
                else:
                    result_electrical_continuity = "FAIL"
                        
                if voltaje[6] =='PASSED':
                    result_voltage = "PASS"
                else:
                    result_voltage = "FAIL"
                        
                if corriente[6] =='PASSED':
                    result_current = "PASS"
                else:
                    result_current = "FAIL"
                        
                if resistencia[6] =='PASSED':
                    result_resistance = "PASS"
                else:
                    result_resistance = "FAIL"

                if continuidad[0] == 'Ct' and voltaje[0] == 'V' and corriente[0] == 'Cr' and resistencia[0] == 'R':
                    continuidad_measurement = conexion.parameters_electrical(continuidad,options[-3])
                    if continuidad_measurement != 'GENERAL_ERROR' and continuidad_measurement != 'FAILED':
                        data_for_table.append([
                            "Voltage",  # Measurement
                            continuidad[1],  # Value
                            continuidad[2],  # Lower limit
                            continuidad[3],  # Upper limit
                            continuidad[4],  # Type
                            continuidad[5],  # Unit
                            result_electrical_continuity
                        ])
                    elif continuidad_measurement == 'FAILED':
                        return "FAILED", []
                    voltaje_measurement = conexion.parameters_electrical(voltaje,options[-3])
                    if voltaje_measurement != 'GENERAL_ERROR':
                        data_for_table.append([
                            "Voltage",  # Measurement
                            voltaje[1],  # Value
                            voltaje[2],  # Lower limit
                            voltaje[3],  # Upper limit
                            voltaje[4],  # Type
                            voltaje[5],  # Unit
                            result_voltage
                        ])
                    corriente_measurement = conexion.parameters_electrical(corriente,options[-3])
                    if corriente_measurement != 'GENERAL_ERROR' and corriente_measurement != 'FAILED':
                        data_for_table.append([
                            "Voltage",  # Measurement
                            corriente[1],  # Value
                            corriente[2],  # Lower limit
                            corriente[3],  # Upper limit
                            corriente[4],  # Type
                            corriente[5],  # Unit
                            result_current
                        ])
                    elif corriente_measurement == 'FAILED':
                        return "FAILED", []
                    resistencia_measurement = conexion.parameters_electrical(resistencia,options[-3])
                    if resistencia_measurement != 'GENERAL_ERROR' and resistencia_measurement != 'FAILED':
                        data_for_table.append([
                            "Voltage",  # Measurement
                            resistencia[1],  # Value
                            resistencia[2],  # Lower limit
                            resistencia[3],  # Upper limit
                            resistencia[4],  # Type
                            resistencia[5],  # Unit
                            result_resistance
                        ])
                    elif resistencia_measurement == 'FAILED':
                        return "FAILED", []

                    return "PASSED",data_for_table
                else:
                    return "FAILED",[]
            else:
                return "FAILED",[]
        case "Continuity":
            if len(options) == 12:
                result_continuity = ""

                if options[6] =='PASSED':
                    result_continuity = "PASS"
                else:
                    result_continuity = "FAIL"

                commits = conexion.parameters_continuity(options)
                if commits == 'FAILED':
                    return "FAILED", []
                else:
                    data_for_table.append([
                        options[1],  # Measurement
                        options[7],  # Value
                        options[3],  # Lower limit
                        options[4],  # Upper limit
                        options[8],  # Type
                        options[5],  # Unit
                        result_continuity
                    ])
                return "PASSED",data_for_table
            else:
                return "FAILED" ,[]
        case "Leak":    
            # print(options)        
            if len(options) == 13:
                result_leak = ""

                if options[4] =='PASSED':
                    result_leak = "PASS"
                else:
                    result_leak = "FAIL"
                commits = conexion.parameters_leak(options)
                if commits == 'FAILED':
                    return "FAILED", []
                else:
                    data_for_table.append([
                        options[9],  # Measurement
                        options[3],  # Value
                        options[7],  # Lower limit
                        options[8],  # Upper limit
                        options[2],  # tiempo_prueba
                        options[5],  # Fuga
                        result_leak
                    ])
                return "PASSED",data_for_table
            else:
                return "FAILED",[]
        case "Temperature":
            if len(options) == 13:
                result_temperatura = ""

                if options[8] =='PASSED':
                    result_temperatura = "PASS"
                else:
                    result_temperatura = "FAIL"

                commits = conexion.parameters_temperature(options)
                if commits == 'FAILED':
                    return "FAILED", []
                else:
                    data_for_table.append([
                        options[1],  # Measurement
                        options[2],  # Value
                        options[3],  # Lower limit
                        options[4],  # Upper limit
                        options[5],  # Type
                        options[6],  # Unit
                        result_temperatura
                    ])
                return "PASSED",data_for_table
            else:
                return "FAILED",[]
        case "Welding":
            welding = 'commit,Welding,welding_time,welding_power,100,mm,PASSED,description,1/'
            if len(options) == 11:
                result_welding = ""

                if options[6] =='PASSED':
                    result_welding = "PASS"
                else:
                    result_welding = "FAIL"
                commits = conexion.parameters_welding(options)
                if commits == 'FAILED':
                    return "FAILED", []
                else:
                    data_for_table.append([
                        options[1],  # Measurement
                        options[2],  # Value
                        options[3],  # Lower limit
                        options[4],  # Upper limit
                        "-",  # Type
                        options[5],  # Unit
                        result_welding
                    ])
                return "PASSED",data_for_table
            else:
                return "FAILED",[]
        
        case "Heatstake":
            if len(options) == 11:
                commits = conexion.parameters_heatstake(options)
                print(commits)
                if commits == 'FAILED':
                    return "FAILED", []
                else:
                    data_for_table.append([
                        options[1],  # Measurement
                        options[3],  # Value
                        options[5],  # Lower limit
                        options[6],  # Upper limit
                        "-",         # Type
                        options[5],  # Unit
                        "-"          # Result
                    ])
                return "PASSED",data_for_table
            else:
                return "FAILED",[]
            
        case "Graph":
            if len(options) == 8:
                commits = conexion.parameters_graph(options)
                print(commits)
                if commits == 'FAILED':
                    return "FAILED", []
                else:
                    data_for_table.append([
                        options[1],  # Measurement
                        options[3],  # Value
                        "-",         # Lower limit
                        "-",         # Upper limit
                        "-",         # Type
                        "-",         # Unit
                        "-"          # Result
                    ])
                return "PASSED",data_for_table
            else:
                return "FAILED",[]
            
        case _:
            # print("default")
            return "FAILED",[]
            

# commit(graph_image,name)