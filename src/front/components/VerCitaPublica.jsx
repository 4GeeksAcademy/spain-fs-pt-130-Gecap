import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

export const VerCitaPublica = () => {   
    const { citaId } = useParams(); 
    const [info, setInfo] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const cargarCita = async () => {
            try {
                
                const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/api/public-appointments/${citaId}`);
                const data = await response.json();

                if (response.ok) {
                    setInfo(data);
                } else {
                    console.error("No se encontró la información");
                }
            } catch (error) {
                console.error("Error de conexión", error);
            } finally {
                setLoading(false);
            }
        };

        if (citaId) cargarCita();
    }, [citaId]);

    if (loading) return <div className="container mt-5 text-center">Cargando detalles de la cita...</div>;
    
    if (!info || !info.citas || info.citas.length === 0) {
        return (
            <div className="container mt-5 alert alert-warning text-center">
                No se encontraron citas pendientes para el DNI: <strong>{citaId}</strong>
            </div>
        );
    }

    return (
        <div className="container mt-5 shadow-sm p-4 bg-white rounded" style={{ maxWidth: "600px" }}>
            <h2 className="text-center mb-4" style={{ color: "#566873" }}>Detalles de tu Cita</h2>
            <p className="mb-3">Hola, <strong>{info.paciente}</strong>. Estas son tus próximas citas:</p>
            
            <div className="list-group">
                {info.citas.map((c, index) => (
                    <div key={index} className="list-group-item mb-2 border rounded">
                        <div><strong>Fecha:</strong> {c.date}</div>
                        <div><strong>Horario:</strong> {c.start} - {c.end}</div>
                        <div><strong>Motivo:</strong> {c.reason}</div>
                        <div>
                            <strong>Estado:</strong> 
                            <span className={`badge ms-2 ${c.status === 'pendiente' ? 'bg-warning text-dark' : 'bg-success'}`}>
                                {c.status.toUpperCase()}
                            </span>
                        </div>
                    </div>
                ))}
            </div>
            <p className="text-muted mt-3 small text-center">Guarda este enlace para consultar tus citas en cualquier momento.</p>
        </div>
    );
};