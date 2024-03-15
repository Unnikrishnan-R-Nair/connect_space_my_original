document.querySelector('.mynavbar .hamburger-btn').addEventListener('click', function(e){
    //console.log('clicked')
    e.stopPropagation()
    document.querySelector('.mynavbar .mobile-navbar').classList.toggle('hidden');

})

window.addEventListener('resize', function(e){
    e.stopPropagation();
    if(this.innerWidth >= 1024) {
        document.querySelector('.mynavbar .mobile-navbar').classList.add('hidden');
    }
})

window.addEventListener('scroll', function(e){
    e.stopPropagation();
    if (this.scrollY > 100 && !document.querySelector('.mynavbar').classList.contains('navhover')) {
        document.querySelector('.mynavbar').classList.add('after-scroll');
        document.querySelector('.mynavbar').style.paddingBottom = '15px';
    }else if (this.scrollY < 100){
        document.querySelector('.mynavbar').classList.remove('after-scroll');      
        document.querySelector('.mynavbar').style.paddingBottom = 'initial';

    } 
})


document.querySelector('.mynavbar').addEventListener('mouseenter', function(e){
    e.stopPropagation()
    // console.log('entered');
    this.classList.add('navhover')
    this.style.paddingBottom = 'initial';


})
document.querySelector('.mynavbar').addEventListener('mouseleave', function(e){
    e.stopPropagation()
    // console.log('left');
    this.classList.remove('navhover')
    if (window.scrollY < 100){
        this.style.paddingBottom = 'initial';
    } else if (window.scrollY > 100) {

        this.style.paddingBottom = '15px';
    }

})

