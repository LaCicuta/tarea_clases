from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Alumno,Genero
from .forms import GeneroForm

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
        

def alumnos_del(request, pk):
    context = {}
    try:
        alumno=Alumno.objects.get(rut=pk)

        alumno.delete()
        mensaje="Bien, datos eliminados..."
        alumnos = Alumno.objects.all()
        context = {'alumnos':alumnos, 'mensaje': mensaje}
        return render(request, 'alumnos/alumnos_list.html', context)
    except Alumno.DoesNotExist:
        mensaje="Error, no se encontró el registro..."
        alumnos = Alumno.objects.all()  
        context = {'alumnos':alumnos, 'mensaje': mensaje}
        return render(request, 'alumnos/alumnos_list.html', context)
    
def alumnos_findEdit(request, pk):

    if pk!="":
        alumno=Alumno.objects.get(rut=pk)
        generos=Genero.objects.all()

        print(type(alumno.id_genero.genero))

        context = {'alumno':alumno, 'generos':generos}
        if alumno:
            return render(request, 'alumnos/alumnos_edit.html', context)
        else:
            context = {'mensaje': "Error, no se encontró el registro..."}
            return render(request, 'alumnos/alumnos_list.html', context)
        
from datetime import datetime

def alumnosUpdate(request):
    if request.method == "POST":
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

        objGenero=Genero.objects.get(id_genero = genero)

        alumno = Alumno.objects.get(rut=rut)
        alumno.nombre=nombre
        alumno.apellido_paterno=aPaterno
        alumno.apellido_materno=aMaterno
        alumno.fecha_nacimiento = datetime.strptime(fechaNac, "%Y-%m-%d")
        alumno.id_genero = objGenero 
        alumno.telefono=telefono
        alumno.email=email
        alumno.direccion=direccion
        alumno.activo=1
        alumno.save()
        
        generos=Genero.objects.all()
        context = {'mensaje': "Ok, datos actualizados...", 'generos':generos, 'alumno':alumno}
        return render(request, 'alumnos/alumnos_edit.html', context)
    else:
        alumnos=Alumno.objects.all()
        context={'alumnos':alumnos}
        return render(request, 'alumnos/alumnos_list.html', context)
        
def crud_generos(request):
    generos=Genero.objects.all()
    context = {'generos':generos}
    print("Enviados datos generos_list")
    return render(request, "alumnos/generos_list.html", context)
        

def generosAdd(request):
    print("Estoy en controlador generosAdd")
    context={}

    if request.method == "POST":
        print("Controlador es un POST")
        form =  GeneroForm(request.POST)
        if form.is_valid():
            print("Es valid")
            form.save()

            #clean form
            form=GeneroForm()

            context={'mensaje':"Ok, datos grabados...", "form":form}
            return render(request, "alumnos/generos_add.html", context)
    else:
        # GET request
        form = GeneroForm()
        context = {"form": form}
        return render(request, "alumnos/generos_add.html", context)

def generos_del(request, pk):
    mensajes=[]
    errores=[]
    generos = Genero.objects.all()

    try:
        genero=Genero.objects.get(id_genero=pk)
        context={}
        if genero:
            genero.delete()
            mensajes.append("Bien, datos borrados")
            context = {'generos': generos, 'mensajes':mensajes, 'errores':errores}
            return render(request, 'alumnos/generos_list.html', context)
        
    except:
        print("Id no existe")
        generos=Genero.objects.all()
        mensaje="Error, id no existe"
        context={'mensaje':mensaje, 'generos':generos}
        return render(request, 'alumnos/generos_list.html', context)


def generos_edit(request, pk):
    try:
        genero=Genero.objects.get(id_genero=pk)
        context={}
        if genero:
            print("Existe genero")
            if request.method == "POST":
                print("edit es un POST")
                form = GeneroForm(request.POST, instance=genero)
                form.save()
                mensaje="Datos actualizados"
                print(mensaje)
                context = {'genero':genero, 'form':form, 'mensaje':mensaje}
                return render(request, 'alumnos/generos_edit.html', context)
            
            else:
                #No POST
                print("No post")
                form = GeneroForm(instance=genero)
                mensaje=""
                context = {'genero':genero, 'form':form, 'mensaje':mensaje}
                return render(request, 'alumnos/generos_edit.html', context)
            
    except:
        print("Id no existe")
        generos=Genero.objects.all()
        mensaje="Id no existe"
        context={'mensaje':mensaje, 'generos':generos}
        return render(request, 'alumnos/generos_list.html', context)
    
