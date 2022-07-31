window.onload = function() {
        
    let y = new Date().getFullYear()

    year_list = document.getElementsByName('years')



    for (let i = 0; i < year_list[0].length; i++) {
    
    if (year_list[0][i].value == y){
        
    year_list[0][i].selected = true;

    return;

    

}

}
    

 

}
