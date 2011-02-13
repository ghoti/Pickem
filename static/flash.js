$(document).ready(function(){
            setTimeout(function(){
            $(".flash").fadeOut("slow", function () {
            $(".flash").remove();
                }); }, 2000);
            });