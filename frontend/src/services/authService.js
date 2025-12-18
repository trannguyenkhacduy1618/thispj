import api from "./api";

const USER_KEY = "current_user";
const TOKEN_KEY = import.meta.env.VITE_AUTH_TOKEN_KEY || "access_token";

/**
 * Login
 */
const login = async (username, password) => {
  const response = await api.post(
    "/auth/login",
    new URLSearchParams({
      username,
      password,
    }),
    {
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
    }
  );

  const { access_token, user } = response.data;

  // Lưu token & user
  localStorage.setItem(TOKEN_KEY, access_token);
  localStorage.setItem(USER_KEY, JSON.stringify(user));

  return user;
};

/**
 * Logout
 */
const logout = () => {
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(USER_KEY);
};

/**
 * Lấy token hiện tại
 */
const getToken = () => {
  return localStorage.getItem(TOKEN_KEY);
};

/**
 * Lấy user hiện tại
 */
const getCurrentUser = () => {
  const user = localStorage.getItem(USER_KEY);
  return user ? JSON.parse(user) : null;
};

/**
 * Kiểm tra đã login chưa
 */
const isAuthenticated = () => {
  return !!getToken();
};

export default {
  login,
  logout,
  getToken,
  getCurrentUser,
  isAuthenticated,
};
