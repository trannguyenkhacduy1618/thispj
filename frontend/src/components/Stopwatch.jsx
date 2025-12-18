import React, { useState, useEffect, useRef } from "react";
import "../styles/stopwatch.css";

const formatTime = (seconds) => {
  const hrs = Math.floor(seconds / 3600);
  const mins = Math.floor((seconds % 3600) / 60);
  const secs = seconds % 60;
  return `${hrs.toString().padStart(2, "0")}:${mins
    .toString()
    .padStart(2, "0")}:${secs.toString().padStart(2, "0")}`;
};

const Stopwatch = ({ taskId, onTimeUpdate }) => {
  const [seconds, setSeconds] = useState(0);
  const [isRunning, setIsRunning] = useState(false);
  const intervalRef = useRef(null);

  useEffect(() => {
    if (isRunning) {
      intervalRef.current = setInterval(() => {
        setSeconds((prev) => prev + 1);
      }, 1000);
    } else if (!isRunning && intervalRef.current) {
      clearInterval(intervalRef.current);
    }
    return () => clearInterval(intervalRef.current);
  }, [isRunning]);

  const handleStart = () => setIsRunning(true);
  const handlePause = () => setIsRunning(false);
  const handleReset = () => {
    setIsRunning(false);
    setSeconds(0);
    if (onTimeUpdate) onTimeUpdate(taskId, 0);
  };

  // Optionally send updated time to parent
  useEffect(() => {
    if (onTimeUpdate) onTimeUpdate(taskId, seconds);
  }, [seconds, taskId, onTimeUpdate]);

  return (
    <div className="stopwatch">
      <h4>Thời gian: {formatTime(seconds)}</h4>
      <div className="stopwatch-buttons">
        {!isRunning ? (
          <button onClick={handleStart}>Bắt đầu</button>
        ) : (
          <button onClick={handlePause}>Tạm dừng</button>
        )}
        <button onClick={handleReset}>Reset</button>
      </div>
    </div>
  );
};

export default Stopwatch;
