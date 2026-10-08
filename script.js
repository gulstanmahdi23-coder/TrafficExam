let driverName = "";
let currentQuestionIndex = 0;
let correctAnswersCount = 0;
let timer = null;
let timeLeft = 60;

let allGroupsQuestions = {};
fetch('questions.json')
.then(response => response.json())
.then(data => {
    allGroupsQuestions = data;
    console.log("پرسیارەکان سەرکەوتووانە بارکران!");
})
.catch(error => console.error("هەڵە لە بارکردنی پرسیارەکاندا:", error));

let examQuestions = [];
let selectedGroupFile = 1;

document.getElementById('modalSubmitBtn').addEventListener('click', function() {
    let password = document.getElementById('modalPasswordInput').value;
    if (password === "Mirkasor2027") {
        document.getElementById('passwordModal').style.display = 'none';
    } else {
        alert("!پاسووردەکە هەڵەیە");
    }
});

function selectGroup(groupInput) {
    if (groupInput === 'A') selectedGroupFile = 1;
    else if (groupInput === 'B') selectedGroupFile = 2;
    else if (groupInput === 'C') selectedGroupFile = 3;
    else if (groupInput === 'D') selectedGroupFile = 4;
    
    // ئەم alertـە لابرا بۆ ئەوەی پەیامەکە دەرنەکەوێت
    // alert("گرووپی " + groupInput + " هەڵبژێردرا. ئێستا دوگمەی دەستپێکردن بگرە!");
}

function startQuiz() {
    const nameInput = document.getElementById('driver-name').value.trim();
    if (nameInput === "") {
        alert("تکایە ناوی سیانی خۆت بنووسە!");
        return;
    }
    driverName = nameInput;

    const groupList = allGroupsQuestions[selectedGroupFile] || allGroupsQuestions[1];
    if (!groupList) {
        console.error("گروپەکە نەدۆزرایەوە یان داتاکە بار نەکراوە!");
        alert("هەڵە: پرسیارەکانی ئەم گروپە بەردەست نیین!");
        return;  
    }
    
    const shuffled = [...groupList].sort(() => Math.random() - 0.5);
    examQuestions = shuffled.slice(0, 25); 

    currentQuestionIndex = 0;
    correctAnswersCount = 0;
    
    document.getElementById('name-section').classList.add('hidden');
    document.getElementById('quiz-section').classList.remove('hidden');
    showQuestion();
}

function showQuestion() {
    if (currentQuestionIndex >= examQuestions.length) {
        endQuiz();
        return;
    }

    clearInterval(timer);
    timeLeft = 60;
    
    timer = setInterval(() => {
        timeLeft--;

        const timerElement = document.getElementById('timer');
        if (timerElement) {
            timerElement.innerText = "⏱️ کاتی ماوە: " + timeLeft + " چرکە";
        }

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
    if (q.image && q.image !== "none" && q.image.trim() !== "") {
        imgElement.style.display = "block";
        imgElement.src = "images/" + q.image.trim(); 
        imgElement.onerror = function() { this.style.display = 'none'; };
    } else {
        imgElement.style.display = "none";
    }
}

function checkAnswer(selectedChoiceNum) {
    clearInterval(timer);
    const q = examQuestions[currentQuestionIndex];
    
    let isCorrect = (q.correctAnswer.trim() === selectedChoiceNum.toString());

    if (isCorrect) {
        correctAnswersCount++;
    }
    
    currentQuestionIndex++;
    showQuestion();
}

function endQuiz() {
    clearInterval(timer);
    const finalScore = correctAnswersCount * 4;
let statusText = finalScore >= 80 ? "شۆفێر: <b>" + driverName + "</b> - دەرچووی 🎉" : "شۆفێر: <b>" + driverName + "</b> - دەرنەچووی ❌";
    document.getElementById('quiz-section').classList.add('hidden');
    const resultSection = document.getElementById('result-section');
    resultSection.classList.remove('hidden');

    document.getElementById('final-score-text').innerHTML =
        statusText + "<br><br>" +
        "کۆی گشتی نمرە: <b>" + finalScore + " لە 100</b>";
}