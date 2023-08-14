document.addEventListener('DOMContentLoaded',()=>{
    document.querySelectorAll('.page').forEach(function(block){
       block.style.display = 'none';});
       loadpage('allposts');



//loads_a_page
function loadpage(page){
    document.querySelectorAll('.page').forEach(function(block){
        block.style.display = 'none';
    })
    document.querySelector(`#${page}`).style.display = 'block';
}
})
