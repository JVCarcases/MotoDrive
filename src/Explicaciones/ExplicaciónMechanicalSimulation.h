/*
Función que se ejecuta en cada frame. Recibe un valor float que representa el tiempo.
*/
void UMotorcycleSimulation::ProcessMechanicalSimulation(float DeltaTime)
{
    /*
    PVehicle es un objeto de la clase FMBSimpleWheeledVehicle, que es únicamente un container para encapsular los componentes de simulación principales del vehículo. 
    El método HasEngine() se encarga de verificar que el número de motores mínimo que tiene el vehículo es al menos uno.
    
        bool HasEngine() const
        {
            return (Engine.Num() > 0);
        }
    */
    if (PVehicle->HasEngine())
	{
        /*
        A partir de PVehicle, se obtienen los componentes de simulación y se almacenan en las variables pertinentes. 
        La declaración de auto& indica lo siguiente: En lugar de especificar explícitamente el tipo de datos de la variable, el compilador deducirá automáticamente el tipo
        basándose en el tipo de la expresión a la que está siendo designada. La presencia del operador & indica que será una referencia al objeto devuelto por el método que lo invoca.

        Entonces, en el caso por ejemplo de GetEngine() y el objeto que devuelva (Engine), entonces PEngine será una referencia a este objeto, y cualquier modificación hecha a través de 
        este último afectará directamente al objeto original devuelto por GetEngine().
        */
        auto& PEngine = PVehicle->GetEngine();
		auto& PTransmission = PVehicle->GetTransmission();
		auto& PDifferential = PVehicle->GetDifferential();

        /*
        Se declara una variable float (WheelRPM)

        Se realiza un bucle for en el que se itera en cada rueda almacenada en PVehicle.
        Dentro de cada iteración, se verifica si la instancia de la rueda tiene la variable EngineEnabled en True. Esta variable parece indicar si la rueda se mueve por influencia del motor. 
        En caso positivo, se actualiza el valor de WheelRPM obtenido a partir de la variable almacenada en GetWheelRPM() de la instancia de la rueda a evaluar.
        Aparentemente, WheelRPM se actualiza con la última variable que tenga establecido EngineEnabled en True. Se presupone que todas las ruedas influenciadas por el motor van a tener las mismas RPM.
        
        La función GetWheelRPM() devuelve OmegaToRPM en función de Omega.
        */
        float WheelRPM = 0;
		for (int I = 0; I < PVehicle->Wheels.Num(); I++)
		{
			if (PVehicle->Wheels[I].EngineEnabled)
			{
				WheelRPM = FMath::Abs(PVehicle->Wheels[I].GetWheelRPM());
			}
		}

        /*
        Con la variable obtenida de WheelRPM, se llama a la función GEtEngineRPMFromWheelRPM pasando como argumento el WheelRPM. Esta función realiza lo siguiente:
        
        Get the expected engine RPM from the wheel RPM taking into account the current gear ratio (assuming no clutch slip)
            float GetEngineRPMFromWheelRPM(float InWheelRPM)
            {
                return InWheelRPM * GetGearRatio(GetCurrentGear());
            }
        */
        float WheelSpeedRPM = FMath::Abs(PTransmission.GetEngineRPMFromWheelRPM(WheelRPM));

        /*Establece las RPM del motor en base a si la transmisión está o no en neutro y las RPM calculadas. El método SetEngineRPM hace lo siguiente:

         * When the wheels are in contact with the ground and clutch engaged then the load 
		 * on the engine from the wheels determines the engine speed. With no clutch simulation
		 * just setting the engine RPM directly to match the wheel speed.
		 */
		void SetEngineRPM(bool FreeRunningIn, float InEngineRPM)
		{
			FreeRunning = FreeRunningIn;
			if (!FreeRunning)
			{
				TargetSpeed = RPMToOmega(FMath::Clamp(FMath::Abs(InEngineRPM), (float)Setup().EngineIdleRPM, (float)Setup().MaxRPM));
			}
		}
        //La función clamp asegura que el valor de las RPM se encuentre entre las idle RPM y las MaxRPM. Si se sale del rango se asigna el valor de las idle o MaxRPM.
        
		PEngine.SetEngineRPM(PTransmission.IsOutOfGear(), PTransmission.GetEngineRPMFromWheelRPM(WheelRPM));

        // Simula el comportamiento del motor en el tiempo dado. El método es el siguiente:
            void FMBSimpleEngineSim::Simulate(float DeltaTime)
            {
                if (!EngineStarted)
                {
                    return;
                }
                
                // Si el motor se encuentra enposición neutral
                if (FreeRunning)
                {
                    // Guarda el valor actual de la velocidad angular Omega para futuros cálculos
                    float PrevOmega = Omega;

                    // Incrementa Omega basado en el torque del motor, el tiempo transcurrido y el momento de inercia. El método GetEngineTorque es el siguiente:

                    /*float FMBEngineSimModule::GetEngineTorque(float ThrottlePosition, float EngineRPM)
                    {
                        if (EngineStarted)
                        {
                            return ThrottlePosition * GetTorqueFromRPM(EngineRPM);
                        }

                        return 0.f;
                    }
                    */
                // Se múltiplica ThrotlePosition que es un valor entre 0 y 1 porque es la entrada del acelerador, por el Torque que se lee de la curva. GetTorqueRPM llama a su ve a GetValue que es el método que modificamos para que cogiera los valores
                // directamente de la curva.
                    Omega += GetEngineTorque() * DeltaTime / Setup().EngineRevUpMOI;

                    // Calcula la desaceleración usando una fórmula basada en la diferencia entre Omega y la media entre la velocidad en ralentí y la máxima. Haciendo in análisis dimensional, EngineRevDownRate está en
                    // 1/s^2
                    float Decel = Setup().EngineRevDownRate * Sqr((Omega - 0.5f*EngineIdleSpeed) / MaxEngineSpeed);

                    // Aplica la desaceleración a Omega.
                    Omega -= Decel * DeltaTime;

                    // Calcula la tasa de revoluciones por minuto (RPM) basándose en el cambio de Omega y el tiempo transcurrido.
                    RevRate = (Omega - PrevOmega) / DeltaTime;
                }
                // Si hay una marcha metida
                else
                {
                    // Guarda el valor actual de Omega para futuros cálculos.
                    float PrevOmega = Omega;

                    // Ajusta Omega para acercarse al TargetSpeed, utilizando una aproximación rápida.
                    Omega += (TargetSpeed - Omega) * 4.0f * DeltaTime;// / Setup().EngineRevUpMOI;

                    RevRate = (Omega - PrevOmega) / DeltaTime;
                }

                // Garantiza que el Omega nunca sea inferior a la velocidad en ralentí del motor para evitar que se apague.
                if (Omega < EngineIdleSpeed)
                {
                    Omega = EngineIdleSpeed;
                }	
                
                // Convierte la velocidad angular Omega a RPM para actualizar la RPM actual del motor.
                CurrentRPM = OmegaToRPM(Omega);
            }
		PEngine.Simulate(DeltaTime);

        // Establece las RPM del motor en la transmisión para controlar los cambios de marcha en una caja automática.
		PTransmission.SetEngineRPM(PEngine.GetEngineRPM());
        // Determina si es posible cambiar de marcha dependiendo de si el vehículo está en el aire o si alguna rueda está girando libremente.
		PTransmission.SetAllowedToChangeGear(!VehicleState.bVehicleInAir && !IsWheelSpinning());
        // Obtiene la relación de la marcha actual en la transmisión.
		float GearRatio = PTransmission.GetGearRatio(PTransmission.GetCurrentGear());

        // Simula el comportamiento de la transmisión en el tiempo dado.
		PTransmission.Simulate(DeltaTime);

        // Calcula el torque de transmisión basado en el torque del motor.
		float TransmissionTorque = PTransmission.GetTransmissionTorque(PEngine.GetEngineTorque());
        // Si las RPM de la rueda exceden el máximo RPM del motor, establece el torque de transmisión a 0.
		if (WheelSpeedRPM > PEngine.Setup().MaxRPM)
		{
			TransmissionTorque = 0.f;
		}

        // Aplica el torque de transmisión a las ruedas.
		for (int WheelIdx = 0; WheelIdx < PVehicle->Wheels.Num(); WheelIdx++)
		{
			auto& PWheel = PVehicle->Wheels[WheelIdx];
            // Si la configuración de la rueda permite ser impulsada por el motor, aplica el torque convertido.
			if (PWheel.Setup().EngineEnabled)
			{
				PWheel.SetDriveTorque(TorqueMToCm(TransmissionTorque) * PWheel.Setup().TorqueRatio);
			}
            // Si la rueda no está habilitada para ser impulsada por el motor, establece su torque a 0.
			else
			{
				PWheel.SetDriveTorque(0.f);
			}
		}

	}
}