CATTA - Sistema de Gestión de Turnos
=====

Catta es un centro de estética que existe desde el año 2015 en la ciudad de Gaiman, dirigido exclusivamente al sector femenino de la población.
El mismo se encuentra ubicado en la zona céntrica de dicha ciudad y tiene sus puertas abiertas de martes a domingos, con un horario de atención de 9:00hs a 12:00hs de mañana y de 16:00hs a 21:00hs por la tarde.
Ofrece servicios de peluquería, entre los que se destacan no sólo los cortes de cabello y las tinturas sino también tratamientos especializados como la nutrición, peinados y alisados. A su vez ofrece servicios de estética corporal y facial, como masajes, depilación y maquillaje.

Alcances y Límites del Sistema
-----
Como alcances del sistema, contamos con:
- Crear los sectores de trabajo del centro de estética.
- Crear los empleados de cada sector del centro de estética.
- Realizar la liquidación de las comisiones para el pago de los empleados.
- Modificar el porcentaje que le corresponde a cada empleado por comisión.
- Crear, modificar, cancelar y confirmar los turnos solicitados por los clientes, además de registrar su realización.
- Crear los servicios y promociones que provee el centro de estética.
- Consultar los horarios disponibles para nuevos turnos.
- Crear y modificar los insumos de peluquería.
- Mantener actualizado el stock de los productos.
- Crear los clientes que asisten al centro de estética.
- Realizar un resumen diario de los turnos realizados.
- Realizar listados y consultas varias.
- Solicitar, modificar, confirmar y cancelar turnos online.

Los aspectos del relevamiento de información que no fueron considerados en el sistema son:
- Llevar control del stock de los insumos utilizados en el sector de gabinete.
- Fraccionar los productos de peluquería.
- Manejar módulos de los turnos diferentes a 15 minutos.
- Recepcionar productos pedidos que llegaron en exceso o que no fueron pedidos.
- Manejar distintas comisiones entre servicios.
- Crear, modificar y eliminar a los proveedores.
- Registrar los pedidos a proveedores, sus pagos, devoluciones y recepciones.
- Registrar las notas de crédito de proveedores.
- Crear, modificar y eliminar los productos para la venta a los clientes.
- Registrar la venta de los productos a los clientes.
- Manejar formas de pago.
- Crear recibos y facturas.

Instalación y Uso
-----
#### Nota: Debemos tener instalado Git en el sistema.

##### Paso 1: Clonar el repositorio a nuestro sistema
    git clone https://github.com/UNPSJB/Catta.git
    cd Catta
    
##### Paso 2: Instalar los requerimientos
    pip install -r requerimientos.txt
    
##### Paso 3: Correr el código
    python manage.py runserver
    
##### Paso 4: Acceder al sistema
    Accedemos a http://localhost:8000 y listo!

Información Adicional
-----
Este trabajo fue realizado para la cátedra de Desarrollo de Software de la Universidad de la Patagonia San Juan Bosco.

###### Integrantes de la Cátedra
- Lic. Gloria Bianchi
- Lic. Diego Van Haaster

###### Integrantes del Grupo
- Matías Acosta
- Maximiliano Aguila
- Tania Aranda
- Germán Bianchini
- Emiliano De Marco
- Ian Mazzaglia
