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
                        });
                });
            });
    });
});