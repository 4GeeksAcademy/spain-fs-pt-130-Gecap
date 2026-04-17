import React, { useState } from "react";
import { DayPilot, DayPilotCalendar } from "@daypilot/daypilot-lite-react";

const CitasPorDia = ({ fechaSeleccionada, createAppointment, onEliminarPaciente, events }) => {
    const [calendar, setCalendar] = useState(null);

    const config = {
        viewType: "Day",
        startDate: new DayPilot.Date(fechaSeleccionada), 
        events: events, 
        headerDateFormat: "dd/MM/yyyy",
        dayBeginsHour: 10,
        dayEndsHour: 21,
        heightSpec: "BusinessHoursNoScroll",
        durationBarVisible: false,

        onTimeRangeSelected: async (args) => {
            const modal = await DayPilot.Modal.prompt("Nueva cita", "Nombre y apellido del paciente:");
            calendar.clearSelection();

            if (modal.canceled || !modal.result) return;

            await createAppointment({
                patient_name: modal.result,
                user_id: 1, 
                date: args.start.toString("dd/MM/yyyy"),
                time: args.start.toString("HH:mm:ss"),
                status: "pending"
            });
        },

        onBeforeEventRender: args => {
            args.data.backColor = args.data.backColor || "#93c47d";
            args.data.fontColor = "white";
            args.data.borderRadius = "5px";
            
            args.data.areas = [
                {
                    right: 5,
                    top: 5,
                    width: 20,
                    height: 20,
                    text: "×",
                    style: "cursor:pointer; background:rgba(0,0,0,0.2); color:white; border-radius:50%; text-align:center; font-size:16px;",
                    onClick: (argsArea) => {
                        onEliminarPaciente(argsArea.source.id());
                    }
                }
            ];
        }
    };

    return (
        <div className="mt-3 border rounded shadow-sm overflow-hidden">
            <DayPilotCalendar {...config} controlRef={setCalendar} />
        </div>
    );
};

export default CitasPorDia;
