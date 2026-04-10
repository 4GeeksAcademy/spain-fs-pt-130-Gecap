import React, { useState, useEffect } from "react";
import { DayPilot, DayPilotCalendar } from "@daypilot/daypilot-lite-react";

const Scheduler = ({ fechaSeleccionada }) => {
    const [calendar, setCalendar] = useState(null);

    const [config, setConfig] = useState({
        viewType: "Day",
        headerDateFormat: "dd/MM/yyyy",
        startDate: DayPilot.Date.today(),
        columns: [{ name: "Citas Médicas", id: "C1" }],
        headerHeight: 40,
        cellHeight: 30,
        theme: "calendar_default",
    });

    useEffect(() => {
        if (calendar && fechaSeleccionada) {
            try {
                const nuevaFecha = new DayPilot.Date(fechaSeleccionada);
                calendar.update({
                    startDate: nuevaFecha
                });
            } catch (e) {
                console.warn("Error al actualizar calendario:", e);
            }
        }
    }, [calendar, fechaSeleccionada]);

    return (
        <div className="mt-3 border rounded shadow-sm overflow-hidden" style={{ height: "400px" }}>
            <DayPilotCalendar 
                {...config} 
                controlRef={setCalendar} 
            />
        </div>
    );
};

export default Scheduler;