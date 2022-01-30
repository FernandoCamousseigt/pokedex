from string import Template

with open('prueba01.html','r') as f1:
    entrada = f1.read()

#print(entrada)


document_template = Template(entrada)
sec = "0008"
nom = "Carlos"
fecha = "28/01/2022"

a = input("Ingrese 1 o 2:")

if a == "1":
    parrafo_cond = """ 
        <p>Usted escogió la opción 1</p>
    """ 
elif a=="2":
    parrafo_cond = """ 
        <p>Usted escogió una opción 2</p>
    """ 
else:
    parrafo_cond = ""

    
document_template_nuevo = document_template.substitute(seccion = sec, nombre = nom, fecha = fecha, parrafo_cond = parrafo_cond)


with open('test03.html','w') as f:
    f.write(document_template_nuevo)

