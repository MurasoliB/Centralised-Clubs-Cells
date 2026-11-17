import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import App from './App.tsx';
import { ErrorBoundary } from './components/ui/ErrorBoundary';
import './index.css';

// Suppress harmless browser resize observer loop notifications emitted by charts
window.addEventListener('error', (e) => {
  if (e.message && (
    e.message.includes('ResizeObserver') ||
    e.message.includes('Script error.')
  )) {
    e.stopImmediatePropagation();
  }
});

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <ErrorBoundary fallbackTitle="ClubHub Portal Auto-Recovery">
      <App />
    </ErrorBoundary>
  </StrictMode>
);
