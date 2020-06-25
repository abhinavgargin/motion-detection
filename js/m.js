var myvideo = document.getElementById('myvideo'),
    playbutton = document.getElementById('playme'),
    jumplink = document.getElementById('jump');

    var submitbutton = document.getElementById('submit');
    var csvData = new Array();
    var i=0;
    var t=0;
    submitbutton.addEventListener("click", function () {
        var url = "js/Time_of_movements.csv";

        var request = new XMLHttpRequest();  
    request.open("GET", url, false);   
    request.send(null);  

   var jsonObject = request.responseText.split(/\r?\n|\r/);
    for (var j = 1; j < jsonObject.length; j++) {
        //console.log(jsonObject[i].split(',')[1])
    csvData.push(jsonObject[j].split(',')[1]);
        }
    // Retrived data from csv file content
    console.log(csvData); 
    t = csvData[i]
}, false);


jumplink.addEventListener("click", function (event) {
    console.log(csvData[i]);
    event.preventDefault();
    myvideo.play();
    myvideo.pause();
    console.log(t)
    myvideo.currentTime = t;
    myvideo.play();
    
    if (i < csvData.length-1){
        t = csvData[++i]}
        else{
            i=0
            t = csvData[i]
        }
}, false);

// only in to demon;strate video
playbutton.addEventListener("click", function () {
    if (myvideo.paused) {
        myvideo.play();
    } else {
        myvideo.pause();
    }
}, false);

