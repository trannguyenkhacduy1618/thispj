import React, { useState } from "react";
import Stopwatch from "./Stopwatch";

const TaskCard = ({ task, onTimeUpdate, onStatusChange }) => {
  const [status, setStatus] = useState(task.status);

  const handleStatusChange = (e) => {
    const newStatus = e.target.value;
    setStatus(newStatus);
    if (onStatusChange) {
      onStatusChange(task.id, newStatus);
    }
  };

  const handleTimeUpdate = (taskId, seconds) => {
    if (onTimeUpdate) {
      onTimeUpdate(taskId, seconds);
    }
  };

  return (
    <div className="task-card">
      <h3>{task.title}</h3>
      {task.description && <p>{task.description}</p>}

      <div className="task-info">
        <span>Priority: {task.priority}</span>
        <span>Assigned to: {task.assigned_to_name || "Unassigned"}</span>
        <span>
          Status:{" "}
          <select value={status} onChange={handleStatusChange}>
            <option value="todo">To Do</option>
            <option value="in_progress">In Progress</option>
            <option value="done">Done</option>
          </select>
        </span>
      </div>

      <Stopwatch taskId={task.id} onTimeUpdate={handleTimeUpdate} />

      <div className="task-footer">
        <small>Created at: {new Date(task.created_at).toLocaleString()}</small>
      </div>
    </div>
  );
};

export default TaskCard;
