function download_graph() {
    let downloadLink = document.createElement('a');
    downloadLink.setAttribute('download', 'GraphAsImage.png');
    let canvas = document.getElementById('lineChart');
    canvas.toBlob(
        function(blob) {
            let url = URL.createObjectURL(blob);
            downloadLink.setAttribute('href', url);
            downloadLink.click();
        }
    );
}

