const BASE_URL = "http://localhost:8000/api/users";

// Auth Endpoints
export const REGISTER_URL = `${BASE_URL}/register/`;
export const LOGIN_URL = `${BASE_URL}/login/`;
export const ME_URL = `${BASE_URL}/me/`;

// Password Reset Flow
export const PASSWORD_RESET_URL = `${BASE_URL}/forgot-password/`;
export const VERIFY_CODE_URL = `${BASE_URL}/verify-reset-code/`;
