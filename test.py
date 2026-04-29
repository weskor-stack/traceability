import conexion

pressfit = "commit,Pressfit,F,50,10,100,Numeric,N,PASSED,Comentarios,dwell_time,D,500,498,502,Numeric,mm,PASSED,Comentarios,dwell_time,PIN1,,,,,,,,,PIN2,,,,,,,,,PIN3,,,,,,,,,PIN4,,,,,,,,,P1106394-71-P:SE4A25079000001,1/"

# print(pressfit.split(","))
print(len(pressfit.split(",")))

force = pressfit.split(",")[2:11]
distance = pressfit.split(",")[11:20]
pin1 = pressfit.split(",")[20:29]
pin2 = pressfit.split(",")[29:38]
pin3 = pressfit.split(",")[38:47]
pin4 = pressfit.split(",")[47:56]

print(force)
print(distance)
print(pin1)
print(pin2)
print(pin3)
print(pin4)
print(pressfit.split(",")[56])
print(pressfit.split(",")[-2])

force_measurement = conexion.parameters_pressfit(force,pressfit.split(",")[-2])
print(force_measurement)