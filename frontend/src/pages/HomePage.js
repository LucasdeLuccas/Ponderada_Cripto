import React, { useState } from 'react';
import {
  Container,
  Typography,
  Box,
  Button,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Paper,
} from '@mui/material';
import axios from 'axios';
import GraphDialog from '../components/GraphDialog'; // Certifique-se de que o caminho está correto

const assets = ['Bitcoin', 'Ethereum', 'BNB', 'Solana', 'Dogecoin'];

function HomePage() {
  const [asset, setAsset] = useState('Bitcoin');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [showGraph, setShowGraph] = useState(false);
  const [error, setError] = useState(''); // Definição do estado 'error'

  const handleSubmit = async () => {
    if (!asset) {
      setError('Por favor, selecione um criptoativo.');
      return;
    }
  
    setLoading(true);
    setError('');
    try {
      const response = await axios.get('http://backend:5001/predict', { // Alterado para 'http://backend:5000/predict'
        params: { asset },
      });
      setResult(response.data);
    } catch (error) {
      console.error(error);
      if (error.response && error.response.data && error.response.data.error) {
        setError(`Erro: ${error.response.data.error}`);
      } else {
        setError('Erro ao obter os dados. Por favor, tente novamente mais tarde.');
      }
    }
    setLoading(false);
  };

  return (
    <Container maxWidth="md" sx={{ mt: 4 }}>
      {/* Seção de Informação */}
      <Box textAlign="center" mb={4}>
        <Typography variant="h3" gutterBottom>
          Bem-vindo ao CryptoPredictor
        </Typography>
        <Typography variant="h6" color="textSecondary">
          Seu sistema de previsão para investimentos em criptoativos.
        </Typography>
      </Box>

      {/* Animação ou Imagem */}
      <Box display="flex" justifyContent="center" mb={4}>
        <img
          src="/assets/images/crypto_animation.gif"
          alt="Animação Cripto"
          style={{ maxWidth: '100%', height: 'auto' }}
        />
      </Box>

      {/* Formulário de Consulta */}
      <Paper elevation={3} sx={{ p: 4 }}>
        <Box display="flex" flexDirection="column" alignItems="center">
          <FormControl fullWidth margin="normal">
            <InputLabel id="asset-label">Criptoativo</InputLabel>
            <Select
              labelId="asset-label"
              value={asset}
              label="Criptoativo"
              onChange={(e) => setAsset(e.target.value)}
            >
              {assets.map((a) => (
                <MenuItem key={a} value={a}>
                  {a}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
          <Button
            variant="contained"
            color="primary"
            fullWidth
            sx={{ mt: 2 }}
            onClick={handleSubmit}
            disabled={loading}
          >
            {loading ? 'Consultando...' : 'Consultar'}
          </Button>
          {/* Exibir Mensagem de Erro */}
          {error && (
            <Typography variant="body1" color="error" mt={2}>
              {error}
            </Typography>
          )}
        </Box>
      </Paper>

      {/* Resultado */}
      {result && (
        <Box mt={4}>
          <Paper elevation={3} sx={{ p: 4 }}>
            <Typography variant="h5" gutterBottom>
              Resultado para {result.asset} em {result.date}
            </Typography>
            <Typography
              variant="h6"
              color={result.signal === 'Buy' ? 'green' : 'red'}
              gutterBottom
            >
              Sinal: {result.signal}
            </Typography>
            <Typography variant="body1" gutterBottom>
              <strong>Preço Atual:</strong> ${result.current_price.toFixed(2)}
            </Typography>
            <Typography variant="body1" gutterBottom>
              <strong>Preço Previsto:</strong> ${result.prediction.toFixed(2)}
            </Typography>
            {/* Botão para ver mais detalhes ou gráficos */}
            <Button
              variant="outlined"
              color="primary"
              onClick={() => setShowGraph(true)}
              sx={{ mt: 2 }}
            >
              Ver Gráfico
            </Button>
          </Paper>
          <GraphDialog
            open={showGraph}
            onClose={() => setShowGraph(false)}
            data={result.graphData}
          />
        </Box>
      )}
    </Container>
  );
}

export default HomePage;
