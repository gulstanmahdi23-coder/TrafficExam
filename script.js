let driverName = "";
let examQuestions = [];
let currentQuestionIndex = 0;
let correctAnswersCount = 0;
let timer = null;
let timeLeft = 60;

document.getElementById('modalSubmitBtn').addEventListener('click', function() {
    let password = document.getElementById('modalPasswordInput').value;
    if (password === "Mirkasor2027") {
    document.getElementById('passwordModal').style.display='none';
    } else {
alert("!پاسووردەکە هەڵەیە")   
}
});
function startquiz(){
    const nameInput = document.getElementById('driver-name').value.trim();
    if (nameInput === "") {
        alert("تکایە ناوی سیانی خۆت بنووسە!");
        return;
    }
    driverName = nameInput;
    document.getElementById('name-section').classList.add('hidden');
    document.getElementById('group-select-section').classList.remove('hidden');
}

function selectGroup(groupInput) {
    let fileNumber = 1;
    if (groupInput === 'B') fileNumber = 2;
    else if (groupInput === 'C') fileNumber = 3;
    else if (groupInput === 'D') fileNumber = 4;

    const fileName = "group" + fileNumber + ".csv";
   
    fetch(fileName)
        .then(response => {
            if (!response.ok) throw new Error("فایلەکە نەدۆزرایەوە");
            return response.text();
        })
        .then(data => {
            const allQuestions = parseCSV(data);
            examQuestions = getRandomQuestions(allQuestions, 25);
            currentQuestionIndex = 0;
            correctAnswersCount = 0;
           
            document.getElementById('group-select-section').classList.add('hidden');
            document.getElementById('quiz-section').classList.remove('hidden');
           
            showQuestion();
        })
        .catch(error => {
            alert("کێشە لە هێنانی فایلدا هەیە: " + fileName);
        });
}

