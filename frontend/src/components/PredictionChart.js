import React from 'react';
import { Image } from 'react-bootstrap';

function PredictionChart({ plot }) {
  return (
    <div>
      <Image src={`data:image/png;base64,${plot}`} alt="Gráfico de Previsão" fluid />
    </div>
  );
}

export default PredictionChart;
