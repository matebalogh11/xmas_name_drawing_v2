
function startTimer() {
    var countDownDate = new Date("Dec 22, 2018 18:00:00").getTime();
    setInterval(function() {
        // Get todays date and time
        var now = new Date().getTime();
    
        // Find the distance between now and the count down date
        var distance = countDownDate - now;
    
        // Time calculations for days, hours, minutes and seconds
        var days = Math.floor(distance / (1000 * 60 * 60 * 24));
        var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        var seconds = Math.floor((distance % (1000 * 60)) / 1000);
    
        // Display the result in the element with id="date"
        document.getElementById("date").innerHTML = "Hátravan: " + days + "d " + hours + "h "
        + minutes + "m " + seconds + "s ";
    
        // If the count down is finished, write some text 
        if (distance < 0) {
            clearInterval(x);
            document.getElementById("date").innerHTML = "Épp megy";
        }
    }, 1000);
}

window.onload = function() {
    startTimer();
}