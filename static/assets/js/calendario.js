$(document).ready(function() {

    $('#calendar').fullCalendar({
        header: {
            left: 'prev,next today',
            center: 'title',
            right: 'month,agendaWeek,agendaDay,listWeek'
        },
        defaultDate: '2016-09-12',
        navLinks: true, // can click day/week names to navigate views

        weekNumbers: true,
        weekNumbersWithinDays: true,
        weekNumberCalculation: 'ISO',

        editable: true,
        eventLimit: true, // allow "more" link when too many events

        eventClick: function(event) {
            // opens events in a popup window
            console.log(event);
            return false;
        },

        events: function(start, end, timezone, callback) {
            $.ajax({
                url: URL_EVENTOS,
                dataType: 'json',
                data: {
                    // our hypothetical feed requires UNIX timestamps
                    start: start.unix(),
                    end: end.unix(),
                    empleado: 1
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
