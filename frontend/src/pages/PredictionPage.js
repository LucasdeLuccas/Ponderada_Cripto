import React, { useState } from 'react';
import PredictionButton from '../components/PredictionButton';
import PredictionChart from '../components/PredictionChart';
import { Container, Row, Col, Image } from 'react-bootstrap';

function PredictionPage() {
  const [predictionData, setPredictionData] = useState(null);

  const handlePrediction = (data) => {
    setPredictionData(data);
  };

  return (
    <Container style={{ marginTop: '20px' }}>
      <Row className="justify-content-md-center">
        <Col md="8" className="text-center">
          <Image src="/images/solana.png" alt="Solana" fluid style={{ maxWidth: '300px', marginBottom: '20px' }} />
          <h2>Previsão de Compra/Venda de Solana</h2>
          <PredictionButton onPrediction={handlePrediction} />
          {predictionData && (
            <div style={{ marginTop: '20px' }}>
              <h4>Recomendação para {predictionData.date}: {predictionData.prediction}</h4>
              <PredictionChart plot={predictionData.plot} />
            </div>
          )}
        </Col>
      </Row>
    </Container>
  );
}

export default PredictionPage;
