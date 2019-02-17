// Handle Modal 
var modal = document.getElementById('session-modal');
var openModalBtn = document.getElementById('book-session-btn');
var closeModalBtn = document.getElementById('close-modal-btn');


// Event Listeners
openModalBtn.addEventListener('click', openModal);
closeModalBtn.addEventListener('click', closeModal);
window.addEventListener('click', clickOutside);


// Event listener functions
function openModal() {
    modal.style.display = 'block';
}

function closeModal() {
    modal.style.display = 'none';
}

function clickOutside(e) {
    if (e.target == modal) {
        modal.style.display = 'none';
    }
}

var modalContainer = document.getElementsByClassName('modal-container');
var pages = document.getElementsByClassName('page');

var modalNextBtns = document.getElementsByClassName('modal-next');
var modalBackBtns = document.getElementsByClassName('modal-back');

for (var i = 0; i < modalNextBtns.length; i++) {
    modalNextBtns[i].addEventListener('click', advanceModal);
}

for (var i = 0; i < modalBackBtns.length; i++) {
    modalBackBtns[i].addEventListener('click', backModal);
}


function advanceModal(e) {
    var btn = e.target;
    var currentPage = parseInt(btn.value);
    
    if (currentPage + 1 == pages.length) {
        return;
    } else {
        pages[currentPage].style.display = 'none';
        pages[currentPage+1].style.display = 'inline';
    }
}

function backModal(e) {
    var btn = e.target;
    var currentPage = parseInt(btn.value);

    if (currentPage == 0) {
        return;
    } else {
        pages[currentPage].style.display = 'none';
        pages[currentPage - 1].style.display = 'inline';
    }
}