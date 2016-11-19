$(document).ready(function() {

    $('#calendar').fullCalendar({
        header: {
            left: 'prev,next today',
            center: 'title',
            right: 'month,agendaWeek,agendaDay,listWeek'
        },
         eventClick:  function(event, jsEvent, view) {
            $('#modalTitle').html("Turno del dia: " + event.fecha);
            $('#modalBody').html("Empleado: " + event.empleado + "<br>" + "Cliente: " + event.cliente + "<br>" +
                                 "Servicios: " + event.servicios + "<br>" + "Promociones: " + event.promociones);
                                  //"Servicios: " + event.servicios  );
            //$('#modalBody1').html("Empleado: " + event.empleado);
            //$('#modalBody2').html("Empleado: " + event.empleado);
            $('#fullCalModal').modal();
        },
        defaultDate: '2016-11-07',
        navLinks: true, // can click day/week names to navigate views

        weekNumbers: true,
        weekNumbersWithinDays: true,
        weekNumberCalculation: 'ISO',
        lang: 'es',
        editable: false,
        eventLimit: true, // allow "more" link when too many events

        events: function(start, end, timezone, callback) {
            $.ajax({
                url: URL_EVENTOS,
                dataType: 'json',
                data: {
                    start: start.unix(),
                    end: end.unix(),
                },
                success: function(data) {
                    callback(data.turnos);
                },
                error: function() {
                    console.log("Error");
                }
            });
        },
        loading: function(bool) {
            $('#loading').toggle(bool);
        }


    });

});
