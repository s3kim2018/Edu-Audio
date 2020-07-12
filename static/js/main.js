const play1 = document.querySelector('.content .create');
const play2 = document.getElementById("dos");
const play3 = document.getElementById("tres");
const close = document.querySelector('.popup p')

play1.addEventListener('contextmenu', function() {
    playtext("Create a Lecture Session")
})
play2.addEventListener('contextmenu', function() {
    playtext("Join a Lecture Session")
})
play3.addEventListener('contextmenu', function() {
    playtext("My Notes")

})
function playtext(text) {
    const utterance = new SpeechSynthesisUtterance(text)
    utterance.rate = 1
    speechSynthesis.speak(utterance)
}

play2.addEventListener('click', function() {
    document.querySelector('.popup').style.setProperty('display', 'block')
})

close.addEventListener('click', function() {
    document.querySelector('.popup').style.setProperty('display', 'none')
})
