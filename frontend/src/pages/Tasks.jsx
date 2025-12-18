import React, { useState, useEffect } from "react";
import axios from "axios";
import TaskCard from "./TaskCard";
import "../styles/task.css";

const Tasks = ({ onSelectTask }) => {
  const [tasks, setTasks] = useState([]);
  const [statusFilter, setStatusFilter] = useState("");
  const [priorityFilter, setPriorityFilter] = useState("");

  // Lấy danh sách tasks
  useEffect(() => {
    const fetchTasks = async () => {
      try {
        let url = "/api/tasks/my/assigned";
        const params = {};
        if (statusFilter) params.status = statusFilter;
        if (priorityFilter) params.priority = priorityFilter;

        const res = await axios.get(url, { params });
        setTasks(res.data);
      } catch (error) {
        console.error("Error fetching tasks:", error);
      }
    };

    fetchTasks();
  }, [statusFilter, priorityFilter]);

  return (
    <div className="tasks-page">
      <h1>Tasks</h1>

      <div className="filters">
        <select
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value)}
        >
          <option value="">All Status</option>
          <option value="todo">To Do</option>
          <option value="in_progress">In Progress</option>
          <option value="done">Done</option>
        </select>

        <select
          value={priorityFilter}
          onChange={(e) => setPriorityFilter(e.target.value)}
        >
          <option value="">All Priority</option>
          <option value="low">Low</option>
          <option value="medium">Medium</option>
          <option value="high">High</option>
        </select>
      </div>

      <div className="task-list">
        {tasks.length === 0 && <p>No tasks found</p>}
        {tasks.map((task) => (
          <TaskCard
            key={task.id}
            task={task}
            onSelect={() => onSelectTask(task.id)}
          />
        ))}
      </div>
    </div>
  );
};

export default Tasks;
