
document.addEventListener('DOMContentLoaded', function() {


    document.getElementById("upload-repo").onclick = function() {selectFiles()};

    var files;
    var reponame;

    function selectFiles() {
        // Trigger click event on the file input element
        document.getElementById('fileInput').click();
    }

    document.getElementById("cpass").addEventListener("input", (event) => {
        //document.getElementById("p1").innerHTML = "codenext.com/{{username}}/"+event.target.value;
        reponame = event.target.value;
        reponame = reponame.replace(/\s/g, '-');
    });

    // Add event listener to handle file selection
    document.getElementById('fileInput').addEventListener('change', function(event) {
        files = event.target.files; // Get the selected files
        if (files && files.length > 0) {
            // Perform actions with the selected files, such as uploading to the server
            console.log('Selected files:', files);
            document.getElementById("selected-files-path").innerHTML="Selected parent -> "+files[0].webkitRelativePath.split('/')[0];
            document.getElementById("selected-files-path").setAttribute("style","display:visible;")
            document.getElementById("upload-repo").setAttribute("style","display:none;")
            //uploadFiles(files);
        } else {
            console.log('No files selected.');
        }
    });

    document.getElementById('file-input').addEventListener('change', function(event) {
        files = event.target.files; // Get the selected files
        if (files && files.length > 0) {
            // Perform actions with the selected files, such as uploading to the server
            console.log('Selected files:', files);
            uploadSingle(files);
        } else {
            console.log('No files selected.');
        }
    });

    // Add event listener to handle file selection
    document.getElementById('btn-primary').addEventListener('click', function(event) {
        validate();
    });

    // Add event listener to handle file selection
    document.getElementById('btn-secondary').addEventListener('click', function(event) {
        location.href = "/dashboard"
    });

    function uploadFiles(files) {
        const formData = new FormData();
        for (const file of files) {
            const fileName = file.name;
            const fileSize = (file.size/(1000));
            formData.append('files[]', file);
            formData.append('filepath[]', file.webkitRelativePath);
            formData.append('filename[]', file.name);
            formData.append('filesize[]', fileSize);
            formData.append('fileextension[]', fileName.split('.').pop());
        }

        formData.append('repo-name',reponame);

        fetch('/upload', {
            method: 'POST',
            body: formData
        })
            .then(response => {
            if (response.ok) {
                console.log('Files uploaded successfully.');
                document.getElementById("loader").setAttribute("style","display:none;")
                document.getElementById("upload-prog-desc").innerHTML= "Repository uploaded successfully";
                //location.href = '/dashboard'
                if (confirm('Uploaded Successfully!')){
                    location.href = '/dashboard'
                }
            } else {
                console.error('Error uploading files.');
                document.getElementById("loader").setAttribute("style","display:none;")
                document.getElementById("upload-prog-desc").innerHTML= "Error uploading repository";
                if (confirm('Error uploading repository!')){
                    location.href = '/upload-repository'
                }

            }
        })
            .catch(error => {
            console.error('Error uploading files:', error);
        });
    }

    function uploadSingle(files) {
        const formData = new FormData();
        for (const file of files) {
            const fileName = file.name;
            const fileSize = (file.size/(1000));
            formData.append('files[]', file);
            formData.append('filepath[]', file.webkitRelativePath);
            formData.append('filename[]', file.name);
            formData.append('filesize[]', fileSize);
            formData.append('fileextension[]', fileName.split('.').pop());
        }

        formData.append('repo-name',reponame);

        fetch('/upload-single', {
            method: 'POST',
            body: formData
        })
            .then(response => {
            if (response.ok) {
                console.log('Files uploaded successfully.');
                document.getElementById("loader").setAttribute("style","display:none;")
                document.getElementById("upload-prog-desc").innerHTML= "Repository uploaded successfully";
                //location.href = '/dashboard'
                if (confirm('Uploaded Successfully!')){
                    location.href = '/dashboard'
                }
            } else {
                console.error('Error uploading files.');
                document.getElementById("loader").setAttribute("style","display:none;")
                document.getElementById("upload-prog-desc").innerHTML= "Error uploading repository";
                if (confirm('Error uploading repository!')){
                    location.href = '/upload-repository'
                }

            }
        })
            .catch(error => {
            console.error('Error uploading files:', error);
        });
    }

    function validate(){
        if (!reponame || reponame.length == 0){
            alert('Please enter a valid repository name.')
            return false;
        }else if (!files || files.length == 0){
            alert('Please select files to upload.')
            return false;
        }else{
            checkRepoAndUpload()
        }

    }

    function checkRepoAndUpload(){
        fetch('/check-repo-exists/'+reponame, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: "message" })
        })
            .then(response => {
            if(response.ok){
                console.log('Selected files:', files);
                document.getElementById("full-screen").setAttribute("style","display:visible;")
                uploadFiles(files);
                console.log('triggered ok')
            }else{
                console.log('triggered else')
                document.getElementById("full-screen").setAttribute("style","display:none;")
                alert('Repository already exists!')
            }
        })
            .then(data => {

        })
            .catch(error => {
            document.getElementById("full-screen").setAttribute("style","display:none;")
            alert('Repository already exists!')
            console.log('triggered error')
            console.error(error)
        });
    }


});