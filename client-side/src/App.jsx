import { Routes, Route, Navigate } from "react-router-dom";
import Login from "./components/Login";
import Register from "./components/Register";
import Verify from "./components/VerifyCode";
import HomePage from "./pages/Home";
import UserDashboard from "./pages/UserDashboard";
import OwnerDashboard from "./pages/OwnerDashboard";
import { useAuth } from "./context/AuthContext";
import { Toaster } from "sonner";

const App = () => {
  const { user } = useAuth();

  return (
    <Routes>
       <Toaster position="top-right" richColors />
      <Route path="/" element={<HomePage />} />
      <Route path="/login" element={!user ? <Login /> : <Navigate to="/" />} />
      <Route path="/register" element={!user ? <Register /> : <Navigate to="/" />} />
      <Route path="/verify" element={<Verify />} />

      {/* Protected Route */}
      <Route
        path="/dashboard"
        element={
          user ? (
            user.is_owner ? <OwnerDashboard /> : <UserDashboard />
          ) : (
            <Navigate to="/login" />
          )
        }
      />
    </Routes>
  );
};

export default App;
