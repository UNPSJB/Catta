from django.core.management.base import BaseCommand
import datetime

class Command(BaseCommand):
    """
    Comando que 'Carga turnos durante el año 2016 utilizando los clientes y los servicios actuales'
    Modo de utilización python manage.py cargar_turnos
    """
    help = 'Carga los datos correspondientes a la fecha (aaaa-mm-dd) dada y genera los recibos de sueldos de ese mes'

    def handle(self, *args, **options):
        pass