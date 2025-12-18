import api from "./api";

/**
 * Lấy danh sách task theo board + filter
 */
const getTasks = async ({
  boardId,
  status = null,
  priority = null,
  assignedTo = null,
}) => {
  const params = { board_id: boardId };

  if (status) params.status = status;
  if (priority) params.priority = priority;
  if (assignedTo) params.assigned_to = assignedTo;

  const response = await api.get("/tasks", { params });
  return response.data;
};

/**
 * Lấy task theo ID
 */
const getTaskById = async (taskId) => {
  const response = await api.get(`/tasks/${taskId}`);
  return response.data;
};

/**
 * Tạo task mới
 */
const createTask = async (taskData) => {
  const response = await api.post("/tasks", taskData);
  return response.data;
};

/**
 * Cập nhật task
 */
const updateTask = async (taskId, taskData) => {
  const response = await api.put(`/tasks/${taskId}`, taskData);
  return response.data;
};

/**
 * Di chuyển task (Kanban / status / position)
 */
const moveTask = async (taskId, status, position = null) => {
  const response = await api.patch(`/tasks/${taskId}/move`, {
    status,
    position,
  });
  return response.data;
};

/**
 * Assign task cho user
 */
const assignTask = async (taskId, userId) => {
  const response = await api.patch(`/tasks/${taskId}/assign`, {
    assigned_to: userId,
  });
  return response.data;
};

/**
 * Xóa task
 */
const deleteTask = async (taskId) => {
  const response = await api.delete(`/tasks/${taskId}`);
  return response.data;
};

/**
 * Lấy task được assign cho user hiện tại
 */
const getMyAssignedTasks = async () => {
  const response = await api.get("/tasks/my/assigned");
  return response.data;
};

export default {
  getTasks,
  getTaskById,
  createTask,
  updateTask,
  moveTask,
  assignTask,
  deleteTask,
  getMyAssignedTasks,
};
