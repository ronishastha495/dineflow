import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const HomePage = () => {
  const { user, logout } = useAuth();

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 px-4">
      <div className="w-full max-w-2xl text-center bg-white shadow-md rounded-xl p-8">
        <h1 className="text-4xl font-bold text-gray-800 mb-6">Welcome to DineFlow</h1>

        {user ? (
          <>
            <p className="mb-6 text-gray-700">
              Logged in as: <span className="font-semibold">{user.username}</span> (
              {user.is_owner ? "Restaurant Owner" : "Customer"})
            </p>
            <div className="flex flex-wrap justify-center gap-4">
              <Link
                to="/dashboard"
                className="bg-blue-600 hover:bg-blue-700 text-white font-medium px-6 py-2 rounded-lg transition"
              >
                Go to Dashboard
              </Link>

              <Link
                to="/verify"
                className="bg-yellow-500 hover:bg-yellow-600 text-white font-medium px-6 py-2 rounded-lg transition"
              >
                Verify Account
              </Link>

              <button
                onClick={logout}
                className="bg-red-500 hover:bg-red-600 text-white font-medium px-6 py-2 rounded-lg transition"
              >
                Logout
              </button>
            </div>
          </>
        ) : (
          <div className="flex justify-center space-x-4">
            <Link
              to="/login"
              className="bg-blue-600 hover:bg-blue-700 text-white font-medium px-6 py-2 rounded-lg transition"
            >
              Login
            </Link>
            <Link
              to="/register"
              className="bg-green-600 hover:bg-green-700 text-white font-medium px-6 py-2 rounded-lg transition"
            >
              Register
            </Link>
          </div>
        )}
      </div>
    </div>
  );
};

export default HomePage;
