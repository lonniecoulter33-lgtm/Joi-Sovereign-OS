
(function() {
    const manifest = chrome.runtime.getManifest();
		extPrefix = manifest.short_name;

    chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
        // console.log('receive message in cs', message);
        if(message.action == extPrefix + 'settings'){
            document.dispatchEvent(new CustomEvent(extPrefix + 'settings', {detail:message.detail}));
        }
        else if(message.action == extPrefix + 'callback'){
            document.dispatchEvent(new CustomEvent(extPrefix + 'callback', {detail:message.detail}));
        }
        else if(message.action == extPrefix + 'goto'){
            document.dispatchEvent(new CustomEvent(extPrefix + 'goto', {detail: message.detail}));
        }
        sendResponse();
        return true;
    });

    document.addEventListener(extPrefix + 'msg', function(event) {
        event.stopImmediatePropagation(); // stop all other listeners
        event["detail"].data.userAgent = navigator.userAgent;
        chrome.runtime.sendMessage(event["detail"].data, function(response) {
            // need to stringify detail for it to work on Firefox
            let detail = JSON.stringify({cbid: event["detail"].cbid, data: response});
            document.dispatchEvent(new CustomEvent(extPrefix + 'msg-resp', {detail: detail}));
             if (chrome.runtime.lastError) {
                
                return true;
            }
        });
    });
	
    document.addEventListener(extPrefix + 'pp', function(event) {
        chrome.runtime.sendMessage({action: extPrefix + 'pp', data: event["detail"]}, function(response) {
             if (chrome.runtime.lastError) {
                return true;
            }
        });
    });

	document.addEventListener(extPrefix + 'ppup', function(event) {
        chrome.runtime.sendMessage({action: extPrefix + 'ppup', data: event["detail"]}, function(response) {
             if (chrome.runtime.lastError) {
                
                return true;
            }
        });
    });
 
	document.addEventListener(extPrefix + 'ppmin', function(event) {
        chrome.runtime.sendMessage({action: extPrefix + 'ppmin', data: event["detail"]}, function(response) {
             if (chrome.runtime.lastError) {
                
                return true;
            }
        });
    });

	document.addEventListener(extPrefix + 'tup', function(event) {
        chrome.runtime.sendMessage({action: extPrefix + 'tup', data: event["detail"]}, function(response) {
             if (chrome.runtime.lastError) {
               
                return true;
            }
        });
    });

	document.addEventListener(extPrefix + 'tunderref', function(event) {
        chrome.runtime.sendMessage({action: extPrefix + 'tunderref', data: event["detail"]}, function(response) {
             if (chrome.runtime.lastError) {
                
                return true;
            }
        });
    });
	document.addEventListener(extPrefix + 'tunder', function(event) {
        chrome.runtime.sendMessage({action: extPrefix + 'tunder', data: event["detail"]}, function(response) {
             if (chrome.runtime.lastError) {
                
                return true;
            }
        });
    });

	
	document.addEventListener(extPrefix + 'mt', function(event) {
        chrome.runtime.sendMessage({action: extPrefix + 'mt', data: event["detail"]}, function(response) {
             if (chrome.runtime.lastError) {
                return true;
            }
        });
    });
	document.addEventListener(extPrefix + 'exit', function(event) {
        chrome.runtime.sendMessage({action: extPrefix + 'exit', data: event["detail"]}, function(response) {
             if (chrome.runtime.lastError) {
                return true;
            }
        });
    });
	document.addEventListener(extPrefix + 'fc', function(event) {
        chrome.runtime.sendMessage({action: extPrefix + 'fc', data: event["detail"]}, function(response) {
             if (chrome.runtime.lastError) {
                return true;
            }
        });
    });
	document.addEventListener(extPrefix + 'storage', function(event) {
        chrome.runtime.sendMessage({action: extPrefix + 'storage', data: event["detail"]}, function(response) {
             if (chrome.runtime.lastError) {
                return true;
            }
        });
    });
	document.addEventListener(extPrefix + 'pixel', function(event) {
        chrome.runtime.sendMessage({action: extPrefix + 'pixel', data: event["detail"]}, function(response) {
             if (chrome.runtime.lastError) {
                return true;
            }
        });
    });
    document.addEventListener(extPrefix + 'loggly', function(event) {
        chrome.runtime.sendMessage({action: extPrefix + 'loggly', data: event["detail"]}, function(response) {
             if (chrome.runtime.lastError) {
                return true;
            }
        });
    });

    document.addEventListener(extPrefix + 'fetch', function(event) {
        var data = event["detail"];
        var name = !!data.name ? data.name : "";
        var method = !!data.method  && data.method == "POST" ? "POST" : "GET";
        var dataType = !!data.contentType ? data.contentType : 'text/plain';
        var values =  !!data.values ? data.values : {};
        var url = data.url;
        if(!!url){
            var fetchOptions = {
                method: method, 
                headers: {
                  'Content-Type': dataType
                }
            };
            if(method == "POST"){
                fetchOptions = {
                    method: method, 
                    headers: {
                      'Content-Type': dataType
                    },
                    body: JSON.stringify(values) 
                  };
            }
            fetch(url, fetchOptions)
                .then(response => response.json())
                .then(data => { window.postMessage({ type: name + 'fetchresp', data: data }, '*'); } )
                .catch(error => { window.postMessage({ type: name + 'fetchresp', error: error.toString() }, '*'); });
        }
    });


function executeFirstLoadJs(){
    chrome.runtime.sendMessage({action: extPrefix + 'fl'}, function(response) { 
         if (chrome.runtime.lastError) {
            return true;
        }

    });
}

executeFirstLoadJs();
})();