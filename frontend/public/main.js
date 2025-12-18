import '../public/styles.css';

// ==== Stopwatch Logic ====
let timerInterval = null;
let elapsedSeconds = 0;

const timerDisplay = document.getElementById("timer");
const startStopBtn = document.getElementById("startStopBtn");
const resetBtn = document.getElementById("resetBtn");

function formatTime(seconds) {
  const hrs = String(Math.floor(seconds / 3600)).padStart(2, "0");
  const mins = String(Math.floor((seconds % 3600) / 60)).padStart(2, "0");
  const secs = String(seconds % 60).padStart(2, "0");
  return `${hrs}:${mins}:${secs}`;
}

function startStopTimer() {
  if (timerInterval) {
    clearInterval(timerInterval);
    timerInterval = null;
    startStopBtn.textContent = "Start";
  } else {
    timerInterval = setInterval(() => {
      elapsedSeconds++;
      timerDisplay.textContent = formatTime(elapsedSeconds);
    }, 1000);
    startStopBtn.textContent = "Stop";
  }
}

function resetTimer() {
  clearInterval(timerInterval);
  timerInterval = null;
  elapsedSeconds = 0;
  timerDisplay.textContent = formatTime(elapsedSeconds);
  startStopBtn.textContent = "Start";
}

startStopBtn.addEventListener("click", startStopTimer);
resetBtn.addEventListener("click", resetTimer);

// ==== Daily Report Mock Data ====
const dailyTasks = [
  { title: "Task 1", time: "2h" },
  { title: "Task 2", time: "1h 30m" },
  { title: "Task 3", time: "45m" }
];

const dailyTasksUl = document.getElementById("dailyTasks");
dailyTasks.forEach(task => {
  const li = document.createElement("li");
  li.textContent = `${task.title} - ${task.time}`;
  dailyTasksUl.appendChild(li);
});

// ==== Statistics Mock Data ====
const statsContent = document.getElementById("statsContent");
const statsData = {
  totalTime: "3h 15m",
  tasksCompleted: 2
};
statsContent.innerHTML = `
  <p>Total time today: ${statsData.totalTime}</p>
  <p>Tasks completed: ${statsData.tasksCompleted}</p>
`;