
document.addEventListener('DOMContentLoaded', function() {


    document.getElementById("upload-repo").onclick = function() {selectFiles()};

    function selectFiles() {
        // Trigger click event on the file input element
        document.getElementById('fileInput').click();
    }

    // Add event listener to handle file selection
    document.getElementById('fileInput').addEventListener('change', function(event) {
        const files = event.target.files; // Get the selected files
        if (files && files.length > 0) {
            // Perform actions with the selected files, such as uploading to the server
            console.log('Selected files:', files);
            uploadFiles(files);
        } else {s
            console.log('No files selected.');
        }
    });

    function uploadFiles(files) {
            const formData = new FormData();
            for (const file of files) {
                formData.append('files[]', file);
            }

            fetch('/upload', {
                method: 'POST',
                body: formData
            })
            .then(response => {
                if (response.ok) {
                    console.log('Files uploaded successfully.');
                } else {
                    console.error('Error uploading files.');
                }
            })
            .catch(error => {
                console.error('Error uploading files:', error);
            });
        }


});