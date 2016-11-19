$(function() {
    var turnero = $("<div>", {class:"turnero"});
    $("#div_id_fecha").append(turnero);

    $("#id_fecha").on("change", function(e) {
        var dia = $(this).val();
        var promociones = $("#id_promociones").val();
        var servicios = $("#id_servicios").val();
        console.log(promociones, servicios);
        $.ajax({
            method: "GET",
            url: URL_TURNOS_LIBRES,
            data: {
                dia: dia,
                promocion: promociones,
                servicio: servicios
            },
            success: function(datos, status, req) {
                var modulos = $(datos.modulos).map(function(index, modulo) {
                    console.log(modulo);
                    var m = $("<div>", {"style": "background:" + modulo.color});
                    m.html("<p>" + modulo.estado + " - " + modulo.hora + ":" + modulo.mins + "</p>");
                    return m;
                });
                modulos.each(function(i, m) {
                    turnero.append(m);
                })
            }
        })
    });
})
