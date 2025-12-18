import { Navigate } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import Tasks from "./pages/Tasks";
import TimeTracking from "./pages/TimeTracking";
import Reports from "./pages/Reports";
import Login from "./pages/Login";
import authService from "./services/authService";

/**
 * Route bảo vệ (yêu cầu đăng nhập)
 */
const PrivateRoute = ({ children }) => {
    return authService.isAuthenticated() ? children : <Navigate to="/login" replace />;
};

/**
 * Khai báo toàn bộ routes
 */
const routes = [
    {
        path: "/login",
        element: <Login />,
    },
{
    path: "/",
    element: (
        <PrivateRoute>
        <Dashboard />
        </PrivateRoute>
    ),
},
{
    path: "/tasks",
    element: (
        <PrivateRoute>
        <Tasks />
        </PrivateRoute>
    ),
},
{
    path: "/time",
    element: (
        <PrivateRoute>
        <TimeTracking />
        </PrivateRoute>
    ),
},
{
    path: "/reports",
    element: (
        <PrivateRoute>
        <Reports />
        </PrivateRoute>
    ),
},
// fallback
{
    path: "*",
    element: <Navigate to="/" replace />,
},
];

export default routes;
