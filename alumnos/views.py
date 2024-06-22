from django.shortcuts import render
from .models import Alumno,Genero

# Create your views here.
class persona:
    def __init__(self, nombre, edad):
        self.nombre=nombre
        self.edad=edad
        super().__init__()


def index(request):
    hijo=persona("Juan Perez", "7")

    lista=["Lazaña", "Charquican", "Porotos granado"]

    alumnos= Alumno.objects.all()


    context={"hijo":hijo, "nombre":"Claudia Andrea", "comidas":lista, "alumnos":alumnos }

    return render(request, 'alumnos/index.html', context)

def crud(request):
    alumnos = Alumno.objects.all()
    context = {'alumnos': alumnos}
    return render(request, 'alumnos/alumnos_list.html', context)

def alumnosAdd(request):
        if request.method != "POST":
            #no es un POST, por lo tanto se muestra el formulario para agregar
            generos=Genero.objects.all()
            context={'generos' :generos}
            return render(request, 'alumnos/alumno_add.html', context)
        elif request.method == "POST":
            #Es un POST, por lo tanto se recuperan los datos del formulario y se graban en la tabla.

            rut=request.POST["rut"]
            nombre=request.POST["nombre"]
            aPaterno=request.POST["paterno"]
            aMaterno=request.POST["materno"]
            fechaNac=request.POST["fechaNac"]
            genero=request.POST["genero"]
            telefono=request.POST["telefono"]
            email=request.POST["email"]
            direccion=request.POST["direccion"]
            activo="1"

            print("Datos recibidos del formulario:")
            print(f"Rut: {rut}, Nombre: {nombre}, Apellido Paterno: {aPaterno}, Apellido Materno: {aMaterno}, Fecha Nacimiento: {fechaNac}, Género: {genero}, Teléfono: {telefono}, Email: {email}, Dirección: {direccion}")

            objGenero=Genero.objects.get(id_genero = genero)
            obj=Alumno.objects.create(  rut=rut,
                                        nombre=nombre,
                                        apellido_paterno=aPaterno,
                                        apellido_materno=aMaterno,
                                        fecha_nacimiento=fechaNac,
                                        id_genero=objGenero,
                                        telefono=telefono,
                                        email=email,
                                        direccion=direccion,
                                        activo=1)
            print("Objeto Alumno creado:", obj)
            obj.save()
            print("Datos guardados en la base de datos")
            context = {'mensaje': "Ok, datos guardados..."}
            return render(request, 'alumnos/alumno_add.html', context)
        
