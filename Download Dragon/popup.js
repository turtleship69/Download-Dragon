document.addEventListener('DOMContentLoaded', function () {
    chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
        var tabUrl = tabs[0].url;
        document.getElementById('url').value = tabUrl;
      });
    document.getElementById("download").addEventListener("click", function () {
        fetch(chrome.runtime.getURL('config.json'))
            .then(response => response.json())
            .then(data => {
                const { clientHost, port } = data;
                const url = `http://${clientHost}:${port}/download`;
                chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
                    var inputUrl = document.getElementById('url').value;
                    var statusElement = document.createElement('div');
                    statusElement.style.backgroundColor = 'blue';
                    statusElement.innerText = 'Downloading';
                    document.body.appendChild(statusElement);
                    fetch(url, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        }, body: JSON.stringify({
                            url: inputUrl,
                            audioOnly: document.getElementById('audioOnly').checked
                        })
                    })
                        .then(response => response.json())
                        .then(data => {
                            console.log(data);
                            if (data.status === 'success') {
                                statusElement.style.backgroundColor = 'green';
                                statusElement.innerText = 'Downloaded';
                            } else {
                                statusElement.style.backgroundColor = 'red';
                                statusElement.innerText = data.message;
                            }
                            document.body.appendChild(statusElement);
                        });
                });
            });
    });
});