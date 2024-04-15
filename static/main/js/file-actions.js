document.addEventListener('DOMContentLoaded', function(){
    document.getElementById('makeStar').addEventListener('click', function(event) {

        const values = JSON.parse(document.getElementById('makeStar').getAttribute("data-values"));
        var star = values.value2;

        fetch('/star/'+values.value1+'/'+star, {
            method: 'POST'
        })
            .then(response => {
            if (response.ok) {
                location.href = '/dashboard'
            } else {
                 location.href = '/dashboard'
            }
        })
            .catch(error => {
            //alert("error");
        });

    });
});