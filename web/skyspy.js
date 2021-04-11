$(document).ready(function() {
    setTimeout(updateData, 5000);

    function updateData(){
        $.ajax({
            type: 'GET',
            url: "data.json",
            dataType: 'json',
            success: function(result){
                $("#ts").text(result.data.ts);
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
                setTimeout(updateData, 5000);
            }
        })
    }
})
