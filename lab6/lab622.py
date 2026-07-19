import datetime
x = datetime.datetime.now()
print(x)
#retona en formato año, mes, dia hora, minutos, segundos y microsegundos
print(x.year)
print(x.strftime("%A"))
#imprime año u dia de semana en ingles
y = datetime.datetime(2020, 5, 11)
print(y)
#crear fecha personalizada, en formato año, mes y dia
