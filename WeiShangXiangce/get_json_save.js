//使用步骤
// 打开浏览器开发者工具：通常使用 F12 或右键点击页面然后选择“检查”。
// 执行脚本：复制并粘贴上述代码到开发者工具的 Console（控制台）中，然后按 Enter 键执行。
// 浏览页面：捕获到的 URL 和请求头会被记录在 window.capturedUrls 中，并会自动发送捕获的请求以获取返回的数据。
// 观察控制台日志：你将看到捕获的 URL 和返回的数据中的 items。并且，items 数据将被保存为 JSON 文件，文件名中包含时间戳。
// 下载 JSON 文件：当捕获到请求并获取 items 数据后，浏览器将自动下载 JSON 文件。

(function() {
    var oldXHR = window.XMLHttpRequest;
    window.capturedUrls = []; // 全局变量保存捕获的 URL

    function newXHR() {
        var realXHR = new oldXHR();

        realXHR.addEventListener('readystatechange', function() {
            if (realXHR.readyState == 1) {
                this.requestURL = this.responseURL || this._url;
                this.requestHeaders = {};
                this.setRequestHeader = (function(original) {
                    return function(name, value) {
                        this.requestHeaders[name] = value;
                        original.apply(this, arguments);
                    };
                })(realXHR.setRequestHeader);
            }

            if (realXHR.readyState == 4 && this.requestURL.includes("/album/personal/") && (this.requestURL.includes("new?") || this.requestURL.includes("all?"))) {
                var fullUrl = "https://www.szwego.com" + this.requestURL; // 组合完整的 URL
                console.log("Captured URL:", fullUrl);
                console.log("Request Headers:", this.requestHeaders);
                window.capturedUrls.push({ url: fullUrl, headers: this.requestHeaders });

                // 获取时间戳
                var timestampMatch = fullUrl.match(/timestamp=(\d+)/);
                var timestamp = timestampMatch ? timestampMatch[1] : Date.now();

                // 发送捕获的请求并处理返回的数据
                fetch(fullUrl, {
                    method: 'POST',
                    headers: {
                        ...this.requestHeaders,
                        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
                    },
                    body: realXHR._body // 将请求体传递过去
                })
                .then(response => response.json())
                .then(data => {
                    if (data.result && data.result.items) {
                        console.log("Items:", data.result.items);
                        saveItemsAsJson(data.result.items, timestamp);
                    }
                })
                .catch(error => console.error("Error fetching data:", error));
            }
        }, false);

        var oldOpen = realXHR.open;
        realXHR.open = function(method, url) {
            this._url = url;
            return oldOpen.apply(this, arguments);
        };

        var oldSend = realXHR.send;
        realXHR.send = function(body) {
            this._body = body; // 保存请求体
            return oldSend.apply(this, arguments);
        };

        return realXHR;
    }

    function saveItemsAsJson(items, timestamp) {
        var json = JSON.stringify(items, null, 2);
        var blob = new Blob([json], { type: 'application/json' });
        var url = URL.createObjectURL(blob);
        var a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = 'items_' + timestamp + '.json';
        document.body.appendChild(a);
        a.click();
        URL.revokeObjectURL(url);
        console.log("JSON file saved:", 'items_' + timestamp + '.json');
    }

    window.XMLHttpRequest = newXHR;

    console.log("XMLHttpRequest overridden and capture initialized."); // 确认脚本加载完毕
})();


