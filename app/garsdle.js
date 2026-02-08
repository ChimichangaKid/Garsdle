

var number_of_guesses = 5;
var game_done = false;
var win = false;
var current_guess = 0;

const months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"];

const slider = document.getElementById("time_slider");
const slider_display = document.getElementById("slider_value");
const hint = document.getElementById("hint_label");
const solution = document.getElementById("solution");
const num_guesses_label = document.getElementById("guesses_label");
const player = document.getElementById("yt_player");



window.onload = function () {
    slider.addEventListener("input", () => {
        slider_display.textContent = sliderToDate(slider.value);
    });

    initialize()
};

function initialize() {
    document.getElementById("guess_button").addEventListener("click", checkAnswer);
    solution.innerText = "";
    fetch("./daily/daily_info.json")
    .then(response => response.json())
    .then(data => {
        player.src = data.url; 
    })
    .catch(err => console.error("Failed to load video URL:", err));
}



function checkAnswer() {  
    fetch("./daily/daily_info.json").then(response => response.json()).then(data => {
        todays_data = data.upload_date_int
    
        if (current_guess >= number_of_guesses) {
            return;
        }

        var guessed_value = slider.value;   

        if (guessed_value == todays_data) {
            solution.innerText = "You Win!";
            win = true;
        }

        if (guessed_value > todays_data) {
            hint.textContent = "You have guessed too high.";
        } else if (guessed_value < todays_data) {
            hint.textContent = "You have guessed too low.";
        }

        current_guess += 1;

        num_guesses_label.innerText = `Number of Guesses Left = ${number_of_guesses - current_guess}`;

        if(current_guess >= number_of_guesses){
            solution.innerText = "You Lose.";
        }
    });

    
}



function sliderToDate(value, startYear = 2023) {
    const monthIndex = (value - 1) % 12;
    const yearOffset = Math.floor((value - 1) / 12);
    return `${months[monthIndex]} ${startYear + yearOffset}`;
}