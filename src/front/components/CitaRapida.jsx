import React, { useState } from "react";

export const CitaRapida = () => {
    const [datos, setDatos] = useState({ 
        nombre: "", 
        telefono: "", 
        fecha: "", 
        motivo: "",
        otroMotivo: "" 
    });

    const handleSubmit = (e) => {
        e.preventDefault();       
        const motivoFinal = datos.motivo === "Otro" ? datos.otroMotivo : datos.motivo;
        
        console.log("Datos finales a enviar:", { ...datos, motivo: motivoFinal });
        alert(`Solicitud enviada. Motivo: ${motivoFinal}`);
    };

    return (
        <div className="container mt-5" style={{ maxWidth: "500px" }}>
            <h2 className="text-center mb-4" style={{ color: "#566873" }}>Solicitar Cita Médica</h2>
            <form onSubmit={handleSubmit} className="card p-4 shadow-sm border-0 bg-light">
                
                <div className="mb-3">
                    <label className="form-label fw-bold">Nombre Completo</label>
                    <input type="text" className="form-control" required 
                        onChange={(e) => setDatos({...datos, nombre: e.target.value})} />
                </div>

                <div className="mb-3">
                    <label className="form-label fw-bold">Teléfono</label>
                    <input type="tel" className="form-control" required 
                        onChange={(e) => setDatos({...datos, telefono: e.target.value})} />
                </div>

                <div className="mb-3">
                    <label className="form-label fw-bold">Fecha</label>
                    <input type="date" className="form-control" required 
                        onChange={(e) => setDatos({...datos, fecha: e.target.value})} />
                </div>

                <div className="mb-3">
                    <label className="form-label fw-bold">Motivo de la Consulta</label>
                    <select className="form-select" required 
                        onChange={(e) => setDatos({...datos, motivo: e.target.value})}>
                        <option value="">Selecciona una opción...</option>
                        <option value="Revision">Revisión General</option>
                        <option value="Urgencia">Urgencia</option>
                        <option value="Analitica">Analítica / Resultados</option>
                        <option value="Otro">Otro (Especificar)</option>
                    </select>
                </div>
               
                {datos.motivo === "Otro" && (
                    <div className="mb-3 animate__animated animate__fadeIn">
                        <label className="form-label fw-bold text-muted">Especifique el motivo</label>
                        <textarea 
                            className="form-control" 
                            rows="2" 
                            placeholder="Describa brevemente..."
                            required={datos.motivo === "Otro"}
                            onChange={(e) => setDatos({...datos, otroMotivo: e.target.value})}
                        ></textarea>
                    </div>
                )}

                <button type="submit" className="btn w-100 mt-3" 
                    style={{ backgroundColor: "#8ea69b", color: "white", fontWeight: "bold" }}>
                    Confirmar Solicitud
                </button>
            </form>
        </div>
    );
};