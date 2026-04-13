import React from 'react';
import Calendario from './MiCalendario/Calendario';
import DoctorScheduleBar from "../components/DoctorScheduleBar/DoctorScheduleBar";

function Homeprivado() {
    const profesional = {
        nombre: "Juan Pérez",
    };

    return (
        <div>
            <div className="d-flex justify-content-between align-items-center mb-4 p-3 rounded shadow-sm bg-white border-start border-5">
                <div className='d-flex'>

                    <h2 className="text-secondary" style={{ color: "#b4d2d9", fontSize: "1em" }}>
                        Bienvenido <span className="mb-0 fw-bold" style={{ color: "#566873", fontSize: "1.5em" }}>
                            {profesional.nombre}!
                        </span>
                    </h2>
                </div>
                <span className="badge mt-2" style={{ backgroundColor: "#93bbbf" }}>Profesional Activo</span>
            </div>
            <div>
                <Calendario />
            </div>
            <div>

                <DoctorScheduleBar />

                <h2>Panel de control</h2>

            </div>
        </div> 
    );
};

export default Homeprivado;
