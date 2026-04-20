import React from "react";
import { Link } from "react-router-dom";

export const Navbar = () => {
    return (
        <nav className="navbar navbar-expand-lg shadow-sm sticky-top"
            style={{ backgroundColor: "#566873", padding: "0.8rem 2rem" }}>
            <div className="container-fluid">

                <Link className="navbar-brand d-flex align-items-center" to="/">
                    <img src="src/front/assets/img/favicon.png" alt="Logo" width="40" className="me-2" />
                    <span style={{ color: "#ebf2f1", fontWeight: "bold", letterSpacing: "1px" }}>GECAP</span>
                </Link>

                <div className="d-flex gap-2 gap-md-3">
                    <button
                        className="btn btn-sm fw-bold"
                        style={{ backgroundColor: "#e8888c", color: "white", borderRadius: "8px" }}
                        onClick={() => {
                            const section = document.getElementById('portal-paciente');
                            if (section) section.scrollIntoView({ behavior: 'smooth' });
                        }}
                    >
                        <i className="fas fa-calendar-check me-2"></i>Portal Paciente
                    </button>
                    <Link to="/login" className="btn fw-bold"
                        style={{
                            backgroundColor: "#5e888c",
                            color: "#ebf2f1",
                            borderRadius: "8px",
                            padding: "8px 20px"
                        }}>
                        <i className="fas fa-user-md me-2"></i>Acceso Médicos
                    </Link>
                </div>
            </div>
        </nav>
    );
};