function parseCSV(data) {
    const lines = data.split('\n');
    const questions = [];
   
    for (let i = 1; i < lines.length; i++) {
        const line = lines[i];
        if (!line || line.trim() === "") continue;
       
        const parts = line.split(/,(?=(?:(?:[^"]*"){2})*[^"]*$)/);
       
        if (parts.length >= 6) {
            let qText = parts[0].replace(/^["']|["'\r]/g, "").trim();
            if (qText.toLowerCase().includes("column")) continue;

            questions.push({
                question: qText,
                choice1: parts[1].replace(/^["']|["'\r]/g, "").trim(),
                choice2: parts[2].replace(/^["']|["'\r]/g, "").trim(),
                choice3: parts[3].replace(/^["']|["'\r]/g, "").trim(),
                correctAnswer: parts[4].replace(/^["']|["'\r]/g, "").trim(),
                image: parts[5].replace(/^["']|["'\r]/g, "").trim()
            });
        }
    }
    return questions;
}

function getRandomQuestions(arr, count) {
    const shuffled = [...arr].sort(() => 0.5 - Math.random());
    return shuffled.slice(0, count);
}

function showQuestion() {
    if (currentQuestionIndex >= examQuestions.length) {
        endQuiz();
        return;
    }

    clearInterval(timer);
    timeLeft = 60;
    updateTimerDisplay();
    updateScoreDisplay();
   
    timer = setInterval(() => {
        timeLeft--;
        updateTimerDisplay();
        if (timeLeft <= 0) {
            clearInterval(timer);
            currentQuestionIndex++;
            showQuestion();
        }
    }, 1000);

    const q = examQuestions[currentQuestionIndex];
    document.getElementById('question-text').innerText = (currentQuestionIndex + 1) + ". " + q.question;
    document.getElementById('choice1-btn').innerText = "1) " + q.choice1;
    document.getElementById('choice2-btn').innerText = "2) " + q.choice2;
    document.getElementById('choice3-btn').innerText = "3) " + q.choice3;

    const imgElement = document.getElementById('question-image');
    let imageName = q.image;
   
    if (imageName && imageName !== "" && imageName.toLowerCase() !== "none") {
        let cleanName = imageName.replace(/\.[^/.]+$/, "");
       
        let possibleSources = [
            imageName,
            cleanName + ".png.jpg",
            cleanName + "png.jpg",
            cleanName + ".jpg",
            cleanName + ".png"
        ];
        let sourceIndex = 0;
        imgElement.style.display = "block";
        function tryLoadNextImage() {
            if (sourceIndex < possibleSources.length) {
                imgElement.src = possibleSources[sourceIndex++];
            } else {
                imgElement.style.display = "none";
            }
        }

        imgElement.onerror = tryLoadNextImage;
        tryLoadNextImage();
    } else {
        imgElement.style.display = "none";
    }
}

function updateTimerDisplay() {
    let timerEl = document.getElementById('timer-display');
    if (!timerEl) {
        const quizSec = document.getElementById('quiz-section');
        timerEl = document.createElement('div');
        timerEl.id = 'timer-display';
        timerEl.style.color = '#e74c3c';
        timerEl.style.fontSize = '16px';
        timerEl.style.fontWeight = 'bold';
        timerEl.style.marginBottom = '10px';
        quizSec.prepend(timerEl);
    }
    timerEl.innerText = "کاتی ماوە: " + timeLeft + " چرکە";
}

function updateScoreDisplay() {
    let scoreEl = document.getElementById('score-display');
    if (!scoreEl) {
        const quizSec = document.getElementById('quiz-section');
        scoreEl = document.createElement('div');
        scoreEl.id = 'score-display';
        scoreEl.style.color = '#27ae60';
        scoreEl.style.fontSize = '16px';
        scoreEl.style.fontWeight = 'bold';
        scoreEl.style.marginBottom = '15px';
        quizSec.prepend(scoreEl);
    }
    let currentScore = correctAnswersCount * 4;
    scoreEl.innerText = "نمرەی ئێستا: " + currentScore + " لە 100 (" + correctAnswersCount + " پرسیاری ڕاست)";
}

function checkAnswer(selectedChoiceNum) {
    clearInterval(timer);
    const q = examQuestions[currentQuestionIndex];
   
    let dbAnswer = q.correctAnswer.toString().trim();
    let isCorrect = false;

    let selectedText = "";
    if (selectedChoiceNum === 1) selectedText = q.choice1;
    else if (selectedChoiceNum === 2) selectedText = q.choice2;
    else if (selectedChoiceNum === 3) selectedText = q.choice3;

    let cleanDbAnswer = dbAnswer.toLowerCase();
    if (cleanDbAnswer === 'a' || cleanDbAnswer === '1') cleanDbAnswer = '1';
    else if (cleanDbAnswer === 'b' || cleanDbAnswer === '2') cleanDbAnswer = '2';
    else if (cleanDbAnswer === 'c' || cleanDbAnswer === '3') cleanDbAnswer = '3';
    let cleanSelectedText = selectedText.toLowerCase();

    if (
        cleanDbAnswer === selectedChoiceNum.toString() || 
        cleanDbAnswer === cleanSelectedText ||
        cleanSelectedText.includes(cleanDbAnswer) ||
        cleanDbAnswer.includes(cleanSelectedText)
    ) {
        isCorrect = true;
    }

    if (isCorrect) {
        correctAnswersCount++;
    }
   
    currentQuestionIndex++;
    showQuestion();
}

function endQuiz() {
    clearInterval(timer);
   
    const timerEl = document.getElementById('timer-display');
    if (timerEl) timerEl.remove();
    const scoreEl = document.getElementById('score-display');
    if (scoreEl) scoreEl.remove();

    const finalScore = correctAnswersCount * 4;
    let statusText = "";
   
    if (finalScore >= 80) {
        statusText = "شۆفێر: <b>" + driverName + "</b> - دەرچووی 🎉";
    } else {
        statusText = "شۆفێر: <b>" + driverName + "</b> - دەرنەچووی ❌";
    }

    document.getElementById('quiz-section').classList.add('hidden');
    const resultSection = document.getElementById('result-section');
    resultSection.classList.remove('hidden');

    document.getElementById('final-score-text').innerHTML =
        statusText + "<br><br>" +
        "کۆی گشتی نمرە: <b>" + finalScore + " لە 100</b>";
}