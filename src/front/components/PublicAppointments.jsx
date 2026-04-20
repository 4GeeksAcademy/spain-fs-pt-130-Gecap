import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

export const PublicAppointments = () => {
    const { dni } = useParams();
    const [datos, setDatos] = useState(null);

    useEffect(() => {
        const dniLimpio = dni.toUpperCase();
        fetch(`${import.meta.env.VITE_BACKEND_URL}/api/public-appointments/${dniLimpio}`)
            .then(res => res.json())
            .then(data => setDatos(data))
            .catch(err => console.error(err));
    }, [dni]);

    if (!datos) return <div className="text-center p-5 fw-bold" style={{ color: "#566873" }}>Buscando tus citas...</div>;

    return (
        <div style={{ backgroundColor: "#ebf2f1", minHeight: "100vh" }}>           
            <nav className="navbar shadow-sm mb-4 d-print-none" style={{ backgroundColor: "#566873" }}>
                <div className="container justify-content-center">
                    <span className="navbar-brand text-white fw-bold">GECAP - Portal del Paciente</span>
                </div>
            </nav>

            <div className="container py-4">
                <div className="row justify-content-center">
                    <div className="col-lg-8">                                                
                        <div className="d-flex justify-content-between align-items-center mb-4">
                            <div>
                                <h2 className="fw-bold m-0" style={{ color: "#566873" }}>Mis Citas</h2>
                                <p className="text-muted m-0">Hola, <strong>{datos.paciente}</strong></p>
                            </div>
                            <button 
                                className="btn btn-sm shadow-sm fw-bold d-print-none px-3 py-2" 
                                style={{ backgroundColor: "#5e888c", color: "white", borderRadius: "10px" }}
                                onClick={() => window.print()}
                            >
                                <i className="fas fa-print me-2"></i>Imprimir
                            </button>
                        </div>
                                               
                        <div className="d-flex flex-column gap-3">
                            {datos.citas && datos.citas.length > 0 ? (
                                datos.citas.map((cita) => (
                                    <div key={cita.id} className="card border-0 shadow-sm overflow-hidden" style={{ borderRadius: "15px" }}>
                                        <div className="row g-0">
                                            <div className="col-3 col-md-2 text-center text-white d-flex flex-column justify-content-center" 
                                                 style={{ backgroundColor: "#93bbbf", minHeight: "100px" }}>
                                                <span className="fw-bold d-block" style={{ fontSize: "1.2rem" }}>{cita.date.split('-')[2]}</span>
                                                <span className="small text-uppercase">{new Date(cita.date).toLocaleString('es-ES', { month: 'short' })}</span>
                                            </div>
                                            <div className="col-9 col-md-10 p-3 d-flex align-items-center justify-content-between">
                                                <div>
                                                    <h5 className="fw-bold mb-1" style={{ color: "#566873" }}>{cita.time} H.</h5>
                                                    <p className="text-muted mb-0 small"><i className="fas fa-stethoscope me-1"></i> {cita.reason}</p>
                                                </div>
                                                <span className="badge rounded-pill px-3" style={{ backgroundColor: "rgba(94, 136, 140, 0.1)", color: "#5e888c" }}>
                                                    Confirmada
                                                </span>
                                            </div>
                                        </div>
                                    </div>
                                ))
                            ) : (
                                <div className="text-center p-5 bg-white rounded-4 shadow-sm">
                                    <i className="fas fa-calendar-times fa-3x mb-3 opacity-25"></i>
                                    <p className="text-muted">No tienes próximas citas agendadas.</p>
                                </div>
                            )}
                        </div>
                       
                        <div className="d-none d-print-block mt-5 text-center border-top pt-4">
                            <p className="small text-muted">Documento generado por GECAP - Sistema de Gestión Sanitaria</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};