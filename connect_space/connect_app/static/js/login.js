document.querySelector('.password-input span i.fa-solid').addEventListener('click', function(e){
    if (document.querySelector('.password-input span i.fa-solid').classList.contains('fa-eye')) {

        document.querySelector('.password-input input#password').setAttribute('type', 'text');
        this.classList.replace('fa-eye', 'fa-eye-slash');
        
    } else if(document.querySelector('.password-input span i.fa-solid').classList.contains('fa-eye-slash')) {

        this.classList.replace('fa-eye-slash', 'fa-eye');
        document.querySelector('.password-input input#password').setAttribute('type', 'password');
    }
});


// message box

document.querySelector(".message-close-btn").addEventListener("click", function(e){
    document.querySelector(".message-box").remove();
})
