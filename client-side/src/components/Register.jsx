import { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { REGISTER_URL } from "../api/auth";
import { toast } from "sonner";

const Register = () => {
  const [form, setForm] = useState({
    username: "",
    email: "",
    password: "",
    is_owner: false,
  });
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setForm((prev) => ({
      ...prev,
      [name]: type === "checkbox" ? checked : value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post(REGISTER_URL, form);
      toast.success("Registered successfully! Please verify your email.");
      navigate("/verify", { state: { email: form.email } });
    } catch (err) {
      const msg = err.response?.data?.email?.[0] || err.response?.data?.detail || "Registration failed.";
      toast.error(msg);
    }
  };

  return (
    <div className="p-6 max-w-md mx-auto">
      <h1 className="text-2xl font-bold mb-4">Register</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        <input name="username" placeholder="Username" value={form.username} onChange={handleChange} className="w-full border px-4 py-2" />
        <input name="email" type="email" placeholder="Email" value={form.email} onChange={handleChange} className="w-full border px-4 py-2" />
        <input name="password" type="password" placeholder="Password" value={form.password} onChange={handleChange} className="w-full border px-4 py-2" />
        <label className="flex items-center space-x-2">
          <input type="checkbox" name="is_owner" checked={form.is_owner} onChange={handleChange} />
          <span>Register as Restaurant Owner</span>
        </label>
        <button type="submit" className="bg-green-600 text-white px-4 py-2">
          Register
        </button>
      </form>
    </div>
  );
};

export default Register;
