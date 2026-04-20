import React, { useState } from "react";
import useGlobalReducer from "../hooks/useGlobalReducer";
import { Link, useNavigate } from "react-router-dom";
import "../pages/SignUp.css";
import logo from "../assets/img/gecap_navbar_clean.png";

function SignUp() {
    const navigate = useNavigate();
    const { store, dispatch } = useGlobalReducer();
    const [formData, setFormData] = useState({
        firstName: "",
        lastName: "",
        email: "",
        password: "",
        confirmPassword: "",
        especialidad: "",
        numColegiado: "",
        role: "medico"
    });
    const [error, setError] = useState(null);
    const [showPassword, setShowPassword] = useState(false);

    const handleChange = (event) => {
        const { name, value } = event.target;
        setFormData({ ...formData, [name]: value });
    };

    const togglePasswordVisibility = () => {
        setShowPassword(!showPassword);
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        setError(null);

        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(formData.email)) {
            return setError("Por favor, introduce un correo electrónico válido.");
        }

        const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$/;
        if (!passwordRegex.test(formData.password)) {
            return setError("La contraseña debe tener al menos 8 caracteres, incluyendo una mayúscula, una minúscula y un número.");
        }

        if (formData.password !== formData.confirmPassword) {
            return setError("Las contraseñas no coinciden.");
        }

        try {
            const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/api/signup`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    email: formData.email,
                    password: formData.password,
                    nombre: formData.firstName,
                    apellidos: formData.lastName,
                    especialidad: formData.especialidad,
                    num_colegiado: formData.numColegiado,
                    role: formData.role
                })
            });

            const data = await response.json();

            if (response.ok) {
                localStorage.clear();

                localStorage.setItem("token", data.token);
                localStorage.setItem("role", data.role);
                localStorage.setItem("userName", data.user.nombre);

                dispatch({ type: "login", payload: data });

                window.location.href = "/areapersonal";

            } else {
                setError(data.msg || "Error en el registro");
            }
        } catch (error) {
            console.error("Error en signup:", error);
            setError("No se pudo conectar con el servidor. Verifica tu conexión.");
        }
    };

    return (
        <div className="signup-page d-flex justify-content-center align-items-center vh-100">

            <div className="d-flex flex-column align-items-center" style={{ width: "100%", maxWidth: "500px" }}>

                <div className="signup-card w-100">
                    <div className="signup-logo">
                        <img src={logo} alt="Logo GECAP" />
                    </div>

                    <h5 className="text-center mb-4 fw-bold" style={{ color: "#5e888c" }}>Registro de Profesional</h5>

                    {error && <div className="alert alert-danger p-2 small text-center">{error}</div>}

                    <form className="signup-form" onSubmit={handleSubmit} autoComplete="off">
                        <input type="password" style={{ display: 'none' }} autoComplete="new-password" />
                        <div className="row g-2 mb-3">
                            <div className="col-md-6">
                                <input type="text" name="firstName" placeholder="Nombre" className="form-control" value={formData.firstName} onChange={handleChange} required />
                            </div>
                            <div className="col-md-6">
                                <input type="text" name="lastName" placeholder="Apellidos" className="form-control" value={formData.lastName} onChange={handleChange} required />
                            </div>
                        </div>

                        <input type="email" name="email" className="form-control mb-3" placeholder="Correo electrónico profesional" value={formData.email} onChange={handleChange} required />

                        <div className="row g-2 mb-3">
                            <div className="col-md-6">
                                <input type="text" name="especialidad" placeholder="Especialidad" className="form-control" value={formData.especialidad} onChange={handleChange} required />
                            </div>
                            <div className="col-md-6">
                                <input type="text" name="numColegiado" placeholder="Nº Colegiado" className="form-control" value={formData.numColegiado} onChange={handleChange} required />
                            </div>
                        </div>

                        <div className="input-group mb-3">
                            <input type={showPassword ? "text" : "password"} name="password" className="form-control" placeholder="Contraseña" value={formData.password} onChange={handleChange} autoComplete="new-password" required />
                            <span className="input-group-text bg-light border-0" onClick={togglePasswordVisibility} style={{ cursor: "pointer" }}>
                                <i className={`fas ${showPassword ? "fa-eye-slash" : "fa-eye"}`} style={{ color: "#5e888c" }}></i>
                            </span>
                        </div>

                        <div className="input-group mb-3">
                            <input type={showPassword ? "text" : "password"} name="confirmPassword" className="form-control" placeholder="Confirmar contraseña" value={formData.confirmPassword} onChange={handleChange} autoComplete="new-password" required />
                        </div>

                        <button type="submit" className="mt-2 w-100 btn text-white" style={{ backgroundColor: "#5e888c" }}>
                            Crear cuenta profesional
                        </button>
                    </form>
                    <div className="signup-links">
                        <Link to="/login">¿Ya tienes una cuenta? Inicia sesión</Link>
                    </div>
                </div>

                <div className="text-center mt-4 w-100" style={{ position: "relative", zIndex: 999 }}>
                    <Link to="/" className="text-decoration-none small fw-bold" style={{ color: "#5e888c", display: "inline-block" }}>
                        <i className="fas fa-arrow-left me-2"></i>Volver a la página principal
                    </Link>
                </div>
            </div>
        </div>
    );
}

export default SignUp;