$(document).ready(function() {

    $('#calendar').fullCalendar({
        header: {
            left: 'prev,next today',
            center: 'title',
            right: 'month,agendaWeek,agendaDay,listWeek'
        },
        defaultDate: '2016-11-07',
        navLinks: true, // can click day/week names to navigate views

        weekNumbers: true,
        weekNumbersWithinDays: true,
        weekNumberCalculation: 'ISO',

        editable: false,
        eventLimit: true, // allow "more" link when too many events

        eventClick: function(event) {
            $("#myModal").modal('show');
        },

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
