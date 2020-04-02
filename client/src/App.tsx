import React from 'react';
import { observer } from 'mobx-react-lite';

import './App.css';
import { useStores } from './hooks/user-stores';

const App: React.FC = observer(() => {
  const { authStore } = useStores();

  return (
    <>
      <div>{authStore.accessToken}</div>
      <button onClick={() => authStore.setAccessToken('123')}>set token</button>
    </>
  );
});

export default App;
