import { Link, useLocation } from "react-router-dom";
import tissLogo from "../assets/tiss-logo.svg";
import { useAuth } from "../context/AuthContext";
import ThemeToggle from "./ThemeToggle";

export default function AppHeader() {
  const { user, logout } = useAuth();
  const location = useLocation();

  return (
    <header className="app-header">
      <Link to="/" className="app-header-logo">
        <img src={tissLogo} alt="TISS" height="44" />
      </Link>

      {user && (
        <nav className="app-header-nav">
          <Link to="/" className={location.pathname === "/" ? "active" : ""}>
            Dashboard
          </Link>
          <Link to="/courses" className={location.pathname === "/courses" ? "active" : ""}>
            Courses
          </Link>
          {user.role === "admin" && (
            <Link to="/admin/courses" className={location.pathname === "/admin/courses" ? "active" : ""}>
              Manage
            </Link>
          )}
        </nav>
      )}

      <div className="app-header-actions">
        <ThemeToggle />
        {user && (
          <>
            <span className="app-header-user">{user.full_name}</span>
            <button type="button" className="btn btn-secondary" onClick={logout}>
              Log out
            </button>
          </>
        )}
      </div>
    </header>
  );
}
