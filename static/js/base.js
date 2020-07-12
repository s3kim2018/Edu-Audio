var button1 = document.querySelector('.firstbutton')
var button2 = document.querySelector('.secondbutton')


button1.addEventListener('contextmenu', function() {
    playtext("Play Lecture")
})
button2.addEventListener('contextmenu', function() {
    playtext("Pause Lecture")
})

function playtext(text) {
    const utterance = new SpeechSynthesisUtterance(text)
    utterance.rate = 1
    speechSynthesis.speak(utterance)
}

button1.addEventListener('click', async function() {
    var thisid = document.getElementById('id').innerHTML
    const response = await fetch('http://127.0.0.1:5000/getlecturemessage/' + thisid, {
        method: 'GET', // *GET, POST, PUT, DELETE, etc.
        mode: 'no-cors', // no-cors, *cors, same-origin
        cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
        credentials: 'same-origin', // include, *same-origin, omit
        headers: {
        },
        redirect: 'follow', // manual, *follow, error
        referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
    });
    window.location.replace("http://127.0.0.1:5000/getlecturemessage/" + thisid);
    console.log(document.getElementById("wb").innerHTML)
    await playtext(document.getElementById("wb").innerHTML)
})