import React, { useState } from 'react';
import {
  Box,
  Typography,
  List,
  ListItem,
  ListItemText,
  Card,
  CardContent,
  Button,
} from '@mui/material';

function PredictionResult({ result }) {
  const [showDetails, setShowDetails] = useState(false);

  if (!result) return null;

  const { asset, date, prediction, signal, features } = result;

  return (
    <Card elevation={3}>
      <CardContent>
        <Typography variant="h5" gutterBottom>
          Resultado para {asset} em {date}
        </Typography>
        <Typography
          variant="h6"
          color={signal === 'Buy' ? 'green' : 'red'}
          gutterBottom
        >
          Sinal: {signal}
        </Typography>
        <Typography variant="body1" gutterBottom>
          <strong>Preço Previsto:</strong> ${prediction.toFixed(2)}
        </Typography>
        <Button
          variant="outlined"
          color="primary"
          onClick={() => setShowDetails(true)}
        >
          Ver Mais
        </Button>
      </CardContent>
      <GraphDialog
        open={showDetails}
        onClose={() => setShowDetails(false)}
        data={result.graphData}
      />
    </Card>
  );
}

export default PredictionResult;
