import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

export const VerCitaPublica = () => {
    const { citaId } = useParams(); 
    const [cita, setCita] = useState(null);

    useEffect(() => {
        
        setCita({
            nombre: "Usuario Invitado",
            fecha: "2024-05-20",
            motivo: "Revisión General",
            estado: "Confirmada"
        });
    }, [citaId]);

    if (!cita) return <div className="container mt-5">Cargando cita...</div>;

    return (
        <div className="container mt-5 shadow-sm p-4 bg-white rounded" style={{ maxWidth: "600px" }}>
            <h2 className="text-center mb-4">Detalles de tu Cita</h2>
            <div className="list-group">
                <div className="list-group-item"><strong>Paciente:</strong> {cita.nombre}</div>
                <div className="list-group-item"><strong>Fecha:</strong> {cita.fecha}</div>
                <div className="list-group-item"><strong>Motivo:</strong> {cita.motivo}</div>
                <div className="list-group-item"><strong>Estado:</strong> <span className="badge bg-success">{cita.estado}</span></div>
            </div>
            <p className="text-muted mt-3 small text-center">Guarda este enlace para consultar tu cita en cualquier momento.</p>
        </div>
    );
};