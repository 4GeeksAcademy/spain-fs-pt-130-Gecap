import React, { useState } from 'react';
import DatePicker from 'react-datepicker';
import "react-datepicker/dist/react-datepicker.css";
import { es } from "date-fns/locale/es";
import Scheduler from './Citaspordia';

function Calendario() {
    const [startDate, setStartDate] = useState(new Date());

    const manejarSeleccionDia = (date) => {
        setStartDate(date);
        // Aquí vamos cargar datos de una API, yo diria que la de calendly pero tendriamos que verlo
        console.log("Cargando observaciones para:", date);
    };

    return (
        <div className=" mt-4">
            <div className="d-flex gap-3 align-items-start">
                
                <div className="card border-0 shadow-sm flex-grow-1">
                    <div className="card-body">
                        <h6 className="card-title text-muted">
                            Agenda del día: <strong>{startDate.toLocaleDateString('es-ES', { day: 'numeric', month: 'long', year: 'numeric' })}</strong>
                        </h6>
                        <hr />
                        <div className="mt-2">
                          
                            <p className="text-secondary">CITAS DE HOY.</p>
                            <Scheduler fechaSeleccionada={startDate} />
                            <textarea 
                                className="form-control border-0 bg-light" 
                                rows="2" 
                                placeholder="Escribir nueva observación..."
                            ></textarea>
                        </div>
                    </div>
                </div>


                <div className='contenedor-calendario shadow-sm bg-white p-2 rounded'>
                    <DatePicker selected={startDate} onChange={manejarSeleccionDia} inline locale={es} outsideClickIgnoreClass="react-datepicker__day--outside-month"/>
                </div>
            </div>

            <style>{`
                .react-datepicker__day--outside-month {
                    visibility: hidden !important;
                    pointer-events: none;
                }
                .react-datepicker {
                    border: none !important;
                    font-family: inherit;
                }
                .react-datepicker__header {
                    background-color: white !important;
                    border-bottom: 1px solid #f0f0f0 !important;
                }
                .react-datepicker__day--selected {
                    background-color: #93bbbf !important;
                    border-radius: 50% !important;
                }
            `}</style>
        </div>
    );
}

export default Calendario;