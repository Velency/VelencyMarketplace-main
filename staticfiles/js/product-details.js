let bigImg =  document.querySelector('.big-img');
let smallImg = document.querySelectorAll('.small-img');

smallImg.forEach( img => {
    img.addEventListener('click', function (ev){
        let imgClicked = ev.target;
        bigImg.src = imgClicked.src;
    })
});