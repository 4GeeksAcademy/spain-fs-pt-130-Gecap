import React, { useState, useEffect } from "react";
import { DayPilot, DayPilotCalendar } from "@daypilot/daypilot-lite-react";


const CitasPorDia = ({ fechaSeleccionada, onAgregarPaciente, onEliminarPaciente }) => {

    const [calendar, setCalendar] = useState(null);
    const [misCitas, setMisCitas] = useState([]);
    const [showModal, setShowModal] = useState(false);
    const [selectedRange, setSelectedRange] = useState({ start: null, end: null });

    const [formData, setFormData] = useState({
        nombre: "",
        telefono: "",
        motivo: "",
        otroMotivo: ""
    });

    useEffect(() => {
        if (!calendar || calendar.disposed())
            return;

        calendar.update({
            startDate: new DayPilot.Date(fechaSeleccionada),
            events: misCitas,

        });
    }, [calendar, fechaSeleccionada, misCitas]);


    const handleGuardarCita = () => {
        // Validaciones
        if (!formData.nombre.trim()) {
            alert("El nombre es obligatorio");
            return;
        }

        if (formData.telefono.length !== 9) {
            alert("El teléfono debe tener 9 números");
            return;
        }
        const motivoFinal =
            formData.motivo === "Otro"
                ? formData.otroMotivo
                : formData.motivo;

        if (!motivoFinal.trim()) {
            alert("El motivo de consulta es obligatorio");
            return;
        }
    

        const nuevaCita = {
            id: DayPilot.guid(),
            text: `${formData.nombre} - ${motivoFinal}`,
            start: selectedRange.start,
            end: selectedRange.end,
            backColor: "#93c47d",
        };

        setMisCitas(prev => [...prev, nuevaCita]);

        onAgregarPaciente({
            id: nuevaCita.id,
            hora: new Date(selectedRange.start).toLocaleTimeString([], {
                hour: "2-digit",
                minute: "2-digit"
            }),
            nombre: formData.nombre,
            motivo: motivoFinal,
            telefono: formData.telefono,
            start: selectedRange.start,
            end: selectedRange.end
        });

        setShowModal(false);

        setFormData({
            nombre: "",
            telefono: "",
            motivo: ""
        });

        if (calendar) {
            calendar.clearSelection();
        }
    };

    const config = {
        viewType: "Day",
        headerDateFormat: "dd/MM/yyyy",
        columns: [{ name: "Agenda Médica", id: "C1" }],
        dayBeginsHour: 10,
        dayEndsHour: 21,
        businessBeginsHour: 10,
        businessEndsHour: 21,
        heightSpec: "BusinessHoursNoScroll",
        headerHeight: 50,
        cellHeight: 40,
        theme: "calendar_default",
        durationBarVisible: false,

        onTimeRangeSelected: async (args) => {
            setSelectedRange({
                start: args.start,
                end: args.end
            });

            setShowModal(true);

            if (calendar) {
                calendar.clearSelection();
            }
        },

        onBeforeEventRender: args => {
            if (!args.data.backColor) {
                args.data.backColor = "#93c47d";
            }

            args.data.borderColor = "darker";
            args.data.fontColor = "white";
            args.data.areas = [
                {
                    right: 5,
                    top: 8,
                    width: 18,
                    height: 18,
                    fontColor: "#fff",
                    text: "X",
                    style: "cursor:pointer; background-color: rgba(0,0,0,0.2); border-radius: 50%; text-align: center; line-height: 18px;",
                    onClick: (argsArea) => {
                        const elimina = argsArea.source;
                        const id = elimina.id();

                        setMisCitas(prev =>
                            prev.filter(cita => cita.id !== id)
                        );

                        onEliminarPaciente(id);
                    }

                }
            ];
        }
    };


return (
    <div className="mt-3 border rounded shadow-sm overflow-hidden">
        <DayPilotCalendar {...config} controlRef={setCalendar} />

        {showModal && (
            <div style={{
                position: "fixed",
                top: 0,
                left: 0,
                width: "100%",
                height: "100%",
                background: "rgba(0,0,0,0.5)",
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
                zIndex: 9999
            }}>
                <div style={{
                    background: "white",
                    padding: "20px",
                    borderRadius: "10px",
                    minWidth: "320px",
                    display: "flex",
                    flexDirection: "column",
                    gap: "10px"
                }}>
                    <h3>Nueva cita</h3>

                    <input
                        type="text"
                        placeholder="Nombre"
                        value={formData.nombre}
                        onChange={(e) =>
                            setFormData({ ...formData, nombre: e.target.value })
                        }
                    />

                    <input
                        type="tel"
                        placeholder="Teléfono"
                        value={formData.telefono}
                        onChange={(e) =>
                            setFormData({
                                ...formData,
                                telefono: e.target.value.replace(/\D/g, "").slice(0, 9)
                            })
                        }
                    />

                    
                    <select className="form-control"
                            value={formData.motivo}
                            onChange={(e) =>
                                setFormData({ ...formData, motivo: e.target.value })
                            }
                        >
                            <option value="">Selecciona un motivo</option>
                            <option value="Pediatra">Pediatra</option>
                            <option value="Revisión">Revisión</option>
                            <option value="Consulta general">Consulta general</option>
                            <option value="Urgencia">Urgencia</option>
                            <option value="Control">Control</option>
                            <option value="Otro">Otro</option>
                    </select> 

                    {formData.motivo === "Otro" && (
                        <input
                            type="text"
                            placeholder="Escribe el motivo"
                            value={formData.otroMotivo}
                            onChange={(e)  =>
                                setFormData({ ...formData, otroMotivo: e.target.value})
                            }
                        />
                    )}

                    <div style={{
                        display: "flex",
                        gap: "10px",
                        justifyContent: "flex-end",
                        marginTop: "10px"
                    }}>
                        <button onClick={handleGuardarCita}>Guardar</button>
                        <button onClick={() => {
                            setShowModal(false);
                            setFormData({
                                nombre: "",
                                telefono: "",
                                motivo: ""
                            });
                        }}>
                            Cancelar
                        </button>
                    </div>
                </div>
            </div>
        )}
        
    </div>
);
};

export default CitasPorDia;
