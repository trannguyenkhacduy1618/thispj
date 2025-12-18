import { useRoutes } from "react-router-dom";
import routes from "./routes";
import "./styles/global.css";

export default function App() {
  const routing = useRoutes(routes);
  return routing;
}
