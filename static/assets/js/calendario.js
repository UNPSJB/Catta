$(document).ready(function() {

    $('#calendar').fullCalendar({
        header: {
            left: 'prev,next today',
            center: 'title',
            right: 'month,agendaWeek,agendaDay,listWeek'
        },
         eventClick:  function(event, jsEvent, view) {
            $('#modalTitle').html("<font color='purple'><font size=4><b>" + "Turno del dia: " + event.fecha + "</b></font></font>");
            $('#modalBody').html("<font size=3>" + "Empleado: " + event.empleado + "<br>" + "Cliente: " + event.cliente + "<br>" +
                                 "Servicios: " + event.servicios + "<br>" + "Promociones: " + event.promociones + "</font>");
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
