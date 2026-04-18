import React from 'react';
import Calendario from "./Calendario/Calendario";
import { useState, useEffect } from 'react';
import DoctorScheduleBar from "./DoctorScheduleBar/DoctorScheduleBar";

function AreaPersonal() {
    const [pacientesHoy, setPacientesHoy] = useState([]);
    const profesional = { nombre: "Juan Pérez" };

    useEffect(() => {
        fetch(`${import.meta.env.VITE_BACKEND_URL}/api/appointments`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${localStorage.getItem("token")}`
            }
        })
            .then((response) => {
                if (!response.ok) throw new Error("Error en la carga de citas");
                return response.json();
            })
            .then((data) => {
                console.log("Citas cargadas:", data);
                setPacientesHoy(data);
            })
            .catch((error) => console.error("Error:", error));
    }, []);

    const stats = {
        totalPacientes: pacientesHoy.length,
    };
    const eliminarPaciente = (id) => {
        setPacientesHoy(prev => prev.filter(p => p.id !== id));
    };
    return (
        <div className="container-fluid" style={{ minHeight: "100vh" }}>

            <div className="card border-0 shadow-sm" style={{ borderRadius: "15px", overflow: "hidden" }}>
                <div style={{ height: "6px", backgroundColor: "#93bbbf" }}></div>

                <div className="card-body py-2 px-1">
                    <div className="d-flex justify-content-between align-items-center mb-2 mx-3">
                        <div>
                            <span className="badge rounded-pill" style={{ fontSize: "0.9rem", backgroundColor: "rgba(147, 187, 191, 0.2)", color: "#566873", border: "1px solid #93bbbf" }}>
                                <i className="fas fa-circle me-1" style={{ fontSize: "0.9rem" }}></i> Profesional Activo
                            </span>
                        </div>

                        <div className="text-end">
                            <p className="text-muted mb-0" style={{ fontSize: "1.3rem" }}>
                                Bienvenido, <span className="fw-bold" style={{ color: "#4a5568" }}>{profesional.nombre}!</span>
                            </p>
                        </div>
                    </div>

                    <div className="px-1">
                        <DoctorScheduleBar appointments={pacientesHoy} />
                    </div>
                </div>
            </div>

            <div className="col-md-12 mt-4">
                <div className="card border-0 shadow-sm h-100" style={{ borderRadius: "20px", overflow: "hidden" }}>                  
                    <div style={{ height: "6px", width: "100%", backgroundColor: "#93bbbf" }}></div>
                    <div className="card-body p-3">
                        <Calendario onAgregarPaciente={(nuevoPaciente) =>
                            setPacientesHoy(prev => [...prev, nuevoPaciente])
                        }
                            onEliminarPaciente={(id) =>
                                setPacientesHoy(prev => prev.filter(p => p.id !== id))} />                     
                    </div>
                </div>
            </div>

        </div>
    );
}

export default AreaPersonal;
