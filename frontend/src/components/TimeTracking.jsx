import React, { useState, useEffect, useRef } from "react";
import axios from "axios";

const TimeTracking = ({ taskId, onStop }) => {
  const [isRunning, setIsRunning] = useState(false);
  const [elapsed, setElapsed] = useState(0); // thời gian tính bằng giây
  const intervalRef = useRef(null);

  useEffect(() => {
    if (isRunning) {
      intervalRef.current = setInterval(() => {
        setElapsed((prev) => prev + 1);
      }, 1000);
    } else {
      clearInterval(intervalRef.current);
    }

    return () => clearInterval(intervalRef.current);
  }, [isRunning]);

  const handleStart = () => setIsRunning(true);
  const handlePause = () => setIsRunning(false);

  const handleStop = async () => {
    setIsRunning(false);
    try {
      await axios.post("/api/time_tracking/", {
        task_id: taskId,
        duration_seconds: elapsed,
      });
      setElapsed(0);
      if (onStop) onStop(); // callback parent
    } catch (error) {
      console.error("Error saving time entry:", error);
    }
  };

  const formatTime = (seconds) => {
    const h = Math.floor(seconds / 3600)
      .toString()
      .padStart(2, "0");
    const m = Math.floor((seconds % 3600) / 60)
      .toString()
      .padStart(2, "0");
    const s = (seconds % 60).toString().padStart(2, "0");
    return `${h}:${m}:${s}`;
  };

  return (
    <div className="time-tracking">
      <h3>Task ID: {taskId}</h3>
      <p>Elapsed: {formatTime(elapsed)}</p>
      <div className="controls">
        {!isRunning ? (
          <button onClick={handleStart}>Start</button>
        ) : (
          <button onClick={handlePause}>Pause</button>
        )}
        <button onClick={handleStop} disabled={elapsed === 0}>
          Stop & Save
        </button>
      </div>
    </div>
  );
};

export default TimeTracking;
