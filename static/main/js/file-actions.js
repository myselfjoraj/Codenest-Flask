document.addEventListener('DOMContentLoaded', function(){

    // starring a file
    document.getElementById('makeStar').addEventListener('click', function(event) {
        const values = JSON.parse(document.getElementById('makeStar').getAttribute("data-values"));
        var star = values.value2;
        fetch('/star/'+values.value1+'/'+star, {
            method: 'POST'
        }).then(response => {
            if (response.ok) {
                location.href = '/'+values.value3
            } else {
                 location.href ='/'+values.value3
            }
        }).catch(error => {
            //alert("error");
        });
    });

    // make public or private a file
    document.getElementById('publicPrivate').addEventListener('click', function(event) {
        const values = JSON.parse(document.getElementById('publicPrivate').getAttribute("data-values"));
        var mode = values.value2;
        fetch('/chmod/'+values.value1+'/'+mode, {
            method: 'POST'
        }).then(response => {
            if (response.ok) {
                location.href = '/'+values.value3
            } else {
                 location.href = '/'+values.value3
            }
        }).catch(error => {
            //alert("error");
        });
    });

    // delete a file
    document.getElementById('delete').addEventListener('click', function(event) {
        const values = JSON.parse(document.getElementById('delete').getAttribute("data-values"));
        fetch('/delete/'+values.value1, {
            method: 'POST'
        }).then(response => {
            if (response.ok) {
                location.href = '/'+values.value3
            } else {
                 location.href = '/'+values.value3
            }
        }).catch(error => {
            //alert("error");
        });
    });



});