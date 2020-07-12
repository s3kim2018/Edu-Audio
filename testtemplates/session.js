$(document).ready(function() {
    function getBase64Image(imgElem) {
        // imgElem must be on the same server otherwise a cross-origin error will be thrown "SECURITY_ERR: DOM Exception 18"
            var canvas = document.createElement("canvas");
            canvas.width = imgElem.clientWidth;
            canvas.height = imgElem.clientHeight;
            var ctx = canvas.getContext("2d");
            ctx.drawImage(imgElem, 0, 0);
            var dataURL = canvas.toDataURL("image/png");
            return dataURL.replace(/^data:image\/(png|jpg);base64,/, "");
        }
    var imageBoard = new DrawingBoard.Board('drawingboard', {
        controls: [
            'Color',
            { Size: { type: 'dropdown' } },
            { DrawingMode: { filler: false } },
            'Navigation',
        ],
        size: 1,
        webStorage: 'session',
        enlargeYourContainer: true
    });
    $("#button").click(async function() {
        var img = await domtoimage.toBlob(document.getElementById('drawingboard')).then(
            value => {
                return value
            }
        )
        console.log(img)
        var reader = new FileReader();
        reader.readAsDataURL(img);
        reader.onloadend = async function() {
            var base64data = reader.result; 
            var sendimg = JSON.stringify(base64data)  
            const response = await fetch('http://127.0.0.1:5000/getimg', {
                method: 'POST', // *GET, POST, PUT, DELETE, etc.
                mode: 'no-cors', // no-cors, *cors, same-origin
                cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
                credentials: 'same-origin', // include, *same-origin, omit
                headers: {
                  'Content-Type': 'application/json'
                },
                redirect: 'follow', // manual, *follow, error
                referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
                body: sendimg // body data type must match "Content-Type" header
              });
              console.log(response)
        }

    
    });
})