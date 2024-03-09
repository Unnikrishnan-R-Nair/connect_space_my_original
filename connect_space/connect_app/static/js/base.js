document.querySelector('.mynavbar .hamburger-btn').addEventListener('click', function(e){
    //console.log('clicked')

    document.querySelector('.mynavbar .mobile-navbar').classList.toggle('hidden');

})

window.addEventListener('resize', function(e){
    if(this.innerWidth >= 1024) {
        document.querySelector('.mynavbar .mobile-navbar').classList.add('hidden');
    }
})