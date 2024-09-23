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

const assets = ['Bitcoin', 'Ethereum', 'BNB', 'Solana', 'Dogecoin'];

function HomePage() {
  const [asset, setAsset] = useState('Bitcoin');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    setLoading(true);
    try {
      const today = new Date().toISOString().split('T')[0]; // Data atual no formato 'YYYY-MM-DD'
      const response = await axios.get('http://localhost:5000/predict', {
        params: { asset, date: today },
      });
      setResult(response.data);
    } catch (error) {
      console.error(error);
      alert('Erro ao obter os dados. Verifique o ativo selecionado.');
    }
    setLoading(false);
  };

  return (
    <Container maxWidth="md" sx={{ mt: 4 }}>
      {/* Seção de Informação */}
      <Box textAlign="center" mb={4}>
        <Typography variant="h3" gutterBottom>
          Bem-vindo ao CryptoDeLuccas
        </Typography>
        <Typography variant="h6" color="textSecondary">
          Seu sistema de previsão pra criptoativos.
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
        <Box component="form" noValidate>
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
              <strong>Preço Previsto:</strong> ${result.prediction.toFixed(2)}
            </Typography>
            {/* Botão para ver mais detalhes ou gráficos */}
            <Button
              variant="outlined"
              color="primary"
              onClick={() => {
                // Lógica para mostrar os gráficos
              }}
            >
              Ver Gráfico
            </Button>
          </Paper>
        </Box>
      )}
    </Container>
  );
}

export default HomePage;
