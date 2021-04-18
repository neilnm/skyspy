$(document).ready(function() {
    let boxes = $(".box").clone();
    boxes.children().text("");
    updateData()

    function updateData(){
        $.ajax({
            type: 'GET',
            url: "data.json",
            dataType: 'json',
            success: function(result){
                $("#flight-info").empty();
                $("#flight-info").append(boxes);

                $("#ts").text(`${result.data.dataTs} | A/C: ${result.data.ts}`);
                $("#last-seen").text(result.data.lastSeen);
                $("#metar").text(result.data.metar);
                $("#description").text(result.data.description);
                $("#type").text(`A/C: ${result.data.type}`);
                $("#altitude").text(`Alt: ${result.data.altitude}`);
                $("#track").text(`Heading: ${result.data.track}`);
                $("#speed").text(`Speed: ${result.data.speed}`);
                $("#origin-name").text(result.data.originName);
                $("#origin").text(result.data.origin);
                $("#destination-name").text(result.data.destinationName);
                $("#destination").text(result.data.destination);
                dataTs = result.data.dataTs;

                checkAntenna(dataTs);
                setTimeout(updateData, 5000);
            },
            error: function(jqXHR, textStatus, errorThrown){
                console.log("error");
                $("#flight-info").empty();
                $("#flight-info").text("Check Server");
                $("#flight-info").addClass("check-antenna");
                setTimeout(updateData, 5000);
            }
        })
    }

    function checkAntenna(dataTs){
        let now = Date.now();
        let diff = Math.floor((now - new Date(dataTs)) / 60000);
        if(diff > 2){
            $("#flight-info").text("Check Antenna");
            $("#flight-info").addClass("check-antenna");
        }
    }
})
