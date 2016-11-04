$(function(){
    /* initialize the calendar
    -----------------------------------------------------------------*/
    $('#calendar').fullCalendar({

        header: {
            left: 'prev,next today',
            center: 'title',
            right: 'month,listYear'
        },

        displayEventTime: false, // don't show the time column in list view

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
