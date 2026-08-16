import { useEffect, useState } from "react";
import { Link, useLocation } from "react-router-dom";
import tissLogo from "../assets/tiss-logo.svg";
import { useAuth } from "../context/AuthContext";
import ThemeToggle from "./ThemeToggle";

function MenuIcon({ open }) {
  return (
    <svg width="20" height="20" viewBox="0 0 20 20" fill="none" aria-hidden="true">
      {open ? (
        <path d="M5 5L15 15M15 5L5 15" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" />
      ) : (
        <path d="M3 6H17M3 10H17M3 14H17" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" />
      )}
    </svg>
  );
}

export default function AppHeader() {
  const { user, logout } = useAuth();
  const location = useLocation();
  const [menuOpen, setMenuOpen] = useState(false);

  useEffect(() => {
    setMenuOpen(false);
  }, [location.pathname]);

  const navLinks = user && (
    <>
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
    </>
  );

  return (
    <header className="app-header">
      <div className="app-header-bar">
        <Link to="/" className="app-header-logo">
          <img src={tissLogo} alt="TISS" height="40" />
        </Link>

        {user && <nav className="app-header-nav app-header-nav--desktop">{navLinks}</nav>}

        <div className="app-header-actions">
          <ThemeToggle />
          {user && (
            <>
              <span className="app-header-user">{user.full_name}</span>
              <button type="button" className="btn btn-secondary app-header-logout" onClick={logout}>
                Log out
              </button>
              <button
                type="button"
                className="app-header-menu-btn"
                aria-expanded={menuOpen}
                aria-controls="app-header-mobile-nav"
                aria-label={menuOpen ? "Close menu" : "Open menu"}
                onClick={() => setMenuOpen((v) => !v)}
              >
                <MenuIcon open={menuOpen} />
              </button>
            </>
          )}
        </div>
      </div>

      {user && menuOpen && (
        <nav id="app-header-mobile-nav" className="app-header-nav app-header-nav--mobile">
          {navLinks}
          <button type="button" className="btn btn-secondary" onClick={logout}>
            Log out
          </button>
        </nav>
      )}
    </header>
  );
}
