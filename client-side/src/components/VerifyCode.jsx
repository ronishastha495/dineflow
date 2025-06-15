import { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import axios from "axios";
import { VERIFY_CODE_URL } from "../api/auth";


const Verify = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const email = location.state?.email || ""; // fallback if no state

  const [code, setCode] = useState("");

  const handleVerify = async (e) => {
    e.preventDefault();
    try {
      await axios.post(VERIFY_CODE_URL, { email, code });
      navigate("/login"); // 👈 redirect after successful verification
    } catch (err) {
      console.error(err.response?.data || err.message);
    }
  };

  return (
    <div className="p-6 max-w-md mx-auto">
      <h1 className="text-2xl font-bold mb-4">Verify Email</h1>
      <p className="mb-2">Verification code has been sent to <strong>{email}</strong>.</p>
      <form onSubmit={handleVerify} className="space-y-4">
        <input
          type="text"
          placeholder="Enter verification code"
          value={code}
          onChange={(e) => setCode(e.target.value)}
          className="w-full border px-4 py-2"
        />
        <button type="submit" className="bg-blue-600 text-white px-4 py-2">
          Verify
        </button>
      </form>
    </div>
  );
};

export default Verify;
