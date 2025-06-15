import { createContext, useContext, useEffect, useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { LOGIN_URL, ME_URL } from "../api/auth";
import { toast } from "sonner";

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(() => localStorage.getItem("token") || "");
  const navigate = useNavigate();

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const res = await axios.get(ME_URL, {
          headers: { Authorization: `Bearer ${token}` },
        });
        setUser(res.data);
      } catch (err) {
        setUser(null);
        setToken("");
        localStorage.removeItem("token");
      }
    };

    if (token) fetchUser();
  }, [token]);

  const login = async (email, password) => {
    try {
      const res = await axios.post(LOGIN_URL, { email, password });
      const access = res.data.access;
      localStorage.setItem("token", access);
      setToken(access);
      toast.success("Logged in successfully!");
      navigate("/");
    } catch (err) {
      const msg = err.response?.data?.detail || "Login failed. Please try again.";
      toast.error(msg);
    }
  };

  const logout = () => {
    localStorage.removeItem("token");
    setUser(null);
    setToken("");
    toast.info("Logged out successfully.");
    navigate("/login");
  };

  return (
    <AuthContext.Provider value={{ user, token, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
