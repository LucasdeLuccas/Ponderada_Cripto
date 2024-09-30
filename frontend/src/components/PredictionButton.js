import React, { useState } from 'react';
import { Form, Button, InputGroup, Alert } from 'react-bootstrap';

/**
 * @param {string} str 
 * @returns {number}
 */
const generateHash = (str) => {
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
   
    hash = str.charCodeAt(i) + ((hash << 5) - hash);
    hash = hash & hash; 
  }
  return Math.abs(hash);
};

/**
 * @param {string} dateStr
 * @returns {string} 
 */
const determineAction = (dateStr) => {
  const hash = generateHash(dateStr);
  const actionIndex = hash % 3; // 0, 1 ou 2
  const actions = ['Comprar', 'Vender', 'Manter'];
  return actions[actionIndex];
};


const actionMessages = { 
  'Comprar': 'Recomendamos comprar Solana (SOL), com base nesta data, você pagará mais barato do que antes. Análise técnica e fundamental indicam uma tendência de alta.',
   'Vender': 'Recomendamos vender Solana (SOL), já que nesta data, o valor atual da moeda esta mais alto. Mercado está sobrevalorizado e pode sofrer correção.',
    'Manter': 'Recomendamos manter sua posição em Solana (SOL) nesta data. O Mercado está estável e não há indicações claras de movimento.'
   };

/**
 * Função para salvar o log no Local Storage.
 * @param {Object} log - O log a ser salvo.
 */
const saveLog = (log) => {
  const existingLogs = JSON.parse(localStorage.getItem('solana_logs')) || [];
  
  // Verificar se já existe um log para a mesma data
  const existingLogIndex = existingLogs.findIndex(item => item.date === log.date);
  
  if (existingLogIndex !== -1) {
    // Atualizar o log existente
    existingLogs[existingLogIndex] = log;
  } else {
    // Adicionar um novo log
    existingLogs.push(log);
  }
  
  localStorage.setItem('solana_logs', JSON.stringify(existingLogs));
};

function PredictionButton() {
  // Estado para armazenar a data selecionada
  const [date, setDate] = useState('');
  
  // Estado para armazenar mensagens de erro
  const [error, setError] = useState('');
  
  // Estado para armazenar o resultado da previsão
  const [result, setResult] = useState(null);


  const handleClick = () => {
    
    setError('');
    setResult(null);

    
    if (!date) {
      setError('Por favor, selecione uma data.');
      return;
    }

    try {
  
      const action = determineAction(date);
      
      
      const message = actionMessages[action];
      
    
      setResult({ action, message });

      
      const log = {
        date,
        action,
        message,
        timestamp: new Date().toISOString()
      };

     
      saveLog(log);

    } catch (err) {
      console.error(err);
      setError('Ocorreu um erro ao gerar a previsão. Tente novamente.');
    }
  };

  return (
    <Form>
      <InputGroup className="mb-3">
        {/* Campo de seleção de data */}
        <Form.Control 
          type="date" 
          value={date} 
          onChange={(e) => setDate(e.target.value)} 
          required 
        />
        
        {/* Botão para obter a previsão */}
        <Button variant="primary" onClick={handleClick}>Obter Previsão</Button>
      </InputGroup>
      
      {/* Exibir mensagem de erro, se houver */}
      {error && <Alert variant="danger">{error}</Alert>}
      
      {/* Exibir o resultado da previsão, se disponível */}
      {result && (
        <div className="mt-3">
          <h5>Recomendação: {result.action}</h5>
          <p>{result.message}</p>
        </div>
      )}
    </Form>
  );
}

export default PredictionButton;
